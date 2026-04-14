"""
hm3301 - Python driver for the Seeed HM3301 laser PM2.5 dust sensor.
"""

from .driver import HM3301
from .exceptions import (
    HM3301ChecksumError,
    HM3301ConnectionError,
    HM3301Error,
    HM3301ReadError,
)
from .models import AirQualityReading

__version__ = "0.0.1"

__all__ = [
    "HM3301",
    "AirQualityReading",
    "HM3301Error",
    "HM3301ChecksumError",
    "HM3301ConnectionError",
    "HM3301ReadError",
    "__version__",
]
