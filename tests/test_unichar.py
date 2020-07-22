import pytest
import json
from unilyze import Unichar

TEST_CHAR = "Ä"
u = Unichar()


def load_json(filename):
    with open(filename, "r", encoding="utf-8") as fp:
        data = fp.read()
    return data


def create_tests():
    u = Unichar()

    raw_info = u.ucd_info_raw(TEST_CHAR)
    with open("tests/testchar_raw.json", "w", encoding="utf-8") as fp:
        json.dump(raw_info, fp, sort_keys=True)

    info = u.ucd_info(TEST_CHAR)
    with open("tests/testchar.json", "w", encoding="utf-8") as fp:
        json.dump(info, fp, sort_keys=True)


def test_ucd_info_raw():
    info = u.ucd_info_raw(TEST_CHAR)
    info_json = json.dumps(info, sort_keys=True)
    info_json_loaded = load_json("tests/testchar_raw.json")
    assert info_json == info_json_loaded


def test_ucd_info():
    info = u.ucd_info(TEST_CHAR)
    info_json = json.dumps(info, sort_keys=True)
    info_json_loaded = load_json("tests/testchar.json")
    assert info_json == info_json_loaded


def test_ucd_info_raw_wrong_char():
    info = u.ucd_info_raw("M")
    info_json = json.dumps(info, sort_keys=True)
    info_json_loaded = load_json("tests/testchar_raw.json")
    assert info_json != info_json_loaded


def test_ucd_info_raw_illegal_parameter():
    with pytest.raises(ValueError):
        info = u.ucd_info_raw("ILLEGAL PARAMETER")


def test_lng_name_lookup():
    name = u.lng_name_lookup("zu")
    assert name == "Zulu"

    name = u.lng_name_lookup("da_DK")
    assert name == "Danish : Denmark"

    name = u.lng_name_lookup("NOT IN DB")
    assert name == ""


def test_lng_usage_raw():
    usage = u.lng_usage_raw("\u06d0")
    assert "ps_PK" in usage["main"]

    usage = u.lng_usage_raw("\uFFFF")
    assert usage is None


def test_lng_usage_():
    usage = u.lng_usage("\u0f10")
    assert "Dzongkha" in usage["punctuation"]
    assert len(usage) == 1
    assert len(usage["punctuation"]) == 1

