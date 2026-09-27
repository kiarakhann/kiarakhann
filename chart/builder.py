"""Deterministic fact builder. Reads BIRTH_INPUT.json, writes MASTER_DATASET.json.

Produces calculations only. Interpretation lives in synthesize.py.
"""
import datetime as dt
import json
import math
import subprocess
from zoneinfo import ZoneInfo

import swisseph as swe
from convertdate import mayan
from lunar_python import Lunar, Solar

from common import (BRANCH_MAIN, BRANCHES, PLANETS7, ROOT, SIGN_RULER, SIGNS, STEM_ELEMENT,
                    STEMS, SWE_ID, angdiff, deg_in_sign, dump, iso, jd_to_utc, jd_ut,
                    load_input, local_instant, norm, sign_of)

FLAGS = swe.FLG_SWIEPH | swe.FLG_SPEED
CONVENTIONS = {
    "shared": {
        "positions": "geocentric apparent (light-time, aberration, nutation), true equinox of date",
        "time_scale": "UT1 input; TT via Swiss Ephemeris delta-T",
        "civil_time": "IANA tz database via zoneinfo + tzdata package",
        "sunrise_sunset": "upper limb, standard atmospheric refraction, Swiss Ephemeris rise_trans",
        "local_mean_time": "UTC + longitude/15 h",
        "local_apparent_time": "LMT + equation of time (Swiss Ephemeris time_equ)",
    },
    "jyotisha": {
        "zodiac": "sidereal", "ayanamsha": "Lahiri (Swiss Ephemeris SIDM_LAHIRI)",
        "houses": "whole-sign from sidereal Lagna (Parashari primary track)",
        "node": "mean node primary; true node reported as alternative",
        "grahas": "Sun..Saturn + Rahu/Ketu",
        "aspects": "graha drishti: all 7th; Mars +4th,+8th; Jupiter +5th,+9th; Saturn +3rd,+10th; nodes excluded",
        "combustion_orbs_deg": {"Moon": 12, "Mars": 17, "Mercury": 14, "Mercury_retro": 12,
                                "Jupiter": 11, "Venus": 10, "Venus_retro": 8, "Saturn": 15},
        "planetary_war": "Mars/Mercury/Jupiter/Venus/Saturn within 1 deg of longitude",
        "dignity": "exaltation/debilitation sign, moolatrikona ranges, own sign, else compound (panchadha) relationship with sign lord (BPHS natural + temporal)",
        "functional_nature": "rule set FN-1: trikona lords (1,5,9) benefic; lords of 3,6,11 malefic unless also trikona lord; natural benefic owning kendra only -> neutral (kendradhipati); 8th lord malefic unless also Lagna lord; 2nd/12th lords take nature of their other house; Moon/Sun owning only 2 or 12 -> neutral; lord of both kendra and trikona -> yogakaraka",
        "divisional": "D9 navamsa: floor(lon/(10/3)) mod 12; D10 dasamsa: odd sign counts from itself, even sign from 9th",
        "vimshottari_year_days": 365.25,
        "vimshottari_levels": "Mahadasha, Antardasha (all), Pratyantardasha (current Antardasha only)",
        "yoga_whitelist": ["Gajakesari", "Budha-Aditya", "Chandra-Mangala", "Pancha-Mahapurusha",
                           "Kemadruma(+cancellation)", "Kendra-Trikona Raja", "Yogakaraka",
                           "Neecha-Bhanga(rule NB-1)", "Parivartana"],
    },
    "western": {
        "zodiac": "tropical", "houses": "whole-sign", "planets": "7 traditional",
        "sect": "day if apparent altitude of Sun centre > 0 at birthplace",
        "triplicity": "Dorothean (day, night, participating)",
        "bounds": "Egyptian", "faces": "Chaldean decans",
        "aspects": "Ptolemaic by whole sign; degree orb reported; 'close' if within 3 deg; applying/separating from relative speed",
        "lots": "Fortune day=Asc+Moon-Sun, night=Asc+Sun-Moon; Spirit is the reverse",
        "under_beams_deg": 15, "combust_deg": 8.5, "cazimi_deg": 0.2833,
        "profection": "annual, age 0 = 1st house, Gregorian birthday to birthday",
        "solar_return": "exact return of natal tropical Sun longitude; computed for birthplace and current residence",
    },
    "bazi": {
        "calendar": "sexagenary; year from Li Chun (Sun 315 deg); month from sectional terms (jie)",
        "primary_time": "local civil time (IST); local apparent solar time retained as alternative track",
        "day_boundary": "local midnight (00:00); late-Zi (23:00-24:00) handled as same-day under sect 2 rule; not applicable here",
        "da_yun_direction": "yang-year male / yin-year female forward, otherwise backward",
        "da_yun_start": "interval to adjacent jie (UTC, astronomical) x (365.2425/3) days; periods of 10 Gregorian years",
        "strength_rule": "DMS-1 (see bazi.day_master_strength.rule)",
        "useful_god_schools": ["Fu-Yi (support/suppress balance)", "Tiao-Hou (seasonal regulation, Qiong Tong Bao Jian table)"],
    },
    "ziwei": {
        "implementation": "iztro (JavaScript) via node", "method": "astro.bySolar(date, timeIndex, gender, fixLeap=true)",
        "time_index": "0=early Zi 00-01, 1=Chou 01-03, 2=Yin 03-05, 3=Mao 05-07, ... from local civil clock",
        "lunar_calendar": "iztro/lunar-lite Chinese lunar calendar (Beijing reference)",
        "leap_month": "fixLeap=true (second half of a leap month counted as next month)",
        "age": "nominal age (xu sui): 1 at birth, +1 at each Chinese New Year",
        "minor_star_set": "iztro default minorStars (14) ; adjective stars excluded from evidence",
    },
    "maya": {"correlation": "GMT 584283 (convertdate EPOCH 584282.5 JD at midnight)"},
    "tibetan": {"scope": "element-animal-gender year and rabjung cycle position only; Mewa, Parkha, la/sok/wangthang/lungta omitted (no validated lineage implementation)"},
}

# ---------------------------------------------------------------- shared base


def body_positions(jd, sidereal=False):
    fl = FLAGS | (swe.FLG_SIDEREAL if sidereal else 0)
    out = {}
    for name, pid in SWE_ID.items():
        x, _ = swe.calc_ut(jd, pid, fl)
        out[name] = {"lon": x[0], "lat": x[1], "dist_au": x[2], "speed": x[3],
                     "retrograde": x[3] < 0}
    return out


def angles(jd, lat, lon, sidereal=False):
    fl = swe.FLG_SIDEREAL if sidereal else 0
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b"W", fl)
    return {"asc": ascmc[0], "mc": ascmc[1], "armc": ascmc[2]}


def asc_speed_deg_per_min(jd, lat, lon, sidereal=False):
    a0 = angles(jd - 0.5 / 1440, lat, lon, sidereal)["asc"]
    a1 = angles(jd + 0.5 / 1440, lat, lon, sidereal)["asc"]
    return norm(a1 - a0)


def sun_altitude(jd, lat, lon, elev):
    x, _ = swe.calc_ut(jd, swe.SUN, swe.FLG_SWIEPH | swe.FLG_EQUATORIAL)
    az = swe.azalt(jd, swe.EQU2HOR, (lon, lat, elev), 1013.25, 15.0, (x[0], x[1], x[2]))
    return {"true_alt": az[1], "apparent_alt": az[2]}


def rise_set(jd_start, lat, lon, elev, which):
    flag = swe.CALC_RISE if which == "rise" else swe.CALC_SET
    res, tret = swe.rise_trans(jd_start, swe.SUN, flag, (lon, lat, elev), 1013.25, 15.0, swe.FLG_SWIEPH)
    return tret[0]


def solar_longitude_crossing(target, jd_guess):
    """Return JD(UT) when apparent tropical Sun longitude == target (bisection, 1 ms)."""
    lo, hi = jd_guess - 20, jd_guess + 20

    def f(j):
        return angdiff(swe.calc_ut(j, swe.SUN, swe.FLG_SWIEPH)[0][0], target)
    for _ in range(80):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def shared_base(local, utc, inp):
    n = inp["normalized"]
    lat, lon, elev = n["latitude"], n["longitude"], n["elevation_m"]
    jd = jd_ut(utc)
    dt_sec = swe.deltat(jd) * 86400
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    ayan = swe.get_ayanamsa_ut(jd)
    eot_days = swe.time_equ(jd)
    lmt = utc + dt.timedelta(hours=lon / 15)
    lat_t = lmt + dt.timedelta(days=eot_days)
    day0 = jd_ut(local.replace(hour=0, minute=0, second=0).astimezone(dt.timezone.utc))
    sunrise = rise_set(day0, lat, lon, elev, "rise")
    sunset = rise_set(day0, lat, lon, elev, "set")
    zone = ZoneInfo(n.get("iana_zone", "Asia/Kolkata"))
    return {
        "jd_ut": jd, "jd_tt": jd + dt_sec / 86400, "delta_t_seconds": dt_sec,
        "utc": iso(utc), "local_civil": iso(local),
        "utc_offset": str(local.utcoffset()), "dst": str(local.dst()),
        "weekday": local.strftime("%A"),
        "local_mean_time": lmt.replace(tzinfo=None).isoformat(timespec="seconds"),
        "equation_of_time_minutes": eot_days * 1440,
        "local_apparent_time": lat_t.replace(tzinfo=None).isoformat(timespec="seconds"),
        "sunrise_local": iso(jd_to_utc(sunrise).astimezone(zone)),
        "sunset_local": iso(jd_to_utc(sunset).astimezone(zone)),
        "minutes_after_sunrise": (jd - sunrise) * 1440,
        "sun_altitude": sun_altitude(jd, lat, lon, elev),
        "ayanamsha_lahiri": ayan,
        "tropical": body_positions(jd, False),
        "sidereal": body_positions(jd, True),
        "angles_tropical": angles(jd, lat, lon, False),
        "angles_sidereal": angles(jd, lat, lon, True),
        "asc_speed_deg_per_min": asc_speed_deg_per_min(jd, lat, lon),
    }

