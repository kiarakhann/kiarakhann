# Master dataset (facts only)

Machine-readable source: `MASTER_DATASET.json`. No interpretation here.

## Jyotisha — sidereal Lahiri, whole-sign, mean node

Lagna **Leo 13.41°** (Purva Phalguni pada 1 — sensitive), D10 Lagna Sagittarius; D9 Lagna **unavailable** (boundary 23 s away). Ayanamsha 23.9360°.

| Graha | Sign | Deg | House | Nakshatra-pada | Dignity | Owns | Functional | D9 | D10 |
|---|---|---|---|---|---|---|---|---|---|
| Sun | Leo | 8.00 | 1 | Magha-3 | moolatrikona | [1] | benefic | Gemini | Libra |
| Moon | Aries | 18.94 | 9 | Bharani-2 | enemy | [12] | neutral | Virgo | Libra |
| Mercury | Cancer | 19.66 | 12 | Ashlesha-1 | neutral | [2, 11] | malefic | Sagittarius | Virgo |
| Venus | Virgo | 15.43 | 2 | Hasta-2 | debilitated | [3, 10] | malefic | Taurus | Libra |
| Mars | Aries | 20.38 | 9 | Bharani-3 | own sign | [4, 9] | yogakaraka | Libra | Libra |
| Jupiter | Virgo | 23.29 | 2 | Hasta-4 | neutral | [5, 8] | benefic | Cancer | Sagittarius |
| Saturn | Cancer | 11.07 | 12 | Pushya-3 | neutral | [6, 7] | malefic | Libra | Gemini |
| Rahu | Pisces | 21.89 | 8 | Revati-2 | — | — | — | Capricorn | Gemini |
| Ketu | Virgo | 21.89 | 2 | Hasta-4 | — | — | — | Cancer | Sagittarius |

Yogas (declared whitelist):

- **Chandra-Mangala** — Moon and Mars in the same sign. Basis: `{"moon": "Aries", "mars": "Aries"}`
- **Kemadruma** — no graha other than Sun/Rahu/Ketu in 2nd or 12th from Moon. Basis: `{"planets_2nd_12th_from_moon": []}` — cancelled per rule (cancelled if any graha other than Sun/Moon/nodes occupies a kendra from Lagna or Moon)
- **Kendra-Trikona Raja** — lord of a kendra and lord of a trikona (different grahas) conjoined, in mutual graha drishti, or in exchange. Basis: `[{"planets": ["Saturn", "Mars"], "relation": ["mutual aspect"], "kendra_lord_houses": [6, 7], "trikona_lord_houses": [4, 9]}, {"planets": ["Venus", "Jupiter"], "relation": ["conjunction"], "kendra_lord_houses": [3, 10], "trikona_lord_houses": [5, 8]}]`
- **Yogakaraka** — single graha owning both a kendra (4/7/10) and a trikona (5/9). Basis: `{"Mars": [4, 9]}`
- **Neecha-Bhanga (NB-1)** — for a debilitated graha: lord of its debilitation sign or lord of its exaltation sign in a kendra from Lagna or Moon. Basis: `[{"debilitated": "Venus", "via": "Mercury", "role": "debilitation-sign lord", "house_from_lagna": 12, "house_from_moon": 4}]`
- Not present: Gajakesari, Budha-Aditya, Pancha-Mahapurusha (Ruchaka), Pancha-Mahapurusha (Bhadra), Pancha-Mahapurusha (Hamsa), Pancha-Mahapurusha (Malavya), Pancha-Mahapurusha (Sasa), Parivartana

Vimshottari: Moon in Bharani (lord Venus), balance 11.583 y. Year = 365.25 d.

| Mahadasha | Start | End |
|---|---|---|
| Venus | 1997-03-25 | 2017-03-25 |
| Sun | 2017-03-25 | 2023-03-26 |
| Moon | 2023-03-26 | 2033-03-25 |
| Mars | 2033-03-25 | 2040-03-25 |
| Rahu | 2040-03-25 | 2058-03-26 |
| Jupiter | 2058-03-26 | 2074-03-26 |

Current: **Moon/Jupiter** 2026-02-23 → 2027-06-25. Pratyantardashas:

