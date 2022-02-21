import csv
import datetime
import statistics


def detect_failuer(input, n, m, t):
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
                "response_time_log": [int(response_time)]
                if response_time != "-"
                else [],
                "is_overload": False,
                "start_overload_date": date,
                "last_overload_date": date,
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

        # 過去m回の平均応答時間の計算
        if response_time != "-":
            last_status[ip_address]["response_time_log"].append(int(response_time))
        response_mean = statistics.mean(
            last_status[ip_address]["response_time_log"][-m:]
        )

        # 平均応答時間がtより長い場合、last_statusを過負荷にする。
        if response_mean > t:
            if not last_status[ip_address]["is_overload"]:
                last_status[ip_address]["start_overload_date"] = date
                last_status[ip_address]["is_overload"] = True
            last_status[ip_address]["last_overload_date"] = date
            continue

        # 　過負荷から復帰した場合、過負荷状態として標準出力する。
        if last_status[ip_address]["is_overload"]:
            print(
                f"[SERVER_OVERLOAD] {ip_address}: "
                f"{last_status[ip_address]['start_overload_date']} - {date}"
            )
            last_status[ip_address]["is_overload"] = False

    # ログがタイムアウトまたは過負荷で終わるデータへの対応
    for k, v in last_status.items():
        if v["is_timeout"]:
            print(
                f"[SERVER_DOWN] {k}: "
                f"{v['start_timeout_date']} - {v['last_timeout_date']}"
            )
        if v["is_overload"]:
            print(
                f"[SERVER_OVERLOAD] {k}: "
                f"{v['start_overload_date']} - {v['last_overload_date']}"
            )
