# Six-culture verified chart — final reading

> This is a comparison of traditional symbolic systems, computed to stated conventions. It is not a scientifically validated forecast and says nothing certain about the future. No medical, financial, legal, lifespan or fertility claims are made.

## 1. Input and sensitivity

- Born **2005-01-23 01:00 local civil time (UTC+05:30, no DST)** = 2005-01-22 19:30 UTC, a **Sunday**, Jalandhar, Punjab, India (31.326° N, 75.5762° E).
- Local mean time 00:32; local apparent solar time **00:20**; sunrise 07:24, so this is a **night chart** (Sun -77.3° altitude).
- Time treated as exact to the minute (±1 min ensemble). No rectification.
- Current residence: Langley, British Columbia, Canada (No state or country was given; Langley, British Columbia is assumed. Langley WA or VA would change only the relocated solar-return angles).
- **Sensitive (changes inside ±1 min):** bazi.pillars: -1 min → 甲申 丁丑 丁未 庚子 / 0.0 min → 甲申 丁丑 丁未 辛丑 / 1 min → 甲申 丁丑 丁未 辛丑; ziwei.soul_palace: -1 min → 丑 / 0.0 min → 子 / 1 min → 子; ziwei.body_palace: -1 min → 丑 / 0.0 min → 寅 / 1 min → 寅. These are excluded as evidence; both alternatives are shown in the master dataset.
- **Near a boundary but stable at ±1 min:** Jyotisha Lagna nakshatra pada = 2 (2.7 / 13.1 min to previous / next change); Jyotisha D9 (Navamsa) Lagna = Capricorn (2.7 / 13.1 min to previous / next change); Jyotisha D10 (Dasamsa) Lagna = Capricorn (7.4 / 6.8 min to previous / next change); Western bound of Ascendant = Mars (30.6 / 11.8 min to previous / next change); Lot of Fortune sign = Gemini (14.8 / — min to previous / next change).
- **Comfortably stable:** Jyotisha Lagna sign (sidereal Lahiri) = Libra (49.7 / 92.4 min to previous / next change); Western Ascendant sign (tropical) = Scorpio (21.2 / 121.3 min to previous / next change); Lot of Spirit sign = Aries (27.1 / 110.4 min to previous / next change); BaZi / Zi Wei two-hour branch (local apparent solar time) = 子 (80.6 / 39.4 min to previous / next change); Moon nakshatra (Vimshottari lord) = Ardra (456.1 / 1163.1 min to previous / next change).
- Month pillar: birth is 17.56 days after 小寒 and 11.93 days before 立春 — stable.
- **Chinese hour:** the recorded 01:00 is exactly the start of the 丑 (Chou) double-hour. One minute earlier, and the local-apparent-solar-time school (solar time 00:20), give 子 (Zi). So BaZi hour pillar (庚子 vs 辛丑) and the whole Zi Wei palace layout are reported for both hours, and Sinic evidence is used only where both hours agree (rule SINIC-HOUR).
- Convention note: sidereal Saturn is at Gemini 29.23° under Lahiri; an ayanamsha about 1° smaller would move it to the next sign. No alternative-ayanamsha track was requested.

## 2. Verification

- 49/51 checks pass, 0 alerts, 0 invariant failures; 2 single-engine items disclosed.
- Swiss Ephemeris vs JPL DE421 (Skyfield): largest planetary difference 0.00007° (Moon); Ascendant/MC ≤ 0.0021°; solar terms ≤ 0.9 s across three sources; sunrise 0.3 s.
- Two verification bugs were fixed before this run (no chart values changed): the Maya check compared two spellings of the same Haab' month, and the sidereal checks used the Lahiri ayanamsha without nutation. A BaZi seasonal-state table bug (相/休 and 囚/死 swapped) was also fixed in the calculator.
- Unavailable or omitted: Shadbala, Ashtakavarga, D7/D12, zodiacal releasing, transits, Tibetan Mewa/Parkha/life-forces, and Maya day-sign meanings (no named source). Zi Wei is single-engine (iztro), checked by structural invariants for both hour charts. DE440 could not be downloaded, so DE421 was used.

