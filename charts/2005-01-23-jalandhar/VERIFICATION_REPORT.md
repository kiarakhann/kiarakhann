# Verification report

Machine-readable source: `VERIFICATION_REPORT.json`.

## Engines

- **primary_astronomy**: Swiss Ephemeris 2.10.03 via pyswisseph 2.10.3.2 (sepl_18.se1, semo_18.se1)
- **validator_astronomy**: Skyfield 1.55 + JPL DE421 (skyfield-data package); DE440/DE441 not reachable (JPL host blocked by network policy)
- **chinese_calendar**: lunar_python 1.4.8; hand-coded sexagenary arithmetic as validator
- **ziwei**: iztro 2.6.1 (single method)
- **maya**: convertdate 2.5.1 + hand-coded arithmetic

## Summary: 49 pass, 0 alert, 0 fail, 2 single-engine (of 51)

Thresholds: {'planet_deg': 0.01, 'angle_deg': 0.05, 'solar_term_s': 120, 'sunrise_s': 60, 'node_deg': 0.01}

Largest differences: degrees: MC tropical longitude = 0.00212; seconds: 小寒 solar term instant (Sun 285 deg) = 0.851; days: Vimshottari balance at birth (Rahu, years) = 0.0348

Invariant failures: none. Systems halted: none.

