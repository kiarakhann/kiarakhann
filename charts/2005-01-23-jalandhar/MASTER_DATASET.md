# Master dataset (facts only)

Machine-readable source: `MASTER_DATASET.json`. No interpretation here.

## Jyotisha — sidereal Lahiri, whole-sign, mean node

Lagna **Libra 10.57°** (Swati pada 2 — stable), D9 Lagna Capricorn (stable), D10 Lagna Capricorn (stable). Ayanamsha 23.9278°.

| Graha | Sign | Deg | House | Nakshatra-pada | Dignity | Owns | Functional | D9 | D10 |
|---|---|---|---|---|---|---|---|---|---|
| Sun | Capricorn | 8.96 | 4 | Uttara Ashadha-4 | great enemy | [11] | malefic | Pisces | Scorpio |
| Moon | Gemini | 10.42 | 9 | Ardra-2 | neutral | [10] | neutral (kendradhipati) | Capricorn | Virgo |
| Mercury | Sagittarius | 24.46 | 3 | Purva Ashadha-4 | friend | [9, 12] | benefic | Scorpio | Leo |
| Venus | Sagittarius | 22.49 | 3 | Purva Ashadha-3 | friend | [1, 8] | benefic | Libra | Cancer |
| Mars | Scorpio | 25.56 | 2 | Jyeshtha-3 | own sign | [2, 7] | neutral | Aquarius | Pisces |
| Jupiter | Virgo | 24.77 | 12 | Chitra-1 | neutral | [3, 6] | malefic | Leo | Capricorn |
| Saturn | Gemini | 29.23 | 9 | Punarvasu-3 | neutral | [4, 5] | yogakaraka | Gemini | Pisces |
| Rahu | Aries | 3.24 | 7 | Ashwini-1 | — | — | — | Aries | Taurus |
| Ketu | Libra | 3.24 | 1 | Chitra-3 | — | — | — | Libra | Scorpio |

Yogas (declared whitelist):

- **Gajakesari** — Jupiter in kendra (1/4/7/10) from Moon. Basis: `{"jupiter_from_moon": 4}`
- **Kemadruma** — no graha other than Sun/Rahu/Ketu in 2nd or 12th from Moon. Basis: `{"planets_2nd_12th_from_moon": []}` — cancelled per rule (cancelled if any graha other than Sun/Moon/nodes occupies a kendra from Lagna or Moon)
- **Kendra-Trikona Raja** — lord of a kendra and lord of a trikona (different grahas) conjoined, in mutual graha drishti, or in exchange. Basis: `[{"planets": ["Moon", "Mercury"], "relation": ["mutual aspect"], "kendra_lord_houses": [10], "trikona_lord_houses": [9, 12]}, {"planets": ["Moon", "Saturn"], "relation": ["conjunction"], "kendra_lord_houses": [10], "trikona_lord_houses": [4, 5]}, {"planets": ["Moon", "Venus"], "relation": ["mutual aspect"], "kendra_lord_houses": [10], "trikona_lord_houses": [1, 8]}, {"planets": ["Saturn", "Mercury"], "relation": ["mutual aspect"], "kendra_lord_houses": [4, 5], "trikona_lord_houses": [9, 12]}, {"planets": ["Saturn", "Venus"], "relation": ["mutual aspect"], "kendra_lord_houses": [4, 5], "trikona_lord_houses": [1, 8]}, {"planets": ["Venus", "Mercury"], "relation": ["conjunction"], "kendra_lord_houses": [1, 8], "trikona_lord_houses": [9, 12]}]`
- **Yogakaraka** — single graha owning both a kendra (4/7/10) and a trikona (5/9). Basis: `{"Saturn": [4, 5]}`
- **Parivartana** — two grahas each in a sign ruled by the other. Basis: `[["Mercury", "Jupiter"]]`
- Not present: Budha-Aditya, Chandra-Mangala, Pancha-Mahapurusha (Ruchaka), Pancha-Mahapurusha (Bhadra), Pancha-Mahapurusha (Hamsa), Pancha-Mahapurusha (Malavya), Pancha-Mahapurusha (Sasa), Neecha-Bhanga (NB-1)

