# Test data

Tests generate synthetic winner lists for all five office schemas in `schemas.json`.
The schemas come from the 226 CSVs saved in this repository at commit
`789462339f5661aa31dd4c05c56bce5f46b5bb94`, collected from
<http://sec.up.nic.in/ElecLive/WinnerList.aspx>. The original capture times are
not recorded. Tests use invented names and numbers, retain the source's two
contest-status labels, and exercise Unicode filenames, repeated rows, and
missing values. No live pages are fetched by tests.
