"""Render human-readable reports and the manifest from the JSON datasets.
Every interpretive sentence in FINAL_READING.md is assembled from SYNTHESIS.json fields.
"""
import datetime as dt
import hashlib
import json
import os
import platform
import subprocess
import sys

from common import ROOT, DATA

J = lambda p: json.load(open(os.path.join(DATA, p)))
m, v, s = J("MASTER_DATASET.json"), J("VERIFICATION_REPORT.json"), J("SYNTHESIS.json")


def write(path, text):
    with open(os.path.join(DATA, path), "w") as f:
        f.write(text.rstrip() + "\n")


def sha(path):
    return hashlib.sha256(open(os.path.join(ROOT, path), "rb").read()).hexdigest()


def f2(x, n=2):
    return f"{x:.{n}f}" if isinstance(x, (int, float)) and x is not None else str(x)

# ---------------------------------------------------------------- manifest


def manifest():
    import tzdata
    pkgs = subprocess.run(["uv", "pip", "freeze", "-p", sys.executable], capture_output=True, text=True).stdout.split()
    try:
        tzv = open(os.path.join(os.path.dirname(tzdata.__file__), "zoneinfo", "tzdata.zi")).readline().strip()
    except OSError:
        tzv = None
    import skyfield_data
    de421 = os.path.join(os.path.dirname(skyfield_data.__file__), "data", "de421.bsp")
    node = subprocess.run(["node", "--version"], capture_output=True, text=True).stdout.strip()
    src = {f"chart/{f}": sha(f"chart/{f}") for f in sorted(os.listdir(os.path.join(ROOT, "chart"))) if f.endswith(".py")}
    src["ziwei/run.js"] = sha("ziwei/run.js")
    src["ziwei/package-lock.json"] = sha("ziwei/package-lock.json")
    return {
        "execution_timestamp_utc": m["generated_utc"],
        "runtime": {"python": sys.version.split()[0], "node": node, "platform": platform.platform()},
        "python_packages": pkgs,
        "node_packages": {"iztro": m["ziwei"]["implementation"]["version"]},
        "ephemerides": {
            "ephe/sepl_18.se1": {"source": "github.com/aloistr/swisseph ephe/", "sha256": sha("ephe/sepl_18.se1")},
            "ephe/semo_18.se1": {"source": "github.com/aloistr/swisseph ephe/", "sha256": sha("ephe/semo_18.se1")},
            "de421.bsp": {"source": "skyfield-data PyPI package (JPL DE421)",
                          "sha256": hashlib.sha256(open(de421, "rb").read()).hexdigest(),
                          "note": "DE440/DE441 unavailable: naif.jpl.nasa.gov and ssd.jpl.nasa.gov returned HTTP 403 through the environment network policy"},
        },
        "iana_tzdata": {"python_tzdata_package": "2026.4", "header": tzv},
        "conventions": m["conventions"],
        "source_sha256": src,
        "deviations_from_preferred_setup": [
            "JPL validator kernel is DE421 (1900-2050) rather than DE440/DE441; adequate for a 2005 birth.",
            "py-iztro not installed: it wraps the same iztro method and would add no independence.",
            "immanuel not used: Western facts computed directly with pyswisseph under explicitly declared conventions.",
        ],
    }

# ---------------------------------------------------------------- input audit


