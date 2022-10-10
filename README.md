# benchmark

In this repository, we intend to provide codes and tools for analyzing the performance of `mosec` as well as benchmarking `mosec` with other model serving alternatives.

**Table of Contents**

- [benchmark](#benchmark)
  - [Preparation](#preparation)
  - [Exploring how `mosec` optimize serving performance](#exploring-how-mosec-optimize-serving-performance)
    - [Free lunch from `rust`](#free-lunch-from-rust)
    - [Batching](#batching)
    - [Pipelining](#pipelining)
    - [Serialization](#serialization)
  - [Comparison results](#comparison-results)

## Preparation

Though this repository serves more as a report to demonstrate `mosec`'s performance advantage, interested readers could also run the experiments on their preferred machines to validate the results. More importantly, if you'd like to contribute the results on your distinct hardware, you are more than welcome to do so! Please join our [discord server](https://discord.gg/eCBFDrUS) to share with us your exciting results and let's put them here together!

We first install the `benchmark` library locally with the latest `mosec`.

```console
pip install --upgrade --upgrade-strategy eager -e .
```

## Exploring how `mosec` optimize serving performance

### Free lunch from `rust`
### Batching

### Pipelining

### Serialization

## Comparison results
