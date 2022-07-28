import asyncio
import concurrent.futures as concurrent_futures
import multiprocessing
import threading
import time

import src.utils.wrappers as wrapper_utils

SIZE = 500
POOL_SIZE = 20
SLEEP_TIME = 0.2


def test_func(value: int) -> int:
    time.sleep(SLEEP_TIME)
    return value + 1


@wrapper_utils.timer_func
@wrapper_utils.measure_max_memory
def time_multiprocessing() -> None:
    processes = [multiprocessing.Process(target=test_func, args=(i,)) for i in range(0, SIZE)]
    for process in processes:
        process.start()

    for process in processes:
        process.join()


@wrapper_utils.timer_func
@wrapper_utils.measure_max_memory
def time_multiprocessing_pool() -> None:
    with multiprocessing.Pool(POOL_SIZE) as pool:
        pool.map(test_func, range(0, SIZE))


@wrapper_utils.timer_func
@wrapper_utils.measure_max_memory
def time_multithreading() -> None:
    processes = [threading.Thread(target=test_func, args=(i,)) for i in range(0, SIZE)]
    for process in processes:
        process.start()

    for process in processes:
        process.join()


@wrapper_utils.timer_func
@wrapper_utils.measure_max_memory
def time_multithreading_pool() -> None:
    with concurrent_futures.ThreadPoolExecutor(max_workers=POOL_SIZE) as executor:
        executor.map(test_func, range(0, SIZE))


async def async_test_func(value: int) -> int:
    time.sleep(SLEEP_TIME)
    return value + 1


async def async_test() -> None:
    tasks = [async_test_func(i) for i in range(0, SIZE)]
    await asyncio.gather(*tasks)


@wrapper_utils.timer_func
@wrapper_utils.measure_max_memory
def time_async() -> None:
    asyncio.run(async_test())


async def real_async_test_func(value: int) -> int:
    await asyncio.sleep(SLEEP_TIME)
    return value + 1


async def real_async_test() -> None:
    tasks = [real_async_test_func(i) for i in range(0, SIZE)]
    await asyncio.gather(*tasks)


@wrapper_utils.timer_func
@wrapper_utils.measure_max_memory
def time_real_async() -> None:
    asyncio.run(real_async_test())


if __name__ == "__main__":
    time_multiprocessing()
    time_multiprocessing_pool()
    time_multithreading()
    time_multithreading_pool()
    # time_async()
    time_real_async()