def input_audit():
    inp = m["input"]
    b = m["shared_astronomy"]
    o = inp["original_user_entry"]
    n = inp["normalized"]
    L = ["# Input audit", "", "## Original entry (verbatim)", ""]
    L += [f"- **{k.replace('_', ' ')}**: {v}" for k, v in o.items()]
    L += ["", "## Normalized", "",
          f"- Calendar: {n['calendar']} — {n['calendar_interpretation']}",
          f"- Local civil time: **{b['local_civil']}** ({b['weekday']})",
          f"- IANA zone: {n['iana_zone']}; UTC offset {b['utc_offset']}; DST {b['dst']}" + (" (India has observed no DST since 1945; the +06:30 war-time offset ended in 1945)" if n['iana_zone'] == "Asia/Kolkata" else ""),
          f"- UTC instant: **{b['utc']}**; JD(UT) {b['jd_ut']:.6f}; ΔT {b['delta_t_seconds']:.2f} s",
          f"- Coordinates: {n['latitude']}° N, {n['longitude']}° E, elevation {n['elevation_m']} m — {n['coordinate_source']}",
          f"- Local mean time: {b['local_mean_time'][11:]}; equation of time {b['equation_of_time_minutes']:.2f} min; local apparent solar time **{b['local_apparent_time'][11:]}**",
          f"- Sunrise {b['sunrise_local'][11:19]}, sunset {b['sunset_local'][11:19]} (local civil time) on the birth date; birth {abs(b['minutes_after_sunrise']):.1f} min {'after' if b['minutes_after_sunrise'] >= 0 else 'before'} that sunrise; Sun apparent altitude {b['sun_altitude']['apparent_alt']:.2f}°",
          f"- Time precision: {n['time_precision']}; ensemble ±{n['time_uncertainty_minutes']} min ({n['time_uncertainty_rationale']})",
          f"- Gender: {n['gender']}; current residence: {n['current_residence']['place_name']}" + (f" ({n['current_residence']['assumption']})" if n['current_residence'].get('assumption') else ""),
          "", "## Boundary audit", "", "| Boundary | Value at birth | Min to previous change | Min to next change | Affects |", "|---|---|---|---|---|"]
    for r in m["boundary_audit"]:
        prev = r.get("minutes_to_previous_change")
        nxt = r.get("minutes_to_next_change")
        pv = f"{f2(prev)} → {r.get('previous_value')}" if prev is not None and r.get("previous_value") is not None else f2(prev) if prev is not None else "—"
        nv = f"{f2(nxt)} → {r.get('next_value')}" if nxt is not None and r.get("next_value") is not None else f2(nxt) if nxt is not None else "—"
        val = r.get("value_at_birth", r.get("note", ""))
        if r["boundary"].startswith("BaZi sectional"):
            val = f"after {r['previous']['name_lunar_python']} {r['previous']['utc_swiss']} by {r['previous']['days_before_birth']:.2f} d; before {r['next']['name_lunar_python']} by {r['next']['days_after_birth']:.2f} d"
        if r["boundary"].startswith("Civil midnight"):
            val = f"{r['minutes_since_midnight']} min after midnight; {r['minutes_to_23:00']} min before 23:00"
        if r["boundary"].startswith("Zi Wei lunar"):
            val = f"lunar {r['lunar_date']['lunarMonth']}/{r['lunar_date']['lunarDay']}, leap={r['lunar_date']['isLeap']}"
        L.append(f"| {r['boundary']} | {val} | {pv} | {nv} | {r['outputs_affected']} |")
    L += ["", "Sect note: Swiss sunrise uses the Sun's upper limb; sect uses the Sun centre's apparent altitude.",
          "", "## Time-uncertainty ensemble (−1, 0, +1 min)", "", "| Datum | −1 min | reported | +1 min | Class |", "|---|---|---|---|---|"]
    st = m["uncertainty_ensemble"]["stability"]
    for k, x in st.items():
        vals = x["values"]
        if x["classification"] == "sensitive" or k.count(".") == 1:
            L.append(f"| {k} | {vals['-1']} | {vals['0.0']} | {vals['1']} | **{x['classification']}** |")
    ns = sum(1 for x in st.values() if x["classification"] == "stable")
    L += ["", f"{ns} of {len(st)} tracked facts are stable across the interval; sensitive: " +
          ", ".join(k for k, x in st.items() if x["classification"] == "sensitive") + ".",
          "No rectification was performed."]
    return "\n".join(L)

# ---------------------------------------------------------------- master dataset md


def stab(key):
    return m["uncertainty_ensemble"]["stability"][key]["classification"]


def ziwei_table(z):
    L = ["| Branch | Palace | Major stars (brightness, 化) | Minor stars | Decadal (nominal age) | Decadal dates |", "|---|---|---|---|---|---|"]
    for p in z["palaces"]:
        ms = ", ".join(f"{x['name']}({x['brightness'] or ''}{'·化' + x['mutagen'] if x['mutagen'] else ''})" for x in p["major_stars"]) or "(empty)"
        mi = ", ".join(x["name"] + (f"·化{x['mutagen']}" if x["mutagen"] else "") for x in p["minor_stars"]) or "—"
        L.append(f"| {p['heavenly_stem']}{p['earthly_branch']} | {p['name']}{' (身)' if p['is_body_palace'] else ''} | {ms} | {mi} | {p['decadal_nominal_age_range'][0]}–{p['decadal_nominal_age_range'][1]} | {p['decadal_start']} → {p['decadal_end']} |")
    return L


