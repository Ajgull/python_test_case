import time
from concurrent.futures import ProcessPoolExecutor, as_completed

import requests

import utils


def parallel_test_host(host: str, count: int) -> dict:
    success_count = 0
    fail_count = 0
    error_count = 0
    time_of_requests = []

    for i in range(count):
        try:
            start_time = time.time()
            response = requests.get(host, timeout=10)
            end_time = time.time()
            if 200 <= response.status_code < 400:
                success_count += 1
            else:
                fail_count += 1

            time_of_requests.append(round((end_time - start_time) * 1000, 3))

        except requests.exceptions.RequestException as e:
            print(f"Connection to host {host} {str(e)}")
            error_count += 1

    if time_of_requests:
        min_time = round(min(time_of_requests), 3)
        max_time = round(max(time_of_requests), 3)
        avg_time = round(sum(time_of_requests) / len(time_of_requests), 3)
    else:
        min_time = max_time = avg_time = 0

    return {
        "Host": host,
        "Success": success_count,
        "Failed": fail_count,
        "Errors": error_count,
        "Min": min_time,
        "Max": max_time,
        "Avg": avg_time,
    }


def parallel_test(hosts: list, count: int) -> tuple:
    results = []
    print("parallel version")
    start = time.time()
    max_workers = min(10, len(hosts))
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(parallel_test_host, host, count) for host in hosts}
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
    end = time.time()

    report_text = utils.format_statistics(results)
    total_time = end - start

    return report_text, total_time
