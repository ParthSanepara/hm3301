# hm3301

A Python driver for the **Seeed HM3301** laser PM2.5 dust sensor, communicating over **I²C**.

## Features

- Read PM1.0, PM2.5, and PM10 concentrations (standard & atmospheric)
- Read particle counts per 0.1 L in six size bins
- Average multiple readings for stability
- AQI category helper property
- JSON-serialisable data model
- Command-line tool (`hm3301-read`)
- Typed, tested, and PyPI-ready

## Installation

```bash
pip install hm3301
```

> **Note:** Requires `smbus2`. On Raspberry Pi OS, you may also need:
> ```bash
> sudo apt install python3-smbus i2c-tools
> sudo raspi-config   # Interface Options → I2C → Enable
> ```

## Quick Start

```python
from hm3301 import HM3301

with HM3301(i2c_bus=1) as sensor:
    reading = sensor.read()
    print(reading)
    # AirQualityReading(PM1.0=5µg/m³, PM2.5=8µg/m³, PM10=9µg/m³, AQI='Good')

    print(f"PM2.5 = {reading.pm2_5_atm} µg/m³ [{reading.aqi_category}]")
```

## Averaged readings

```python
with HM3301(i2c_bus=1) as sensor:
    reading = sensor.read_average(samples=10, delay=1.0)
    print(reading.to_dict())
```

## Command-line tool

```bash
# Single reading
hm3301-read

# Average 5 readings, output as JSON
hm3301-read --samples 5 --json
```

## Wiring (Raspberry Pi)

| HM3301 pin | RPi pin |
|------------|---------|
| VCC        | 3.3 V (pin 1) |
| GND        | GND (pin 6)   |
| SDA        | GPIO 2 / SDA (pin 3) |
| SCL        | GPIO 3 / SCL (pin 5) |

## API Reference

### `HM3301(i2c_bus=1, i2c_address=0x40)`

| Method | Description |
|--------|-------------|
| `read()` | Return one `AirQualityReading` |
| `read_average(samples=5, delay=0.5)` | Return averaged reading |
| `close()` | Release the I²C bus |

### `AirQualityReading`

| Attribute | Type | Description |
|-----------|------|-------------|
| `pm1_0_std` / `pm1_0_atm` | `int` | PM1.0 µg/m³ |
| `pm2_5_std` / `pm2_5_atm` | `int` | PM2.5 µg/m³ |
| `pm10_std`  / `pm10_atm`  | `int` | PM10  µg/m³ |
| `count_0_3um` … `count_10um` | `int` | Particle counts per 0.1 L |
| `aqi_category` | `str` | US EPA AQI category |
| `timestamp` | `datetime` | Time of reading |
| `to_dict()` | `dict` | JSON-serialisable dict |

## Development

```bash
git clone https://github.com/ParthSanepara/hm3301
cd hm3301
pip install -e ".[dev]"
pytest
```

