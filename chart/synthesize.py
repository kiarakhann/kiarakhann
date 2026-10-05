"""Synthesis: predeclared mapping registry -> projections -> grades, temperament, chronology.
Reads MASTER_DATASET.json + VERIFICATION_REPORT.json, writes SYNTHESIS.json.
"""
import datetime as dt
import json
import os

from common import ROOT, DATA, SIGN_RULER, SIGNS, dump

m = json.load(open(os.path.join(DATA, "MASTER_DATASET.json")))
ver = json.load(open(os.path.join(DATA, "VERIFICATION_REPORT.json")))
if ver["summary"]["systems_halted"]:
    raise SystemExit(f"invariant failure; halted systems: {ver['summary']['systems_halted']}")

GENDER = m["input"]["normalized"]["gender"]
DOMAINS = {"D1": "Self/identity", "D2": "Career/status", "D3": "Wealth/gains", "D4": "Partnership",
           "D5": "Family/roots/home", "D6": "Children/creation", "D7": "Health/routine",
           "D8": "Mind/education/craft", "D9": "Fortune/spirituality/worldview"}
BANDS = ["low", "medium", "high"]

REGISTRY = {
    "MAP-H": {"description": "house -> domain (Jyotisha and Western whole-sign houses)",
              "map": {"D1": [1], "D2": [10], "D3": [2, 11], "D4": [7], "D5": [4], "D6": [5],
                      "D7": [6], "D8": [3], "D9": [9, 12]}, "unmapped": [8]},
    "MAP-ZW": {"description": "Zi Wei palace -> domain",
               "map": {"D1": ["命宫"], "D2": ["官禄"], "D3": ["财帛"], "D4": ["夫妻"], "D5": ["田宅", "父母", "兄弟"],
                       "D6": ["子女"], "D7": ["疾厄"], "D9": ["福德"]}, "unmapped": ["迁移", "仆役"]},
    "MAP-TG": {"description": "BaZi ten god -> domain; spouse and children stars follow the chart's gender convention "
                              "(male: wealth = spouse, officer = children; female: officer = spouse, output = children)",
               "gender": GENDER,
               "map": {"比肩": ["D1"], "劫财": ["D1"], "食神": ["D8", "D6"], "伤官": ["D8", "D6"],
                       "偏财": ["D3"], "正财": ["D3", "D4"] if GENDER == "male" else ["D3"],
                       "七杀": ["D2", "D6"] if GENDER == "male" else ["D2", "D4"],
                       "正官": ["D2", "D6"] if GENDER == "male" else ["D2", "D4"],
                       "偏印": ["D8", "D5"], "正印": ["D8", "D5"]},
               "positional": {"year": ["D5"], "month": ["D5"], "day_branch": ["D4"], "hour": ["D6"]}},
    "J-DOM-1": "Jyotisha per house: P = 2*occupants(9 grahas) + [lord in 1/4/5/7/9/10] + [lord exalted/moolatrikona/own]; "
               "net = sum(occupant weights) + sum(graha-drishti weights) + lord score; weights: Jupiter/Venus/Mercury/Moon +1, "
               "Sun/Mars/Saturn/Rahu/Ketu -1; lord score: +1 strong dignity, -1 debilitated (0 if NB-1 neecha-bhanga present), "
               "+1 kendra/trikona, -1 in 6/8/12, -1 combust. Multi-house domain: P = max, net = mean.",
    "W-DOM-1": "Western per whole-sign house: P = 2*occupants(7 planets) + [ruler angular] + [ruler domicile/exaltation]; "
               "net = occupant weights + aspect weights + ruler score; occupant weights: benefic of sect +2, other benefic +1, "
               "malefic of sect -1, malefic contrary to sect -2, luminaries/Mercury 0; aspects to the sign: benefic by trine/sextile +1, "
               "malefic by square/opposition -1 (contrary malefic -2); ruler score: +1 domicile/exaltation, -1 detriment/fall, "
               "+1 angular, -1 in 6/8/12, -1 under beams. Multi-house domain: P = max, net = mean.",
    "Z-DOM-1": "Zi Wei per palace: P = 2*major stars + auspicious(左辅右弼文昌文曲天魁天钺禄存) + malefic(擎羊陀罗火星铃星地空地劫) + transformations; "
               "net = major brightness (庙/旺 +1, 得/利/平 0, 不/陷 -1) + 禄/权/科 +1, 忌 -1 + auspicious +1 - malefic 1. "
               "Empty palace borrows opposite palace major stars for net only (借星). Multi-palace domain: P = max, net = mean.",
    "B-DOM-1": "BaZi: P = weighted ten-god occurrences mapped by MAP-TG (visible stem 1.0, hidden main 1.0, middle 0.5, residual 0.3) + positional pillar 0.5; "
               "net = sum over those occurrences of element favourability (Fu-Yi favourable +1, unfavourable -1, +0.5 extra for an element both Fu-Yi and Tiao-Hou favour) "
               "scaled by weight, + interactions on positional pillars (clash -1, destruction/punishment -0.5, combination +0.5). "
               "Bands P: high >= 2.0, medium 1.0-1.99, low < 1.0; polarity threshold +/-1.",
    "BANDS": "J/W/Z prominence: high P>=4, medium 2-3, low <=1. Polarity (J/W/Z): supportive net>=2, challenging net<=-2, else mixed.",
    "SINIC-COMBINE": "BaZi and Zi Wei form one vote: if only one speaks, use it; else prominence = lower band if they differ by one, "
                     "'medium' if they differ by two; polarity = shared value if equal, else 'mixed'. Internal agreement recorded.",
    "SINIC-HOUR": "When the hour branch is sensitive, SINIC-COMBINE is evaluated for every hour alternative; the Sinic cluster "
                  "speaks on a domain, temperament axis or timing activation only if all alternatives give the same result. "
                  "Otherwise it is recorded as 'sensitive' and does not vote.",
    "AGREE": "Two cluster themes agree iff prominence band equal AND polarity equal. They conflict iff prominence differs by two bands "
             "OR one is supportive and the other challenging. Otherwise neither.",
    "GRADE": "DIVERGENT if any pair conflicts; else STRONG if all three speak and all pairs agree; else MODERATE if any pair agrees; "
             "else WEAK if one speaks or none agree/conflict; INSUFFICIENT if none speak.",
    "J-TIME-1": "Jyotisha activation = houses owned and occupied by the current Antardasha lord -> MAP-H",
    "W-TIME-1": "Western activation = profected house + natal house of the year ruler -> MAP-H",
    "S-TIME-1": "Sinic activation = Da Yun stem and branch-main-qi ten gods -> MAP-TG, plus Zi Wei decadal palace -> MAP-ZW",
    "T-AX-1": "Temperament: planet/star associations T1 Sun|紫微,太阳; T2 Mars|七杀,破军,武曲; T3 Moon,Jupiter|天同,天梁,太阴; "
              "T4 Mercury,Jupiter|天机,巨门,文昌,文曲; T5 Mercury,Moon|贪狼,廉贞,天机; T6 Saturn|天府,天相,武曲. "
              "J/W per planet: +1 strong dignity, +1 angular/kendra, +1 Asc/Lagna ruler, -1 debilitated/detriment/fall, -1 in 6/8/12, -1 combust/under beams. "
              "Sinic: +1 per associated major star in 命宫 (-1 if 陷/不), +1 life/body ruler association, BaZi strong Day Master +1 to T2. "
              "Axis supported by a cluster if score >= 2; counter if <= -1.",
}