# ---------------------------------------------------------------- Jyotisha


EXALT = {"Sun": (0, 10), "Moon": (1, 3), "Mars": (9, 28), "Mercury": (5, 15),
         "Jupiter": (3, 5), "Venus": (11, 27), "Saturn": (6, 20)}
MOOLA = {"Sun": (4, 0, 20), "Moon": (1, 4, 30), "Mars": (0, 0, 12), "Mercury": (5, 16, 20),
         "Jupiter": (8, 0, 10), "Venus": (6, 0, 15), "Saturn": (10, 0, 20)}
OWN = {"Sun": [4], "Moon": [3], "Mars": [0, 7], "Mercury": [2, 5], "Jupiter": [8, 11],
       "Venus": [1, 6], "Saturn": [9, 10]}
NATURAL_REL = {
    "Sun": {"f": ["Moon", "Mars", "Jupiter"], "n": ["Mercury"], "e": ["Venus", "Saturn"]},
    "Moon": {"f": ["Sun", "Mercury"], "n": ["Mars", "Jupiter", "Venus", "Saturn"], "e": []},
    "Mars": {"f": ["Sun", "Moon", "Jupiter"], "n": ["Venus", "Saturn"], "e": ["Mercury"]},
    "Mercury": {"f": ["Sun", "Venus"], "n": ["Mars", "Jupiter", "Saturn"], "e": ["Moon"]},
    "Jupiter": {"f": ["Sun", "Moon", "Mars"], "n": ["Saturn"], "e": ["Mercury", "Venus"]},
    "Venus": {"f": ["Mercury", "Saturn"], "n": ["Mars", "Jupiter"], "e": ["Sun", "Moon"]},
    "Saturn": {"f": ["Mercury", "Venus"], "n": ["Jupiter"], "e": ["Sun", "Moon", "Mars"]},
}
NAKSHATRAS = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
              "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
              "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
              "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
              "Uttara Bhadrapada", "Revati"]
DASHA_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
DASHA_YEARS = {"Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18,
               "Jupiter": 16, "Saturn": 19, "Mercury": 17}
DRISHTI = {"Sun": [7], "Moon": [7], "Mercury": [7], "Venus": [7], "Mars": [4, 7, 8],
           "Jupiter": [5, 7, 9], "Saturn": [3, 7, 10]}
COMBUST = CONVENTIONS["jyotisha"]["combustion_orbs_deg"]


def compound_rel(planet, lord, planet_sign, lord_sign):
    if planet == lord:
        return "own"
    nat = "f" if lord in NATURAL_REL[planet]["f"] else ("e" if lord in NATURAL_REL[planet]["e"] else "n")
    dist = (lord_sign - planet_sign) % 12 + 1
    temp = "f" if dist in (2, 3, 4, 10, 11, 12) else "e"
    table = {("f", "f"): "great friend", ("f", "e"): "neutral", ("n", "f"): "friend",
             ("n", "e"): "enemy", ("e", "f"): "neutral", ("e", "e"): "great enemy"}
    return table[(nat, temp)]


def jy_dignity(p, lon, signs):
    s, d = sign_of(lon), deg_in_sign(lon)
    if p in EXALT:
        es, _ = EXALT[p]
        if s == es:
            return "exalted"
        if s == (es + 6) % 12:
            return "debilitated"
        ms, a, b = MOOLA[p]
        if s == ms and a <= d < b:
            return "moolatrikona"
        if s in OWN[p]:
            return "own sign"
        lord = SIGN_RULER[s]
        return compound_rel(p, lord, s, signs[lord])
    return None


