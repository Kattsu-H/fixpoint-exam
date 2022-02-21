from apps.question1 import detect_failuer


def test_question1(capfd):
    detect_failuer("test/data/ping_log.csv")
    out, err = capfd.readouterr()
    expect = open("test/data/output1.txt").read()
    assert out == expect
    assert err == ""
