# hm3301

A Python driver for the **Seeed HM3301** laser PM2.5 dust sensor, communicating over **I2C**.

[![CI](https://github.com/ParthSanepara/hm3301/actions/workflows/ci.yml/badge.svg)](https://github.com/ParthSanepara/hm3301/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/hm3301)](https://pypi.org/project/hm3301/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/hm3301)](https://pypi.org/project/hm3301/)
[![Python](https://img.shields.io/pypi/pyversions/hm3301)](https://pypi.org/project/hm3301/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[![codecov](https://codecov.io/gh/ParthSanepara/hm3301/graph/badge.svg?token=mSUgdBM93N)](https://codecov.io/gh/ParthSanepara/hm3301)


## Features

- Read PM1.0, PM2.5, and PM10 concentrations (standard & atmospheric)
- Read particle counts per 0.1 L in six size bins (0.3 / 0.5 / 1.0 / 2.5 / 5.0 / 10 um)
- Average multiple readings for stability
- AQI category helper (US EPA breakpoints)
- JSON-serialisable data model
- Command-line tool (`hm3301-read`)
- Typed (PEP 561) and tested

## Installation

Requires **Python 3.12+**.

```bash
pip install hm3301
```

### Prerequisites (Raspberry Pi)

```bash
sudo apt install python3-smbus i2c-tools
sudo raspi-config   # Interface Options -> I2C -> Enable
```

## Wiring (Raspberry Pi)

| HM3301 pin | RPi pin               |
| ---------- | --------------------- |
| VCC        | 3.3 V (pin 1)        |
| GND        | GND (pin 6)           |
| SDA        | GPIO 2 / SDA (pin 3)  |
| SCL        | GPIO 3 / SCL (pin 5)  |

## Quick Start

### Python API

```python
from hm3301 import HM3301

with HM3301(i2c_bus=1) as sensor:
    reading = sensor.read()
    print(reading)
    # AirQualityReading(PM1.0=5ug/m3, PM2.5=8ug/m3, PM10=9ug/m3, AQI='Good')

    print(f"PM2.5 = {reading.pm2_5_atm} ug/m3 [{reading.aqi_category}]")
```

### Averaged Readings

```python
with HM3301(i2c_bus=1) as sensor:
    reading = sensor.read_average(samples=10, delay=1.0)
    print(reading.to_dict())
```

### Command-Line Tool

```bash
# Single reading
hm3301-read

# Average 5 readings, output as JSON
hm3301-read --samples 5 --json

# Use a different I2C bus or address
hm3301-read --bus 0 --address 0x40

# All options
hm3301-read --help
```

## API Reference

### `HM3301(i2c_bus=1, i2c_address=0x40)`

| Method                             | Description                  |
| ---------------------------------- | ---------------------------- |
| `read()`                           | Return one `AirQualityReading` |
| `read_average(samples=5, delay=0.5)` | Return averaged reading     |
| `close()`                          | Release the I2C bus          |

Supports context manager (`with` statement).

### `AirQualityReading`

| Attribute                            | Type       | Description                     |
| ------------------------------------ | ---------- | ------------------------------- |
| `pm1_0_std` / `pm1_0_atm`           | `int`      | PM1.0 ug/m3                     |
| `pm2_5_std` / `pm2_5_atm`           | `int`      | PM2.5 ug/m3                     |
| `pm10_std` / `pm10_atm`             | `int`      | PM10 ug/m3                      |
| `count_0_3um` ... `count_10um`       | `int`      | Particle counts per 0.1 L       |
| `aqi_category`                       | `str`      | US EPA AQI category             |
| `timestamp`                          | `datetime` | Time of reading                 |

| Method       | Returns | Description                |
| ------------ | ------- | -------------------------- |
| `to_dict()`  | `dict`  | JSON-serialisable dict     |

### Exceptions

| Exception                | Description                              |
| ------------------------ | ---------------------------------------- |
| `HM3301Error`            | Base exception                           |
| `HM3301ConnectionError`  | I2C bus or sensor unreachable            |
| `HM3301ReadError`        | Read failed or unexpected frame length   |
| `HM3301ChecksumError`    | Frame checksum mismatch                  |

```python
from hm3301 import HM3301, HM3301ConnectionError

try:
    sensor = HM3301(i2c_bus=1)
except HM3301ConnectionError as e:
    print(f"Sensor not found: {e}")
```

---

## Development

### Setup

```bash
git clone https://github.com/ParthSanepara/hm3301.git
cd hm3301
pip install -e ".[dev]"
```

### Project Structure

```
src/
  hm3301/
    __init__.py       # Public API exports
    driver.py         # HM3301 I2C driver
    models.py         # AirQualityReading data model
    exceptions.py     # Custom exceptions
    cli.py            # CLI entry point
tests/
    test_driver.py    # Driver tests (mocked I2C)
    test_models.py    # Model + AQI tests
```

### Running Tests

```bash
# All tests with coverage
pytest

# Single test
pytest tests/test_models.py::test_aqi_good

# Verbose output
pytest -v
```

### Linting & Type Checking

```bash
# Lint
ruff check .

# Lint with auto-fix
ruff check --fix .

# Type check (strict)
mypy .
```


## License

[MIT](LICENSE)
