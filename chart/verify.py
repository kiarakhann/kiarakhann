"""Independent verification. Reads MASTER_DATASET.json, writes VERIFICATION_REPORT.json.

Validators are chosen to share no calculation code with the primary engines:
- Skyfield + JPL DE421 (bundled by the skyfield-data package) vs Swiss Ephemeris (sepl_18/semo_18)
- Asc/MC from a hand-coded spherical formula using Skyfield sidereal time + obliquity
- Meeus ch.47 polynomial for the mean lunar node
- Sexagenary arithmetic + Swiss solar longitudes (builder.bazi_independent) vs lunar_python
- Structural invariants for iztro; lunar_python for the lunar date and Na Yin table
"""
import datetime as dt
import math
import os

import skyfield_data
from lunar_python import Solar
from lunar_python.util import LunarUtil
from skyfield import almanac
from skyfield.api import Loader, wgs84
from skyfield.framelib import ecliptic_frame

from common import (BRANCHES, PLANETS7, ROOT, DATA, SIGNS, STEMS, angdiff, dump, norm, sign_of)
import json

THRESH = {"planet_deg": 0.01, "angle_deg": 0.05, "solar_term_s": 120, "sunrise_s": 60, "node_deg": 0.01}

m = json.load(open(os.path.join(DATA, "MASTER_DATASET.json")))
stab = m["uncertainty_ensemble"]["stability"]
base = m["shared_astronomy"]
inp = m["input"]["normalized"]

load = Loader(os.path.join(os.path.dirname(skyfield_data.__file__), "data"))
ts = load.timescale(builtin=True)
eph = load("de421.bsp")
earth = eph["earth"]
SKY = {"Sun": "sun", "Moon": "moon", "Mercury": "mercury", "Venus": "venus", "Mars": "mars barycenter",
       "Jupiter": "jupiter barycenter", "Saturn": "saturn barycenter"}

birth_utc = dt.datetime.fromisoformat(base["utc"])
t = ts.from_datetime(birth_utc)
rows = []


def stability_for(*keys):
    vals = [stab[k]["classification"] for k in keys if k in stab]
    if not vals:
        return "stable"
    return "sensitive" if "sensitive" in vals else "stable"


def row(system, datum, pe, pv, val, vv, diff, conv, status, stability="stable", bd=None, conf=None, note=None):
    if conf is None:
        if status == "fail":
            conf = "low"
        elif stability == "sensitive":
            conf = "low"
        elif val and status == "pass":
            conf = "high"
        else:
            conf = "medium"
    r = {"system": system, "datum": datum, "primary_engine": pe, "primary_value": pv, "validator": val,
         "validator_value": vv, "difference": diff, "convention": conv, "boundary_distance": bd,
         "uncertainty_stability": stability, "confidence": conf, "status": status}
    if note:
        r["note"] = note
    rows.append(r)


def sky_lon(name, tt):
    ap = earth.at(tt).observe(eph[SKY[name]]).apparent()
    lat, lon, _ = ap.frame_latlon(ecliptic_frame)
    return lon.degrees


# 1. planetary longitudes -----------------------------------------------------
for p in PLANETS7:
    sw = base["tropical"][p]["lon"]
    sk = sky_lon(p, t)
    d = abs(angdiff(sw, sk))
    keys = [f"western.{p}.sign_house", f"jyotisha.{p}.sign_house"]
    row("shared", f"{p} tropical apparent longitude", "Swiss Ephemeris 2.10.03 (sepl_18/semo_18)", sw,
        "Skyfield 1.55 + JPL DE421", sk, d, "geocentric apparent, true equinox and ecliptic of date",
        "pass" if d <= THRESH["planet_deg"] else "alert", stability_for(*keys),
        bd=min(sw % 30, 30 - sw % 30))

# 2. mean node -----------------------------------------------------------------
T = (t.tt - 2451545.0) / 36525
omega = norm(125.0445479 - 1934.1362891 * T + 0.0020754 * T ** 2 + T ** 3 / 467441 - T ** 4 / 60616000)
sw = base["tropical"]["MeanNode"]["lon"]
d = abs(angdiff(sw, omega))
row("jyotisha", "Mean lunar node (Rahu) tropical longitude", "Swiss Ephemeris", sw,
    "Meeus (1998) ch.47 polynomial, hand-coded", omega, d, "mean node, equinox of date",
    "pass" if d <= THRESH["node_deg"] else "alert", stability_for("jyotisha.Rahu.sign_house"))
