import copy
import csv
import json

import pyarrow.parquet as pq
import pytest
import to_parquet as converter


@pytest.fixture
def sample(tmp_path):
    data = tmp_path / "data"
    data.mkdir()
    contract = copy.deepcopy(converter.CONTRACT)
    contract["sources"] = []
    for kind, spec in contract["contracts"].items():
        name = f"क़स्बा-{spec['post']}.csv"
        district = None if kind.endswith("heads") and kind != "gp_heads" else "क़स्बा"
        contract["sources"].append(
            {"file": name, "kind": kind, "district_from_filename": district}
        )
        values = dict.fromkeys(spec["columns"], "source text")
        values.update(
            उम्मीदवार="Test winner",
            परिणाम="सविरोध",
        )
        values["पद का आरक्षण"] = "महिला"
        values["प्रत्याशी का आरक्षण"] = "अनारक्षित"
        values["मोबाइल नं०"] = "0012345"
        values["प्राप्त मत %"] = "55.20"
        values["मतदान %"] = "70.00"
        with (data / name).open("w", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(spec["columns"])
            writer.writerow(values.values())
            writer.writerow(values.values())
            values["परिणाम"] = "निर्विरोध"
            values["उम्मीदवार"] = ""
            writer.writerow(values.values())
    return data, tmp_path / "out", contract


@pytest.mark.parametrize("kind", converter.CONTRACT["contracts"])
def test_office_roundtrip_preserves_source_meanings(sample, kind):
    data, out, contract = sample
    converter.export(data, out, contract=contract)
    converter.export(data, out, check=True, contract=contract)
    spec = contract["contracts"][kind]
    table = pq.read_table(out / spec["output"])
    rows = table.to_pylist()
    assert table.schema.equals(converter.schema(spec), check_metadata=True)
    assert len(rows) == 3
    assert [row["source_row"] for row in rows] == [1, 2, 3]
    assert [row["unopposed"] for row in rows] == [False, False, True]
    assert rows[0]["seat_reservation_raw"] == "महिला"
    assert rows[0]["candidate_reservation_raw"] == "अनारक्षित"
    assert rows[0]["mobile_raw"] == "0012345"
    assert rows[0]["vote_percent_raw"] == "55.20"
    assert rows[0]["turnout_percent_raw"] == "70.00"
    assert rows[2]["winner_name_raw"] is None
    assert rows[2]["winner_missing"] is True
    assert rows[0]["source_file"].startswith("क़स्बा-")
    assert rows[0]["year"] == 2015
    assert rows[0]["post"] == spec["post"]
    if kind in {"block_heads", "district_heads"}:
        assert rows[0]["district_from_filename"] is None
        key = "district_raw" if kind == "block_heads" else "district_body_raw"
        assert rows[0][key] == "source text"
    else:
        assert rows[0]["district_from_filename"] == "क़स्बा"


@pytest.mark.parametrize("problem", ["header", "ragged", "status", "empty"])
def test_invalid_source_preserves_existing_export(sample, problem):
    data, out, contract = sample
    converter.export(data, out, contract=contract)
    before = {p.name: p.read_bytes() for p in out.iterdir()}
    path = data / contract["sources"][0]["file"]
    with path.open(newline="") as stream:
        rows = list(csv.reader(stream))
    if problem == "header":
        rows[0][0] = "Unexpected"
    elif problem == "ragged":
        rows[-1].pop()
    elif problem == "status":
        rows[-1][-1] = "won"
    else:
        rows = rows[:1]
    with path.open("w", newline="") as stream:
        csv.writer(stream).writerows(rows)
    with pytest.raises(ValueError):
        converter.export(data, out, contract=contract)
    assert {p.name: p.read_bytes() for p in out.iterdir()} == before


def test_unlisted_source_is_not_silently_ignored(sample):
    data, out, contract = sample
    (data / "extra.csv").write_text("data")
    with pytest.raises(ValueError, match="source manifest"):
        converter.export(data, out, contract=contract)


def test_verification_detects_changed_values(sample):
    data, out, contract = sample
    converter.export(data, out, contract=contract)
    path = data / contract["sources"][0]["file"]
    path.write_text(path.read_text().replace("Test winner", "Changed winner"))
    with pytest.raises(ValueError, match="rows differ"):
        converter.export(data, out, check=True, contract=contract)


def test_verification_detects_changed_manifest(sample):
    data, out, contract = sample
    converter.export(data, out, contract=contract)
    path = out / "MANIFEST.json"
    manifest = json.loads(path.read_text())
    manifest["files"][0]["rows"] = 100
    path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="manifest differs"):
        converter.export(data, out, check=True, contract=contract)