Vimshottari: Moon in Ardra (lord Rahu), balance 12.930 y. Year = 365.25 d.

| Mahadasha | Start | End |
|---|---|---|
| Rahu | 1999-12-28 | 2017-12-28 |
| Jupiter | 2017-12-28 | 2033-12-28 |
| Saturn | 2033-12-28 | 2052-12-28 |
| Mercury | 2052-12-28 | 2069-12-28 |
| Ketu | 2069-12-28 | 2076-12-28 |
| Venus | 2076-12-28 | 2096-12-28 |

Current: **Jupiter/Venus** 2025-11-09 → 2028-07-10. Pratyantardashas:

- Venus: 2025-11-09 → 2026-04-21
- Sun: 2026-04-21 → 2026-06-08
- Moon: 2026-06-08 → 2026-08-28
- Mars: 2026-08-28 → 2026-10-24
- Rahu: 2026-10-24 → 2027-03-19
- Jupiter: 2027-03-19 → 2027-07-27
- Saturn: 2027-07-27 → 2027-12-28
- Mercury: 2027-12-28 → 2028-05-14
- Ketu: 2028-05-14 → 2028-07-10

## Western / Hellenistic — tropical, whole-sign, 7 planets

Ascendant **Scorpio 4.50°**, MC Leo 7.90° (whole-sign H10). **Night chart**; sect benefic Venus, contrary malefic Saturn.

| Planet | Sign | Deg | House | Essential dignity | Bound | Face | Speed |
|---|---|---|---|---|---|---|---|
| Sun | Aquarius | 2.89 | 4 | detriment, peregrine | Mercury | Venus | 1.017 |
| Moon | Cancer | 4.35 | 9 | domicile, triplicity_any | Mars | Venus | 11.858 |
| Mercury | Capricorn | 18.39 | 3 | peregrine | Venus | Mars | 1.526 |
| Venus | Capricorn | 16.42 | 3 | triplicity_any, bound | Venus | Mars | 1.253 |
| Mars | Sagittarius | 19.49 | 2 | peregrine | Mercury | Moon | 0.699 |
| Jupiter | Libra | 18.70 | 12 | triplicity_any, bound | Jupiter | Saturn | 0.032 |
| Saturn | Cancer | 23.16 | 9 | detriment, peregrine | Jupiter | Moon | -0.081 |

Lots: Fortune Gemini (H8), Spirit Aries (H6). Dispositor terminals (final dispositor or closed reception loop): [['Moon']].

Close aspects (≤3°): Mercury–Venus conjunction 1.97° separating; Mercury–Jupiter square 0.31° applying; Venus–Jupiter square 2.28° applying; Mars–Jupiter sextile 0.79° separating

Current profection: age 21 → H10 Leo, year ruler Sun (natal H4).

- Solar return 2025: 2025-01-22T16:07:37+00:00 UTC — birthplace Asc Virgo 21.2°; current-residence Asc Aquarius 6.0° (location changes Asc: True)
- Solar return 2026: 2026-01-22T21:51:08+00:00 UTC — birthplace Asc Sagittarius 4.1°; current-residence Asc Gemini 27.6° (location changes Asc: True)

## BaZi

Pillars (civil clock): **甲申 丁丑 丁未 辛丑**; solar-time track: 甲申 丁丑 丁未 庚子 (differs); Day Master 丁 (fire).

| Pillar | Stem | Ten God | Branch | Hidden stems | Hidden Ten Gods | Na Yin (traditional) |
|---|---|---|---|---|---|---|
| year | 甲 (wood, yang) | 正印 | 申 | 庚壬戊 | 正财, 正官, 伤官 | 泉中水 |
| month | 丁 (fire, yin) | 比肩 | 丑 | 己癸辛 | 食神, 七杀, 偏财 | 涧下水 |
| day | 丁 (fire, yin) | Day Master | 未 | 己丁乙 | 食神, 比肩, 偏印 | 天河水 |
| hour | 辛 (metal, yin) | 偏财 | 丑 | 己癸辛 | 食神, 七杀, 偏财 | 壁上土 |