def master_md():
    j, w, b, z = m["jyotisha"], m["western"], m["bazi"], m["ziwei"]
    L = ["# Master dataset (facts only)", "", "Machine-readable source: `MASTER_DATASET.json`. No interpretation here.", "",
         "## Jyotisha — sidereal Lahiri, whole-sign, mean node", "",
         f"Lagna **{j['lagna']['sign']} {j['lagna']['deg_in_sign']:.2f}°** ({j['lagna']['nakshatra']['name']} pada {j['lagna']['nakshatra']['pada']} — {stab('jyotisha.lagna_nakshatra_pada')}), D9 Lagna {j['lagna']['d9_sign']} ({stab('jyotisha.D9_lagna')}), D10 Lagna {j['lagna']['d10_sign']} ({stab('jyotisha.D10_lagna')}). Ayanamsha {m['shared_astronomy']['ayanamsha_lahiri']:.4f}°.", "",
         "| Graha | Sign | Deg | House | Nakshatra-pada | Dignity | Owns | Functional | D9 | D10 |", "|---|---|---|---|---|---|---|---|---|---|"]
    for p, g in j["grahas"].items():
        L.append(f"| {p} | {g['sign']} | {g['deg_in_sign']:.2f} | {g['house']} | {g['nakshatra']['name']}-{g['nakshatra']['pada']} | {g.get('dignity') or '—'} | {g.get('houses_owned') or '—'} | {g.get('functional_nature') or '—'} | {g['d9_sign']} | {g['d10_sign']} |")
    L += ["", "Yogas (declared whitelist):", ""]
    for y in j["yogas"]:
        if y["present"]:
            extra = y.get("instances") or y.get("basis")
            canc = f" — cancelled per rule ({y['cancellation_rule']})" if y.get("cancelled") else ""
            L.append(f"- **{y['yoga']}** — {y['rule']}. Basis: `{json.dumps(extra, ensure_ascii=False)}`{canc}")
    L.append("- Not present: " + ", ".join(y["yoga"] for y in j["yogas"] if not y["present"]))
    cd = j["current_dasha"]
    L += ["", f"Vimshottari: Moon in {j['vimshottari']['moon_nakshatra']['name']} (lord {j['vimshottari']['moon_nakshatra']['lord']}), balance {j['vimshottari']['balance_years_at_birth']:.3f} y. Year = 365.25 d.", "",
          "| Mahadasha | Start | End |", "|---|---|---|"]
    for md in j["vimshottari"]["mahadashas"][:6]:
        L.append(f"| {md['lord']} | {md['start'][:10]} | {md['end'][:10]} |")
    L += ["", f"Current: **{cd['mahadasha']}/{cd['antardasha']}** {cd['ad_start'][:10]} → {cd['ad_end'][:10]}. Pratyantardashas:", ""]
    L += [f"- {p['lord']}: {p['start'][:10]} → {p['end'][:10]}" for p in cd["pratyantardashas"]]
    L += ["", "## Western / Hellenistic — tropical, whole-sign, 7 planets", "",
          f"Ascendant **{w['ascendant']['sign']} {w['ascendant']['deg_in_sign']:.2f}°**, MC {w['mc']['sign']} {w['mc']['deg_in_sign']:.2f}° (whole-sign H{w['mc']['whole_sign_house_of_mc']}). **{w['sect']['chart'].title()} chart**; sect benefic {w['sect']['benefic_of_sect']}, contrary malefic {w['sect']['malefic_contrary']}.", "",
          "| Planet | Sign | Deg | House | Essential dignity | Bound | Face | Speed |", "|---|---|---|---|---|---|---|---|"]
    for p, g in w["planets"].items():
        dg = [k for k, x in g["dignity"].items() if x]
        L.append(f"| {p} | {g['sign']} | {g['deg_in_sign']:.2f} | {g['house']} | {', '.join(dg)} | {g['bound_lord']} | {g['face_lord']} | {g['speed']:.3f} |")
    L += ["", f"Lots: Fortune {w['lots']['fortune']['sign']} (H{w['lots']['fortune']['house']}), Spirit {w['lots']['spirit']['sign']} (H{w['lots']['spirit']['house']}). Dispositor terminals (final dispositor or closed reception loop): {w['dispositor_terminals']}.", "",
          "Close aspects (≤3°): " + "; ".join(f"{a['a']}–{a['b']} {a['aspect']} {a['orb']:.2f}° {'applying' if a['applying'] else 'separating'}" for a in w["aspects"] if a["close"]), "",
          f"Current profection: age {w['profection_current']['age']} → H{w['profection_current']['house']} {w['profection_current']['sign']}, year ruler {w['profection_current']['year_ruler']} (natal H{w['profection_current']['year_ruler_natal']['house']}).", ""]
    for r in w["solar_returns"]:
        L.append(f"- Solar return {r['year']}: {r['utc']} UTC — birthplace Asc {r['birthplace']['asc_sign']} {r['birthplace']['asc_deg']:.1f}°; current-residence Asc {r['current_residence']['asc_sign']} {r['current_residence']['asc_deg']:.1f}° (location changes Asc: {r['asc_sign_differs_by_location']})")
    L += ["", "## BaZi", "", f"Pillars (civil clock): **{' '.join(b['pillars'].values())}**; solar-time track: {' '.join(b['solar_time_track_pillars'].values())} ({'differs' if b['solar_time_track_differs'] else 'identical'}); Day Master {b['day_master_strength']['day_master']} ({b['day_master_strength']['element']}).", "",
          "| Pillar | Stem | Ten God | Branch | Hidden stems | Hidden Ten Gods | Na Yin (traditional) |", "|---|---|---|---|---|---|---|"]
    for k, d in b["pillar_detail"].items():
        L.append(f"| {k} | {d['stem']} ({d['stem_element']}, {d['stem_polarity']}) | {d['stem_ten_god'] or 'Day Master'} | {d['branch']} | {''.join(d['hidden_stems'])} | {', '.join(d['hidden_ten_gods'])} | {b['na_yin_traditional_attribute'][k]} |")
    L += ["", "Interactions: " + "; ".join(f"{x['type']} {x.get('stems', x.get('branches'))}" + (f" {x['pillars']}" if 'pillars' in x else "") for x in b["stem_interactions"] + b["branch_interactions"]) + ". No transformation asserted.",
          "", f"Day Master strength (DMS-1): **{b['day_master_strength']['verdict']}**; support share {b['day_master_strength']['support_share']:.2f}; season {b['day_master_strength']['seasonal_state']}; roots in {b['day_master_strength']['roots_in_pillars']}.",
          f"Useful element: Fu-Yi favors {b['useful_god']['fu_yi']['favorable']}; Tiao-Hou " + (f"({b['useful_god']['tiao_hou']['source']}) favors {b['useful_god']['tiao_hou']['favorable']}, secondary {b['useful_god']['tiao_hou']['secondary']}" if b['useful_god']['tiao_hou'] else b['useful_god']['tiao_hou_status']) + f". Schools agree on: **{', '.join(b['useful_god']['schools_agree_on']) or 'nothing'}**; confidence {b['useful_god']['confidence']}.",
          "", f"Da Yun {b['da_yun']['direction']}, start {b['da_yun']['start'][:10]} (offset {b['da_yun']['start_offset_years']:.2f} y; lunar_python cross-checks {b['da_yun']['cross_check_lunar_python']['sect1_start'][:10]} / {b['da_yun']['cross_check_lunar_python']['sect2_start'][:10]}).", "",
          "| Da Yun | Start | End | Stem god | Branch god |", "|---|---|---|---|---|"]
    for p in b["da_yun"]["periods"][:6]:
        L.append(f"| {p['pillar']} | {p['start'][:10]} | {p['end'][:10]} | {p['stem_ten_god']} | {p['branch_main_ten_god']} |")
    alts = {hp: x for hp, x in m["sinic_hour_alternatives"]["alternatives"].items() if x["ziwei"]}
    if len(alts) > 1:
        L += ["", "### Hour alternatives (sensitive)", "", m["sinic_hour_alternatives"]["rule"] + ".", ""]
        for hp, x in alts.items():
            bb = x["bazi"]
            L.append(f"- **{hp} hour** (ensemble offsets {x['offsets_minutes']} min; matches solar-time track: {x['matches_solar_time_track']}): pillars {' '.join(bb['pillars'].values())}; DMS-1 {bb['day_master_strength']['verdict']} (support share {bb['day_master_strength']['support_share']:.3f}); interactions: "
                     + "; ".join(f"{i['type']} {i.get('stems', i.get('branches'))}" for i in bb["stem_interactions"] + bb["branch_interactions"]))
    L += ["", "## Zi Wei Dou Shu (iztro " + z["implementation"]["version"] + ")", ""]
    for hp, x in (alts.items() if len(alts) > 1 else [(b["pillars"]["hour"], {"ziwei": z, "offsets_minutes": [0]})]):
        zz = x["ziwei"]
        L += ["", f"### {hp} hour chart" + (" (reported instant)" if 0.0 in x["offsets_minutes"] else ""), "",
              f"Lunar {zz['lunar']['lunarYear']}-{zz['lunar']['lunarMonth']}-{zz['lunar']['lunarDay']} (leap {zz['lunar']['isLeap']}), hour {zz['time_branch']}; Ming {zz['soul_palace_branch']}, Shen {zz['body_palace_branch']}; life ruler {zz['life_ruler']}, body ruler {zz['body_ruler']}; bureau {zz['five_elements_bureau']}.", ""]
        L += ziwei_table(zz)
    mm, tb = m["maya"], m["tibetan"]
    L += ["", "## Maya calendar (GMT 584283)", "", f"Long Count **{mm['long_count']}**, Calendar Round **{mm['calendar_round_independent']}**; round-trip OK: {mm['round_trip_ok']}. Day-sign meaning: {mm['day_sign_meaning_status']}.",
          "", "## Tibetan elemental (limited)", "", f"**{tb['gender'].title()} {tb['element']} {tb['animal']}** year, rabjung {tb['rabjung']} year {tb['year_in_rabjung']}. Omitted: {', '.join(tb['omitted'])} — {tb['omitted_reason']}.",
          "", "## Excluded methods", ""]
    for k, x in m["excluded_methods"].items():
        L.append(f"- **{k}**: {json.dumps(x, ensure_ascii=False)}")
    return "\n".join(L)

