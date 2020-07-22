from unilyze import Unistat

u = Unistat()


def test_charstat():
    stat = u.charstat()
    assert stat == {}

    u.add_text("test1!")
    stat = u.charstat()
    assert stat["t"] == 2

    u.reset_stat()
    stat = u.charstat()
    assert stat == {}


def test_unistat():
    u.reset_stat()

    u.add_text("TesT1!")
    stat = u.unistat()
    assert stat["Uppercase"][True]["total-count"] == 2
    assert "e" in stat["Script"]["Latin"]["chars"]

    u.add_text("Another little test to be added")
    stat = u.unistat()
    assert len(stat["Lowercase"][True]["chars"]) == 12  # 12 different lowercase characters
    assert stat["General_Category"]["Space_Separator"]["total-count"] == 5
