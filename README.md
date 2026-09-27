# Six-culture verified chart

A birth chart computed and cross-checked in Jyotisha, BaZi, Western/Hellenistic, Zi Wei Dou Shu, Maya-calendar and Tibetan elemental traditions, with independent verification, time-uncertainty testing and a synthesis that counts each tradition's vote once.

Start with **`FINAL_READING.md`**. This is computed symbolic corroboration, not a validated forecast.

| File | Contents |
|---|---|
| `BIRTH_INPUT.json` | Verbatim and normalized birth data |
| `INPUT_AUDIT.md` | Civil-time audit, boundary distances, ±1 min ensemble |
| `CALCULATION_MANIFEST.json` | Runtime, package versions, ephemeris checksums, conventions, source hashes |
| `MASTER_DATASET.json` / `.md` | All computed facts (no interpretation) |
| `VERIFICATION_REPORT.json` / `.md` | Engine-vs-validator comparisons and invariants |
| `SYNTHESIS.json` | Mapping registry, projections, domain grades, temperament, chronology |
| `FINAL_READING.md` | The reading |

## Reproduce

```bash
uv venv -p python3.12 .venv
uv pip install -p .venv/bin/python pyswisseph==2.10.3.2 skyfield==1.55 skyfield-data tzdata==2026.4 \
    timezonefinder==9.0.0 lunar_python==1.4.8 convertdate==2.5.1 jplephem numpy
(cd ziwei && npm ci)
mkdir -p ephe && for f in sepl_18.se1 semo_18.se1; do
  curl -sSfL -o ephe/$f https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/$f; done
sha256sum ephe/*.se1   # compare with CALCULATION_MANIFEST.json
chart/run_all.sh
```

The chronology is computed relative to the run date, so a later run moves the "current" window forward.