## 3. Divergence rate (read this first)

- **0/9 domains divergent** (0%); 0/9 of domains with sufficient evidence (0%).
- The Sinic cluster is silent on 7 of 9 domains because its two hour charts disagree, so most grades rest on two traditions only. Zero divergence here partly reflects that missing third voice.
- No domain reached STRONG (all three traditions agreeing).
- MODERATE agreements below that say an area is 'not strongly emphasized' are agreements about *low emphasis*, not predictions.

## 4. Cross-cultural themes

### D1 Self/identity — MODERATE (Jyotisha + Sinic (BaZi + Zi Wei) agree: moderately emphasized, mixed testimony)
- Western/Hellenistic: not strongly emphasized, mixed testimony — neither agreeing nor conflicting.
- Jyotisha basis: H1 Libra: occupants Ketu, lord Venus in H3 (friend), drishti from none
- Sinic (BaZi + Zi Wei) basis: [庚子 hour] Zi Wei 命宫 丑: 天梁(旺) + 天魁 + 陀罗 | BaZi 比肩(丁,month stem,w=1.0), 比肩(丁,day hidden,w=0.5) ‖ [辛丑 hour] Zi Wei 命宫 子: 廉贞(平,禄), 天相(庙) + 地劫 | BaZi 比肩(丁,month stem,w=1.0), 比肩(丁,day hidden,w=0.5)

### D2 Career/status — MODERATE (Jyotisha + Western/Hellenistic agree: not strongly emphasized, mixed testimony)
- Sinic (BaZi + Zi Wei): moderately emphasized, mixed testimony — neither agreeing nor conflicting.
- Jyotisha basis: H10 Cancer: occupants none, lord Moon in H9 (neutral), drishti from Sun
- Western/Hellenistic basis: H10 Leo: occupants none, ruler Sun in H4 (detriment, peregrine)

### D3 Wealth/gains — MODERATE (Jyotisha + Western/Hellenistic agree: moderately emphasized, mixed testimony)
- Sinic (BaZi + Zi Wei): silent (no stable basis) — hour-sensitive: 庚子 hour moderately emphasized, mixed testimony; 辛丑 hour emphasized, mixed testimony — neither agreeing nor conflicting.
- Jyotisha basis: H2 Scorpio: occupants Mars, lord Mars in H2 (own sign), drishti from none; H11 Leo: occupants none, lord Sun in H4 (great enemy), drishti from Saturn
- Western/Hellenistic basis: H2 Sagittarius: occupants Mars, ruler Jupiter in H12 (triplicity_any, bound); H11 Virgo: occupants none, ruler Mercury in H3 (peregrine)

### D5 Family/roots/home — MODERATE (Jyotisha + Western/Hellenistic agree: moderately emphasized, mixed testimony)
- Sinic (BaZi + Zi Wei): silent (no stable basis) — hour-sensitive: 庚子 hour emphasized, mostly supportive testimony; 辛丑 hour emphasized, mixed testimony — neither agreeing nor conflicting.
- Jyotisha basis: H4 Capricorn: occupants Sun, lord Saturn in H9 (neutral), drishti from Jupiter
- Western/Hellenistic basis: H4 Aquarius: occupants Sun, ruler Saturn in H9 (detriment, peregrine)

### D6 Children/creation — MODERATE (Jyotisha + Western/Hellenistic agree: not strongly emphasized, mixed testimony)
- Sinic (BaZi + Zi Wei): silent (no stable basis) — hour-sensitive: 庚子 hour emphasized, mixed testimony; 辛丑 hour moderately emphasized, mixed testimony — neither agreeing nor conflicting.
- Jyotisha basis: H5 Aquarius: occupants none, lord Saturn in H9 (neutral), drishti from Mars
- Western/Hellenistic basis: H5 Pisces: occupants none, ruler Jupiter in H12 (triplicity_any, bound)

