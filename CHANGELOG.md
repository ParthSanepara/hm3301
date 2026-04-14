# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.1.0] - Unreleased

### Added

- `HM3301` driver class with I2C communication via `smbus2`
- `AirQualityReading` data model with PM1.0, PM2.5, PM10 and particle counts
- `aqi_category` property using US EPA PM2.5 breakpoints
- `read_average()` for multi-sample averaging
- `to_dict()` for JSON serialisation
- `hm3301-read` CLI tool with `--samples`, `--json`, `--bus`, `--address` options
- Custom exception hierarchy (`HM3301Error`, `HM3301ConnectionError`, `HM3301ReadError`, `HM3301ChecksumError`)
- PEP 561 type marker (`py.typed`)
- CI workflow (Python 3.8-3.12 matrix)
- Release workflow with PyPI Trusted Publishing (OIDC)