AUSP = {"左辅", "右弼", "文昌", "文曲", "天魁", "天钺", "禄存"}
SHA = {"擎羊", "陀罗", "火星", "铃星", "地空", "地劫"}
J_W = {"Jupiter": 1, "Venus": 1, "Mercury": 1, "Moon": 1, "Sun": -1, "Mars": -1, "Saturn": -1, "Rahu": -1, "Ketu": -1}


def band(P):
    return "high" if P >= 4 else ("medium" if P >= 2 else "low")


def polarity(net, th=2):
    return "supportive" if net >= th else ("challenging" if net <= -th else "mixed")

# ------------------------------------------------------------ Jyotisha projections


def jyotisha_domains():
    j = m["jyotisha"]
    g = j["grahas"]
    nb = {i["debilitated"] for y in j["yogas"] if y["yoga"].startswith("Neecha") for i in y.get("instances", [])}
    out = {}
    for d, houses in REGISTRY["MAP-H"]["map"].items():
        Ps, nets, basis = [], [], []
        for h in houses:
            occ = [p for p in g if g[p]["house"] == h]
            lord = j["house_lords"][str(h)]
            L = g[lord]
            strong = L["dignity"] in ("exalted", "moolatrikona", "own sign")
            ls = (1 if strong else 0) + (0 if L["dignity"] != "debilitated" else (0 if lord in nb else -1))
            ls += 1 if L["house"] in (1, 4, 5, 7, 9, 10) else 0
            ls -= 1 if L["house"] in (6, 8, 12) else 0
            ls -= 1 if L.get("combust") else 0
            asp = [a["from"] for a in j["graha_drishti"] if a["to_house"] == h]
            P = 2 * len(occ) + (1 if L["house"] in (1, 4, 5, 7, 9, 10) else 0) + (1 if strong else 0)
            net = sum(J_W[p] for p in occ) + sum(J_W[p] for p in asp) + ls
            Ps.append(P)
            nets.append(net)
            basis.append({"house": h, "sign": SIGNS[(SIGNS.index(j["lagna"]["sign"]) + h - 1) % 12], "occupants": occ,
                          "lord": lord, "lord_house": L["house"], "lord_dignity": L["dignity"],
                          "neecha_bhanga_applied": lord in nb and L["dignity"] == "debilitated",
                          "drishti_from": asp, "P": P, "net": net})
        net = sum(nets) / len(nets)
        out[d] = {"domain": d, "system": "jyotisha", "cluster": "jyotisha", "prominence": band(max(Ps)),
                  "polarity": polarity(net), "confidence": "high", "basis": basis, "mapping_rule": "MAP-H + J-DOM-1",
                  "scores": {"P": max(Ps), "net": net}}
    return out