- Jupiter: 2026-02-23 → 2026-04-29
- Saturn: 2026-04-29 → 2026-07-15
- Mercury: 2026-07-15 → 2026-09-22
- Ketu: 2026-09-22 → 2026-10-21
- Venus: 2026-10-21 → 2027-01-10
- Sun: 2027-01-10 → 2027-02-03
- Moon: 2027-02-03 → 2027-03-16
- Mars: 2027-03-16 → 2027-04-13
- Rahu: 2027-04-13 → 2027-06-25

## Western / Hellenistic — tropical, whole-sign, 7 planets

Ascendant **Virgo 7.35°**, MC Gemini 5.22° (whole-sign H10). **Day chart**; sect benefic Jupiter, contrary malefic Mars.

| Planet | Sign | Deg | House | Essential dignity | Bound | Face | Speed |
|---|---|---|---|---|---|---|---|
| Sun | Virgo | 1.94 | 1 | face | Mercury | Sun | 0.964 |
| Moon | Taurus | 12.88 | 9 | exaltation, triplicity_any, face | Mercury | Moon | 13.215 |
| Mercury | Leo | 13.60 | 12 | peregrine | Saturn | Jupiter | 1.075 |
| Venus | Libra | 9.36 | 2 | domicile | Mercury | Moon | 1.179 |
| Mars | Taurus | 14.32 | 9 | detriment, triplicity_any | Jupiter | Moon | 0.429 |
| Jupiter | Libra | 17.22 | 2 | triplicity_any, bound | Jupiter | Saturn | 0.180 |
| Saturn | Leo | 5.01 | 12 | detriment, triplicity_any, face | Jupiter | Saturn | 0.120 |

Lots: Fortune Taurus (H9), Spirit Sagittarius (H4). Dispositor terminals: [['Mercury', 'Sun'], ['Venus']] (Venus final dispositor; Sun–Mercury mutual reception loop).

Close aspects (≤3°): Moon–Mercury square 0.72° applying; Moon–Mars conjunction 1.44° applying; Mercury–Mars square 0.72° applying

Current profection: age 21 → H10 Gemini, year ruler Mercury (natal H12).

- Solar return 2025: 2025-08-24T20:46:02+00:00 UTC — Udhampur Asc Cancer 14.5°; Langley Asc Scorpio 22.2° (location changes Asc: True)
- Solar return 2026: 2026-08-25T02:32:42+00:00 UTC — Udhampur Asc Virgo 27.2°; Langley Asc Aquarius 17.8° (location changes Asc: True)

## BaZi

Pillars (civil = solar-time track): **乙酉 甲申 辛巳 辛卯**; Day Master 辛 (metal).

| Pillar | Stem | Ten God | Branch | Hidden stems | Hidden Ten Gods | Na Yin (traditional) |
|---|---|---|---|---|---|---|
| year | 乙 (wood, yin) | 偏财 | 酉 | 辛 | 比肩 | 泉中水 |
| month | 甲 (wood, yang) | 正财 | 申 | 庚壬戊 | 劫财, 伤官, 正印 | 泉中水 |
| day | 辛 (metal, yin) | Day Master | 巳 | 丙庚戊 | 正官, 劫财, 正印 | 白蜡金 |
| hour | 辛 (metal, yin) | 比肩 | 卯 | 乙 | 偏财 | 松柏木 |

Interactions: stem clash 天干冲 乙辛 ['year', 'day']; stem clash 天干冲 乙辛 ['year', 'hour']; clash 六冲 酉卯 ['year', 'hour']; six-combination 六合 申巳 ['month', 'day']; destruction 六破 申巳 ['month', 'day']; half three-harmony 半合 (includes central branch) 巳酉; directional 三会 (partial, not formed) 申酉; punishment 三刑 (partial) 巳申. No transformation asserted.

Day Master strength (DMS-1): **strong**; support share 0.52; season 旺 prosperous; roots in ['year', 'month', 'day'].
Useful element: Fu-Yi favors ['fire', 'water', 'wood']; Tiao-Hou (Qiong Tong Bao Jian (穷通宝鉴), 辛金 七月: 壬水为尊，甲戊酌用) favors ['water (壬)']. Schools agree only on **water**; confidence medium.

