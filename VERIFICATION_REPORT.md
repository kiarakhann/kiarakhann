# Verification report

Machine-readable source: `VERIFICATION_REPORT.json`.

## Engines

- **primary_astronomy**: Swiss Ephemeris 2.10.03 via pyswisseph 2.10.3.2 (sepl_18.se1, semo_18.se1)
- **validator_astronomy**: Skyfield 1.55 + JPL DE421 (skyfield-data package); DE440/DE441 not reachable (JPL host blocked by network policy)
- **chinese_calendar**: lunar_python 1.4.8; hand-coded sexagenary arithmetic as validator
- **ziwei**: iztro 2.6.1 (single method)
- **maya**: convertdate 2.5.1 + hand-coded arithmetic

## Summary: 41 pass, 0 alert, 0 fail, 2 single-engine (of 43)

Thresholds: {'planet_deg': 0.01, 'angle_deg': 0.05, 'solar_term_s': 120, 'sunrise_s': 60, 'node_deg': 0.01}

Largest differences: degrees: Sun apparent altitude (sect) = 0.0139; seconds: Sunrise at birthplace = 2.21; days: Vimshottari balance at birth (Venus, years) = 0.628

Invariant failures: none. Systems halted: none.

| System | Datum | Primary | Validator | Difference | Stability | Confidence | Status |
|---|---|---|---|---|---|---|---|
| shared | Sun tropical apparent longitude | 151.93690 | 151.93689 (Skyfield 1.55 + JPL DE421) | 6.48e-06 | stable | high | pass |
| shared | Moon tropical apparent longitude | 42.87936 | 42.87927 (Skyfield 1.55 + JPL DE421) | 9.10e-05 | stable | high | pass |
| shared | Mercury tropical apparent longitude | 133.59844 | 133.59843 (Skyfield 1.55 + JPL DE421) | 7.20e-06 | stable | high | pass |
| shared | Venus tropical apparent longitude | 189.36044 | 189.36043 (Skyfield 1.55 + JPL DE421) | 8.05e-06 | stable | high | pass |
| shared | Mars tropical apparent longitude | 44.31823 | 44.31823 (Skyfield 1.55 + JPL DE421) | 3.01e-06 | stable | high | pass |
| shared | Jupiter tropical apparent longitude | 197.22324 | 197.22324 (Skyfield 1.55 + JPL DE421) | 1.52e-06 | stable | high | pass |
| shared | Saturn tropical apparent longitude | 125.00873 | 125.00873 (Skyfield 1.55 + JPL DE421) | 8.33e-07 | stable | high | pass |
| jyotisha | Mean lunar node (Rahu) tropical longitude | 15.82415 | 15.82520 (Meeus (1998) ch.47 polynomial, hand-coded) | 1.05e-03 | stable | high | pass |
| jyotisha | True lunar node | 14.45963 | — (none) | — | stable | medium | single-engine |
| western | Ascendant tropical longitude | 157.34821 | 157.34608 (spherical formula with Skyfield GAST + true obliquity (hand-coded)) | 2.12e-03 | stable | high | pass |
| western | MC tropical longitude | 65.21944 | 65.21705 (spherical formula with Skyfield GAST + true obliquity (hand-coded)) | 2.39e-03 | stable | high | pass |
| jyotisha | Lagna sidereal longitude (Lahiri) | 133.41329 | 133.41011 (independent tropical Asc minus Swiss Lahiri ayanamsha) | 3.18e-03 | stable | high | pass |
| jyotisha | D9 (Navamsa) Lagna | Leo | — (none) | — | sensitive | low | pass |
| jyotisha | D10 (Dasamsa) Lagna | Sagittarius | — (none) | — | stable | medium | pass |
| shared | Sunrise at birthplace | 2005-08-25T05:59:13+05:30 | 2005-08-25T05:59:10+05:30 (Skyfield almanac.find_risings (DE421)) | 2.21e+00 | stable | high | pass |
| western | Sun apparent altitude (sect) | 5.45236 | 5.43842 (Skyfield altaz(standard refraction)) | 1.39e-02 | stable | high | pass |
| bazi | 立秋 solar term instant (Sun 135 deg) | 2005-08-07T10:03:21+00:00 | {"skyfield": "2005-08-07T10:03:22+00:00", "lunar_python": "2005-08-07T10:03:21+00:00"} (Skyfield DE421 bisection; lunar_python table) | 1.39e+00 | stable | high | pass |
| bazi | 白露 solar term instant (Sun 165 deg) | 2005-09-07T12:56:39+00:00 | {"skyfield": "2005-09-07T12:56:40+00:00", "lunar_python": "2005-09-07T12:56:40+00:00"} (Skyfield DE421 bisection; lunar_python table) | 1.42e+00 | stable | high | pass |
| bazi | Birth after 立秋 and before 白露 (month pillar 申) | true | true (invariant) | — | stable | high | pass |
| bazi | Four Pillars (civil time) | 乙酉 甲申 辛巳 辛卯 | 乙酉 甲申 辛巳 辛卯 (hand-coded sexagenary arithmetic + Swiss solar longitude) | 0 | stable | high | pass |
| bazi | Four Pillars (local apparent solar time track) | 乙酉 甲申 辛巳 辛卯 | — (none) | — | stable | high | pass |
| bazi | Hidden stems | [["辛"], ["庚", "壬", "戊"], ["丙", "庚", "戊"], ["乙"]] | [["辛"], ["庚", "壬", "戊"], ["丙", "庚", "戊"], ["乙"]] (lunar_python table) | 0 | stable | high | pass |
| bazi | Day Master strength | strong | — (none) | — | stable | medium | pass |
| bazi | Useful God / favorable element | ["water"] | — (none) | — | stable | medium | pass |
| bazi | Da Yun start | 2011-07-10T16:49:25+05:30 | {"input": "birth converted to Beijing time 2005-08-25 08:59", "sect1_start": "2011-07-05 08:59:00", "sect2_start": "2011-07-10 00:59:00", "sect1_first_pillar": "癸未", "note": "different day-count conventions; spread is school-dependent"} (lunar_python sect1/sect2 (Beijing-time input)) | ~0-5 days | stable | medium | pass |
| jyotisha | Vimshottari full cycle = 120 years | 120 | 120 (invariant) | 0 | stable | high | pass |
| jyotisha | Vimshottari balance at birth (Venus, years) | 11.58334 | 11.58506 (Skyfield Moon - Lahiri) | 6.28e-01 | stable | high | pass |
| jyotisha | Rahu-Ketu separation | 180.00000 | 180.00000 (invariant) | 5.68e-14 | stable | high | pass |
| jyotisha | Vimshottari MD/AD continuity | true | true (invariant) | — | stable | high | pass |
| bazi | Da Yun continuity | true | true (invariant) | — | stable | high | pass |
| ziwei | Decadal period continuity | true | true (invariant) | — | stable | high | pass |
| western | Profection continuity | true | true (invariant) | — | stable | high | pass |
| ziwei | 12 unique palaces and branches | [12, 12] | [12, 12] (invariant) | — | stable | high | pass |
| ziwei | 14 major stars each placed once | 14 | 14 (invariant) | — | stable | high | pass |
| ziwei | 紫微/天府 mirror across 寅-申 axis | 辰/子 | true (invariant (i+j) mod 12 = 4) | — | stable | high | pass |
| ziwei | Ming (命) palace branch | 巳 | 巳 (hand formula 寅+(month-1)-hour) | — | stable | high | pass |
| ziwei | Shen (身) palace branch | 亥 | 亥 (hand formula 寅+(month-1)+hour) | — | stable | high | pass |
| ziwei | Five Elements Bureau | 金四局 | 辛巳 白蜡金 -> 金四局 (五虎遁 + lunar_python Na Yin table) | — | stable | high | pass |
| ziwei | Lunar date and pillars match lunar_python | 7/21 乙酉 甲申 辛巳 辛卯 | 7/21 (lunar_python) | — | stable | high | pass |
| ziwei | Four Transformations (birth-year stem 乙) | {"天机": "禄", "紫微": "科", "天梁": "权", "太阴": "忌"} | {"天机": "禄", "天梁": "权", "紫微": "科", "太阴": "忌"} (standard 乙年 table (机梁紫阴)) | — | stable | high | pass |
| ziwei | Independence disclosure | single method | — (none) | — | stable | medium | single-engine |
| maya | Long Count / Tzolk'in / Haab' (GMT 584283) | 12.19.12.10.5 7 Chikchan 3 Mol | 12.19.12.10.5 7 Chikchan 3 Mol (hand-coded JDN arithmetic) | — | stable | high | pass |
| tibetan | Element-animal year | Wood Bird (female) | — (none) | — | stable | medium | pass |

Independence disclosure: Skyfield/DE421, the hand-coded Asc/MC and Meeus node formulas, and the hand-coded sexagenary and Maya arithmetic share no code with Swiss Ephemeris, lunar_python, or convertdate. The Lahiri ayanamsha, the true node, and all Zi Wei star placement are single-engine; Zi Wei is checked by structural invariants, not by a second engine.
