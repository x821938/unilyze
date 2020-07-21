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

    raw_info = u.raw_info(TEST_CHAR)
    with open("tests/testchar_raw.json", "w", encoding="utf-8") as fp:
        json.dump(raw_info, fp, sort_keys=True)

    info = u.info(TEST_CHAR)
    with open("tests/testchar.json", "w", encoding="utf-8") as fp:
        json.dump(info, fp, sort_keys=True)


def test_unichar_raw_info():
    info = u.raw_info(TEST_CHAR)
    info_json = json.dumps(info, sort_keys=True)
    info_json_loaded = load_json("tests/testchar_raw.json")
    assert info_json == info_json_loaded


def test_unichar_info():
    info = u.info(TEST_CHAR)
    info_json = json.dumps(info, sort_keys=True)
    info_json_loaded = load_json("tests/testchar.json")
    assert info_json == info_json_loaded


def test_unichar_raw_info_wrong_char():
    info = u.raw_info("M")
    info_json = json.dumps(info, sort_keys=True)
    info_json_loaded = load_json("tests/testchar_raw.json")
    assert info_json != info_json_loaded


def test_unichar_raw_info_illegal_parameter():
    with pytest.raises(ValueError):
        info = u.raw_info("ILLEGAL PARAMETER")