# ---------------------------------------------------------------- verification md


def verification_md():
    L = ["# Verification report", "", "Machine-readable source: `VERIFICATION_REPORT.json`.", "", "## Engines", ""]
    L += [f"- **{k}**: {x}" for k, x in v["engines"].items()]
    sm = v["summary"]
    L += ["", f"## Summary: {sm['pass']} pass, {sm['alert']} alert, {sm['fail']} fail, {sm['single_engine']} single-engine (of {sm['total']})", "",
          f"Thresholds: {v['thresholds']}", "", "Largest differences: " + "; ".join(f"{k}: {x['datum']} = {x['difference']:.3g}" for k, x in sm["largest_differences"].items()),
          "", "Invariant failures: " + (", ".join(sm["invariant_failures"]) or "none") + ". Systems halted: " + (", ".join(sm["systems_halted"]) or "none") + ".",
          "", "| System | Datum | Primary | Validator | Difference | Stability | Confidence | Status |", "|---|---|---|---|---|---|---|---|"]
    for r in v["rows"]:
        pv = r["primary_value"]
        pv = f"{pv:.5f}" if isinstance(pv, float) else json.dumps(pv, ensure_ascii=False) if not isinstance(pv, str) else pv
        vv = r["validator_value"]
        vv = f"{vv:.5f}" if isinstance(vv, float) else json.dumps(vv, ensure_ascii=False) if vv is not None and not isinstance(vv, str) else (vv or "—")
        d = r["difference"]
        d = f"{d:.2e}" if isinstance(d, float) else ("—" if d is None else str(d))
        L.append(f"| {r['system']} | {r['datum']} | {pv} | {vv} ({r['validator'] or 'none'}) | {d} | {r['uncertainty_stability']} | {r['confidence']} | {r['status']} |")
    L += ["", "Independence disclosure: Skyfield/DE421, the hand-coded Asc/MC and Meeus node formulas, and the hand-coded sexagenary and Maya arithmetic share no code with Swiss Ephemeris, lunar_python, or convertdate. The Lahiri ayanamsha, the true node, and all Zi Wei star placement are single-engine; Zi Wei is checked by structural invariants, not by a second engine."]
    return "\n".join(L)

