from apps.question3 import detect_failuer


def test_question3(capfd):
    detect_failuer("test/data/ping_log.csv", 2, 2, 100)
    out, err = capfd.readouterr()
    expect = open("test/data/output3.txt").read()
    assert out == expect
    assert err == ""