def nakshatra(lon):
    i = int(norm(lon) // (40 / 3))
    pada = int((norm(lon) % (40 / 3)) // (10 / 3)) + 1
    return {"index": i, "name": NAKSHATRAS[i], "pada": pada, "lord": DASHA_ORDER[i % 9],
            "fraction_elapsed": (norm(lon) % (40 / 3)) / (40 / 3)}


def d9_sign(lon):
    return int(norm(lon) // (10 / 3)) % 12


def d10_sign(lon):
    s, n = sign_of(lon), int(deg_in_sign(lon) // 3)
    return (s + n) % 12 if s % 2 == 0 else (s + 8 + n) % 12


def functional_nature(planet, houses_owned):
    tri = {1, 5, 9}
    kendra = {1, 4, 7, 10}
    h = set(houses_owned)
    natural_benefic = planet in ("Jupiter", "Venus", "Mercury", "Moon")
    if h & kendra - {1} and h & tri:
        return "yogakaraka"
    if h & tri:
        return "benefic"
    if h & {3, 6, 11}:
        return "malefic"
    if 8 in h and 1 not in h:
        return "malefic"
    if natural_benefic and h & kendra:
        return "neutral (kendradhipati)"
    if h <= {2, 12}:
        return "neutral"
    return "neutral"


def vimshottari(moon_lon, birth_utc, year_days):
    nk = nakshatra(moon_lon)
    start_idx = DASHA_ORDER.index(nk["lord"])
    balance = (1 - nk["fraction_elapsed"]) * DASHA_YEARS[nk["lord"]]
    md_start = birth_utc - dt.timedelta(days=(DASHA_YEARS[nk["lord"]] - balance) * year_days)
    mds = []
    t = md_start
    for k in range(10):
        lord = DASHA_ORDER[(start_idx + k) % 9]
        span = DASHA_YEARS[lord] * year_days
        ads = []
        at = t
        ai = DASHA_ORDER.index(lord)
        for j in range(9):
            al = DASHA_ORDER[(ai + j) % 9]
            aspan = span * DASHA_YEARS[al] / 120
            ads.append({"lord": al, "start": iso(at), "end": iso(at + dt.timedelta(days=aspan)),
                        "start_dt": at, "end_dt": at + dt.timedelta(days=aspan)})
            at += dt.timedelta(days=aspan)
        mds.append({"lord": lord, "start": iso(t), "end": iso(t + dt.timedelta(days=span)),
                    "start_dt": t, "end_dt": t + dt.timedelta(days=span), "antardashas": ads})
        t += dt.timedelta(days=span)
    return {"moon_nakshatra": nk, "balance_years_at_birth": balance,
            "cycle_start_theoretical": iso(md_start), "mahadashas": mds}


def pratyantar(ad):
    out = []
    span = (ad["end_dt"] - ad["start_dt"]).total_seconds() / 86400
    i = DASHA_ORDER.index(ad["lord"])
    t = ad["start_dt"]
    for j in range(9):
        pl = DASHA_ORDER[(i + j) % 9]
        s = span * DASHA_YEARS[pl] / 120
        out.append({"lord": pl, "start": iso(t), "end": iso(t + dt.timedelta(days=s))})
        t += dt.timedelta(days=s)
    return out


def jyotisha(base, utc, now_utc):
    sid = base["sidereal"]
    lagna = base["angles_sidereal"]["asc"]
    lsign = sign_of(lagna)
    lon = {p: sid[p]["lon"] for p in PLANETS7}
    lon["Rahu"] = sid["MeanNode"]["lon"]
    lon["Ketu"] = norm(sid["MeanNode"]["lon"] + 180)
    speed = {p: sid[p]["speed"] for p in PLANETS7}
    speed["Rahu"] = speed["Ketu"] = sid["MeanNode"]["speed"]
    signs = {p: sign_of(v) for p, v in lon.items()}
    house = {p: (signs[p] - lsign) % 12 + 1 for p in lon}
    owners = {}
    for h in range(1, 13):
        owners.setdefault(SIGN_RULER[(lsign + h - 1) % 12], []).append(h)
    grahas = {}
    for p in lon:
        g = {"sidereal_lon": lon[p], "sign": SIGNS[signs[p]], "deg_in_sign": deg_in_sign(lon[p]),
             "house": house[p], "speed": speed[p], "retrograde": speed[p] < 0 if p in PLANETS7 else True,
             "nakshatra": nakshatra(lon[p]), "d9_sign": SIGNS[d9_sign(lon[p])],
             "d10_sign": SIGNS[d10_sign(lon[p])]}
        if p in PLANETS7:
            g["dignity"] = jy_dignity(p, lon[p], signs)
            g["houses_owned"] = owners.get(p, [])
            g["functional_nature"] = functional_nature(p, owners.get(p, []))
            if p not in ("Sun",):
                orb = COMBUST.get(p + ("_retro" if speed[p] < 0 and p in ("Mercury", "Venus") else ""), COMBUST.get(p))
                sep = abs(angdiff(lon[p], lon["Sun"]))
                g["distance_from_sun"] = sep
                g["combust"] = sep <= orb
        grahas[p] = g
    # Sun and Moon owning only 2/12 etc. handled by functional_nature rule; lagna lord special
    wars = []
    wp = ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    for i, a in enumerate(wp):
        for b in wp[i + 1:]:
            if abs(angdiff(lon[a], lon[b])) <= 1.0:
                wars.append([a, b, abs(angdiff(lon[a], lon[b]))])
    aspects = []
    for p, offs in DRISHTI.items():
        for o in offs:
            target = (house[p] + o - 2) % 12 + 1
            aspects.append({"from": p, "aspect": o, "to_house": target,
                            "to_sign": SIGNS[(lsign + target - 1) % 12],
                            "planets_aspected": [q for q in lon if house[q] == target and q != p]})
    yogas = jy_yogas(lon, signs, house, owners, grahas, lsign)
    v = vimshottari(lon["Moon"], utc, CONVENTIONS["jyotisha"]["vimshottari_year_days"])
    cur = None
    for md in v["mahadashas"]:
        for ad in md["antardashas"]:
            if ad["start_dt"] <= now_utc < ad["end_dt"]:
                cur = {"mahadasha": md["lord"], "antardasha": ad["lord"], "ad_start": ad["start"],
                       "ad_end": ad["end"], "pratyantardashas": pratyantar(ad)}
    for md in v["mahadashas"]:
        md.pop("start_dt"), md.pop("end_dt")
        for ad in md["antardashas"]:
            ad.pop("start_dt"), ad.pop("end_dt")
    return {
        "lagna": {"sidereal_lon": lagna, "sign": SIGNS[lsign], "deg_in_sign": deg_in_sign(lagna),
                  "nakshatra": nakshatra(lagna), "d9_sign": SIGNS[d9_sign(lagna)],
                  "d10_sign": SIGNS[d10_sign(lagna)]},
        "true_node_alternative": {"rahu_sidereal_lon": sid["TrueNode"]["lon"],
                                  "rahu_sign": SIGNS[sign_of(sid["TrueNode"]["lon"])],
                                  "same_sign_as_mean": sign_of(sid["TrueNode"]["lon"]) == signs["Rahu"]},
        "rahu_ketu_separation": abs(angdiff(lon["Rahu"], lon["Ketu"])),
        "grahas": grahas, "house_lords": {h: SIGN_RULER[(lsign + h - 1) % 12] for h in range(1, 13)},
        "planetary_war": wars, "graha_drishti": aspects, "yogas": yogas,
        "vimshottari": v, "current_dasha": cur,
        "unavailable": {
            "shadbala": "no validated implementation available in this environment",
            "ashtakavarga": "not computed: no validated implementation; transit support not requested",
            "D7_D12": "not computed: domain-specific charts not requested",
        },
    }


def jy_yogas(lon, signs, house, owners, grahas, lsign):
    out = []
    from_moon = {p: (signs[p] - signs["Moon"]) % 12 + 1 for p in lon}
    kendra = {1, 4, 7, 10}
    out.append({"yoga": "Gajakesari", "rule": "Jupiter in kendra (1/4/7/10) from Moon",
                "present": from_moon["Jupiter"] in kendra, "basis": {"jupiter_from_moon": from_moon["Jupiter"]}})
    out.append({"yoga": "Budha-Aditya", "rule": "Sun and Mercury in the same sign",
                "present": signs["Sun"] == signs["Mercury"], "basis": {"sun": SIGNS[signs["Sun"]], "mercury": SIGNS[signs["Mercury"]]}})
    out.append({"yoga": "Chandra-Mangala", "rule": "Moon and Mars in the same sign",
                "present": signs["Moon"] == signs["Mars"], "basis": {"moon": SIGNS[signs["Moon"]], "mars": SIGNS[signs["Mars"]]}})
    for p, name in [("Mars", "Ruchaka"), ("Mercury", "Bhadra"), ("Jupiter", "Hamsa"), ("Venus", "Malavya"), ("Saturn", "Sasa")]:
        pres = house[p] in kendra and grahas[p]["dignity"] in ("exalted", "moolatrikona", "own sign")
        out.append({"yoga": f"Pancha-Mahapurusha ({name})", "rule": f"{p} in own/exaltation sign in kendra from Lagna",
                    "present": pres, "basis": {"house": house[p], "dignity": grahas[p]["dignity"]}})
    adj = [p for p in PLANETS7 if p not in ("Sun", "Moon") and from_moon[p] in (2, 12)]
    kendra_any = [p for p in PLANETS7 if p != "Moon" and p != "Sun" and (house[p] in kendra or from_moon[p] in kendra)]
    out.append({"yoga": "Kemadruma", "rule": "no graha other than Sun/Rahu/Ketu in 2nd or 12th from Moon",
                "present": not adj, "basis": {"planets_2nd_12th_from_moon": adj},
                "cancellation_rule": "cancelled if any graha other than Sun/Moon/nodes occupies a kendra from Lagna or Moon",
                "cancelled": bool(kendra_any) if not adj else None, "cancellation_basis": kendra_any})
    kendra_lords = {SIGN_RULER[(lsign + h - 1) % 12] for h in (1, 4, 7, 10)}
    tri_lords = {SIGN_RULER[(lsign + h - 1) % 12] for h in (1, 5, 9)}

    def aspects(a, b):
        return any((house[b] - house[a]) % 12 + 1 == o for o in DRISHTI[a])
    raja = []
    for a in sorted(kendra_lords):
        for b in sorted(tri_lords):
            if a == b:
                continue
            rel = []
            if signs[a] == signs[b]:
                rel.append("conjunction")
            if aspects(a, b) and aspects(b, a):
                rel.append("mutual aspect")
            if SIGN_RULER[signs[a]] == b and SIGN_RULER[signs[b]] == a:
                rel.append("exchange")
            if rel and [b, a, rel] not in [[r["planets"][0], r["planets"][1], r["relation"]] for r in raja]:
                raja.append({"planets": [a, b], "relation": rel,
                             "kendra_lord_houses": owners[a], "trikona_lord_houses": owners[b]})
    out.append({"yoga": "Kendra-Trikona Raja", "rule": "lord of a kendra and lord of a trikona (different grahas) conjoined, in mutual graha drishti, or in exchange",
                "present": bool(raja), "instances": raja})
    yk = [p for p in PLANETS7 if grahas[p]["functional_nature"] == "yogakaraka"]
    out.append({"yoga": "Yogakaraka", "rule": "single graha owning both a kendra (4/7/10) and a trikona (5/9)",
                "present": bool(yk), "basis": {p: owners[p] for p in yk}})
    nb = []
    for p in PLANETS7:
        if grahas[p]["dignity"] == "debilitated":
            deb_lord = SIGN_RULER[signs[p]]
            ex_lord = SIGN_RULER[EXALT[p][0]]
            for L in {deb_lord, ex_lord}:
                h_l = house[L]
                h_m = (signs[L] - signs["Moon"]) % 12 + 1
                if h_l in kendra or h_m in kendra:
                    nb.append({"debilitated": p, "via": L, "role": "debilitation-sign lord" if L == deb_lord else "exaltation-sign lord",
                               "house_from_lagna": h_l, "house_from_moon": h_m})
    out.append({"yoga": "Neecha-Bhanga (NB-1)", "rule": "for a debilitated graha: lord of its debilitation sign or lord of its exaltation sign in a kendra from Lagna or Moon",
                "present": bool(nb), "instances": nb})
    par = []
    for i, a in enumerate(PLANETS7):
        for b in PLANETS7[i + 1:]:
            if SIGN_RULER[signs[a]] == b and SIGN_RULER[signs[b]] == a:
                par.append([a, b])
    out.append({"yoga": "Parivartana", "rule": "two grahas each in a sign ruled by the other", "present": bool(par), "instances": par})
    return out

# ---------------------------------------------------------------- Western


EG_BOUNDS = [
    [("Jupiter", 6), ("Venus", 12), ("Mercury", 20), ("Mars", 25), ("Saturn", 30)],
    [("Venus", 8), ("Mercury", 14), ("Jupiter", 22), ("Saturn", 27), ("Mars", 30)],
    [("Mercury", 6), ("Jupiter", 12), ("Venus", 17), ("Mars", 24), ("Saturn", 30)],
    [("Mars", 7), ("Venus", 13), ("Mercury", 19), ("Jupiter", 26), ("Saturn", 30)],
    [("Jupiter", 6), ("Venus", 11), ("Saturn", 18), ("Mercury", 24), ("Mars", 30)],
    [("Mercury", 7), ("Venus", 17), ("Jupiter", 21), ("Mars", 28), ("Saturn", 30)],
    [("Saturn", 6), ("Mercury", 14), ("Jupiter", 21), ("Venus", 28), ("Mars", 30)],
    [("Mars", 7), ("Venus", 11), ("Mercury", 19), ("Jupiter", 24), ("Saturn", 30)],
    [("Jupiter", 12), ("Venus", 17), ("Mercury", 21), ("Saturn", 26), ("Mars", 30)],
    [("Mercury", 7), ("Jupiter", 14), ("Venus", 22), ("Saturn", 26), ("Mars", 30)],
    [("Mercury", 7), ("Venus", 13), ("Jupiter", 20), ("Mars", 25), ("Saturn", 30)],
    [("Venus", 12), ("Jupiter", 16), ("Mercury", 19), ("Mars", 28), ("Saturn", 30)],
]
TRIPLICITY = {"fire": ("Sun", "Jupiter", "Saturn"), "earth": ("Venus", "Moon", "Mars"),
              "air": ("Saturn", "Mercury", "Jupiter"), "water": ("Venus", "Mars", "Moon")}
SIGN_TRIP = ["fire", "earth", "air", "water"] * 3
CHALDEAN = ["Mars", "Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter"]
W_EXALT = {"Sun": 0, "Moon": 1, "Mercury": 5, "Venus": 11, "Mars": 9, "Jupiter": 3, "Saturn": 6}
ASPECTS = {0: "conjunction", 2: "sextile", 3: "square", 4: "trine", 6: "opposition"}


def bound_lord(lon):
    s, d = sign_of(lon), deg_in_sign(lon)
    for lord, end in EG_BOUNDS[s]:
        if d < end:
            return lord


def face_lord(lon):
    return CHALDEAN[int(norm(lon) // 10) % 7]


def w_dignity(p, lon, is_day):
    s = sign_of(lon)
    trip = TRIPLICITY[SIGN_TRIP[s]]
    ess = {
        "domicile": SIGN_RULER[s] == p,
        "exaltation": W_EXALT[p] == s,
        "detriment": SIGN_RULER[(s + 6) % 12] == p,
        "fall": (W_EXALT[p] + 6) % 12 == s,
        "triplicity_sect_ruler": trip[0 if is_day else 1] == p,
        "triplicity_any": p in trip,
        "bound": bound_lord(lon) == p,
        "face": face_lord(lon) == p,
    }
    ess["peregrine"] = not (ess["domicile"] or ess["exaltation"] or ess["triplicity_any"] or ess["bound"] or ess["face"])
    return ess


def western(base, now_local_date, birth_local, inp):
    trop = base["tropical"]
    asc, mc = base["angles_tropical"]["asc"], base["angles_tropical"]["mc"]
    asign = sign_of(asc)
    is_day = base["sun_altitude"]["apparent_alt"] > 0
    lon = {p: trop[p]["lon"] for p in PLANETS7}
    spd = {p: trop[p]["speed"] for p in PLANETS7}
    house = {p: (sign_of(lon[p]) - asign) % 12 + 1 for p in PLANETS7}
    planets = {}
    for p in PLANETS7:
        sep = abs(angdiff(lon[p], lon["Sun"]))
        planets[p] = {
            "tropical_lon": lon[p], "sign": SIGNS[sign_of(lon[p])], "deg_in_sign": deg_in_sign(lon[p]),
            "house": house[p], "angular": house[p] in (1, 4, 7, 10),
            "succedent": house[p] in (2, 5, 8, 11), "cadent": house[p] in (3, 6, 9, 12),
            "speed": spd[p], "retrograde": spd[p] < 0,
            "sun_distance": sep if p != "Sun" else None,
            "cazimi": p != "Sun" and sep <= CONVENTIONS["western"]["cazimi_deg"],
            "combust": p != "Sun" and CONVENTIONS["western"]["cazimi_deg"] < sep <= CONVENTIONS["western"]["combust_deg"],
            "under_beams": p != "Sun" and sep <= CONVENTIONS["western"]["under_beams_deg"],
            "bound_lord": bound_lord(lon[p]), "face_lord": face_lord(lon[p]),
            "dignity": w_dignity(p, lon[p], is_day),
            "dispositor": SIGN_RULER[sign_of(lon[p])],
        }
    diurnal = {"Sun", "Jupiter", "Saturn"}
    sect = {"chart": "day" if is_day else "night",
            "sect_light": "Sun" if is_day else "Moon",
            "benefic_of_sect": "Jupiter" if is_day else "Venus",
            "benefic_contrary": "Venus" if is_day else "Jupiter",
            "malefic_of_sect": "Saturn" if is_day else "Mars",
            "malefic_contrary": "Mars" if is_day else "Saturn",
            "planet_in_sect": {p: (p in diurnal) == is_day for p in PLANETS7 if p != "Mercury"}}
    # dispositor chains
    chains = {}
    for p in PLANETS7:
        chain, cur = [p], p
        while True:
            nxt = SIGN_RULER[sign_of(lon[cur])]
            if nxt in chain:
                chain.append(nxt)
                break
            chain.append(nxt)
            cur = nxt
        chains[p] = chain
    terminals = sorted({tuple(sorted(set(c[c.index(c[-1]):]))) for c in chains.values()})
    # aspects
    asp = []
    for i, a in enumerate(PLANETS7):
        for b in PLANETS7[i + 1:]:
            sd = (sign_of(lon[b]) - sign_of(lon[a])) % 12
            k = min(sd, 12 - sd)
            if k not in ASPECTS:
                continue
            exact = [0, 60, 90, 120, 180][[0, 2, 3, 4, 6].index(k)]
            sep = abs(angdiff(lon[a], lon[b]))
            orb = sep - exact
            dt_ = 1 / 24
            sep2 = abs(angdiff(lon[a] + spd[a] * dt_, lon[b] + spd[b] * dt_))
            applying = abs(sep2 - exact) < abs(orb)
            asp.append({"a": a, "b": b, "aspect": ASPECTS[k], "separation": sep,
                        "orb": abs(orb), "close": abs(orb) <= 3, "applying": applying})
    fortune = norm(asc + lon["Moon"] - lon["Sun"]) if is_day else norm(asc + lon["Sun"] - lon["Moon"])
    spirit = norm(asc + lon["Sun"] - lon["Moon"]) if is_day else norm(asc + lon["Moon"] - lon["Sun"])
    # profection for current age
    age = now_local_date.year - birth_local.year - ((now_local_date.month, now_local_date.day) < (birth_local.month, birth_local.day))
    prof_house = age % 12 + 1
    prof_sign = (asign + prof_house - 1) % 12
    prof = []
    for a in range(0, 41):
        s = (asign + a % 12) % 12
        start = birth_local.date().replace(year=birth_local.year + a)
        end = birth_local.date().replace(year=birth_local.year + a + 1)
        ruler = SIGN_RULER[s]
        prof.append({"age": a, "start": start.isoformat(), "end": end.isoformat(), "house": a % 12 + 1,
                     "sign": SIGNS[s], "year_ruler": ruler, "ruler_natal_house": house[ruler]})
    return {
        "ascendant": {"lon": asc, "sign": SIGNS[asign], "deg_in_sign": deg_in_sign(asc)},
        "mc": {"lon": mc, "sign": SIGNS[sign_of(mc)], "deg_in_sign": deg_in_sign(mc),
               "whole_sign_house_of_mc": (sign_of(mc) - asign) % 12 + 1},
        "sect": sect, "planets": planets,
        "house_rulers": {h: SIGN_RULER[(asign + h - 1) % 12] for h in range(1, 13)},
        "dispositor_chains": chains, "dispositor_terminals": [list(t) for t in terminals],
        "aspects": asp,
        "lots": {"fortune": {"lon": fortune, "sign": SIGNS[sign_of(fortune)], "house": (sign_of(fortune) - asign) % 12 + 1},
                 "spirit": {"lon": spirit, "sign": SIGNS[sign_of(spirit)], "house": (sign_of(spirit) - asign) % 12 + 1}},
        "profection_current": {"age": age, "house": prof_house, "sign": SIGNS[prof_sign],
                               "year_ruler": SIGN_RULER[prof_sign],
                               "year_ruler_natal": planets[SIGN_RULER[prof_sign]] | {"name": SIGN_RULER[prof_sign]}},
        "profections": prof,
        "solar_returns": solar_returns(lon["Sun"], inp, now_local_date),
        "unavailable": {
            "zodiacal_releasing": "not computed: no validated implementation in this environment",
            "transits": "not computed: specific transit windows not requested",
            "modern_outer_planets_placidus": "optional modern track not requested; excluded from Hellenistic votes",
        },
    }


def solar_returns(natal_sun, inp, now_date):
    out = []
    n = inp["normalized"]
    places = {"birthplace": (n["latitude"], n["longitude"], "Asia/Kolkata"),
              "current_residence": (n["current_residence"]["latitude"], n["current_residence"]["longitude"],
                                    n["current_residence"]["iana_zone"])}
    for yr in (now_date.year - 1, now_date.year):
        guess = jd_ut(dt.datetime(yr, 8, 25, tzinfo=dt.timezone.utc))
        jd = solar_longitude_crossing(natal_sun, guess)
        rec = {"year": yr, "utc": iso(jd_to_utc(jd))}
        for k, (la, lo, tz) in places.items():
            a = angles(jd, la, lo)
            rec[k] = {"local": iso(jd_to_utc(jd).astimezone(ZoneInfo(tz))), "asc_sign": SIGNS[sign_of(a["asc"])],
                      "asc_deg": deg_in_sign(a["asc"]), "mc_sign": SIGNS[sign_of(a["mc"])]}
        rec["asc_sign_differs_by_location"] = rec["birthplace"]["asc_sign"] != rec["current_residence"]["asc_sign"]
        out.append(rec)
    return out

# ---------------------------------------------------------------- BaZi


TEN_GODS = ["比肩", "劫财", "食神", "伤官", "偏财", "正财", "七杀", "正官", "偏印", "正印"]
TEN_GOD_EN = {"比肩": "Companion", "劫财": "Rob Wealth", "食神": "Eating God", "伤官": "Hurting Officer",
              "偏财": "Indirect Wealth", "正财": "Direct Wealth", "七杀": "Seven Killings",
              "正官": "Direct Officer", "偏印": "Indirect Resource", "正印": "Direct Resource"}
ELEMS = ["wood", "fire", "earth", "metal", "water"]


def ten_god(dm, stem):
    de, se = ELEMS.index(STEM_ELEMENT[dm]), ELEMS.index(STEM_ELEMENT[stem])
    rel = (se - de) % 5
    same_pol = STEMS.index(dm) % 2 == STEMS.index(stem) % 2
    return TEN_GODS[rel * 2 + (0 if same_pol else 1)]


def pillar_from_index(i):
    return STEMS[i % 10] + BRANCHES[i % 12]


def bazi_independent(local_dt, utc):
    """Independent pillar calculation from astronomy + sexagenary arithmetic (not lunar_python)."""
    jd = jd_ut(utc)
    sun = swe.calc_ut(jd, swe.SUN, swe.FLG_SWIEPH)[0][0]
    y = local_dt.year
    lichun = solar_longitude_crossing(315.0, jd_ut(dt.datetime(y, 2, 4, tzinfo=dt.timezone.utc)))
    by = y if jd >= lichun else y - 1
    year_p = pillar_from_index((by - 4) % 60)
    mnum = int(((sun - 315) % 360) // 30)  # 0 = Yin month
    m_branch = BRANCHES[(2 + mnum) % 12]
    first_stem = {"甲": 2, "己": 2, "乙": 4, "庚": 4, "丙": 6, "辛": 6, "丁": 8, "壬": 8, "戊": 0, "癸": 0}[year_p[0]]
    month_p = STEMS[(first_stem + mnum) % 10] + m_branch
    jdn = int(swe.julday(local_dt.year, local_dt.month, local_dt.day, 12.0))
    day_p = pillar_from_index((jdn + 49) % 60)
    hb = ((local_dt.hour + 1) // 2) % 12
    zi_stem = {"甲": 0, "己": 0, "乙": 2, "庚": 2, "丙": 4, "辛": 4, "丁": 6, "壬": 6, "戊": 8, "癸": 8}[day_p[0]]
    hour_p = STEMS[(zi_stem + hb) % 10] + BRANCHES[hb]
    return {"year": year_p, "month": month_p, "day": day_p, "hour": hour_p}


HIDDEN = {"子": ["癸"], "丑": ["己", "癸", "辛"], "寅": ["甲", "丙", "戊"], "卯": ["乙"],
          "辰": ["戊", "乙", "癸"], "巳": ["丙", "庚", "戊"], "午": ["丁", "己"],
          "未": ["己", "丁", "乙"], "申": ["庚", "壬", "戊"], "酉": ["辛"],
          "戌": ["戊", "辛", "丁"], "亥": ["壬", "甲"]}
SEASON = {"寅": "wood", "卯": "wood", "辰": "earth", "巳": "fire", "午": "fire", "未": "earth",
          "申": "metal", "酉": "metal", "戌": "earth", "亥": "water", "子": "water", "丑": "earth"}


def seasonal_state(elem, month_branch):
    s = SEASON[month_branch]
    i, j = ELEMS.index(elem), ELEMS.index(s)
    return {0: "旺 prosperous", 4: "相 assisted", 1: "休 resting", 2: "囚 confined", 3: "死 dead"}[(i - j) % 5]


def branch_interactions(branches, labels):
    six_combo = {frozenset("子丑"): "earth", frozenset("寅亥"): "wood", frozenset("卯戌"): "fire",
                 frozenset("辰酉"): "metal", frozenset("巳申"): "water", frozenset("午未"): "fire/earth"}
    clash = [frozenset(x) for x in ["子午", "丑未", "寅申", "卯酉", "辰戌", "巳亥"]]
    harm = [frozenset(x) for x in ["子未", "丑午", "寅巳", "卯辰", "申亥", "酉戌"]]
    destroy = [frozenset(x) for x in ["子酉", "卯午", "辰丑", "未戌", "寅亥", "巳申"]]
    trines = {"申子辰": "water", "亥卯未": "wood", "寅午戌": "fire", "巳酉丑": "metal"}
    directional = {"寅卯辰": "wood", "巳午未": "fire", "申酉戌": "metal", "亥子丑": "water"}
    punish3 = ["寅巳申", "丑戌未"]
    out = []
    n = len(branches)
    for i in range(n):
        for j in range(i + 1, n):
            pair = frozenset(branches[i] + branches[j])
            where = [labels[i], labels[j]]
            if pair in six_combo:
                out.append({"type": "six-combination 六合", "branches": branches[i] + branches[j], "pillars": where,
                            "nominal_element": six_combo[pair], "transformation_asserted": False})
            if pair in clash:
                out.append({"type": "clash 六冲", "branches": branches[i] + branches[j], "pillars": where})
            if pair in harm:
                out.append({"type": "harm 六害", "branches": branches[i] + branches[j], "pillars": where})
            if pair in destroy:
                out.append({"type": "destruction 六破", "branches": branches[i] + branches[j], "pillars": where})
            if branches[i] + branches[j] in ("子卯", "卯子"):
                out.append({"type": "punishment 子卯刑", "branches": branches[i] + branches[j], "pillars": where})
            if branches[i] == branches[j] and branches[i] in "辰午酉亥":
                out.append({"type": "self-punishment 自刑", "branches": branches[i] * 2, "pillars": where})
    bs = set(branches)
    for k, el in trines.items():
        present = [b for b in k if b in bs]
        if len(present) == 3:
            out.append({"type": "three-harmony 三合 (complete)", "branches": k, "element": el, "transformation_asserted": False})
        elif len(present) == 2 and k[1] in present:
            out.append({"type": "half three-harmony 半合 (includes central branch)", "branches": "".join(present), "element": el,
                        "transformation_asserted": False})
    for k, el in directional.items():
        present = [b for b in k if b in bs]
        if len(present) == 3:
            out.append({"type": "directional 三会 (complete)", "branches": k, "element": el})
        elif len(present) == 2:
            out.append({"type": "directional 三会 (partial, not formed)", "branches": "".join(present), "element": el})
    for k in punish3:
        present = [b for b in k if b in bs]
        if len(present) == 3:
            out.append({"type": "punishment 三刑 (complete)", "branches": k})
        elif len(present) == 2:
            out.append({"type": "punishment 三刑 (partial)", "branches": "".join(present)})
    return out


def stem_interactions(stems, labels):
    combos = {frozenset("甲己"): "earth", frozenset("乙庚"): "metal", frozenset("丙辛"): "water",
              frozenset("丁壬"): "wood", frozenset("戊癸"): "fire"}
    clashes = [frozenset(x) for x in ["甲庚", "乙辛", "丙壬", "丁癸"]]
    out = []
    for i in range(len(stems)):
        for j in range(i + 1, len(stems)):
            pr = frozenset(stems[i] + stems[j])
            if pr in combos:
                out.append({"type": "stem combination 天干合", "stems": stems[i] + stems[j], "pillars": [labels[i], labels[j]],
                            "nominal_element": combos[pr], "transformation_asserted": False})
            if pr in clashes:
                out.append({"type": "stem clash 天干冲", "stems": stems[i] + stems[j], "pillars": [labels[i], labels[j]]})
    return out


def day_master_strength(pillars):
    """Rule DMS-1: visible stems (excluding DM) weight 1.0; branch hidden stems weight 1.0/0.5/0.3
    (main/middle/residual); month branch weights doubled. Support = same element + resource.
    Strong if support share > 0.5 and DM seasonal state is 旺 or 相; weak if share < 0.4
    and state is 休/囚/死; otherwise balanced."""
    dm = pillars["day"][0]
    de = STEM_ELEMENT[dm]
    res_el = ELEMS[(ELEMS.index(de) - 1) % 5]
    tally = {e: 0.0 for e in ELEMS}
    for k in ("year", "month", "hour"):
        tally[STEM_ELEMENT[pillars[k][0]]] += 1.0
    for k in ("year", "month", "day", "hour"):
        for w, s in zip((1.0, 0.5, 0.3), HIDDEN[pillars[k][1]]):
            tally[STEM_ELEMENT[s]] += w * (2 if k == "month" else 1)
    support = tally[de] + tally[res_el]
    total = sum(tally.values())
    share = support / total
    state = seasonal_state(de, pillars["month"][1])
    roots = [k for k in ("year", "month", "day", "hour") if any(STEM_ELEMENT[s] == de for s in HIDDEN[pillars[k][1]])]
    if share > 0.5 and state[0] in "旺相":
        verdict = "strong"
    elif share < 0.4 and state[0] in "休囚死":
        verdict = "weak"
    else:
        verdict = "balanced"
    return {"rule": day_master_strength.__doc__.strip(), "day_master": dm, "element": de,
            "element_tally": tally, "support_share": share, "seasonal_state": state,
            "roots_in_pillars": roots, "verdict": verdict}


def useful_god(strength, pillars):
    de = strength["element"]
    i = ELEMS.index(de)
    output, wealth, officer, resource = ELEMS[(i + 1) % 5], ELEMS[(i + 2) % 5], ELEMS[(i + 3) % 5], ELEMS[(i - 1) % 5]
    if strength["verdict"] == "strong":
        fuyi = {"favorable": [officer, output, wealth], "unfavorable": [de, resource]}
    elif strength["verdict"] == "weak":
        fuyi = {"favorable": [resource, de], "unfavorable": [officer, output, wealth]}
    else:
        fuyi = {"favorable": [], "unfavorable": [], "note": "balanced: Fu-Yi school gives no decisive preference"}
    tiaohou = None
    if pillars["day"][0] == "辛" and pillars["month"][1] == "申":
        tiaohou = {"source": "Qiong Tong Bao Jian (穷通宝鉴), 辛金 七月: 壬水为尊，甲戊酌用",
                   "favorable": ["water (壬)"], "secondary": ["wood (甲)", "earth (戊)"]}
    agree = tiaohou is not None and "water" in fuyi.get("favorable", [])
    return {"fu_yi": {"school": "Fu-Yi 扶抑 (support/suppress)", "rule_chain": f"Day Master {strength['verdict']} -> "
                      + ("drain/control/exhaust favored" if strength["verdict"] == "strong" else "support favored"), **fuyi},
            "tiao_hou": tiaohou,
            "schools_agree_on": ["water"] if agree else [],
            "confidence": "medium" if agree else "low"}


def bazi(local, utc, base, inp):
    gender = 1 if inp["normalized"]["gender"] == "male" else 0
    # lunar_python treats input as Beijing time for solar terms: feed it the CST equivalent.
    cst = utc.astimezone(ZoneInfo("Asia/Shanghai"))
    lp_local = Solar.fromYmdHms(local.year, local.month, local.day, local.hour, local.minute, local.second).getLunar().getEightChar()
    lp_cst = Solar.fromYmdHms(cst.year, cst.month, cst.day, cst.hour, cst.minute, cst.second).getLunar()
    ec_cst = lp_cst.getEightChar()
    pillars = {"year": lp_local.getYear(), "month": lp_local.getMonth(), "day": lp_local.getDay(), "hour": lp_local.getTime()}
    indep = bazi_independent(local, utc)
    lat_t = dt.datetime.fromisoformat(base["local_apparent_time"])
    solar_track = bazi_independent(lat_t, utc)
    dm = pillars["day"][0]
    labels = ["year", "month", "day", "hour"]
    detail = {}
    for k in labels:
        s, b = pillars[k][0], pillars[k][1]
        detail[k] = {"pillar": pillars[k], "stem": s, "branch": b, "stem_element": STEM_ELEMENT[s],
                     "stem_polarity": "yang" if STEMS.index(s) % 2 == 0 else "yin",
                     "branch_polarity": "yang" if BRANCHES.index(b) % 2 == 0 else "yin",
                     "hidden_stems": HIDDEN[b],
                     "stem_ten_god": None if k == "day" else ten_god(dm, s),
                     "hidden_ten_gods": [ten_god(dm, h) for h in HIDDEN[b]]}
    ny = {"year": lp_local.getYearNaYin(), "month": lp_local.getMonthNaYin(), "day": lp_local.getDayNaYin(), "hour": lp_local.getTimeNaYin()}
    lp_hidden = [lp_local.getYearHideGan(), lp_local.getMonthHideGan(), lp_local.getDayHideGan(), lp_local.getTimeHideGan()]
    # solar terms
    jd = base["jd_ut"]
    sun = base["tropical"]["Sun"]["lon"]
    prev_jie_lon = 315 + 30 * int(((sun - 315) % 360) // 30)
    prev_jie = solar_longitude_crossing(norm(prev_jie_lon), jd - 15)
    next_jie = solar_longitude_crossing(norm(prev_jie_lon + 30), jd + 15)
    pj, nj = lp_cst.getPrevJie(), lp_cst.getNextJie()

    def lp_utc(s):
        return dt.datetime.strptime(s.getSolar().toYmdHms(), "%Y-%m-%d %H:%M:%S").replace(tzinfo=ZoneInfo("Asia/Shanghai")).astimezone(dt.timezone.utc)
    strength = day_master_strength(pillars)
    # Da Yun
    year_yang = STEMS.index(pillars["year"][0]) % 2 == 0
    forward = (year_yang and gender == 1) or (not year_yang and gender == 0)
    target = next_jie if forward else prev_jie
    interval_days = abs(target - jd)
    offset_days = interval_days * 365.2425 / 3
    start = utc + dt.timedelta(days=offset_days)
    start_local = start.astimezone(local.tzinfo)
    m_idx = [pillar_from_index(i) for i in range(60)].index(pillars["month"])
    dayun = []
    for k in range(1, 11):
        pil = pillar_from_index((m_idx + (k if forward else -k)) % 60)
        s_ = start_local.replace(year=start_local.year + 10 * (k - 1))
        e_ = start_local.replace(year=start_local.year + 10 * k)
        dayun.append({"index": k, "pillar": pil, "start": iso(s_), "end": iso(e_),
                      "stem_ten_god": ten_god(dm, pil[0]), "branch_main_ten_god": ten_god(dm, BRANCH_MAIN[pil[1]]),
                      "hidden_ten_gods": [ten_god(dm, h) for h in HIDDEN[pil[1]]]})
    yun1 = ec_cst.getYun(gender, 1)
    yun2 = ec_cst.getYun(gender, 2)
    annual = []
    for yr in range(local.year, local.year + 41):
        lc = solar_longitude_crossing(315.0, jd_ut(dt.datetime(yr, 2, 4, tzinfo=dt.timezone.utc)))
        p = pillar_from_index((yr - 4) % 60)
        annual.append({"year_pillar": p, "starts_utc": iso(jd_to_utc(lc)), "stem_ten_god": ten_god(dm, p[0]),
                       "branch_main_ten_god": ten_god(dm, BRANCH_MAIN[p[1]])})
    return {
        "primary_track": "local civil time",
        "pillars": pillars, "pillar_detail": detail, "na_yin_traditional_attribute": ny,
        "independent_pillars": indep, "solar_time_track_pillars": solar_track,
        "solar_time_track_differs": solar_track != pillars,
        "lunar_python_hidden_stems": lp_hidden,
        "solar_terms": {
            "previous_jie": {"sun_lon": norm(prev_jie_lon), "utc_swiss": iso(jd_to_utc(prev_jie)),
                             "name_lunar_python": pj.getName(), "utc_lunar_python": iso(lp_utc(pj)),
                             "days_before_birth": jd - prev_jie},
            "next_jie": {"sun_lon": norm(prev_jie_lon + 30), "utc_swiss": iso(jd_to_utc(next_jie)),
                         "name_lunar_python": nj.getName(), "utc_lunar_python": iso(lp_utc(nj)),
                         "days_after_birth": next_jie - jd},
        },
        "stem_interactions": stem_interactions([pillars[k][0] for k in labels], labels),
        "branch_interactions": branch_interactions([pillars[k][1] for k in labels], labels),
        "day_master_strength": strength,
        "useful_god": useful_god(strength, pillars),
        "da_yun": {"direction": "forward" if forward else "backward",
                   "rule": CONVENTIONS["bazi"]["da_yun_start"],
                   "interval_to_jie_days": interval_days, "start_offset_years": offset_days / 365.2425,
                   "start": iso(start_local), "periods": dayun,
                   "cross_check_lunar_python": {
                       "input": "birth converted to Beijing time " + cst.strftime("%Y-%m-%d %H:%M"),
                       "sect1_start": yun1.getStartSolar().toYmdHms(), "sect2_start": yun2.getStartSolar().toYmdHms(),
                       "sect1_first_pillar": yun1.getDaYun()[1].getGanZhi(),
                       "note": "different day-count conventions; spread is school-dependent"}},
        "annual_pillars": annual,
    }

# ---------------------------------------------------------------- Zi Wei


def ziwei(local, inp, yearly_dates):
    hb = ((local.hour + 1) // 2) % 12
    ti = 0 if local.hour == 0 else (12 if local.hour == 23 else hb)
    req = {"solar_date": f"{local.year}-{local.month}-{local.day}", "time_index": ti,
           "gender": "男" if inp["normalized"]["gender"] == "male" else "女", "fix_leap": True,
           "yearly_dates": yearly_dates}
    out = subprocess.run(["node", "run.js", json.dumps(req)], cwd=f"{ROOT}/ziwei",
                         capture_output=True, text=True, check=True)
    z = json.loads(out.stdout)
    # nominal-age -> Gregorian dates via Chinese New Year (lunar_python)
    by = local.year

    def cny(y):
        return Lunar.fromYmd(y, 1, 1).getSolar().toYmd()
    for p in z["palaces"]:
        a, b = p["decadal_nominal_age_range"]
        p["decadal_start"] = local.date().isoformat() if a == 1 else cny(by + a - 1)
        p["decadal_end"] = cny(by + b)
    z["age_convention"] = CONVENTIONS["ziwei"]["age"]
    return z

# ---------------------------------------------------------------- Maya / Tibetan


TZOLKIN = ["Imix", "Ik'", "Ak'bal", "K'an", "Chikchan", "Kimi", "Manik'", "Lamat", "Muluk", "Ok",
           "Chuwen", "Eb", "Ben", "Ix", "Men", "Kib", "Kaban", "Etz'nab", "Kawak", "Ajaw"]
HAAB = ["Pop", "Wo'", "Sip", "Sotz'", "Sek", "Xul", "Yaxk'in", "Mol", "Ch'en", "Yax", "Sak'",
        "Keh", "Mak", "K'ank'in", "Muwan", "Pax", "K'ayab", "Kumk'u", "Wayeb"]


def maya(local):
    lc = mayan.from_gregorian(local.year, local.month, local.day)
    mjd = mayan.to_jd(*lc)
    tz = mayan.to_tzolkin(mjd)
    hb = mayan.to_haab(mjd)
    rt = mayan.to_gregorian(*lc)
    # independent arithmetic
    jdn = int(swe.julday(local.year, local.month, local.day, 12.0))
    days = jdn - 584283
    parts, r = [], days
    for u in (144000, 7200, 360, 20):
        parts.append(r // u)
        r %= u
    parts.append(r)
    num = (4 + days - 1) % 13 + 1
    name = TZOLKIN[(19 + days) % 20]
    hpos = (days + 348) % 365
    h_month, h_day = (HAAB[hpos // 20], hpos % 20) if hpos < 360 else ("Wayeb", hpos - 360)
    return {"correlation": 584283, "long_count": ".".join(map(str, lc)),
            "tzolkin": {"number": tz[0], "day_name_convertdate": tz[1]},
            "haab": {"day": hb[0], "month_convertdate": hb[1]},
            "round_trip_gregorian": list(rt), "round_trip_ok": tuple(rt) == (local.year, local.month, local.day),
            "independent": {"long_count": ".".join(map(str, parts)), "tzolkin": f"{num} {name}",
                            "haab": f"{h_day} {h_month}", "days_since_epoch": days},
            "calendar_round_independent": f"{num} {name} {h_day} {h_month}",
            "day_sign_meaning": None,
            "day_sign_meaning_status": "omitted: no named Maya source bundled in dataset"}


def tibetan(local):
    y = local.year
    # Losar always falls between late January and mid-March; a birth outside that window
    # has an unambiguous Tibetan year regardless of lineage calendar details.
    in_window = (local.month, local.day) >= (1, 20) and (local.month, local.day) <= (3, 20)
    ty = y if (local.month, local.day) > (3, 20) else (None if in_window else y - 1)
    if ty is None:
        return {"status": "unavailable", "reason": "birth date within possible Losar window; lineage calendar needed"}
    idx = (ty - 4) % 60
    stem = STEMS[idx % 10]
    elem = {"wood": "Wood", "fire": "Fire", "earth": "Earth", "metal": "Iron", "water": "Water"}[STEM_ELEMENT[stem]]
    animals = ["Mouse", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Sheep", "Monkey", "Bird", "Dog", "Pig"]
    rabjung = (ty - 1027) // 60 + 1
    return {"tibetan_year_gregorian_start": ty, "element": elem, "animal": animals[idx % 12],
            "gender": "male" if idx % 2 == 0 else "female",
            "rabjung": rabjung, "year_in_rabjung": (ty - 1027) % 60 + 1,
            "losar_boundary": "Losar falls between ~20 Jan and ~20 Mar in any year; birth date is outside that window, so the year is lineage-independent",
            "omitted": ["Mewa", "Parkha", "la/sok/wangthang/lungta/life-force", "annual obstacles"],
            "omitted_reason": "no validated lineage-specific implementation available"}

# ---------------------------------------------------------------- driver


def compute_all(inp, offset_minutes=0.0, now_utc=None, full=True):
    n = inp["normalized"]
    local, utc = local_instant(n["local_date"], n["local_time_24h"], "Asia/Kolkata", offset_minutes)
    now_utc = now_utc or dt.datetime.now(dt.timezone.utc)
    base = shared_base(local, utc, inp)
    out = {"instant": {"offset_minutes": offset_minutes, "local": iso(local), "utc": iso(utc)},
           "base": base,
           "jyotisha": jyotisha(base, utc, now_utc),
           "western": western(base, now_utc.astimezone(ZoneInfo("America/Vancouver")).date(), local, inp),
           "bazi": bazi(local, utc, base, inp)}
    if full:
        dates = [f"{y}-06-01" for y in range(local.year + 1, local.year + 41)]
        out["ziwei"] = ziwei(local, inp, dates)
        out["maya"] = maya(local)
        out["tibetan"] = tibetan(local)
    else:
        out["ziwei"] = ziwei(local, inp, [])
    return out


def signature(c):
    """Flattened facts compared across the uncertainty ensemble."""
    j, w, b, z = c["jyotisha"], c["western"], c["bazi"], c["ziwei"]
    sig = {
        "jyotisha.lagna_sign": j["lagna"]["sign"], "jyotisha.lagna_nakshatra_pada": f'{j["lagna"]["nakshatra"]["name"]}-{j["lagna"]["nakshatra"]["pada"]}',
        "jyotisha.D9_lagna": j["lagna"]["d9_sign"], "jyotisha.D10_lagna": j["lagna"]["d10_sign"],
        "jyotisha.moon_nakshatra_pada": f'{j["grahas"]["Moon"]["nakshatra"]["name"]}-{j["grahas"]["Moon"]["nakshatra"]["pada"]}',
        "jyotisha.current_dasha": f'{j["current_dasha"]["mahadasha"]}/{j["current_dasha"]["antardasha"]}',
        "western.asc_sign": w["ascendant"]["sign"], "western.mc_sign": w["mc"]["sign"],
        "western.sect": w["sect"]["chart"], "western.fortune_sign": w["lots"]["fortune"]["sign"],
        "western.spirit_sign": w["lots"]["spirit"]["sign"], "western.profection": w["profection_current"]["sign"],
        "bazi.pillars": " ".join(b["pillars"].values()), "bazi.solar_track": " ".join(b["solar_time_track_pillars"].values()),
        "bazi.da_yun_direction": b["da_yun"]["direction"],
        "ziwei.soul_palace": z["soul_palace_branch"], "ziwei.body_palace": z["body_palace_branch"],
        "ziwei.bureau": z["five_elements_bureau"],
        "ziwei.major_stars": ";".join(f'{p["earthly_branch"]}:{",".join(s["name"] for s in p["major_stars"])}' for p in z["palaces"]),
    }
    for p, g in j["grahas"].items():
        sig[f"jyotisha.{p}.sign_house"] = f'{g["sign"]}/{g["house"]}'
        sig[f"jyotisha.{p}.nakshatra_pada"] = f'{g["nakshatra"]["name"]}-{g["nakshatra"]["pada"]}'
        sig[f"jyotisha.{p}.D9"] = g["d9_sign"]
        sig[f"jyotisha.{p}.D10"] = g["d10_sign"]
    for p, g in w["planets"].items():
        sig[f"western.{p}.sign_house"] = f'{g["sign"]}/{g["house"]}'
        sig[f"western.{p}.bound"] = g["bound_lord"]
    return sig


def find_crossing(inp, fn, lo_min, hi_min, step=0.05):
    """Nearest clock offset (minutes) from 0 toward lo_min or hi_min where fn changes value:
    step-scan outward from 0, then bisect within the first changed step."""
    direction = 1 if hi_min > 0 else -1
    span = hi_min if direction > 0 else -lo_min
    v0 = fn(0)
    prev = 0.0
    k = 1
    while k * step <= span + 1e-9:
        cur = direction * k * step
        if fn(cur) != v0:
            lo, hi = prev, cur
            for _ in range(40):
                mid = (lo + hi) / 2
                if fn(mid) == v0:
                    lo = mid
                else:
                    hi = mid
            return (lo + hi) / 2
        prev = cur
        k += 1
    return None


def boundary_audit(inp, c):
    n = inp["normalized"]
    base = c["base"]
    lat, lon = n["latitude"], n["longitude"]

    def at(off):
        local, utc = local_instant(n["local_date"], n["local_time_24h"], "Asia/Kolkata", off)
        return jd_ut(utc)
    sid_asc = lambda off: angles(at(off), lat, lon, True)["asc"]
    trop_asc = lambda off: angles(at(off), lat, lon, False)["asc"]
    rows = []

    def add(name, fn, span, affects, fmt=lambda v: v):
        back = find_crossing(inp, fn, -span, 0)
        fwd = find_crossing(inp, fn, 0, span)
        rows.append({"boundary": name, "value_at_birth": fmt(fn(0)),
                     "minutes_to_previous_change": None if back is None else -back,
                     "previous_value": None if back is None else fmt(fn(back - 1e-6)),
                     "minutes_to_next_change": fwd, "next_value": None if fwd is None else fmt(fn(fwd + 1e-6)),
                     "search_window_minutes": span, "outputs_affected": affects})
    add("Jyotisha Lagna sign (sidereal Lahiri)", lambda o: SIGNS[sign_of(sid_asc(o))], 180,
        "Lagna, all whole-sign houses, house lords, functional natures, yogas, domain projections")
    add("Jyotisha Lagna nakshatra pada", lambda o: nakshatra(sid_asc(o))["pada"], 60, "Lagna pada")
    add("Jyotisha D9 (Navamsa) Lagna", lambda o: SIGNS[d9_sign(sid_asc(o))], 30, "D9 Lagna and D9 houses")
    add("Jyotisha D10 (Dasamsa) Lagna", lambda o: SIGNS[d10_sign(sid_asc(o))], 30, "D10 Lagna and D10 houses")
    add("Western Ascendant sign (tropical)", lambda o: SIGNS[sign_of(trop_asc(o))], 180,
        "Ascendant, whole-sign houses, lots, profections, domain projections")
    add("Western bound of Ascendant", lambda o: bound_lord(trop_asc(o)), 60, "Ascendant bound lord")

    def sect(o):
        return "day" if sun_altitude(at(o), lat, lon, n["elevation_m"])["apparent_alt"] > 0 else "night"
    add("Sunrise / Western sect", sect, 120, "sect, Lot of Fortune/Spirit formulas, sect benefic/malefic")

    def fortune_sign(o):
        j = at(o)
        a = angles(j, lat, lon)["asc"]
        s = swe.calc_ut(j, swe.SUN, FLAGS)[0][0]
        m = swe.calc_ut(j, swe.MOON, FLAGS)[0][0]
        day = sect(o) == "day"
        return SIGNS[sign_of(a + m - s if day else a + s - m)]
    add("Lot of Fortune sign", fortune_sign, 120, "Lot of Fortune house")

    def spirit_sign(o):
        j = at(o)
        a = angles(j, lat, lon)["asc"]
        s = swe.calc_ut(j, swe.SUN, FLAGS)[0][0]
        m = swe.calc_ut(j, swe.MOON, FLAGS)[0][0]
        day = sect(o) == "day"
        return SIGNS[sign_of(a + s - m if day else a + m - s)]
    add("Lot of Spirit sign", spirit_sign, 120, "Lot of Spirit house")

    def hour_branch(o):
        local, _ = local_instant(n["local_date"], n["local_time_24h"], "Asia/Kolkata", o)
        return BRANCHES[((local.hour + 1) // 2) % 12]
    add("BaZi / Zi Wei two-hour branch (civil clock)", hour_branch, 180, "hour pillar; Zi Wei Ming/Shen palaces and hour stars")
    eot = base["equation_of_time_minutes"]
    lmt_off = n["longitude"] / 15 * 60 - 330
    rows.append({"boundary": "BaZi / Zi Wei two-hour branch (local apparent solar time)",
                 "value_at_birth": c["bazi"]["solar_time_track_pillars"]["hour"][1],
                 "local_apparent_time": base["local_apparent_time"],
                 "minutes_to_previous_change": (dt.datetime.fromisoformat(base["local_apparent_time"]) - dt.datetime.fromisoformat(base["local_apparent_time"][:11] + "05:00:00")).total_seconds() / 60,
                 "minutes_to_next_change": (dt.datetime.fromisoformat(base["local_apparent_time"][:11] + "07:00:00") - dt.datetime.fromisoformat(base["local_apparent_time"])).total_seconds() / 60,
                 "note": f"clock-to-solar correction = {lmt_off + eot:.2f} min (longitude {lmt_off:.2f} + equation of time {eot:.2f})",
                 "outputs_affected": "hour pillar under solar-time school"})
    local_birth = dt.datetime.fromisoformat(c["instant"]["local"])
    rows.append({"boundary": "Civil midnight / late-Zi day boundary",
                 "minutes_since_midnight": local_birth.hour * 60 + local_birth.minute,
                 "minutes_to_23:00": (23 - local_birth.hour) * 60 - local_birth.minute,
                 "outputs_affected": "day pillar, Zi Wei lunar day (not at risk)"})
    st = c["bazi"]["solar_terms"]
    rows.append({"boundary": "BaZi sectional solar term (month pillar)",
                 "previous": st["previous_jie"], "next": st["next_jie"],
                 "outputs_affected": "month pillar, Da Yun start"})
    rows.append({"boundary": "Zi Wei lunar day / leap month",
                 "lunar_date": c["ziwei"]["lunar"], "note": "lunar day 21 of a non-leap month; nearest new moons ~6-9 days away",
                 "outputs_affected": "Ming/Shen palaces, bureau, star placement"})
    rows.append({"boundary": "Tibetan Losar", "note": c["tibetan"].get("losar_boundary"), "outputs_affected": "element-animal year"})
    rows.append({"boundary": "Gregorian adoption", "note": "India used the Gregorian civil calendar long before 2005; not applicable",
                 "outputs_affected": "none"})
    # Moon nakshatra boundary via Moon speed
    moon = c["base"]["sidereal"]["Moon"]
    nk_frac = (norm(moon["lon"]) % (40 / 3))
    speed_min = moon["speed"] / 1440
    rows.append({"boundary": "Moon nakshatra (Vimshottari lord)", "value_at_birth": nakshatra(moon["lon"])["name"],
                 "minutes_to_previous_change": nk_frac / speed_min, "minutes_to_next_change": (40 / 3 - nk_frac) / speed_min,
                 "outputs_affected": "Vimshottari sequence and all dasha dates; each clock minute shifts every dasha boundary by "
                 f"{(speed_min / (40 / 3)) * DASHA_YEARS[nakshatra(moon['lon'])['lord']] * 365.25:.2f} days"})
    return rows


def main():
    inp = load_input()
    now = dt.datetime.now(dt.timezone.utc)
    unc = inp["normalized"]["time_uncertainty_minutes"]
    c = compute_all(inp, 0.0, now)
    ens = {}
    sigs = {}
    for off in (-unc, 0.0, unc):
        cc = c if off == 0 else compute_all(inp, off, now, full=False)
        sigs[off] = signature(cc)
        ens[str(off)] = {"local": cc["instant"]["local"],
                         "vimshottari_first_md_end": cc["jyotisha"]["vimshottari"]["mahadashas"][0]["end"],
                         "da_yun_start": cc["bazi"]["da_yun"]["start"],
                         "asc_tropical": cc["base"]["angles_tropical"]["asc"],
                         "asc_sidereal": cc["base"]["angles_sidereal"]["asc"]}
    stability = {}
    for k in sigs[0.0]:
        vals = {str(o): sigs[o][k] for o in sigs}
        stability[k] = {"values": vals, "classification": "stable" if len(set(vals.values())) == 1 else "sensitive"}
    audit = boundary_audit(inp, c)
    master = {
        "schema": "six-culture-verified-chart/master/v2",
        "generated_utc": iso(now),
        "input": inp,
        "conventions": CONVENTIONS,
        "reported_instant": c["instant"],
        "shared_astronomy": c["base"],
        "jyotisha": c["jyotisha"], "western": c["western"], "bazi": c["bazi"],
        "ziwei": c["ziwei"], "maya": c["maya"], "tibetan": c["tibetan"],
        "uncertainty_ensemble": {"offsets_minutes": [-unc, 0, unc], "instants": ens, "stability": stability},
        "boundary_audit": audit,
        "excluded_methods": {
            "jyotisha": c["jyotisha"]["unavailable"], "western": c["western"]["unavailable"],
            "maya": {"day_sign_meaning": c["maya"]["day_sign_meaning_status"]},
            "tibetan": {"omitted": c["tibetan"]["omitted"], "reason": c["tibetan"]["omitted_reason"]},
            "ziwei": {"py-iztro": "not used: same underlying iztro method, would add no independence"},
            "jaimini_kp_alt_ayanamsha": "separate tracks not requested; not computed",
        },
    }
    dump("MASTER_DATASET.json", master)
    print("MASTER_DATASET.json written")


if __name__ == "__main__":
    main()