Interactions: clash 六冲 丑未 ['month', 'day']; clash 六冲 未丑 ['day', 'hour']; punishment 三刑 (partial) 丑未. No transformation asserted.

Day Master strength (DMS-1): **weak**; support share 0.23; season 休 resting; roots in ['day'].
Useful element: Fu-Yi favors ['wood', 'fire']; Tiao-Hou (Qiong Tong Bao Jian (穷通宝鉴), 丁火 三冬 (亥子丑月): 甲木为尊，庚金为佐) favors ['wood (甲)'], secondary ['metal (庚)']. Schools agree on: **wood**; confidence medium.

Da Yun backward, start 2010-11-30 (offset 5.85 y; lunar_python cross-checks 2010-12-03 / 2010-11-30).

| Da Yun | Start | End | Stem god | Branch god |
|---|---|---|---|---|
| 丙子 | 2010-11-30 | 2020-11-30 | 劫财 | 七杀 |
| 乙亥 | 2020-11-30 | 2030-11-30 | 偏印 | 正官 |
| 甲戌 | 2030-11-30 | 2040-11-30 | 正印 | 伤官 |
| 癸酉 | 2040-11-30 | 2050-11-30 | 七杀 | 偏财 |
| 壬申 | 2050-11-30 | 2060-11-30 | 正官 | 正财 |
| 辛未 | 2060-11-30 | 2070-11-30 | 偏财 | 食神 |

### Hour alternatives (sensitive)

BaZi hour pillar and every Zi Wei placement are recomputed for each two-hour branch reached by the uncertainty ensemble or by the local-apparent-solar-time track; Sinic facts that differ between alternatives are sensitive and are not used as evidence.

- **庚子 hour** (ensemble offsets [-1] min; matches solar-time track: True): pillars 甲申 丁丑 丁未 庚子; DMS-1 weak (support share 0.250); interactions: stem clash 天干冲 甲庚; clash 六冲 丑未; six-combination 六合 丑子; harm 六害 未子; half three-harmony 半合 (includes central branch) 申子; directional 三会 (partial, not formed) 子丑; punishment 三刑 (partial) 丑未
- **辛丑 hour** (ensemble offsets [0.0, 1] min; matches solar-time track: False): pillars 甲申 丁丑 丁未 辛丑; DMS-1 weak (support share 0.233); interactions: clash 六冲 丑未; clash 六冲 未丑; punishment 三刑 (partial) 丑未

## Zi Wei Dou Shu (iztro 2.6.1)


### 庚子 hour chart

Lunar 2004-12-14 (leap False), hour 早子时; Ming 丑, Shen 丑; life ruler 巨门, body ruler 天梁; bureau 水二局.

| Branch | Palace | Major stars (brightness, 化) | Minor stars | Decadal (nominal age) | Decadal dates |
|---|---|---|---|---|---|
| 丙寅 | 父母 | 七杀(庙) | 禄存, 天马, 火星 | 112–121 | 2116-02-14 → 2126-01-23 |
| 丁卯 | 福德 | 天同(平) | 左辅, 擎羊 | 102–111 | 2106-02-04 → 2116-02-14 |
| 戊辰 | 田宅 | 武曲(庙·化科) | 文曲 | 92–101 | 2096-01-25 → 2106-02-04 |
| 己巳 | 官禄 | 太阳(旺·化忌) | — | 82–91 | 2086-02-14 → 2096-01-25 |
| 庚午 | 仆役 | 破军(庙·化权) | — | 72–81 | 2076-02-05 → 2086-02-14 |
| 辛未 | 迁移 | 天机(陷) | 天钺 | 62–71 | 2066-01-26 → 2076-02-05 |
| 壬申 | 疾厄 | 紫微(旺), 天府(得) | — | 52–61 | 2056-02-15 → 2066-01-26 |
| 癸酉 | 财帛 | 太阴(旺) | — | 42–51 | 2046-02-06 → 2056-02-15 |
| 甲戌 | 子女 | 贪狼(庙) | 文昌, 铃星 | 32–41 | 2036-01-28 → 2046-02-06 |
| 乙亥 | 夫妻 | 巨门(旺) | 右弼, 地空, 地劫 | 22–31 | 2026-02-17 → 2036-01-28 |
| 丙子 | 兄弟 | 廉贞(平·化禄), 天相(庙) | — | 12–21 | 2016-02-08 → 2026-02-17 |
| 丁丑 | 命宫 (身) | 天梁(旺) | 天魁, 陀罗 | 2–11 | 2006-01-29 → 2016-02-08 |