# ---------------------------------------------------------------- final reading
PROM = {"high": "emphasized", "medium": "moderately emphasized", "low": "not strongly emphasized"}
POL = {"supportive": "mostly supportive testimony", "challenging": "mostly difficult testimony", "mixed": "mixed testimony"}
CL = {"jyotisha": "Jyotisha", "western": "Western/Hellenistic", "sinic": "Sinic (BaZi + Zi Wei)"}


def basis_line(d, cluster):
    p = next(x for x in s["projections"] if x["domain"] == d and x["cluster"] == cluster)
    if cluster == "jyotisha":
        return "; ".join(f"H{b['house']} {b['sign']}: occupants {', '.join(b['occupants']) or 'none'}, lord {b['lord']} in H{b['lord_house']} ({b['lord_dignity']}{', neecha-bhanga' if b['neecha_bhanga_applied'] else ''}), drishti from {', '.join(b['drishti_from']) or 'none'}" for b in p["basis"])
    if cluster == "western":
        return "; ".join(f"H{b['house']} {b['sign']}: occupants {', '.join(b['occupants']) or 'none'}, ruler {b['ruler']} in H{b['ruler_house']} ({', '.join(b['ruler_dignity'])})" for b in p["basis"])
    if p.get("hour_alternatives"):
        return " ‖ ".join(f"[{hp} hour] " + sinic_basis(x) for hp, x in p["hour_alternatives"].items())
    return sinic_basis(p["basis"])


def sinic_basis(basis):
    zb, bb = basis["ziwei"], basis["bazi"]
    parts = []
    if zb:
        parts.append("Zi Wei " + "; ".join(f"{b['palace']} {b['branch']}: {', '.join(b['major_stars']) or 'empty (borrows ' + str(b['borrowed_stars']) + ')'}{' + ' + ','.join(b['auspicious']) if b['auspicious'] else ''}{' + ' + ','.join(b['malefic']) if b['malefic'] else ''}" for b in zb["basis"]))
    if bb:
        parts.append("BaZi " + ", ".join(bb["basis"][:4]) + (" …" if len(bb["basis"]) > 4 else ""))
    return " | ".join(parts)