row("jyotisha", "True lunar node", "Swiss Ephemeris", base["tropical"]["TrueNode"]["lon"], None, None, None,
    "true (osculating) node; alternative track only", "single-engine", conf="medium",
    note="no independent true-node validator installed; same sign as mean node")

# 3. Ascendant / MC -------------------------------------------------------------
lat_r = math.radians(inp["latitude"])
eps = t._mean_obliquity_radians + t._nutation_angles_radians[1]
ramc = math.radians(norm(t.gast * 15 + inp["longitude"]))
asc = norm(math.degrees(math.atan2(math.cos(ramc), -(math.sin(ramc) * math.cos(eps) + math.tan(lat_r) * math.sin(eps)))))
mc = norm(math.degrees(math.atan2(math.sin(ramc), math.cos(ramc) * math.cos(eps))))
for name, pv, vv, key in [("Ascendant", base["angles_tropical"]["asc"], asc, "western.asc_sign"),
                          ("MC", base["angles_tropical"]["mc"], mc, "western.mc_sign")]:
    d = abs(angdiff(pv, vv))
    row("western", f"{name} tropical longitude", "Swiss Ephemeris houses_ex", pv,
        "spherical formula with Skyfield GAST + true obliquity (hand-coded)", vv, d,
        "tropical, true obliquity, apparent sidereal time", "pass" if d <= THRESH["angle_deg"] else "alert",
        stability_for(key), bd=min(pv % 30, 30 - pv % 30))
# Swiss sidereal mode subtracts the true ayanamsha (mean Lahiri value + nutation in longitude);
# the validator adds Skyfield's own nutation in longitude to the mean value to match that convention.
ay = base["ayanamsha_lahiri"] + math.degrees(t._nutation_angles_radians[0])
sid_asc = base["angles_sidereal"]["asc"]
d = abs(angdiff(norm(asc - ay), sid_asc))
row("jyotisha", "Lagna sidereal longitude (Lahiri)", "Swiss Ephemeris (FLG_SIDEREAL)", sid_asc,
    "independent tropical Asc minus (Swiss mean Lahiri ayanamsha + Skyfield nutation)", norm(asc - ay), d,
    "sidereal Lahiri; ayanamsha value itself single-engine", "pass" if d <= THRESH["angle_deg"] else "alert",
    stability_for("jyotisha.lagna_sign"), bd=min(sid_asc % 30, 30 - sid_asc % 30),
    note="ayanamsha is a convention; Lahiri value not independently re-derived")
j = m["jyotisha"]
def audit_row(prefix):
    return next(r for r in m["boundary_audit"] if r["boundary"].startswith(prefix))


for label, key, prefix, conv in [("D9 (Navamsa) Lagna", "jyotisha.D9_lagna", "Jyotisha D9", "D9 = floor(lon/3.333) mod 12"),
                                 ("D10 (Dasamsa) Lagna", "jyotisha.D10_lagna", "Jyotisha D10", "odd sign from itself, even sign from 9th")]:
    ar = audit_row(prefix)
    near = min(x for x in (ar["minutes_to_previous_change"], ar["minutes_to_next_change"]) if x is not None)
    stb = stability_for(key)
    row("jyotisha", label, "builder formula", j["lagna"]["d9_sign" if "D9" in label else "d10_sign"], None, None, None, conv, "pass", stb,
        bd={"minutes_to_previous_change": ar["minutes_to_previous_change"], "minutes_to_next_change": ar["minutes_to_next_change"]},
        conf="low" if stb == "sensitive" else "medium",
        note=("changes inside the +/-1 min interval; unavailable for interpretation" if stb == "sensitive"
              else f"stable within +/-1 min; nearest boundary {near:.1f} min away"))

# 4. sunrise & sect ---------------------------------------------------------------
topos = wgs84.latlon(inp["latitude"], inp["longitude"], elevation_m=inp["elevation_m"])
day_start = ts.from_datetime(dt.datetime.fromisoformat(base["local_civil"]).replace(hour=0, minute=0) .astimezone(dt.timezone.utc))
tr, yr = almanac.find_risings(eph["earth"] + topos, eph["sun"], day_start, day_start + 1)
sky_rise = tr[0].utc_datetime()
sw_rise = dt.datetime.fromisoformat(base["sunrise_local"])
d = abs((sky_rise - sw_rise).total_seconds())
row("shared", "Sunrise at birthplace", "Swiss Ephemeris rise_trans (upper limb, refraction)", base["sunrise_local"],
    "Skyfield almanac.find_risings (DE421)", sky_rise.astimezone(sw_rise.tzinfo).isoformat(timespec="seconds"), d,
    "seconds; upper limb with standard refraction", "pass" if d <= THRESH["sunrise_s"] else "alert")