# ------------------------------------------------------------ Western projections


def western_domains():
    w = m["western"]
    pl = w["planets"]
    sect = w["sect"]
    asc_i = SIGNS.index(w["ascendant"]["sign"])

    def occ_w(p):
        if p == sect["benefic_of_sect"]:
            return 2
        if p == sect["benefic_contrary"]:
            return 1
        if p == sect["malefic_of_sect"]:
            return -1
        if p == sect["malefic_contrary"]:
            return -2
        return 0
    out = {}
    for d, houses in REGISTRY["MAP-H"]["map"].items():
        Ps, nets, basis = [], [], []
        for h in houses:
            s = (asc_i + h - 1) % 12
            occ = [p for p in pl if pl[p]["house"] == h]
            ruler = SIGN_RULER[s]
            R = pl[ruler]
            dig = R["dignity"]
            good = dig["domicile"] or dig["exaltation"]
            rs = (1 if good else 0) - (1 if dig["detriment"] or dig["fall"] else 0)
            rs += 1 if R["angular"] else 0
            rs -= 1 if R["house"] in (6, 8, 12) else 0
            rs -= 1 if R["under_beams"] else 0
            asp = []
            for p in pl:
                if p in occ:
                    continue
                k = (s - SIGNS.index(pl[p]["sign"])) % 12
                k = min(k, 12 - k)
                if p in (sect["benefic_of_sect"], sect["benefic_contrary"]) and k in (2, 4):
                    asp.append([p, {2: "sextile", 4: "trine"}[k], 1])
                if p in (sect["malefic_of_sect"], sect["malefic_contrary"]) and k in (3, 6):
                    asp.append([p, {3: "square", 6: "opposition"}[k], -2 if p == sect["malefic_contrary"] else -1])
            P = 2 * len(occ) + (1 if R["angular"] else 0) + (1 if good else 0)
            net = sum(occ_w(p) for p in occ) + sum(a[2] for a in asp) + rs
            Ps.append(P)
            nets.append(net)
            basis.append({"house": h, "sign": SIGNS[s], "occupants": occ, "ruler": ruler, "ruler_house": R["house"],
                          "ruler_dignity": [k for k, v in dig.items() if v], "aspects_in": asp, "P": P, "net": net})
        net = sum(nets) / len(nets)
        out[d] = {"domain": d, "system": "western", "cluster": "western", "prominence": band(max(Ps)),
                  "polarity": polarity(net), "confidence": "high", "basis": basis, "mapping_rule": "MAP-H + W-DOM-1",
                  "scores": {"P": max(Ps), "net": net}}
    return out

# ------------------------------------------------------------ Sinic projections


