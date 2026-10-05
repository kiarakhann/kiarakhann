"""Shared constants, tables and helpers. Facts only; no interpretation."""
import datetime as dt
import json
import os
from zoneinfo import ZoneInfo

import swisseph as swe

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Per-person input/output folder; defaults to the repository root.
DATA = os.path.abspath(os.environ.get("CHART_DIR", ROOT))
EPHE = os.path.join(ROOT, "ephe")
swe.set_ephe_path(EPHE)

SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
SIGN_RULER = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
              "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
PLANETS7 = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]
SWE_ID = {"Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY, "Venus": swe.VENUS,
          "Mars": swe.MARS, "Jupiter": swe.JUPITER, "Saturn": swe.SATURN,
          "MeanNode": swe.MEAN_NODE, "TrueNode": swe.TRUE_NODE}

STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"
STEM_ELEMENT = {"甲": "wood", "乙": "wood", "丙": "fire", "丁": "fire", "戊": "earth",
                "己": "earth", "庚": "metal", "辛": "metal", "壬": "water", "癸": "water"}
BRANCH_MAIN = {"子": "癸", "丑": "己", "寅": "甲", "卯": "乙", "辰": "戊", "巳": "丙",
               "午": "丁", "未": "己", "申": "庚", "酉": "辛", "戌": "戊", "亥": "壬"}


def load_input():
    with open(os.path.join(DATA, "BIRTH_INPUT.json")) as f:
        return json.load(f)


def norm(x):
    return x % 360.0


def sign_of(lon):
    return int(norm(lon) // 30)


def deg_in_sign(lon):
    return norm(lon) % 30.0


def angdiff(a, b):
    """Signed smallest difference a-b in (-180, 180]."""
    d = (a - b + 180.0) % 360.0 - 180.0
    return 180.0 if d == -180.0 else d


def local_instant(date_str, time_str, tz_name, offset_minutes=0.0):
    zone = ZoneInfo(tz_name)
    y, m, d = map(int, date_str.split("-"))
    hh, mm = map(int, time_str.split(":"))
    local = dt.datetime(y, m, d, hh, mm, tzinfo=zone) + dt.timedelta(minutes=offset_minutes)
    local = local.astimezone(zone)
    utc = local.astimezone(dt.timezone.utc)
    return local, utc


def jd_ut(utc):
    h = utc.hour + utc.minute / 60 + utc.second / 3600 + utc.microsecond / 3.6e9
    return swe.julday(utc.year, utc.month, utc.day, h, swe.GREG_CAL)


def jd_to_utc(jd):
    y, m, d, h = swe.revjul(jd, swe.GREG_CAL)
    base = dt.datetime(y, m, d, tzinfo=dt.timezone.utc)
    return base + dt.timedelta(hours=h)


def iso(t):
    return t.isoformat(timespec="seconds")


def dump(path, obj):
    with open(os.path.join(DATA, path), "w") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, default=str)
        f.write("\n")
