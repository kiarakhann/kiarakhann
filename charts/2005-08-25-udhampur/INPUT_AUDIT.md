# Input audit

## Original entry (verbatim)

- **date of birth**: 25th of August 2005
- **time of birth**: 6:29 a.m.
- **time certainty**: The time is very accurate.
- **birthplace**: Udhampur, J and K, India. It was in a nursing home. It's a big nursing home in Udhampur.
- **gender**: male
- **current residence**: Langley, Canada
- **calendar note**: The date of birth is recorded in Indian calendar. No.

## Normalized

- Calendar: gregorian — User answered 'No' to the non-Gregorian calendar question; date treated as Gregorian civil date.
- Local civil time: **2005-08-25T06:29:00+05:30** (Thursday)
- IANA zone: Asia/Kolkata; UTC offset 5:30:00; DST 0:00:00 (India has not observed DST since 1945)
- UTC instant: **2005-08-25T00:59:00+00:00**; JD(UT) 2453607.540972; ΔT 64.78 s
- Coordinates: 32.916° N, 75.1416° E, elevation 756 m — Udhampur town centre, standard gazetteer values (approx. +/-3 km for an unnamed in-town facility)
- Local mean time: 05:59:33; equation of time -2.15 min; local apparent solar time **05:57:24**
- Sunrise 05:59:13, sunset 19:03:18 (IST); birth 29.8 min after sunrise; Sun apparent altitude 5.45°
- Time precision: minute; ensemble ±1 min (User reports the time as very accurate but recorded only to the minute; a +/-1 minute ensemble covers minute rounding/truncation.)
- Gender: male; current residence: Langley, British Columbia, Canada

## Boundary audit

| Boundary | Value at birth | Min to previous change | Min to next change | Affects |
|---|---|---|---|---|
| Jyotisha Lagna sign (sidereal Lahiri) | Leo | 63.87 → Cancer | 78.12 → Virgo | Lagna, all whole-sign houses, house lords, functional natures, yogas, domain projections |
| Jyotisha Lagna nakshatra pada | 1 | 0.38 → 4 | 15.39 → 2 | Lagna pada |
| Jyotisha D9 (Navamsa) Lagna | Leo | 0.38 → Cancer | 15.39 → Virgo | D9 Lagna and D9 houses |
| Jyotisha D10 (Dasamsa) Lagna | Sagittarius | 6.70 → Scorpio | 7.51 → Capricorn | D10 Lagna and D10 houses |
| Western Ascendant sign (tropical) | Virgo | 34.90 → Leo | 106.55 → Libra | Ascendant, whole-sign houses, lots, profections, domain projections |
| Western bound of Ascendant | Venus | 1.65 → Mercury | 45.54 → Jupiter | Ascendant bound lord |
| Sunrise / Western sect | day | 28.50 → night | — | sect, Lot of Fortune/Spirit formulas, sect benefic/malefic |
| Lot of Fortune sign | Taurus | 28.50 → Sagittarius | 53.10 → Gemini | Lot of Fortune house |
| Lot of Spirit sign | Sagittarius | 28.50 → Taurus | 17.71 → Capricorn | Lot of Spirit house |
| BaZi / Zi Wei two-hour branch (civil clock) | 卯 | 89.00 → 寅 | 31.00 → 辰 | hour pillar; Zi Wei Ming/Shen palaces and hour stars |
| BaZi / Zi Wei two-hour branch (local apparent solar time) | 卯 | 57.40 | 62.60 | hour pillar under solar-time school |
| Civil midnight / late-Zi day boundary | 389 min after midnight; 991 min before 23:00 | — | — | day pillar, Zi Wei lunar day (not at risk) |
| BaZi sectional solar term (month pillar) | after 立秋 2005-08-07T10:03:21+00:00 by 17.62 d; before 白露 by 13.50 d | — | — | month pillar, Da Yun start |
| Zi Wei lunar day / leap month | lunar 7/21, leap=False | — | — | Ming/Shen palaces, bureau, star placement |
| Tibetan Losar | Losar falls between ~20 Jan and ~20 Mar in any year; birth date is outside that window, so the year is lineage-independent | — | — | element-animal year |
| Gregorian adoption | India used the Gregorian civil calendar long before 2005; not applicable | — | — | none |
| Moon nakshatra (Vimshottari lord) | Bharani | 611.43 | 841.47 | Vimshottari sequence and all dasha dates; each clock minute shifts every dasha boundary by 5.03 days |

Sect note: Swiss sunrise uses the Sun's upper limb; sect uses the Sun centre's apparent altitude, which crosses 0° about 1.3 min later (28.5 min before birth).

## Time-uncertainty ensemble (−1, 0, +1 min)

| Datum | −1 min | reported | +1 min | Class |
|---|---|---|---|---|
| jyotisha.lagna_sign | Leo | Leo | Leo | **stable** |
| jyotisha.lagna_nakshatra_pada | Magha-4 | Purva Phalguni-1 | Purva Phalguni-1 | **sensitive** |
| jyotisha.D9_lagna | Cancer | Leo | Leo | **sensitive** |
| jyotisha.D10_lagna | Sagittarius | Sagittarius | Sagittarius | **stable** |
| jyotisha.moon_nakshatra_pada | Bharani-2 | Bharani-2 | Bharani-2 | **stable** |
| jyotisha.current_dasha | Moon/Jupiter | Moon/Jupiter | Moon/Jupiter | **stable** |
| western.asc_sign | Virgo | Virgo | Virgo | **stable** |
| western.mc_sign | Gemini | Gemini | Gemini | **stable** |
| western.sect | day | day | day | **stable** |
| western.fortune_sign | Taurus | Taurus | Taurus | **stable** |
| western.spirit_sign | Sagittarius | Sagittarius | Sagittarius | **stable** |
| western.profection | Gemini | Gemini | Gemini | **stable** |
| bazi.pillars | 乙酉 甲申 辛巳 辛卯 | 乙酉 甲申 辛巳 辛卯 | 乙酉 甲申 辛巳 辛卯 | **stable** |
| bazi.solar_track | 乙酉 甲申 辛巳 辛卯 | 乙酉 甲申 辛巳 辛卯 | 乙酉 甲申 辛巳 辛卯 | **stable** |
| bazi.da_yun_direction | backward | backward | backward | **stable** |
| ziwei.soul_palace | 巳 | 巳 | 巳 | **stable** |
| ziwei.body_palace | 亥 | 亥 | 亥 | **stable** |
| ziwei.bureau | 金四局 | 金四局 | 金四局 | **stable** |
| ziwei.major_stars | 寅:贪狼;卯:天机,巨门;辰:紫微,天相;巳:天梁;午:七杀;未:;申:廉贞;酉:;戌:破军;亥:天同;子:武曲,天府;丑:太阳,太阴 | 寅:贪狼;卯:天机,巨门;辰:紫微,天相;巳:天梁;午:七杀;未:;申:廉贞;酉:;戌:破军;亥:天同;子:武曲,天府;丑:太阳,太阴 | 寅:贪狼;卯:天机,巨门;辰:紫微,天相;巳:天梁;午:七杀;未:;申:廉贞;酉:;戌:破军;亥:天同;子:武曲,天府;丑:太阳,太阴 | **stable** |

67 of 69 tracked facts are stable across the interval; sensitive: jyotisha.lagna_nakshatra_pada, jyotisha.D9_lagna.
No rectification was performed.