### D8 Mind/education/craft — MODERATE (Jyotisha + Western/Hellenistic agree: emphasized, mixed testimony)
- Sinic (BaZi + Zi Wei): silent (no stable basis) — hour-sensitive: 庚子 hour emphasized, mixed testimony; 辛丑 hour emphasized, mostly difficult testimony — neither agreeing nor conflicting.
- Jyotisha basis: H3 Sagittarius: occupants Mercury, Venus, lord Jupiter in H12 (neutral), drishti from Moon, Saturn
- Western/Hellenistic basis: H3 Capricorn: occupants Mercury, Venus, ruler Saturn in H9 (detriment, peregrine)

### D9 Fortune/spirituality/worldview — MODERATE (Jyotisha + Western/Hellenistic agree: emphasized, mixed testimony)
- Sinic (BaZi + Zi Wei): silent (no stable basis) — hour-sensitive: 庚子 hour emphasized, mixed testimony; 辛丑 hour moderately emphasized, mostly supportive testimony — neither agreeing nor conflicting.
- Jyotisha basis: H9 Gemini: occupants Moon, Saturn, lord Mercury in H3 (friend), drishti from Mercury, Venus, Mars; H12 Virgo: occupants Jupiter, lord Mercury in H3 (friend), drishti from none
- Western/Hellenistic basis: H9 Cancer: occupants Moon, Saturn, ruler Moon in H9 (domicile, triplicity_any); H12 Libra: occupants Jupiter, ruler Venus in H3 (triplicity_any, bound)

## 5. Disagreements

- No domain has two traditions in direct conflict.
- **Internal disagreement (Sinic, by hour):** D3 Wealth/gains: 庚子 moderately emphasized, mixed testimony vs 辛丑 emphasized, mixed testimony; D4 Partnership: 庚子 emphasized, mixed testimony vs 辛丑 moderately emphasized, mixed testimony; D5 Family/roots/home: 庚子 emphasized, mostly supportive testimony vs 辛丑 emphasized, mixed testimony; D6 Children/creation: 庚子 emphasized, mixed testimony vs 辛丑 moderately emphasized, mixed testimony; D7 Health/routine: 庚子 emphasized, mixed testimony vs 辛丑 moderately emphasized, mixed testimony; D8 Mind/education/craft: 庚子 emphasized, mixed testimony vs 辛丑 emphasized, mostly difficult testimony; D9 Fortune/spirituality/worldview: 庚子 emphasized, mixed testimony vs 辛丑 moderately emphasized, mostly supportive testimony. Not resolved; neither hour is preferred.

## 6. Weak and insufficient areas

- **D4 Partnership — WEAK**: Jyotisha moderately emphasized, mixed testimony; Western/Hellenistic not strongly emphasized, mixed testimony; Sinic (BaZi + Zi Wei) silent (no stable basis). No cross-tradition theme should be read here.
- **D7 Health/routine — WEAK**: Jyotisha not strongly emphasized, mixed testimony; Western/Hellenistic not strongly emphasized, mostly difficult testimony; Sinic (BaZi + Zi Wei) silent (no stable basis). No cross-tradition theme should be read here. This is a symbolic 'routine/health' house or palace only, not a medical statement.

## 7. Temperament overlay