def theme_sentence(t):
    return "silent (no stable basis)" if t is None else f"{PROM[t['prominence']]}, {POL[t['polarity']]}"


def sensitivity_bullets():
    st = m["uncertainty_ensemble"]["stability"]
    sens = [k for k, x in st.items() if x["classification"] == "sensitive"]
    out = []
    if sens:
        out.append("- **Sensitive (changes inside ±1 min):** " + "; ".join(
            f"{k}: " + " / ".join(f"{o} min → {v}" for o, v in st[k]["values"].items()) for k in sens) +
            ". These are excluded as evidence; both alternatives are shown in the master dataset.")
    near, comfy = [], []
    for r in m["boundary_audit"]:
        pv, nx = r.get("minutes_to_previous_change"), r.get("minutes_to_next_change")
        if pv is None and nx is None or "value_at_birth" not in r:
            continue
        d = min(x for x in (pv, nx) if x is not None)
        txt = f"{r['boundary']} = {r['value_at_birth']} ({f2(pv, 1) if pv is not None else '—'} / {f2(nx, 1) if nx is not None else '—'} min to previous / next change)"
        if d < 1.0:
            continue
        (near if d < 15 else comfy).append(txt)
    if near:
        out.append("- **Near a boundary but stable at ±1 min:** " + "; ".join(near) + ".")
    if comfy:
        out.append("- **Comfortably stable:** " + "; ".join(comfy) + ".")
    st_ = m["bazi"]["solar_terms"]
    out.append(f"- Month pillar: birth is {st_['previous_jie']['days_before_birth']:.2f} days after {st_['previous_jie']['name_lunar_python']} and {st_['next_jie']['days_after_birth']:.2f} days before {st_['next_jie']['name_lunar_python']} — stable.")
    return out