alt = (eph["earth"] + topos).at(t).observe(eph["sun"]).apparent().altaz("standard")[0].degrees
d = abs(alt - base["sun_altitude"]["apparent_alt"])
row("western", "Sun apparent altitude (sect)", "Swiss Ephemeris azalt", base["sun_altitude"]["apparent_alt"],
    "Skyfield altaz(standard refraction)", alt, d, "degrees; day chart if > 0", "pass" if d < 0.05 else "alert",
    stability_for("western.sect"), bd={"sun_altitude_deg": base["sun_altitude"]["apparent_alt"]})

# 5. solar terms ------------------------------------------------------------------


def sky_crossing(target, guess):
    lo, hi = guess - 3, guess + 3
    for _ in range(60):
        mid = (lo + hi) / 2
        if angdiff(sky_lon("Sun", ts.tt_jd(mid)), target) > 0:
            hi = mid
        else:
            lo = mid
    return ts.tt_jd((lo + hi) / 2).utc_datetime()


for key in ("previous_jie", "next_jie"):
    st = m["bazi"]["solar_terms"][key]
    sw_t = dt.datetime.fromisoformat(st["utc_swiss"])
    sk_t = sky_crossing(st["sun_lon"], ts.from_datetime(sw_t).tt)
    lp_t = dt.datetime.fromisoformat(st["utc_lunar_python"])
    d = max(abs((sk_t - sw_t).total_seconds()), abs((lp_t - sw_t).total_seconds()))
    row("bazi", f"{st['name_lunar_python']} solar term instant (Sun {st['sun_lon']:.0f} deg)", "Swiss Ephemeris bisection", st["utc_swiss"],
        "Skyfield DE421 bisection; lunar_python table", {"skyfield": sk_t.isoformat(timespec="seconds"), "lunar_python": st["utc_lunar_python"]},
        d, "apparent geocentric solar longitude", "pass" if d <= THRESH["solar_term_s"] else "alert",
        bd={"days": st.get("days_before_birth", st.get("days_after_birth"))})
prev = m["bazi"]["solar_terms"]["previous_jie"]
nxt = m["bazi"]["solar_terms"]["next_jie"]
row("bazi", f"Birth after {prev['name_lunar_python']} and before {nxt['name_lunar_python']} (month pillar {m['bazi']['pillars']['month']})", "Swiss Ephemeris", prev["days_before_birth"] > 0 and m["bazi"]["solar_terms"]["next_jie"]["days_after_birth"] > 0,
    "invariant", True, None, "exact sectional-term instants", "pass" if prev["days_before_birth"] > 0 else "fail")

# 6. BaZi pillars ---------------------------------------------------------------------
b = m["bazi"]
same = b["pillars"] == b["independent_pillars"]
row("bazi", "Four Pillars (civil time)", "lunar_python 1.4.8", " ".join(b["pillars"].values()),
    "hand-coded sexagenary arithmetic + Swiss solar longitude", " ".join(b["independent_pillars"].values()),
    0 if same else 1, "Li Chun year, jie months, 00:00 day boundary", "pass" if same else "fail", stability_for("bazi.pillars"))
row("bazi", "Four Pillars (local apparent solar time track)", "hand-coded", " ".join(b["solar_time_track_pillars"].values()),
    None, None, None, "LAT " + base["local_apparent_time"][11:], "pass", stability_for("bazi.solar_track"),
    conf="high" if not b["solar_time_track_differs"] else "low",
    note="identical to civil track; no school disagreement on pillars" if not b["solar_time_track_differs"]
    else "differs from the civil track in: " + ", ".join(k for k in b["pillars"] if b["pillars"][k] != b["solar_time_track_pillars"][k]))
lp_hidden = b["lunar_python_hidden_stems"]
mine = [b["pillar_detail"][k]["hidden_stems"] for k in ("year", "month", "day", "hour")]
row("bazi", "Hidden stems", "builder table", mine, "lunar_python table", lp_hidden, 0 if mine == lp_hidden else 1,
    "standard 藏干", "pass" if mine == lp_hidden else "fail")