- **T1 Leadership/visibility — NOT EMPHASIZED**: Jyotisha not emphasized (Sun kendra H4); Western/Hellenistic not emphasized (Sun angular H4, Sun detriment); Sinic (BaZi + Zi Wei) not emphasized (庚子 hour: no qualifying factor; 辛丑 hour: no qualifying factor).
- **T2 Drive/initiative — NOT EMPHASIZED**: Jyotisha not emphasized (Mars own sign); Western/Hellenistic not emphasized (Mars Asc ruler); Sinic (BaZi + Zi Wei) not emphasized (庚子 hour: no qualifying factor; 辛丑 hour: no qualifying factor).
- **T3 Nurturing/service — NOT EMPHASIZED**: Jyotisha not emphasized (Jupiter in H12); Western/Hellenistic not emphasized (Moon domicile, Jupiter in H12); Sinic (BaZi + Zi Wei) sensitive (庚子 hour: 命宫 天梁(旺) +1, body ruler 天梁 +1 → supported; 辛丑 hour: body ruler 天梁 +1 → not emphasized).
- **T4 Intellect/craft — WEAK (counter)**: Jyotisha not emphasized (Jupiter in H12); Western/Hellenistic counter (Mercury under beams, Jupiter in H12); Sinic (BaZi + Zi Wei) not emphasized (庚子 hour: life ruler 巨门 +1; 辛丑 hour: no qualifying factor).
- **T5 Adaptability — NOT EMPHASIZED**: Jyotisha not emphasized (no qualifying factor); Western/Hellenistic not emphasized (Mercury under beams, Moon domicile); Sinic (BaZi + Zi Wei) sensitive (庚子 hour: no qualifying factor → not emphasized; 辛丑 hour: 命宫 廉贞(平) +1, life ruler 贪狼 +1 → supported).
- **T6 Discipline/structure — WEAK (counter)**: Jyotisha not emphasized (no qualifying factor); Western/Hellenistic counter (Saturn detriment); Sinic (BaZi + Zi Wei) not emphasized (庚子 hour: no qualifying factor; 辛丑 hour: 命宫 天相(庙) +1).

Symbolic, non-voting overlays: the Maya Calendar Round is **1 Chuwen 14 Muwan** (Long Count 12.19.11.17.11), and the Tibetan year is **male Wood Monkey** (birth precedes Losar, so the previous Tibetan year applies). No sourced meaning is in the dataset for either, so they neither corroborate nor dissent.

## 8. Timing

- Base rate: 94% of all days from birth to age 40 carry at least one two-tradition (MODERATE) overlap, so a single MODERATE window means little. STRONG overlaps cover 12.9% of days.
- **Now (2026-01-23 → 2027-01-23)**: Career/status MODERATE (Western/Hellenistic + Sinic (BaZi + Zi Wei)); Family/roots/home MODERATE (Western/Hellenistic + Sinic (BaZi + Zi Wei)); Mind/education/craft MODERATE (Jyotisha + Sinic (BaZi + Zi Wei)). Active: Jyotisha Jupiter/Venus MD/AD; Western profection H10 Leo (Sun in natal H4); Sinic Da Yun 乙亥 (偏印/正官), Zi Wei decadal 兄弟 子 [庚子 hour], Zi Wei decadal 兄弟 亥 [辛丑 hour].
- **Next STRONG window: 2027-01-23 → 2028-07-10**, Mind/education/craft activated by all three traditions (Jyotisha Jupiter/Venus MD/AD; Western profection H11 Virgo (Mercury in natal H3); Sinic Da Yun 乙亥 (偏印/正官), Zi Wei decadal 夫妻 亥 [庚子 hour], Zi Wei decadal 夫妻 戌 [辛丑 hour]). The natal grade for that domain is MODERATE; this marks *activation* only, not a good or bad outcome.
- Zi Wei decadal palaces differ between the two hour charts; a Zi Wei activation is counted only when both hour charts activate the same domain.
- Date precision: Vimshottari dates move about 4.06 days per clock minute; Da Yun start dates vary by a few days between conventions.

## 9. Claims removed

- 38 candidate claims; 7 kept as domain statements. Removed: missing basis 0, low confidence 3, merged into single domain statement 9, weak or insufficient domain 4, generic barnum 8, sinic hour sensitive domain themes 7.

## 10. Closing frame

This reading shows where three independent symbolic traditions agree or disagree when each is computed to stated rules. The calculations are reproducible and verified. The meanings are traditional conventions, not established causes. Nothing here is fate or a guaranteed event, and it should not replace judgment, professional advice or your own choices.