def ziwei_domains(z):
    by_name = {p["name"]: p for p in z["palaces"]}
    by_branch = {p["earthly_branch"]: p for p in z["palaces"]}
    BR = "子丑寅卯辰巳午未申酉戌亥"
    out = {}
    for d, names in REGISTRY["MAP-ZW"]["map"].items():
        Ps, nets, basis = [], [], []
        for n in names:
            p = by_name[n]
            majors = p["major_stars"]
            minors = [s["name"] for s in p["minor_stars"]]
            aus = [s for s in minors if s in AUSP]
            sha = [s for s in minors if s in SHA]
            muts = [s["mutagen"] for s in p["major_stars"] + p["minor_stars"] if s["mutagen"]]
            borrowed = None
            src = majors
            if not majors:
                opp = by_branch[BR[(BR.index(p["earthly_branch"]) + 6) % 12]]
                src = opp["major_stars"]
                borrowed = opp["name"]
                muts_b = [s["mutagen"] for s in src if s["mutagen"]]
            else:
                muts_b = []
            bright = sum(1 if s["brightness"] in ("庙", "旺") else (-1 if s["brightness"] in ("不", "陷") else 0) for s in src)
            mnet = sum(1 if x in ("禄", "权", "科") else -1 for x in muts + muts_b)
            P = 2 * len(majors) + len(aus) + len(sha) + len(muts)
            net = bright + mnet + len(aus) - len(sha)
            Ps.append(P)
            nets.append(net)
            basis.append({"palace": n, "branch": p["earthly_branch"],
                          "major_stars": [f'{s["name"]}({s["brightness"]}{"," + s["mutagen"] if s["mutagen"] else ""})' for s in majors],
                          "borrowed_from": borrowed, "borrowed_stars": [s["name"] for s in src] if borrowed else None,
                          "auspicious": aus, "malefic": sha, "P": P, "net": net})
        net = sum(nets) / len(nets)
        out[d] = {"prominence": band(max(Ps)), "polarity": polarity(net), "basis": basis, "scores": {"P": max(Ps), "net": net}}
    return out


def bazi_domains(b):
    fav = set(b["useful_god"]["fu_yi"]["favorable"])
    unf = set(b["useful_god"]["fu_yi"]["unfavorable"])
    agree = set(b["useful_god"]["schools_agree_on"])
    from common import STEM_ELEMENT

    def fscore(stem):
        e = STEM_ELEMENT[stem]
        return (1 if e in fav else (-1 if e in unf else 0)) + (0.5 if e in agree else 0)
    occ = []
    for k in ("year", "month", "day", "hour"):
        pd = b["pillar_detail"][k]
        if pd["stem_ten_god"]:
            occ.append((pd["stem_ten_god"], 1.0, pd["stem"], f"{k} stem"))
        for w, s, tg in zip((1.0, 0.5, 0.3), pd["hidden_stems"], pd["hidden_ten_gods"]):
            occ.append((tg, w, s, f"{k} hidden"))
    P = {d: 0.0 for d in DOMAINS}
    net = {d: 0.0 for d in DOMAINS}
    basis = {d: [] for d in DOMAINS}
    for tg, w, s, where in occ:
        for d in REGISTRY["MAP-TG"]["map"][tg]:
            P[d] += w
            net[d] += w * fscore(s)
            basis[d].append(f"{tg}({s},{where},w={w})")
    pos = REGISTRY["MAP-TG"]["positional"]
    pillar_of = {"year": "year", "month": "month", "day_branch": "day", "hour": "hour"}
    for slot, ds in pos.items():
        for d in ds:
            P[d] += 0.5
            basis[d].append(f"positional:{slot}")
    for it in b["branch_interactions"]:
        if "pillars" not in it:
            continue
        wv = -1 if "clash" in it["type"] else (-0.5 if ("destruction" in it["type"] or "punishment" in it["type"]) else (0.5 if "combination" in it["type"] else 0))
        for pl in it["pillars"]:
            for slot, ds in pos.items():
                if pillar_of[slot] == pl:
                    for d in ds:
                        net[d] += wv
                        basis[d].append(f"{it['type']} {it['branches']} ({wv:+})")
    out = {}
    for d in DOMAINS:
        if P[d] == 0:
            continue
        out[d] = {"prominence": "high" if P[d] >= 2 else ("medium" if P[d] >= 1 else "low"),
                  "polarity": polarity(net[d], 1), "basis": basis[d], "scores": {"P": P[d], "net": net[d]}}
    return out


HOUR_ALTS = {hp: a for hp, a in m["sinic_hour_alternatives"]["alternatives"].items() if a["bazi"] and a["ziwei"]}