### 辛丑 hour chart (reported instant)

Lunar 2004-12-14 (leap False), hour 丑时; Ming 子, Shen 寅; life ruler 贪狼, body ruler 天梁; bureau 水二局.

| Branch | Palace | Major stars (brightness, 化) | Minor stars | Decadal (nominal age) | Decadal dates |
|---|---|---|---|---|---|
| 丙寅 | 福德 (身) | 七杀(庙) | 禄存, 天马 | 102–111 | 2106-02-04 → 2116-02-14 |
| 丁卯 | 田宅 | 天同(平) | 左辅, 火星, 擎羊 | 92–101 | 2096-01-25 → 2106-02-04 |
| 戊辰 | 官禄 | 武曲(庙·化科) | — | 82–91 | 2086-02-14 → 2096-01-25 |
| 己巳 | 仆役 | 太阳(旺·化忌) | 文曲 | 72–81 | 2076-02-05 → 2086-02-14 |
| 庚午 | 迁移 | 破军(庙·化权) | — | 62–71 | 2066-01-26 → 2076-02-05 |
| 辛未 | 疾厄 | 天机(陷) | 天钺 | 52–61 | 2056-02-15 → 2066-01-26 |
| 壬申 | 财帛 | 紫微(旺), 天府(得) | — | 42–51 | 2046-02-06 → 2056-02-15 |
| 癸酉 | 子女 | 太阴(旺) | 文昌 | 32–41 | 2036-01-28 → 2046-02-06 |
| 甲戌 | 夫妻 | 贪狼(庙) | 地空 | 22–31 | 2026-02-17 → 2036-01-28 |
| 乙亥 | 兄弟 | 巨门(旺) | 右弼, 铃星 | 12–21 | 2016-02-08 → 2026-02-17 |
| 丙子 | 命宫 | 廉贞(平·化禄), 天相(庙) | 地劫 | 2–11 | 2006-01-29 → 2016-02-08 |
| 丁丑 | 父母 | 天梁(旺) | 天魁, 陀罗 | 112–121 | 2116-02-14 → 2126-01-23 |

## Maya calendar (GMT 584283)

Long Count **12.19.11.17.11**, Calendar Round **1 Chuwen 14 Muwan**; round-trip OK: True. Day-sign meaning: omitted: no named Maya source bundled in dataset.

## Tibetan elemental (limited)

**Male Wood Monkey** year, rabjung 17 year 18. Omitted: Mewa, Parkha, la/sok/wangthang/lungta/life-force, annual obstacles — no validated lineage-specific implementation available.

## Excluded methods

- **jyotisha**: {"shadbala": "no validated implementation available in this environment", "ashtakavarga": "not computed: no validated implementation; transit support not requested", "D7_D12": "not computed: domain-specific charts not requested"}
- **western**: {"zodiacal_releasing": "not computed: no validated implementation in this environment", "transits": "not computed: specific transit windows not requested", "modern_outer_planets_placidus": "optional modern track not requested; excluded from Hellenistic votes"}
- **maya**: {"day_sign_meaning": "omitted: no named Maya source bundled in dataset"}
- **tibetan**: {"omitted": ["Mewa", "Parkha", "la/sok/wangthang/lungta/life-force", "annual obstacles"], "reason": "no validated lineage-specific implementation available"}
- **ziwei**: {"py-iztro": "not used: same underlying iztro method, would add no independence"}
- **jaimini_kp_alt_ayanamsha**: "separate tracks not requested; not computed"
