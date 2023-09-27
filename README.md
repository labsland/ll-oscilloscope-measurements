# ll-oscilloscope-measurements

[![CircleCI](https://circleci.com/gh/labsland/ll-oscilloscope-measurements.svg?style=svg)](https://circleci.com/gh/labsland/ll-oscilloscope-measurements)
[![Supported Versions](https://img.shields.io/pypi/pyversions/ll-oscilloscope-measurements.svg)](https://pypi.org/project/ll-oscilloscope-measurements)
[![pypi](https://img.shields.io/pypi/v/ll-oscilloscope-measurements.svg)](https://pypi.org/project/ll-oscilloscope-measurements)

Library for calculating oscilloscope measurements based on graph data.

The goal is to provide transparency on how the LabsLand Hive ( https://labsland.com/web/hive )
takes measurements, but it can be used for other purposes.

## Installation
```
$ pip install ll-oscilloscope-measurements
```

## Usage

```python
import numpy as np
import ll_oscilloscope_measurements as llom

sin_signal = np.sin(np.linspace(0, 500))
# ~0
llom.calculate_voltage_average(sin_signal)
# ~1
llom.calculate_voltage_max(sin_signal)
# ~0.69
llom.calculate_voltage_rms(sin_signal)

# etc.
```

See [the code](ll_oscilloscope_measurements.py) for all the functions.

## Testing

In the [tests/data](tests/data) folder there are a set of CSV, JSON, and images of different sets of samples (500 samples each).

In the [tests/unit/test_ll_oscilloscope_measurements.py](tests/unit/test_ll_oscilloscope_measurements.py) file, you will find tests using those samples and evaluating the code with them.

Feel free to add tests and run the following to test them:

```
pytest tests
```