def sinic_domains_for(b, z):
    zw, bz = ziwei_domains(z), bazi_domains(b)
    out = {}
    for d in DOMAINS:
        a, b = zw.get(d), bz.get(d)
        if not a and not b:
            continue
        if a and b:
            ia, ib = BANDS.index(a["prominence"]), BANDS.index(b["prominence"])
            prom = BANDS[min(ia, ib)] if abs(ia - ib) == 1 else (a["prominence"] if ia == ib else "medium")
            pol = a["polarity"] if a["polarity"] == b["polarity"] else "mixed"
            internal = "agree" if (ia == ib and a["polarity"] == b["polarity"]) else "differ"
        else:
            src = a or b
            prom, pol, internal = src["prominence"], src["polarity"], "single-method"
        out[d] = {"domain": d, "system": "bazi+ziwei", "cluster": "sinic", "prominence": prom, "polarity": pol,
                  "confidence": "medium", "basis": {"ziwei": a, "bazi": b}, "internal_agreement": internal,
                  "mapping_rule": "MAP-ZW + Z-DOM-1; MAP-TG + B-DOM-1; SINIC-COMBINE"}
    return out


def sinic_domains():
    per = {hp: sinic_domains_for(a["bazi"], a["ziwei"]) for hp, a in HOUR_ALTS.items()}
    out, sensitive = {}, {}
    for d in DOMAINS:
        th = {hp: (None if d not in x else (x[d]["prominence"], x[d]["polarity"])) for hp, x in per.items()}
        if len(set(th.values())) == 1:
            if d in next(iter(per.values())):
                rep = next(iter(per.values()))[d]
                rep["hour_alternatives"] = {hp: x[d]["basis"] for hp, x in per.items()} if len(per) > 1 else None
                rep["mapping_rule"] += "; SINIC-HOUR" if len(per) > 1 else ""
                out[d] = rep
        else:
            sensitive[d] = {hp: (None if t is None else {"prominence": t[0], "polarity": t[1], "basis": per[hp][d]["basis"],
                                                          "internal_agreement": per[hp][d]["internal_agreement"]})
                            for hp, t in th.items()}
    return out, sensitive

# ------------------------------------------------------------ grading


def agree(x, y):
    return x["prominence"] == y["prominence"] and x["polarity"] == y["polarity"]


def conflict(x, y):
    ib, jb = BANDS.index(x["prominence"]), BANDS.index(y["prominence"])
    return abs(ib - jb) == 2 or {x["polarity"], y["polarity"]} == {"supportive", "challenging"}


def grade(ths):
    sp = {k: v for k, v in ths.items() if v}
    ks = list(sp)
    pairs = [(a, b) for i, a in enumerate(ks) for b in ks[i + 1:]]
    conf = [(a, b) for a, b in pairs if conflict(sp[a], sp[b])]
    agr = [(a, b) for a, b in pairs if agree(sp[a], sp[b])]
    if not sp:
        g = "INSUFFICIENT"
    elif conf:
        g = "DIVERGENT"
    elif len(sp) == 3 and len(agr) == 3:
        g = "STRONG"
    elif agr:
        g = "MODERATE"
    else:
        g = "WEAK"
    return g, agr, conf


J, W = jyotisha_domains(), western_domains()
S, S_SENSITIVE = sinic_domains()
domains = {}
for d in DOMAINS:
    th = {"jyotisha": J.get(d), "western": W.get(d), "sinic": S.get(d)}
    g, agr, conf = grade(th)
    shared = None
    if agr:
        a0 = th[agr[0][0]]
        shared = {"prominence": a0["prominence"], "polarity": a0["polarity"]}
    domains[d] = {"name": DOMAINS[d], "grade": g, "agreeing_pairs": agr, "conflicting_pairs": conf,
                  "sinic_hour_sensitive": {hp: (None if t is None else {"prominence": t["prominence"], "polarity": t["polarity"]})
                                           for hp, t in S_SENSITIVE[d].items()} if d in S_SENSITIVE else None,
                  "shared_theme": shared,
                  "themes": {k: (None if v is None else {"prominence": v["prominence"], "polarity": v["polarity"]}) for k, v in th.items()},
                  "note": "WEAK: clusters speak but neither agree nor conflict" if g == "WEAK" and sum(1 for v in th.values() if v) > 1 else None}
projections = [p for src in (J, W, S) for p in src.values()]
div = [d for d, v in domains.items() if v["grade"] == "DIVERGENT"]
suff = [d for d, v in domains.items() if v["grade"] != "INSUFFICIENT"]
rates = {"divergent_over_all_nine": f"{len(div)}/9", "divergent_over_all_nine_pct": 100 * len(div) / 9,
         "divergent_over_sufficient": f"{len(div)}/{len(suff)}", "divergent_over_sufficient_pct": 100 * len(div) / len(suff) if suff else None,
         "divergent_domains": div}

