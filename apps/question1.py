import csv
import datetime


def detect_failuer(input):
    with open(input, "r") as f:
        reader = csv.reader(f)
        logs = [
            [datetime.datetime.strptime(row[0], "%Y%m%d%H%M%S"), row[1], row[2]]
            for row in reader
        ]

    last_status = dict()
    for date, ip_address, response_time in logs:
        # 新規ip_addressが記録された時のlast_statusの初期化
        if ip_address not in last_status.keys():
            last_status[ip_address] = {
                "is_timeout": response_time == "-",
                "start_timeout_date": date,
                "last_timeout_date": date,
            }
            continue

        # 応答時間が"-"の場合、last_statusをタイムアウトにする。
        if response_time == "-":
            if not last_status[ip_address]["is_timeout"]:
                last_status[ip_address]["start_timeout_date"] = date
                last_status[ip_address]["is_timeout"] = True
            last_status[ip_address]["last_timeout_date"] = date
            continue

        # タイムアウトから復帰した場合、故障として標準出力する。
        if last_status[ip_address]["is_timeout"]:
            print(
                f"[SERVER_DOWN] {ip_address}: "
                f"{last_status[ip_address]['start_timeout_date']} - {date}"
            )
            last_status[ip_address]["is_timeout"] = False

    # ログがタイムアウトで終わるデータへの対応
    for k, v in last_status.items():
        if v["is_timeout"]:
            print(
                f"[SERVER_DOWN] {k}: "
                f"{v['start_timeout_date']} - {v['last_timeout_date']}"
            )
