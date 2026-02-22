import time

import utils


def linear_test(hosts: list, count: int) -> tuple:
    results = []
    print("linear version")
    start = time.time()
    for host in hosts:
        statistics = utils.test_host(host, count)
        results.append(statistics)
    end = time.time()

    report_text = utils.format_statistics(results)
    total_time = end - start

    return report_text, total_time
