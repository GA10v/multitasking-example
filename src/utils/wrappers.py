import functools
import threading
import time
import typing

import psutil

PROCNAME = "python"
B_TO_MB = 1 / (1024 * 1024)


def timer_func(func: typing.Callable) -> typing.Callable:
    @functools.wraps(func)
    def wrap_func(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print(f"Function {func.__name__!r} executed in {(t2 - t1):.4f}s")
        return result

    return wrap_func


class RamMeasurementThread(threading.Thread):
    def __init__(self) -> None:
        super().__init__()
        self.init_value = self._measure()
        self.max_value = self.init_value
        self._finish_event = False

    def run(self) -> None:
        while not self._finish_event:
            self.max_value = max(self._measure(), self.max_value)

    def _measure(self) -> int:
        result = 0
        for proc in psutil.process_iter():
            try:
                if proc.name() == PROCNAME:
                    result += proc.memory_info().rss
            except psutil.NoSuchProcess:
                ...
        return result

    def join(self, timeout: typing.Optional[float] = None) -> None:
        self._finish_event = True
        return super().join(timeout)


def measure_max_memory(func: typing.Callable) -> typing.Callable:
    @functools.wraps(func)
    def wrap_func(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        ram = RamMeasurementThread()
        ram.start()
        result = func(*args, **kwargs)
        ram.join()
        print(f"Function {func.__name__!r} used up to {(ram.max_value-ram.init_value)*B_TO_MB}mb")
        return result

    return wrap_func


__all__ = ["timer_func"]
