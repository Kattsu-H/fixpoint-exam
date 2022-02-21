from apps.question4 import detect_failuer


def test_question4(capfd):
    detect_failuer("test/data/ping_log.csv", 2, 2, 100)
    out, err = capfd.readouterr()
    expect = open("test/data/output4.txt").read()
    assert out == expect
    assert err == ""
