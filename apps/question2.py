import csv
import datetime


def detect_failuer(input, n):
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
                "timeout_count": 0 if response_time != "-" else 1,
            }
            continue

        # 応答時間が"-"の場合タイムアウト回数を加算し、タイムアウトがn回以上の時、last_statusをタイムアウトにする。
        if response_time == "-":
            last_status[ip_address]["timeout_count"] += 1
            if (
                not last_status[ip_address]["is_timeout"]
                and last_status[ip_address]["timeout_count"] >= n
            ):
                last_status[ip_address]["start_timeout_date"] = date
                last_status[ip_address]["is_timeout"] = True
            last_status[ip_address]["last_timeout_date"] = date
            continue

        # タイムアウトから復帰した場合、タイムアウトがn回以上の時、故障として標準出力する。
        if last_status[ip_address]["is_timeout"]:
            print(
                f"[SERVER_DOWN] {ip_address}: "
                f"{last_status[ip_address]['start_timeout_date']} - {date}"
            )
            last_status[ip_address]["is_timeout"] = False
            last_status[ip_address]["timeout_count"] = 0

    # ログがタイムアウトで終わるデータへの対応
    for k, v in last_status.items():
        if v["is_timeout"]:
            print(
                f"[SERVER_DOWN] {k}: "
                f"{v['start_timeout_date']} - {v['last_timeout_date']}"
            )