# ------------------------------------------------------------ temperament
AX = {"T1": ("Leadership/visibility", ["Sun"], ["紫微", "太阳"]),
      "T2": ("Drive/initiative", ["Mars"], ["七杀", "破军", "武曲"]),
      "T3": ("Nurturing/service", ["Moon", "Jupiter"], ["天同", "天梁", "太阴"]),
      "T4": ("Intellect/craft", ["Mercury", "Jupiter"], ["天机", "巨门", "文昌", "文曲"]),
      "T5": ("Adaptability", ["Mercury", "Moon"], ["贪狼", "廉贞", "天机"]),
      "T6": ("Discipline/structure", ["Saturn"], ["天府", "天相", "武曲"])}


def jy_planet_score(p):
    g = m["jyotisha"]["grahas"][p]
    s, why = 0, []
    if g["dignity"] in ("exalted", "moolatrikona", "own sign"):
        s += 1; why.append(f"{p} {g['dignity']}")
    if g["house"] in (1, 4, 7, 10):
        s += 1; why.append(f"{p} kendra H{g['house']}")
    if m["jyotisha"]["house_lords"]["1"] == p:
        s += 1; why.append(f"{p} Lagna lord")
    if g["dignity"] == "debilitated":
        s -= 1; why.append(f"{p} debilitated")
    if g["house"] in (6, 8, 12):
        s -= 1; why.append(f"{p} in H{g['house']}")
    if g.get("combust"):
        s -= 1; why.append(f"{p} combust")
    return s, why


def w_planet_score(p):
    g = m["western"]["planets"][p]
    d = g["dignity"]
    s, why = 0, []
    if d["domicile"] or d["exaltation"]:
        s += 1; why.append(f"{p} {'domicile' if d['domicile'] else 'exaltation'}")
    if g["angular"]:
        s += 1; why.append(f"{p} angular H{g['house']}")
    if m["western"]["house_rulers"]["1"] == p:
        s += 1; why.append(f"{p} Asc ruler")
    if d["detriment"] or d["fall"]:
        s -= 1; why.append(f"{p} {'detriment' if d['detriment'] else 'fall'}")
    if g["house"] in (6, 8, 12):
        s -= 1; why.append(f"{p} in H{g['house']}")
    if g["under_beams"]:
        s -= 1; why.append(f"{p} under beams")
    return s, why


def sinic_axis_score(stars, ax, b, z):
    ming = next(p for p in z["palaces"] if p["name"] == "命宫")
    ssc, swhy = 0, []
    for s_ in ming["major_stars"]:
        if s_["name"] in stars:
            v = -1 if s_["brightness"] in ("陷", "不") else 1
            ssc += v; swhy.append(f"命宫 {s_['name']}({s_['brightness']}) {v:+}")
    for role, star in (("life ruler", z["life_ruler"]), ("body ruler", z["body_ruler"])):
        if star in stars:
            ssc += 1; swhy.append(f"{role} {star} +1")
    if ax == "T2" and b["day_master_strength"]["verdict"] == "strong":
        ssc += 1; swhy.append("BaZi Day Master strong +1")
    return ssc, swhy


temper = {}
for ax, (name, planets, stars) in AX.items():
    js = [jy_planet_score(p) for p in planets]
    ws = [w_planet_score(p) for p in planets]
    jsc, jwhy = max(x[0] for x in js), [w for x in js for w in x[1]]
    wsc, wwhy = max(x[0] for x in ws), [w for x in ws for w in x[1]]

    def st(x):
        return "supported" if x >= 2 else ("counter" if x <= -1 else "not emphasized")
    alts = {hp: sinic_axis_score(stars, ax, a["bazi"], a["ziwei"]) for hp, a in HOUR_ALTS.items()}
    statuses = {st(x[0]) for x in alts.values()}
    if len(statuses) == 1:
        ssc, swhy = next(iter(alts.values()))
        sv = {"score": ssc, "status": st(ssc), "basis": swhy}
        if len(alts) > 1:
            sv["hour_alternatives"] = {hp: {"score": x[0], "basis": x[1]} for hp, x in alts.items()}
    else:
        sv = {"score": None, "status": "sensitive", "basis": [],
              "hour_alternatives": {hp: {"score": x[0], "status": st(x[0]), "basis": x[1]} for hp, x in alts.items()}}
    votes = {"jyotisha": {"score": jsc, "status": st(jsc), "basis": jwhy},
             "western": {"score": wsc, "status": st(wsc), "basis": wwhy},
             "sinic": sv}
    sup = [k for k, v in votes.items() if v["status"] == "supported"]
    ctr = [k for k, v in votes.items() if v["status"] == "counter"]
    temper[ax] = {"name": name, "votes": votes, "supported_by": sup, "countered_by": ctr,
                  "grade": ("DIVERGENT" if sup and ctr else
                            ("STRONG" if len(sup) == 3 else ("MODERATE" if len(sup) == 2 else ("WEAK" if sup else
                             ("STRONG (counter)" if len(ctr) == 3 else ("MODERATE (counter)" if len(ctr) == 2 else
                              ("WEAK (counter)" if ctr else "NOT EMPHASIZED"))))))),
                  "symbolic_overlay": {"maya": "no attributed meaning in dataset; no corroboration or dissent",
                                       "tibetan": "no attributed meaning in dataset; no corroboration or dissent"}}