Da Yun backward, start 2011-07-10 (offset 5.87 y; lunar_python cross-checks 2011-07-05 / 2011-07-10).

| Da Yun | Start | End | Stem god | Branch god |
|---|---|---|---|---|
| 癸未 | 2011-07-10 | 2021-07-10 | 食神 | 偏印 |
| 壬午 | 2021-07-10 | 2031-07-10 | 伤官 | 七杀 |
| 辛巳 | 2031-07-10 | 2041-07-10 | 比肩 | 正官 |
| 庚辰 | 2041-07-10 | 2051-07-10 | 劫财 | 正印 |
| 己卯 | 2051-07-10 | 2061-07-10 | 偏印 | 偏财 |
| 戊寅 | 2061-07-10 | 2071-07-10 | 正印 | 正财 |

## Zi Wei Dou Shu (iztro 2.6.1)

Lunar 2005-7-21 (leap False), hour 卯时; Ming 巳, Shen 亥; life ruler 武曲, body ruler 天同; bureau 金四局.

| Branch | Palace | Major stars (brightness, 化) | Minor stars | Decadal (nominal age) | Decadal dates |
|---|---|---|---|---|---|
| 戊寅 | 子女 | 贪狼(平) | 地劫, 陀罗 | 34–43 | 2038-02-04 → 2048-02-14 |
| 己卯 | 夫妻 | 天机(旺·化禄), 巨门(庙) | 禄存 | 24–33 | 2028-01-26 → 2038-02-04 |
| 庚辰 | 兄弟 | 紫微(得·化科), 天相(得) | 右弼, 擎羊 | 14–23 | 2018-02-16 → 2028-01-26 |
| 辛巳 | 命宫 | 天梁(陷·化权) | — | 4–13 | 2008-02-07 → 2018-02-16 |
| 壬午 | 父母 | 七杀(旺) | 火星 | 114–123 | 2118-01-22 → 2128-02-01 |
| 癸未 | 福德 | (empty) | 文昌, 文曲 | 104–113 | 2108-02-12 → 2118-01-22 |
| 甲申 | 田宅 | 廉贞(庙) | 天钺, 地空 | 94–103 | 2098-02-01 → 2108-02-12 |
| 乙酉 | 官禄 | (empty) | — | 84–93 | 2088-01-24 → 2098-02-01 |
| 丙戌 | 仆役 | 破军(旺) | 左辅 | 74–83 | 2078-02-12 → 2088-01-24 |
| 丁亥 | 迁移 (身) | 天同(庙) | 天马 | 64–73 | 2068-02-03 → 2078-02-12 |
| 戊子 | 疾厄 | 武曲(旺), 天府(庙) | 天魁 | 54–63 | 2058-01-24 → 2068-02-03 |
| 己丑 | 财帛 | 太阳(不), 太阴(庙·化忌) | 铃星 | 44–53 | 2048-02-14 → 2058-01-24 |

## Maya calendar (GMT 584283)

Long Count **12.19.12.10.5**, Calendar Round **7 Chikchan 3 Mol**; round-trip OK: True. Day-sign meaning: omitted: no named Maya source bundled in dataset.

## Tibetan elemental (limited)

**Female Wood Bird** year, rabjung 17 year 19. Omitted: Mewa, Parkha, la/sok/wangthang/lungta/life-force, annual obstacles — no validated lineage-specific implementation available.

## Excluded methods

- **jyotisha**: {"shadbala": "no validated implementation available in this environment", "ashtakavarga": "not computed: no validated implementation; transit support not requested", "D7_D12": "not computed: domain-specific charts not requested"}
- **western**: {"zodiacal_releasing": "not computed: no validated implementation in this environment", "transits": "not computed: specific transit windows not requested", "modern_outer_planets_placidus": "optional modern track not requested; excluded from Hellenistic votes"}
- **maya**: {"day_sign_meaning": "omitted: no named Maya source bundled in dataset"}
- **tibetan**: {"omitted": ["Mewa", "Parkha", "la/sok/wangthang/lungta/life-force", "annual obstacles"], "reason": "no validated lineage-specific implementation available"}
- **ziwei**: {"py-iztro": "not used: same underlying iztro method, would add no independence"}
- **jaimini_kp_alt_ayanamsha**: "separate tracks not requested; not computed"