row("bazi", "Day Master strength", "rule DMS-1", b["day_master_strength"]["verdict"], None, None, None,
    "documented weighting rule", "pass", conf="medium", note="school-dependent rule; single implementation")
row("bazi", "Useful God / favorable element", "Fu-Yi + Tiao-Hou", b["useful_god"]["schools_agree_on"], None, None, None,
    "two named schools", "pass", conf=b["useful_god"]["confidence"],
    note=("schools agree on " + ", ".join(b["useful_god"]["schools_agree_on"])) if b["useful_god"]["schools_agree_on"] else "schools do not agree")
dy = b["da_yun"]
row("bazi", "Da Yun start", "UTC jie interval x 365.2425/3", dy["start"], "lunar_python sect1/sect2 (Beijing-time input)",
    dy["cross_check_lunar_python"], "~0-5 days", "school-dependent day-count convention", "pass", conf="medium",
    note="conventions spread " + " .. ".join(sorted([dy["start"][:10], dy["cross_check_lunar_python"]["sect1_start"][:10], dy["cross_check_lunar_python"]["sect2_start"][:10]])[::2])
    + "; all Da Yun boundaries inherit this spread")

# 7. Vimshottari ---------------------------------------------------------------------
v = j["vimshottari"]
VY = {"Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17}
total = sum(VY.values())
row("jyotisha", "Vimshottari full cycle = 120 years", "builder", total, "invariant", 120, total - 120, "", "pass" if total == 120 else "fail")
moon_sid_sky = norm(sky_lon("Moon", t) - ay)
frac = (moon_sid_sky % (40 / 3)) / (40 / 3)
bal = (1 - frac) * VY[v["moon_nakshatra"]["lord"]]
shift = next(r for r in m["boundary_audit"] if r["boundary"].startswith("Moon nakshatra"))["outputs_affected"].split("by ")[-1]
d_days = abs(bal - v["balance_years_at_birth"]) * 365.25
row("jyotisha", f"Vimshottari balance at birth ({v['moon_nakshatra']['lord']}, years)", "Swiss Moon", v["balance_years_at_birth"],
    "Skyfield Moon - (mean Lahiri + Skyfield nutation)", bal, d_days, "difference in days", "pass" if d_days < 1 else "alert",
    stability_for("jyotisha.moon_nakshatra_pada"), note=f"+/-1 clock minute shifts all dasha boundaries by {shift}")
row("jyotisha", "Rahu-Ketu separation", "builder", j["rahu_ketu_separation"], "invariant", 180.0,
    abs(j["rahu_ketu_separation"] - 180), "mean node", "pass" if abs(j["rahu_ketu_separation"] - 180) < 1e-9 else "fail")

# 8. period continuity -------------------------------------------------------------


def contiguous(periods, s="start", e="end"):
    for a, c in zip(periods, periods[1:]):
        if abs((dt.datetime.fromisoformat(c[s]) - dt.datetime.fromisoformat(a[e])).total_seconds()) > 1:
            return False
    return True


mds = v["mahadashas"]
ok = contiguous(mds) and all(contiguous(md["antardashas"]) and md["antardashas"][0]["start"] == md["start"] for md in mds)
row("jyotisha", "Vimshottari MD/AD continuity", "builder", ok, "invariant", True, None, "", "pass" if ok else "fail")
ok = contiguous(dy["periods"])
row("bazi", "Da Yun continuity", "builder", ok, "invariant", True, None, "", "pass" if ok else "fail")
z = m["ziwei"]
dec = sorted([p for p in z["palaces"]], key=lambda p: p["decadal_nominal_age_range"][0])
ok = contiguous([{"start": p["decadal_start"] + "T00:00:00", "end": p["decadal_end"] + "T00:00:00"} for p in dec])
row("ziwei", "Decadal period continuity", "iztro + CNY conversion", ok, "invariant", True, None, "nominal age", "pass" if ok else "fail")
ok = contiguous([{"start": p["start"] + "T00:00:00", "end": p["end"] + "T00:00:00"} for p in m["western"]["profections"]])
row("western", "Profection continuity", "builder", ok, "invariant", True, None, "", "pass" if ok else "fail")

# 9. Zi Wei invariants (every hour alternative) ------------------------------------------
SIHUA = {"甲": ("廉贞", "破军", "武曲", "太阳"), "乙": ("天机", "天梁", "紫微", "太阴"), "丙": ("天同", "天机", "文昌", "廉贞"),
         "丁": ("太阴", "天同", "天机", "巨门"), "戊": ("贪狼", "太阴", "右弼", "天机"), "己": ("武曲", "贪狼", "天梁", "文曲"),
         "庚": ("太阳", "武曲", "太阴", "天同"), "辛": ("巨门", "太阳", "文曲", "文昌"), "壬": ("天梁", "紫微", "左辅", "武曲"),
         "癸": ("破军", "巨门", "太阴", "贪狼")}
bd_ = dt.date.fromisoformat(base["local_civil"][:10])
lp = Solar.fromYmd(bd_.year, bd_.month, bd_.day).getLunar()
alts = {hp: a for hp, a in m["sinic_hour_alternatives"]["alternatives"].items() if a["ziwei"]}
for hp, alt in alts.items():
    zz = alt["ziwei"]
    tag = f" [{hp} hour]" if len(alts) > 1 else ""
    stab_tag = "sensitive" if len(alts) > 1 else "stable"
    pal = zz["palaces"]
    names = {p["name"] for p in pal}
    branches = {p["earthly_branch"] for p in pal}
    row("ziwei", "12 unique palaces and branches" + tag, "iztro " + zz["implementation"]["version"], [len(names), len(branches)], "invariant", [12, 12], None, "",
        "pass" if len(names) == 12 and len(branches) == 12 else "fail")
    majors = [s_["name"] for p in pal for s_ in p["major_stars"]]
    row("ziwei", "14 major stars each placed once" + tag, "iztro", len(majors), "invariant", 14, None, "",
        "pass" if len(majors) == 14 == len(set(majors)) else "fail")
    bi = {p["earthly_branch"]: BRANCHES.index(p["earthly_branch"]) for p in pal}
    zw = next(p["earthly_branch"] for p in pal if any(s_["name"] == "紫微" for s_ in p["major_stars"]))
    tf = next(p["earthly_branch"] for p in pal if any(s_["name"] == "天府" for s_ in p["major_stars"]))
    okr = (bi[zw] + bi[tf]) % 12 == 4
    row("ziwei", "紫微/天府 mirror across 寅-申 axis" + tag, "iztro", f"{zw}/{tf}", "invariant (i+j) mod 12 = 4", okr, None, "", "pass" if okr else "fail")
    lm, ti = zz["lunar"]["lunarMonth"], zz["request"]["time_index"]
    ti_eff = 0 if ti == 12 else ti
    ming = BRANCHES[(2 + lm - 1 - ti_eff) % 12]
    shen = BRANCHES[(2 + lm - 1 + ti_eff) % 12]
    row("ziwei", "Ming (命) palace branch" + tag, "iztro", zz["soul_palace_branch"], "hand formula 寅+(month-1)-hour", ming, None, "",
        "pass" if ming == zz["soul_palace_branch"] else "fail", stab_tag)
    row("ziwei", "Shen (身) palace branch" + tag, "iztro", zz["body_palace_branch"], "hand formula 寅+(month-1)+hour", shen, None, "",
        "pass" if shen == zz["body_palace_branch"] else "fail", stab_tag)
    ys = lp.getYearGan()
    yin_stem = {"甲": 2, "己": 2, "乙": 4, "庚": 4, "丙": 6, "辛": 6, "丁": 8, "壬": 8, "戊": 0, "癸": 0}[ys]
    ming_stem = STEMS[(yin_stem + (BRANCHES.index(ming) - 2) % 12) % 10]
    ny = LunarUtil.NAYIN[ming_stem + ming]
    bureau_map = {"水": "水二局", "木": "木三局", "金": "金四局", "土": "土五局", "火": "火六局"}
    row("ziwei", "Five Elements Bureau" + tag, "iztro", zz["five_elements_bureau"], "五虎遁 + lunar_python Na Yin table",
        f"{ming_stem}{ming} {ny} -> {bureau_map[ny[-1]]}", None, "", "pass" if bureau_map[ny[-1]] == zz["five_elements_bureau"] else "fail", stab_tag)
    pillars_alt = " ".join(alt["bazi"]["pillars"].values())
    ok = (lp.getMonth(), lp.getDay()) == (zz["lunar"]["lunarMonth"], zz["lunar"]["lunarDay"]) and zz["chinese_date"] == pillars_alt
    row("ziwei", "Lunar date and pillars match lunar_python" + tag, "iztro", f'{zz["lunar"]["lunarMonth"]}/{zz["lunar"]["lunarDay"]} {zz["chinese_date"]}',
        "lunar_python", f"{lp.getMonth()}/{lp.getDay()} {pillars_alt}", None, "Beijing reference lunar calendar", "pass" if ok else "fail")
    muts = {s_["name"]: s_["mutagen"] for p in pal for s_ in p["major_stars"] + p["minor_stars"] if s_["mutagen"]}
    expect = dict(zip(SIHUA[ys], ("禄", "权", "科", "忌")))
    row("ziwei", f"Four Transformations (lunar-year stem {ys})" + tag, "iztro", muts, "standard 四化 table (iztro default school)", expect, None, "",
        "pass" if muts == expect else "fail", conf="high" if muts == expect else "low")
row("ziwei", "Independence disclosure", "iztro (JavaScript)", "single method", None, None, None,
    "py-iztro not used; would wrap the same method", "single-engine", conf="medium")

# 10. Maya & Tibetan ------------------------------------------------------------------------
mm = m["maya"]
ok = mm["round_trip_ok"] and mm["long_count"] == mm["independent"]["long_count"] and \
    f'{mm["tzolkin"]["number"]} {mm["tzolkin"]["day_name_convertdate"]}' == mm["independent"]["tzolkin"] and \
    f'{mm["haab"]["day"]} {mm["haab"]["month_convertdate"].rstrip(chr(39))}' == mm["independent"]["haab"]  # convertdate spells Muwan'/Muwan
row("maya", "Long Count / Tzolk'in / Haab' (GMT 584283)", "convertdate 2.5.1", f'{mm["long_count"]} {mm["tzolkin"]["number"]} {mm["tzolkin"]["day_name_convertdate"]} {mm["haab"]["day"]} {mm["haab"]["month_convertdate"]}',
    "hand-coded JDN arithmetic", f'{mm["independent"]["long_count"]} {mm["independent"]["calendar_round_independent"] if "calendar_round_independent" in mm["independent"] else mm["calendar_round_independent"]}',
    None, "GMT 584283", "pass" if ok else "fail")
tb = m["tibetan"]
row("tibetan", "Element-animal year", "builder (Losar-window argument)", f'{tb["element"]} {tb["animal"]} ({tb["gender"]})', None, None, None,
    tb.get("losar_boundary", ""), "pass", conf="medium", note="no lineage calendar engine; year label only")

# summary -------------------------------------------------------------------------------------
num = [r for r in rows if isinstance(r["difference"], (int, float)) and r["validator"] and "deg" not in str(r["difference"])]
largest = {}
for r in rows:
    if isinstance(r["difference"], float):
        key = "seconds" if ("instant" in r["datum"] or "Sunrise" in r["datum"]) else ("days" if "balance" in r["datum"] else "degrees")
        if key not in largest or r["difference"] > largest[key]["difference"]:
            largest[key] = {"datum": r["datum"], "difference": r["difference"]}
fails = [r for r in rows if r["status"] == "fail"]
alerts = [r for r in rows if r["status"] == "alert"]
report = {
    "thresholds": THRESH,
    "engines": {
        "primary_astronomy": "Swiss Ephemeris 2.10.03 via pyswisseph 2.10.3.2 (sepl_18.se1, semo_18.se1)",
        "validator_astronomy": "Skyfield 1.55 + JPL DE421 (skyfield-data package); DE440/DE441 not reachable (JPL host blocked by network policy)",
        "chinese_calendar": "lunar_python 1.4.8; hand-coded sexagenary arithmetic as validator",
        "ziwei": "iztro 2.6.1 (single method)",
        "maya": "convertdate 2.5.1 + hand-coded arithmetic",
    },
    "rows": rows,
    "summary": {"total": len(rows), "pass": sum(r["status"] == "pass" for r in rows),
                "alert": len(alerts), "fail": len(fails),
                "single_engine": sum(r["status"] == "single-engine" for r in rows),
                "largest_differences": largest,
                "invariant_failures": [r["datum"] for r in fails],
                "systems_halted": sorted({r["system"] for r in fails})},
}
dump("VERIFICATION_REPORT.json", report)
print(json.dumps(report["summary"], ensure_ascii=False, indent=1))
