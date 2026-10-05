# Input audit

## Original entry (verbatim)

- **date of birth**: 23 January 2005
- **time of birth**: 1 a.m.
- **time certainty**: I am sure about my birth time because doctors had a stopwatch in their hand to calculate that.
- **birthplace**: Jalandhar which is in Punjab in India
- **gender**: female
- **current residence**: Langley
- **calendar note**: No non-Gregorian calendar or DST/time-zone uncertainty mentioned.

## Normalized

- Calendar: gregorian — No other calendar mentioned; date treated as a Gregorian civil date.
- Local civil time: **2005-01-23T01:00:00+05:30** (Sunday)
- IANA zone: Asia/Kolkata; UTC offset 5:30:00; DST 0:00:00 (India has observed no DST since 1945; the +06:30 war-time offset ended in 1945)
- UTC instant: **2005-01-22T19:30:00+00:00**; JD(UT) 2453393.312500; ΔT 64.69 s
- Coordinates: 31.326° N, 75.5762° E, elevation 228 m — Jalandhar city centre, standard gazetteer values (about +/-5 km for an unnamed in-city hospital)
- Local mean time: 00:32:18; equation of time -11.73 min; local apparent solar time **00:20:34**
- Sunrise 07:24:56, sunset 17:54:26 (local civil time) on the birth date; birth 384.9 min before that sunrise; Sun apparent altitude -77.31°
- Time precision: minute; ensemble ±1 min (Reported as exact (timed by the delivery staff) but stated only to the minute; a +/-1 minute ensemble covers minute rounding/truncation.)
- Gender: female; current residence: Langley, British Columbia, Canada (No state or country was given; Langley, British Columbia is assumed. Langley WA or VA would change only the relocated solar-return angles.)

## Boundary audit

| Boundary | Value at birth | Min to previous change | Min to next change | Affects |
|---|---|---|---|---|
| Jyotisha Lagna sign (sidereal Lahiri) | Libra | 49.70 → Virgo | 92.37 → Scorpio | Lagna, all whole-sign houses, house lords, functional natures, yogas, domain projections |
| Jyotisha Lagna nakshatra pada | 2 | 2.69 → 1 | 13.08 → 3 | Lagna pada |
| Jyotisha D9 (Navamsa) Lagna | Capricorn | 2.69 → Sagittarius | 13.08 → Aquarius | D9 Lagna and D9 houses |
| Jyotisha D10 (Dasamsa) Lagna | Capricorn | 7.41 → Sagittarius | 6.77 → Aquarius | D10 Lagna and D10 houses |
| Western Ascendant sign (tropical) | Scorpio | 21.20 → Libra | 121.29 → Sagittarius | Ascendant, whole-sign houses, lots, profections, domain projections |
| Western bound of Ascendant | Mars | 30.60 → Venus | 11.85 → Venus | Ascendant bound lord |
| Sunrise / Western sect | night | — | — | sect, Lot of Fortune/Spirit formulas, sect benefic/malefic |
| Lot of Fortune sign | Gemini | 14.85 → Taurus | — | Lot of Fortune house |
| Lot of Spirit sign | Aries | 27.10 → Pisces | 110.39 → Taurus | Lot of Spirit house |
| BaZi / Zi Wei two-hour branch (civil clock) | 丑 | 0.00 → 子 | 120.00 → 寅 | hour pillar; Zi Wei Ming/Shen palaces and hour stars |
| BaZi / Zi Wei two-hour branch (local apparent solar time) | 子 | 80.57 → 亥 | 39.43 → 丑 | hour pillar and Zi Wei Ming/Shen palaces under the solar-time school |
| Civil midnight / late-Zi day boundary | 60 min after midnight; 1320 min before 23:00 | — | — | day pillar, Zi Wei lunar day (not at risk) |
| BaZi sectional solar term (month pillar) | after 小寒 2005-01-05T06:02:59+00:00 by 17.56 d; before 立春 by 11.93 d | — | — | month pillar, Da Yun start |
| Zi Wei lunar day / leap month | lunar 12/14, leap=False | — | — | Ming/Shen palaces, bureau, star placement |
| Tibetan Losar | birth 2005-01-23 is before 2005-02-08 (day before Chinese New Year 2005-02-09), the earliest possible Losar; year label is lineage-independent | — | — | element-animal year |
| Gregorian adoption | civil calendar has been Gregorian at the birthplace for the whole period; not applicable | — | — | none |
| Moon nakshatra (Vimshottari lord) | Ardra | 456.07 | 1163.07 | Vimshottari sequence and all dasha dates; each clock minute shifts every dasha boundary by 4.06 days |

Sect note: Swiss sunrise uses the Sun's upper limb; sect uses the Sun centre's apparent altitude.

## Time-uncertainty ensemble (−1, 0, +1 min)

| Datum | −1 min | reported | +1 min | Class |
|---|---|---|---|---|
| jyotisha.lagna_sign | Libra | Libra | Libra | **stable** |
| jyotisha.lagna_nakshatra_pada | Swati-2 | Swati-2 | Swati-2 | **stable** |
| jyotisha.D9_lagna | Capricorn | Capricorn | Capricorn | **stable** |
| jyotisha.D10_lagna | Capricorn | Capricorn | Capricorn | **stable** |
| jyotisha.moon_nakshatra_pada | Ardra-2 | Ardra-2 | Ardra-2 | **stable** |
| jyotisha.current_dasha | Jupiter/Venus | Jupiter/Venus | Jupiter/Venus | **stable** |
| western.asc_sign | Scorpio | Scorpio | Scorpio | **stable** |
| western.mc_sign | Leo | Leo | Leo | **stable** |
| western.sect | night | night | night | **stable** |
| western.fortune_sign | Gemini | Gemini | Gemini | **stable** |
| western.spirit_sign | Aries | Aries | Aries | **stable** |
| western.profection | Leo | Leo | Leo | **stable** |
| bazi.pillars | 甲申 丁丑 丁未 庚子 | 甲申 丁丑 丁未 辛丑 | 甲申 丁丑 丁未 辛丑 | **sensitive** |
| bazi.solar_track | 甲申 丁丑 丁未 庚子 | 甲申 丁丑 丁未 庚子 | 甲申 丁丑 丁未 庚子 | **stable** |
| bazi.da_yun_direction | backward | backward | backward | **stable** |
| ziwei.soul_palace | 丑 | 子 | 子 | **sensitive** |
| ziwei.body_palace | 丑 | 寅 | 寅 | **sensitive** |
| ziwei.bureau | 水二局 | 水二局 | 水二局 | **stable** |
| ziwei.major_stars | 寅:七杀;卯:天同;辰:武曲;巳:太阳;午:破军;未:天机;申:紫微,天府;酉:太阴;戌:贪狼;亥:巨门;子:廉贞,天相;丑:天梁 | 寅:七杀;卯:天同;辰:武曲;巳:太阳;午:破军;未:天机;申:紫微,天府;酉:太阴;戌:贪狼;亥:巨门;子:廉贞,天相;丑:天梁 | 寅:七杀;卯:天同;辰:武曲;巳:太阳;午:破军;未:天机;申:紫微,天府;酉:太阴;戌:贪狼;亥:巨门;子:廉贞,天相;丑:天梁 | **stable** |

66 of 69 tracked facts are stable across the interval; sensitive: bazi.pillars, ziwei.soul_palace, ziwei.body_palace.
No rectification was performed.
