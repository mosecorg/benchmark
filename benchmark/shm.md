# Benchmark of shared memory mixins

# Prerequisites
redis-server should be installed and running.
you can run redis-server with the following command:
```bash
sudo apt install redis-server
```

# Run

`python ./shm.py`

# Results


The benchmark on my machine(AMD Ryzen 9 5900X) is as follows:

plasma          size:         1 times: min(0.00024435)  mid(0.00027904) max(0.0016582)  95%(0.00025926) Std.(2.5355e-05)
redis_unix      size:         1 times: min(0.0001597)   mid(0.00018997) max(0.00060593) 95%(0.00016197) Std.(2.8627e-05)
redis_tcp       size:         1 times: min(0.00020048)  mid(0.00022785) max(0.0013715)  95%(0.00021585) Std.(3.0378e-05)
plasma          size:      1024 times: min(0.00024969)  mid(0.00028456) max(0.00059021) 95%(0.00027068) Std.(2.4854e-05)
redis_unix      size:      1024 times: min(0.00017412)  mid(0.00020382) max(0.00056432) 95%(0.00018177) Std.(2.6104e-05)
redis_tcp       size:      1024 times: min(0.00020199)  mid(0.00023232) max(0.00047119) 95%(0.00021916) Std.(2.5673e-05)
plasma          size:     65536 times: min(0.00065814)  mid(0.00070226) max(0.0019353)  95%(0.00066868) Std.(5.567e-05)
redis_unix      size:     65536 times: min(0.00089813)  mid(0.0009925)  max(0.0014891)  95%(0.00091763) Std.(6.3486e-05)
redis_tcp       size:     65536 times: min(0.0011009)   mid(0.0011716)  max(0.0016486)  95%(0.0011106)  Std.(7.29e-05)
plasma          size:   3145728 times: min(0.028673)    mid(0.029416)   max(0.037621)   95%(0.028706)   Std.(0.0021678)
redis_unix      size:   3145728 times: min(0.046763)    mid(0.04841)    max(0.055645)   95%(0.046845)   Std.(0.0020143)
redis_tcp       size:   3145728 times: min(0.040182)    mid(0.051077)   max(0.059047)   95%(0.040738)   Std.(0.0035537)
>>> benchmark for normal data mixed with numpy array
========================================================================================================================
plasma          size: <unknown> times: min(0.00025614)  mid(0.00029197) max(0.0025628)  95%(0.00027462) Std.(4.3949e-05)
redis_unix      size: <unknown> times: min(0.00018343)  mid(0.00021754) max(0.00064727) 95%(0.00019482) Std.(3.6763e-05)
redis_tcp       size: <unknown> times: min(0.00020191)  mid(0.00025083) max(0.00062813) 95%(0.0002194)  Std.(4.2144e-05)
========================================================================================================================
plasma          size: <unknown> times: min(0.0005683)   mid(0.0006267)  max(0.0010101)  95%(0.00057886) Std.(5.818e-05)
redis_unix      size: <unknown> times: min(0.00064607)  mid(0.00071034) max(0.0012368)  95%(0.00065222) Std.(7.1132e-05)
redis_tcp       size: <unknown> times: min(0.00060924)  mid(0.00071632) max(0.0011938)  95%(0.00061993) Std.(8.9151e-05)

The table above shows how the data size affects the performance rank of different methods. Redis_unix performs better than redis_tcp and plasma when the data size is small, but plasma outperforms redis when the data size is large.