| System | Datum | Primary | Validator | Difference | Stability | Confidence | Status |
|---|---|---|---|---|---|---|---|
| shared | Sun tropical apparent longitude | 302.88831 | 302.88831 (Skyfield 1.55 + JPL DE421) | 5.86e-06 | stable | high | pass |
| shared | Moon tropical apparent longitude | 94.34837 | 94.34830 (Skyfield 1.55 + JPL DE421) | 7.05e-05 | stable | high | pass |
| shared | Mercury tropical apparent longitude | 288.39007 | 288.39007 (Skyfield 1.55 + JPL DE421) | 8.86e-06 | stable | high | pass |
| shared | Venus tropical apparent longitude | 286.41955 | 286.41954 (Skyfield 1.55 + JPL DE421) | 7.25e-06 | stable | high | pass |
| shared | Mars tropical apparent longitude | 259.48774 | 259.48773 (Skyfield 1.55 + JPL DE421) | 4.04e-06 | stable | high | pass |
| shared | Jupiter tropical apparent longitude | 198.69557 | 198.69557 (Skyfield 1.55 + JPL DE421) | 5.48e-07 | stable | high | pass |
| shared | Saturn tropical apparent longitude | 113.15507 | 113.15507 (Skyfield 1.55 + JPL DE421) | 4.00e-07 | stable | high | pass |
| jyotisha | Mean lunar node (Rahu) tropical longitude | 27.16764 | 27.16941 (Meeus (1998) ch.47 polynomial, hand-coded) | 1.76e-03 | stable | high | pass |
| jyotisha | True lunar node | 27.10619 | — (none) | — | stable | medium | single-engine |
| western | Ascendant tropical longitude | 214.49503 | 214.49321 (spherical formula with Skyfield GAST + true obliquity (hand-coded)) | 1.83e-03 | stable | high | pass |
| western | MC tropical longitude | 127.90471 | 127.90259 (spherical formula with Skyfield GAST + true obliquity (hand-coded)) | 2.12e-03 | stable | high | pass |
| jyotisha | Lagna sidereal longitude (Lahiri) | 190.56902 | 190.56719 (independent tropical Asc minus (Swiss mean Lahiri ayanamsha + Skyfield nutation)) | 1.83e-03 | stable | high | pass |
| jyotisha | D9 (Navamsa) Lagna | Capricorn | — (none) | — | stable | medium | pass |
| jyotisha | D10 (Dasamsa) Lagna | Capricorn | — (none) | — | stable | medium | pass |
| shared | Sunrise at birthplace | 2005-01-23T07:24:56+05:30 | 2005-01-23T07:24:56+05:30 (Skyfield almanac.find_risings (DE421)) | 3.40e-01 | stable | high | pass |
| western | Sun apparent altitude (sect) | -77.31293 | -77.31415 (Skyfield altaz(standard refraction)) | 1.22e-03 | stable | high | pass |
| bazi | 小寒 solar term instant (Sun 285 deg) | 2005-01-05T06:02:59+00:00 | {"skyfield": "2005-01-05T06:02:59+00:00", "lunar_python": "2005-01-05T06:02:59+00:00"} (Skyfield DE421 bisection; lunar_python table) | 8.51e-01 | stable | high | pass |
| bazi | 立春 solar term instant (Sun 315 deg) | 2005-02-03T17:43:02+00:00 | {"skyfield": "2005-02-03T17:43:02+00:00", "lunar_python": "2005-02-03T17:43:02+00:00"} (Skyfield DE421 bisection; lunar_python table) | 6.65e-01 | stable | high | pass |
| bazi | Birth after 小寒 and before 立春 (month pillar 丁丑) | true | true (invariant) | — | stable | high | pass |
| bazi | Four Pillars (civil time) | 甲申 丁丑 丁未 辛丑 | 甲申 丁丑 丁未 辛丑 (hand-coded sexagenary arithmetic + Swiss solar longitude) | 0 | sensitive | low | pass |
| bazi | Four Pillars (local apparent solar time track) | 甲申 丁丑 丁未 庚子 | — (none) | — | stable | low | pass |
| bazi | Hidden stems | [["庚", "壬", "戊"], ["己", "癸", "辛"], ["己", "丁", "乙"], ["己", "癸", "辛"]] | [["庚", "壬", "戊"], ["己", "癸", "辛"], ["己", "丁", "乙"], ["己", "癸", "辛"]] (lunar_python table) | 0 | stable | high | pass |
| bazi | Day Master strength | weak | — (none) | — | stable | medium | pass |
| bazi | Useful God / favorable element | ["wood"] | — (none) | — | stable | medium | pass |
| bazi | Da Yun start | 2010-11-30T23:30:22+05:30 | {"input": "birth converted to Beijing time 2005-01-23 03:30", "sect1_start": "2010-12-03 03:30:00", "sect2_start": "2010-11-30 11:30:00", "sect1_first_pillar": "丙子", "note": "different day-count conventions; spread is school-dependent"} (lunar_python sect1/sect2 (Beijing-time input)) | ~0-5 days | stable | medium | pass |
| jyotisha | Vimshottari full cycle = 120 years | 120 | 120 (invariant) | 0 | stable | high | pass |
| jyotisha | Vimshottari balance at birth (Rahu, years) | 12.92982 | 12.92992 (Skyfield Moon - (mean Lahiri + Skyfield nutation)) | 3.48e-02 | stable | high | pass |
| jyotisha | Rahu-Ketu separation | 180.00000 | 180.00000 (invariant) | 0.00e+00 | stable | high | pass |
| jyotisha | Vimshottari MD/AD continuity | true | true (invariant) | — | stable | high | pass |
| bazi | Da Yun continuity | true | true (invariant) | — | stable | high | pass |
| ziwei | Decadal period continuity | true | true (invariant) | — | stable | high | pass |
| western | Profection continuity | true | true (invariant) | — | stable | high | pass |
| ziwei | 12 unique palaces and branches [庚子 hour] | [12, 12] | [12, 12] (invariant) | — | stable | high | pass |
| ziwei | 14 major stars each placed once [庚子 hour] | 14 | 14 (invariant) | — | stable | high | pass |
| ziwei | 紫微/天府 mirror across 寅-申 axis [庚子 hour] | 申/申 | true (invariant (i+j) mod 12 = 4) | — | stable | high | pass |
| ziwei | Ming (命) palace branch [庚子 hour] | 丑 | 丑 (hand formula 寅+(month-1)-hour) | — | sensitive | low | pass |
| ziwei | Shen (身) palace branch [庚子 hour] | 丑 | 丑 (hand formula 寅+(month-1)+hour) | — | sensitive | low | pass |
| ziwei | Five Elements Bureau [庚子 hour] | 水二局 | 丁丑 涧下水 -> 水二局 (五虎遁 + lunar_python Na Yin table) | — | sensitive | low | pass |
| ziwei | Lunar date and pillars match lunar_python [庚子 hour] | 12/14 甲申 丁丑 丁未 庚子 | 12/14 甲申 丁丑 丁未 庚子 (lunar_python) | — | stable | high | pass |
| ziwei | Four Transformations (lunar-year stem 甲) [庚子 hour] | {"武曲": "科", "太阳": "忌", "破军": "权", "廉贞": "禄"} | {"廉贞": "禄", "破军": "权", "武曲": "科", "太阳": "忌"} (standard 四化 table (iztro default school)) | — | stable | high | pass |
| ziwei | 12 unique palaces and branches [辛丑 hour] | [12, 12] | [12, 12] (invariant) | — | stable | high | pass |
| ziwei | 14 major stars each placed once [辛丑 hour] | 14 | 14 (invariant) | — | stable | high | pass |
| ziwei | 紫微/天府 mirror across 寅-申 axis [辛丑 hour] | 申/申 | true (invariant (i+j) mod 12 = 4) | — | stable | high | pass |
| ziwei | Ming (命) palace branch [辛丑 hour] | 子 | 子 (hand formula 寅+(month-1)-hour) | — | sensitive | low | pass |
| ziwei | Shen (身) palace branch [辛丑 hour] | 寅 | 寅 (hand formula 寅+(month-1)+hour) | — | sensitive | low | pass |
| ziwei | Five Elements Bureau [辛丑 hour] | 水二局 | 丙子 涧下水 -> 水二局 (五虎遁 + lunar_python Na Yin table) | — | sensitive | low | pass |
| ziwei | Lunar date and pillars match lunar_python [辛丑 hour] | 12/14 甲申 丁丑 丁未 辛丑 | 12/14 甲申 丁丑 丁未 辛丑 (lunar_python) | — | stable | high | pass |
| ziwei | Four Transformations (lunar-year stem 甲) [辛丑 hour] | {"武曲": "科", "太阳": "忌", "破军": "权", "廉贞": "禄"} | {"廉贞": "禄", "破军": "权", "武曲": "科", "太阳": "忌"} (standard 四化 table (iztro default school)) | — | stable | high | pass |
| ziwei | Independence disclosure | single method | — (none) | — | stable | medium | single-engine |
| maya | Long Count / Tzolk'in / Haab' (GMT 584283) | 12.19.11.17.11 1 Chuwen 14 Muwan' | 12.19.11.17.11 1 Chuwen 14 Muwan (hand-coded JDN arithmetic) | — | stable | high | pass |
| tibetan | Element-animal year | Wood Monkey (male) | — (none) | — | stable | medium | pass |

Independence disclosure: Skyfield/DE421, the hand-coded Asc/MC and Meeus node formulas, and the hand-coded sexagenary and Maya arithmetic share no code with Swiss Ephemeris, lunar_python, or convertdate. The Lahiri ayanamsha, the true node, and all Zi Wei star placement are single-engine; Zi Wei is checked by structural invariants, not by a second engine.