def final_reading():
    b = m["shared_astronomy"]
    n = m["input"]["normalized"]
    dv = s["divergence"]
    D = s["domains"]
    sm = v["summary"]
    rows = v["rows"]
    planet_rows = [r for r in rows if "tropical apparent longitude" in r["datum"]]
    worst = max(planet_rows, key=lambda r: r["difference"])
    ang = max(r["difference"] for r in rows if r["datum"] in ("Ascendant tropical longitude", "MC tropical longitude"))
    terms = max(r["difference"] for r in rows if "solar term instant" in r["datum"])
    rise = next(r["difference"] for r in rows if r["datum"] == "Sunrise at birthplace")
    alts = {hp: x for hp, x in m["sinic_hour_alternatives"]["alternatives"].items() if x["ziwei"]}
    L = ["# Six-culture verified chart — final reading", "",
         "> This is a comparison of traditional symbolic systems, computed to stated conventions. It is not a scientifically validated forecast and says nothing certain about the future. No medical, financial, legal, lifespan or fertility claims are made.", "",
         "## 1. Input and sensitivity", "",
         f"- Born **{b['local_civil'][:10]} {b['local_civil'][11:16]} local civil time (UTC{b['local_civil'][19:]}, {'no DST' if b['dst'] == '0:00:00' else 'DST ' + b['dst']})** = {b['utc'][:16].replace('T', ' ')} UTC, a **{b['weekday']}**, {n['place_name']} ({n['latitude']}° N, {n['longitude']}° E).",
         f"- Local mean time {b['local_mean_time'][11:16]}; local apparent solar time **{b['local_apparent_time'][11:16]}**; sunrise {b['sunrise_local'][11:16]}, so this is a **{m['western']['sect']['chart']} chart** (Sun {b['sun_altitude']['apparent_alt']:.1f}° altitude).",
         f"- Time treated as exact to the minute (±{n['time_uncertainty_minutes']} min ensemble). No rectification.",
         f"- Current residence: {n['current_residence']['place_name']}" + (f" ({n['current_residence']['assumption'].rstrip('.')})" if n['current_residence'].get('assumption') else "") + "."]
    L += sensitivity_bullets()
    if len(alts) > 1:
        L.append("- **Chinese hour:** the recorded 01:00 is exactly the start of the 丑 (Chou) double-hour. One minute earlier, and the local-apparent-solar-time school "
                 f"(solar time {b['local_apparent_time'][11:16]}), give 子 (Zi). So BaZi hour pillar ({' vs '.join(alts)}) and the whole Zi Wei palace layout are reported for both hours, "
                 "and Sinic evidence is used only where both hours agree (rule SINIC-HOUR).")
    sat = m["jyotisha"]["grahas"]["Saturn"]
    if sat["deg_in_sign"] > 29 or sat["deg_in_sign"] < 1:
        L.append(f"- Convention note: sidereal Saturn is at {sat['sign']} {sat['deg_in_sign']:.2f}° under Lahiri; an ayanamsha about 1° smaller would move it to the next sign. No alternative-ayanamsha track was requested.")
    L += ["", "## 2. Verification", "",
          f"- {sm['pass']}/{sm['total']} checks pass, {sm['alert']} alerts, {sm['fail']} invariant failures; {sm['single_engine']} single-engine items disclosed.",
          f"- Swiss Ephemeris vs JPL DE421 (Skyfield): largest planetary difference {worst['difference']:.5f}° ({worst['datum'].split()[0]}); Ascendant/MC ≤ {ang:.4f}°; solar terms ≤ {terms:.1f} s across three sources; sunrise {rise:.1f} s.",
          "- Two verification bugs were fixed before this run (no chart values changed): the Maya check compared two spellings of the same Haab' month, and the sidereal checks used the Lahiri ayanamsha without nutation. A BaZi seasonal-state table bug (相/休 and 囚/死 swapped) was also fixed in the calculator.",
          "- Unavailable or omitted: Shadbala, Ashtakavarga, D7/D12, zodiacal releasing, transits, Tibetan Mewa/Parkha/life-forces, and Maya day-sign meanings (no named source). Zi Wei is single-engine (iztro), checked by structural invariants for both hour charts. DE440 could not be downloaded, so DE421 was used.", "",
          "## 3. Divergence rate (read this first)", "",
          f"- **{dv['divergent_over_all_nine']} domains divergent** ({dv['divergent_over_all_nine_pct']:.0f}%); {dv['divergent_over_sufficient']} of domains with sufficient evidence ({dv['divergent_over_sufficient_pct']:.0f}%).",
          f"- The Sinic cluster is silent on {sum(1 for x in D.values() if x['sinic_hour_sensitive'])} of 9 domains because its two hour charts disagree, so most grades rest on two traditions only. Zero divergence here partly reflects that missing third voice."]
    nstrong = sum(1 for x in D.values() if x["grade"] == "STRONG")
    L.append("- No domain reached STRONG (all three traditions agreeing)." if not nstrong else f"- {nstrong} domain(s) reached STRONG.")
    L += ["- MODERATE agreements below that say an area is 'not strongly emphasized' are agreements about *low emphasis*, not predictions.", "",
          "## 4. Cross-cultural themes", ""]
    for gname in ("STRONG", "MODERATE"):
        for d, x in D.items():
            if x["grade"] != gname:
                continue
            a, c = x["agreeing_pairs"][0]
            agreeing = sorted({k for pr in x["agreeing_pairs"] for k in pr}, key=list(CL).index)
            L.append(f"### {d} {x['name']} — {gname} ({' + '.join(CL[k] for k in agreeing)} agree: {theme_sentence(x['shared_theme'])})")
            for k in CL:
                if k in agreeing:
                    continue
                t3 = x["themes"][k]
                extra = ""
                if t3 is None and x["sinic_hour_sensitive"] and k == "sinic":
                    extra = " — hour-sensitive: " + "; ".join(f"{hp} hour {theme_sentence(t)}" for hp, t in x["sinic_hour_sensitive"].items())
                L.append(f"- {CL[k]}: {theme_sentence(t3)}{extra} — neither agreeing nor conflicting.")
            for k in agreeing:
                L.append(f"- {CL[k]} basis: {basis_line(d, k)}")
            L.append("")
    L += ["## 5. Disagreements", ""]
    any_div = False
    for d, x in D.items():
        if x["grade"] != "DIVERGENT":
            continue
        any_div = True
        L.append(f"### {d} {x['name']} — DIVERGENT")
        for k, t in x["themes"].items():
            L.append(f"- {CL[k]}: {theme_sentence(t)}" + (f". Basis: {basis_line(d, k)}" if t else ""))
        L.append("- Conflicting pairs: " + "; ".join(f"{CL[p]} vs {CL[q]}" for p, q in x["conflicting_pairs"]) + ". This is left unresolved.")
        L.append("")
    if not any_div:
        L.append("- No domain has two traditions in direct conflict.")
    hs = [(d, x) for d, x in D.items() if x["sinic_hour_sensitive"]]
    if hs:
        L.append("- **Internal disagreement (Sinic, by hour):** " + "; ".join(
            f"{d} {x['name']}: " + " vs ".join(f"{hp} {theme_sentence(t)}" for hp, t in x["sinic_hour_sensitive"].items()) for d, x in hs) +
            ". Not resolved; neither hour is preferred.")
    L += ["", "## 6. Weak and insufficient areas", ""]
    for d, x in D.items():
        if x["grade"] in ("WEAK", "INSUFFICIENT"):
            L.append(f"- **{d} {x['name']} — {x['grade']}**: " + "; ".join(f"{CL[k]} {theme_sentence(t)}" for k, t in x["themes"].items()) + ". No cross-tradition theme should be read here."
                     + (" This is a symbolic 'routine/health' house or palace only, not a medical statement." if d == "D7" else ""))
    L += ["", "## 7. Temperament overlay", ""]
    for ax, t in s["temperament"].items():
        def why(x):
            if x.get("hour_alternatives"):
                return "; ".join(f"{hp} hour: {', '.join(h['basis']) or 'no qualifying factor'}" + (f" → {h['status']}" if "status" in h else "")
                                 for hp, h in x["hour_alternatives"].items())
            return ', '.join(x['basis']) or 'no qualifying factor'
        votes = "; ".join(f"{CL[k]} {x['status']} ({why(x)})" for k, x in t["votes"].items())
        L.append(f"- **{ax} {t['name']} — {t['grade']}**: {votes}.")
    ov = s["symbolic_overlays"]
    L += ["", f"Symbolic, non-voting overlays: the Maya Calendar Round is **{ov['maya']['calendar_round']}** (Long Count {ov['maya']['long_count']}), and the Tibetan year is **{ov['tibetan']['year']}** (birth precedes Losar, so the previous Tibetan year applies). No sourced meaning is in the dataset for either, so they neither corroborate nor dissent.", "",
          "## 8. Timing", ""]
    ch = s["chronology"]
    cur = ch["current"]
    L.append(f"- Base rate: {ch['base_rate']['share_of_days_with_any_moderate_or_strong'] * 100:.0f}% of all days from birth to age 40 carry at least one two-tradition (MODERATE) overlap, so a single MODERATE window means little. STRONG overlaps cover {ch['base_rate']['share_of_days_with_any_strong'] * 100:.1f}% of days.")
    L.append(f"- **Now ({cur['start']} → {cur['end']})**: " + ("; ".join(f"{c['domain_name']} {c['level']} ({' + '.join(CL[k] for k in c['clusters'])})" for c in cur["convergences"]) or "no convergence") +
             f". Active: Jyotisha {', '.join(cur['active']['jyotisha'])}; Western {', '.join(cur['active']['western'])}; Sinic {', '.join(cur['active']['sinic'])}.")
    ns = ch["next_strong"]
    if ns:
        nd = [c["domain"] for c in ns["convergences"] if c["level"] == "STRONG"]
        L.append(f"- **Next STRONG window: {ns['start']} → {ns['end']}**, {', '.join(c['domain_name'] for c in ns['convergences'] if c['level'] == 'STRONG')} activated by all three traditions (Jyotisha {', '.join(ns['active']['jyotisha'])}; Western {', '.join(ns['active']['western'])}; Sinic {', '.join(ns['active']['sinic'])}). "
                 f"The natal grade for that domain is {', '.join(D[d]['grade'] for d in nd)}; this marks *activation* only, not a good or bad outcome.")
    else:
        L.append("- No STRONG window occurs within the horizon.")
    if len(alts) > 1:
        L.append("- Zi Wei decadal palaces differ between the two hour charts; a Zi Wei activation is counted only when both hour charts activate the same domain.")
    shift = next(r for r in m["boundary_audit"] if r["boundary"].startswith("Moon nakshatra"))["outputs_affected"].split("by ")[-1]
    L.append(f"- Date precision: Vimshottari dates move about {shift} per clock minute; Da Yun start dates vary by a few days between conventions.")
    ca = s["claims_audit"]
    L += ["", "## 9. Claims removed", "", f"- {ca['candidates']} candidate claims; {ca['kept']} kept as domain statements. Removed: " + ", ".join(f"{k.replace('_', ' ')} {x}" for k, x in ca["removed"].items()) + ".",
          "", "## 10. Closing frame", "",
          "This reading shows where three independent symbolic traditions agree or disagree when each is computed to stated rules. The calculations are reproducible and verified. The meanings are traditional conventions, not established causes. Nothing here is fate or a guaranteed event, and it should not replace judgment, professional advice or your own choices."]
    return "\n".join(L)


if __name__ == "__main__":
    write("INPUT_AUDIT.md", input_audit())
    write("MASTER_DATASET.md", master_md())
    write("VERIFICATION_REPORT.md", verification_md())
    write("FINAL_READING.md", final_reading())
    with open(os.path.join(DATA, "CALCULATION_MANIFEST.json"), "w") as f:
        json.dump(manifest(), f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("reports written")
