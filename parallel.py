import time
from concurrent.futures import ProcessPoolExecutor, as_completed

import utils


def parallel_test(hosts: list, count: int) -> tuple:
    results = []
    print("parallel version")
    start = time.time()
    max_workers = min(10, len(hosts))
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(utils.test_host, host, count) for host in hosts}
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
    end = time.time()

    report_text = utils.format_statistics(results)
    total_time = end - start

    return report_text, total_time
