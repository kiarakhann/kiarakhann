// Zi Wei Dou Shu extractor: reads a JSON request on argv[2], prints facts as JSON.
// Request: {"solar_date":"YYYY-M-D","time_index":n,"gender":"男"|"女","fix_leap":true}
const { astro } = require('iztro');
const pkg = require('iztro/package.json');

const req = JSON.parse(process.argv[2]);
const a = astro.bySolar(req.solar_date, req.time_index, req.gender, req.fix_leap, 'zh-CN');
const o = JSON.parse(JSON.stringify(a));

const palaces = o.palaces.map((p) => ({
  index: p.index,
  name: p.name,
  heavenly_stem: p.heavenlyStem,
  earthly_branch: p.earthlyBranch,
  is_body_palace: p.isBodyPalace,
  major_stars: p.majorStars.map((s) => ({ name: s.name, brightness: s.brightness || null, mutagen: s.mutagen || null })),
  minor_stars: p.minorStars.map((s) => ({ name: s.name, type: s.type, brightness: s.brightness || null, mutagen: s.mutagen || null })),
  decadal_nominal_age_range: p.decadal.range,
  decadal_stem_branch: p.decadal.heavenlyStem + p.decadal.earthlyBranch,
}));

// Yearly (流年) palace activation for a set of Gregorian dates.
const yearly = (req.yearly_dates || []).map((d) => {
  const h = a.horoscope(new Date(d + 'T12:00:00'));
  return {
    date: d,
    nominal_age: h.age.nominalAge,
    decadal_palace_branch: h.decadal.earthlyBranch,
    yearly_stem_branch: h.yearly.heavenlyStem + h.yearly.earthlyBranch,
    yearly_life_palace_index: h.yearly.index,
    yearly_mutagen: h.yearly.mutagen,
  };
});

console.log(JSON.stringify({
  implementation: { name: 'iztro', version: pkg.version, runtime: 'node ' + process.version },
  request: req,
  lunar: o.rawDates.lunarDate,
  chinese_date: o.chineseDate,
  time_branch: o.time,
  time_range: o.timeRange,
  soul_palace_branch: o.earthlyBranchOfSoulPalace,
  body_palace_branch: o.earthlyBranchOfBodyPalace,
  life_ruler: o.soul,
  body_ruler: o.body,
  five_elements_bureau: o.fiveElementsClass,
  palaces,
  yearly,
}));