# ------------------------------------------------------------ chronology
TG_TIME = REGISTRY["MAP-TG"]["map"]
H2D = {h: d for d, hs in REGISTRY["MAP-H"]["map"].items() for h in hs}
ZW2D = {n: d for d, ns in REGISTRY["MAP-ZW"]["map"].items() for n in ns}
g = m["jyotisha"]["grahas"]


def parse(s):
    x = dt.datetime.fromisoformat(s)
    return x.date() if isinstance(x, dt.datetime) else x


jy_periods = []
for md in m["jyotisha"]["vimshottari"]["mahadashas"]:
    for ad in md["antardashas"]:
        L = ad["lord"]
        hs = set(g[L].get("houses_owned", [])) | {g[L]["house"]}
        jy_periods.append((parse(ad["start"]), parse(ad["end"]), {H2D[h] for h in hs if h in H2D}, f"{md['lord']}/{L} MD/AD"))
w_periods = []
for p in m["western"]["profections"]:
    ds = {H2D.get(p["house"]), H2D.get(p["ruler_natal_house"])} - {None}
    w_periods.append((parse(p["start"]), parse(p["end"]), ds, f"profection H{p['house']} {p['sign']} ({p['year_ruler']} in natal H{p['ruler_natal_house']})"))
dy = [(parse(p["start"]), parse(p["end"]), set(TG_TIME[p["stem_ten_god"]]) | set(TG_TIME[p["branch_main_ten_god"]]), f"Da Yun {p['pillar']} ({p['stem_ten_god']}/{p['branch_main_ten_god']})") for p in m["bazi"]["da_yun"]["periods"]]
zwd_alts = {hp: [(parse(p["decadal_start"]), parse(p["decadal_end"]), {ZW2D[p["name"]]} if p["name"] in ZW2D else set(),
                   f"Zi Wei decadal {p['name']} {p['earthly_branch']}" + (f" [{hp} hour]" if len(HOUR_ALTS) > 1 else ""))
                  for p in a["ziwei"]["palaces"]] for hp, a in HOUR_ALTS.items()}


def active(periods, day):
    return [p for p in periods if p[0] <= day < p[1]]


birth = parse(m["reported_instant"]["local"])
now = dt.date.fromisoformat(m["generated_utc"][:10])
horizon = birth.replace(year=birth.year + 40)
day = birth
timeline = []
cur_key, cur_start, cur_detail = None, None, None
days_with_mod = days_with_strong = total_days = 0
while day < horizon:
    jd_ = active(jy_periods, day)
    wd_ = active(w_periods, day)
    dy_ = active(dy, day)
    zw_by_alt = {hp: active(ps, day) for hp, ps in zwd_alts.items()}
    # SINIC-HOUR: a Zi Wei decadal activation counts only if every hour alternative gives it
    zw_dom = set.intersection(*[set().union(*[p[2] for p in v]) if v else set() for v in zw_by_alt.values()])
    sd_ = dy_ + [p for v in zw_by_alt.values() for p in v]
    act = {"jyotisha": set().union(*[p[2] for p in jd_]) if jd_ else set(),
           "western": set().union(*[p[2] for p in wd_]) if wd_ else set(),
           "sinic": (set().union(*[p[2] for p in dy_]) if dy_ else set()) | zw_dom}
    conv = {}
    for d in DOMAINS:
        cl = tuple(k for k in act if d in act[k])
        if len(cl) >= 2:
            conv[d] = cl
    total_days += 1
    days_with_mod += bool(conv)
    days_with_strong += any(len(v) == 3 for v in conv.values())
    key = tuple(sorted(conv.items()))
    if key != cur_key:
        if cur_key is not None:
            timeline.append({"start": cur_start.isoformat(), "end": day.isoformat(), **cur_detail})
        cur_key, cur_start = key, day
        cur_detail = {"convergences": [{"domain": d, "domain_name": DOMAINS[d], "clusters": list(c),
                                        "level": "STRONG" if len(c) == 3 else "MODERATE"} for d, c in conv.items()],
                      "active": {"jyotisha": [p[3] for p in jd_], "western": [p[3] for p in wd_], "sinic": [p[3] for p in sd_]}}
    day += dt.timedelta(days=1)
