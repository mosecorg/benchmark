from __future__ import annotations
from functools import partial

import gc
import subprocess
import traceback
from dataclasses import dataclass
from time import perf_counter
from typing import Any
from mosec import Worker
import numpy as np

from pyarrow import plasma

from mosec.mixin import PlasmaShmIPCMixin,RedisShmIPCMixin


unix_path = "/tmp/redis/redis.sock"
tcp_path = "127.0.0.1:6379"

@dataclass(frozen=True)
class Data:
    arr: np.ndarray | dict
    msg: str
    epoch: int

class PlasmaForwardWorker(PlasmaShmIPCMixin):
    def forward(self, data: Data) -> Any:
        return data
    
class RedisForwardWorker(RedisShmIPCMixin):
    def forward(self, data: Data) -> Any:
        return data

def generate_data():
    return (
        Data(
            {"msg": "long message" * 1000, "vec": np.random.rand(1024)},
            "long message with 1024 vector",
            10000,
        ),
        Data(
            {
                "int": 233,
                "float": 3.14,
                "vec": np.random.rand(1024),
                "matrix": np.random.rand(64, 1024),
            },
            "int, float, vector and matrix",
            100,
        ),
    )


def generate_np_data():
    return (
        Data(np.random.rand(1), "scalar", 10000),
        Data(np.random.rand(1024), "vector", 10000),
        Data(np.random.rand(64, 1024), "matrix", 1000),
        Data(np.random.rand(3, 1024, 1024), "image", 100),
    )

def test_shm_worker(worker:Worker,data: Data):
    _id=worker.serialize_ipc(data.arr)
    worker.deserialize_ipc(_id)

def time_record(func, data: Data, threshold=1):
    res = []
    total_sec = 0
    while total_sec < threshold:
        for _ in range(data.epoch):
            t0 = perf_counter()
            try:
                func(data)
            except:
                print(traceback.format_exc())
            finally:
                res.append(perf_counter() - t0)
                total_sec += res[-1]
    return res


def display_result(func, data):
    gc_flag = gc.isenabled()
    gc.disable()
    try:
        t = time_record(func, data)
    finally:
        if gc_flag:
            gc.enable()
    size = data.arr.size if isinstance(data.arr, np.ndarray) else "<unknown>"
    print(
        f"{func.__name__}\tsize: {size:9}\ttimes: "
        f"min({np.min(t):.5})\tmid({np.median(t):.5})\tmax({np.max(t):.5})\t"
        f"95%({np.percentile(t, 0.95):.5})\tStd.({np.std(t):.5})",
    )

def init_redis_shm_worker(url):
    RedisShmIPCMixin.set_redis_url(url)
    worker=RedisForwardWorker()
    worker._get_client()
    return worker

def benchmark():

    with plasma.start_plasma_store(plasma_store_memory=10 * 1000 * 1000 * 1000) as ( 
        shm_path,
        plasma_proc,
    ), subprocess.Popen(["redis-server","--unixsocket",unix_path]) as redis_proc:
        global plasma_worker,redis_unix_worker,redis_tcp_worker
        PlasmaForwardWorker.set_plasma_path(shm_path)
        plasma_worker=PlasmaForwardWorker()
        redis_unix_worker=init_redis_shm_worker(f"unix://{unix_path}")
        redis_tcp_worker=init_redis_shm_worker(f"redis://@{tcp_path}")
        
        name_worker={
            "plasma\t":plasma_worker,
            "redis_unix":redis_unix_worker,
            "redis_tcp":redis_tcp_worker
        }
        funcs=[]
        for name,worker in name_worker.items():
            f=partial(test_shm_worker,worker)
            setattr(f,"__name__",name)
            funcs.append(f)

        print(">>> benchmark for numpy array")
        
        for data in generate_np_data():
            for func in funcs:
                display_result(func, data)

        print(">>> benchmark for normal data mixed with numpy array")
        for data in generate_data():
            print("=" * 120)
            for func in funcs:
                display_result(func, data)
        plasma_proc.kill()
        redis_proc.kill()

if __name__ == "__main__":
    benchmark()
