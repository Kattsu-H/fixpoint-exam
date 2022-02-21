from apps.question2 import detect_failuer


def test_question2(capfd):
    detect_failuer("test/data/ping_log.csv", 2)
    out, err = capfd.readouterr()
    expect = open("test/data/output2.txt").read()
    assert out == expect
    assert err == ""