timeline.append({"start": cur_start.isoformat(), "end": horizon.isoformat(), **cur_detail})
current = next(t for t in timeline if t["start"] <= now.isoformat() < t["end"])
upcoming = [t for t in timeline if t["start"] > now.isoformat()][:6]
next_strong = next((t for t in timeline if t["start"] > now.isoformat() and any(c["level"] == "STRONG" for c in t["convergences"])), None)

# ------------------------------------------------------------ claims audit
candidates = []
for p in projections:
    candidates.append({"claim": f"{p['cluster']}:{p['domain']} {p['prominence']}/{p['polarity']}", "domain": p["domain"],
                       "confidence": p["confidence"]})
generic = ["You are sometimes outgoing and sometimes reserved", "You have untapped potential", "You value honesty",
           "You can be self-critical", "Relationships are important to you", "You seek security",
           "You will face challenges and grow from them", "You have a creative side"]
kept, removed = [], {"missing_basis": 0, "low_confidence": 0, "merged_into_single_domain_statement": 0, "weak_or_insufficient_domain": 0, "generic_barnum": len(generic)}
seen = set()
for c in candidates:
    g_ = domains[c["domain"]]["grade"]
    if g_ in ("WEAK", "INSUFFICIENT"):
        removed["weak_or_insufficient_domain"] += 1
        continue
    key = (c["domain"], g_)
    if key in seen:
        removed["merged_into_single_domain_statement"] += 1
        continue
    seen.add(key)
    kept.append(c)
sens = [k for k, x in m["uncertainty_ensemble"]["stability"].items() if x["classification"] == "sensitive"]
removed["low_confidence"] += len(sens)  # boundary-sensitive facts excluded from interpretation
removed["sinic_hour_sensitive_domain_themes"] = len(S_SENSITIVE)

syn = {
    "schema": "six-culture-verified-chart/synthesis/v2",
    "primary_clusters": ["jyotisha", "western", "sinic"],
    "overlays_non_voting": ["maya", "tibetan"],
    "mapping_registry": REGISTRY,
    "projections": projections,
    "domains": domains,
    "divergence": rates,
    "temperament": temper,
    "chronology": {"reference_date": now.isoformat(), "horizon": horizon.isoformat(),
                   "base_rate": {"share_of_days_with_any_moderate_or_strong": days_with_mod / total_days,
                                 "share_of_days_with_any_strong": days_with_strong / total_days,
                                 "note": "high base rate means individual MODERATE windows carry little information"},
                   "current": current, "upcoming": upcoming, "next_strong": next_strong,
                   "timeline": timeline,
                   "date_precision": {"vimshottari": "+/-5 days per clock minute; Moon-based", "da_yun": "convention spread ~5 days",
                                      "ziwei_decadal": "Chinese New Year boundaries", "profection": "birthday boundaries"}},
    "claims_audit": {"candidates": len(candidates) + len(generic) + len(sens) + len(S_SENSITIVE), "sensitive_facts_excluded": sens, "kept": len(kept), "removed": removed, "generic_dropped": generic},
    "symbolic_overlays": {"maya": {"calendar_round": m["maya"]["calendar_round_independent"], "long_count": m["maya"]["long_count"],
                                   "meaning": None, "votes": 0},
                          "tibetan": {"year": f'{m["tibetan"]["gender"]} {m["tibetan"]["element"]} {m["tibetan"]["animal"]}', "meaning": None, "votes": 0}},
}
dump("SYNTHESIS.json", syn)
for d, v in domains.items():
    print(d, v["name"], v["grade"], v["themes"])
print(rates)
for k, v in temper.items():
    print(k, v["name"], v["grade"], {c: (x["score"], x["status"]) for c, x in v["votes"].items()})
print("base rate", syn["chronology"]["base_rate"])
print("current", json.dumps(current, ensure_ascii=False))
for u in upcoming:
    print(u["start"], u["end"], [(c["domain"], c["clusters"]) for c in u["convergences"]])
print("next strong", next_strong and (next_strong["start"], next_strong["convergences"]))
print(syn["claims_audit"]["removed"], syn["claims_audit"]["kept"])
