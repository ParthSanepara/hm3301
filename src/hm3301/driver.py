"""
HM3301 laser PM2.5 dust sensor driver.

The HM3301 communicates over I2C (default address 0x40).
Each read returns a 29-byte frame:

  Byte  0      : Header (0x42 - always)
  Byte  1      : Sensor number (0x4d normally)
  Bytes 2-3    : PM1.0 standard (big-endian uint16)
  Bytes 4-5    : PM2.5 standard
  Bytes 6-7    : PM10  standard
  Bytes 8-9    : PM1.0 atmospheric
  Bytes 10-11  : PM2.5 atmospheric
  Bytes 12-13  : PM10  atmospheric
  Bytes 14-15  : Particle count  >0.3 um / 0.1 L
  Bytes 16-17  : Particle count  >0.5 um / 0.1 L
  Bytes 18-19  : Particle count  >1.0 um / 0.1 L
  Bytes 20-21  : Particle count  >2.5 um / 0.1 L
  Bytes 22-23  : Particle count  >5.0 um / 0.1 L
  Bytes 24-25  : Particle count  >10  um / 0.1 L
  Bytes 26-27  : Reserved
  Byte  28     : Checksum (sum of bytes 0-27, low byte)
"""

import struct
import time
from typing import Any

from .exceptions import (
    HM3301ChecksumError,
    HM3301ConnectionError,
    HM3301ReadError,
)
from .models import AirQualityReading

# Default I2C address
_DEFAULT_I2C_ADDRESS = 0x40
# Frame size in bytes
_FRAME_LEN = 29
# Command to select I2C mode
_CMD_SELECT_COMM = 0x88


class HM3301:
    """
    Driver for the Seeed HM3301 laser PM2.5 dust sensor over I2C.

    Parameters
    ----------
    i2c_bus : int
        I2C bus number (e.g. 1 on Raspberry Pi).
    i2c_address : int
        I2C address of the sensor (default: 0x40).

    Example
    -------
    >>> from hm3301 import HM3301
    >>> with HM3301(i2c_bus=1) as sensor:
    ...     reading = sensor.read()
    ...     print(reading)
    AirQualityReading(PM1.0=5ug/m3, PM2.5=8ug/m3, PM10=9ug/m3, AQI='Good')
    """

    def __init__(
        self,
        i2c_bus: int = 1,
        i2c_address: int = _DEFAULT_I2C_ADDRESS,
    ) -> None:
        self._address = i2c_address
        self._bus_num = i2c_bus
        self._bus: Any = None
        self._connect()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def read(self) -> AirQualityReading:
        """
        Read one frame from the sensor and return an AirQualityReading.

        Raises
        ------
        HM3301ReadError
            If the frame length is unexpected.
        HM3301ChecksumError
            If the frame checksum does not match.
        """
        raw = self._read_raw()
        self._validate_checksum(raw)
        return self._parse_frame(raw)

    def read_average(
        self, samples: int = 5, delay: float = 0.5
    ) -> AirQualityReading:
        """
        Take *samples* readings and return their average as an
        AirQualityReading.

        Parameters
        ----------
        samples : int
            Number of readings to average (default: 5).
        delay : float
            Seconds to wait between readings (default: 0.5).
        """
        if samples < 1:
            raise ValueError("samples must be >= 1")

        readings = []
        for i in range(samples):
            readings.append(self.read())
            if i < samples - 1:
                time.sleep(delay)

        def _avg(attr: str) -> int:
            total: int = sum(int(getattr(r, attr)) for r in readings)
            return round(total / len(readings))

        return AirQualityReading(
            pm1_0_std=_avg("pm1_0_std"),
            pm2_5_std=_avg("pm2_5_std"),
            pm10_std=_avg("pm10_std"),
            pm1_0_atm=_avg("pm1_0_atm"),
            pm2_5_atm=_avg("pm2_5_atm"),
            pm10_atm=_avg("pm10_atm"),
            count_0_3um=_avg("count_0_3um"),
            count_0_5um=_avg("count_0_5um"),
            count_1_0um=_avg("count_1_0um"),
            count_2_5um=_avg("count_2_5um"),
            count_5_0um=_avg("count_5_0um"),
            count_10um=_avg("count_10um"),
            sensor_num=readings[0].sensor_num,
        )

    def close(self) -> None:
        """Release the I2C bus resource."""
        if self._bus is not None:
            try:
                self._bus.close()
            except Exception:
                pass
            self._bus = None

    # ------------------------------------------------------------------
    # Context manager support
    # ------------------------------------------------------------------

    def __enter__(self) -> "HM3301":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _connect(self) -> None:
        """Open the I2C bus and send the select-comm command."""
        try:
            import smbus2

            self._bus = smbus2.SMBus(self._bus_num)
            # Wake the sensor and select I2C mode
            self._bus.write_byte(self._address, _CMD_SELECT_COMM)
            time.sleep(0.1)
        except ImportError as exc:
            raise HM3301ConnectionError(
                "smbus2 is required but not installed. "
                "Install it with: pip install smbus2"
            ) from exc
        except OSError as exc:
            raise HM3301ConnectionError(
                f"Cannot open I2C bus {self._bus_num} at address "
                f"0x{self._address:02X}: {exc}"
            ) from exc

    def _read_raw(self) -> bytes:
        """Read a raw 29-byte frame from the sensor."""
        try:
            import smbus2

            msg = smbus2.i2c_msg.read(self._address, _FRAME_LEN)
            self._bus.i2c_rdwr(msg)
            raw = bytes(msg)
        except OSError as exc:
            raise HM3301ReadError(f"I2C read failed: {exc}") from exc

        if len(raw) != _FRAME_LEN:
            raise HM3301ReadError(
                f"Expected {_FRAME_LEN} bytes, got {len(raw)}"
            )
        return raw

    @staticmethod
    def _validate_checksum(raw: bytes) -> None:
        """Verify the frame checksum (sum of bytes 0-27, low byte)."""
        expected = sum(raw[:-1]) & 0xFF
        actual = raw[-1]
        if expected != actual:
            raise HM3301ChecksumError(
                f"Checksum mismatch: expected 0x{expected:02X}, "
                f"got 0x{actual:02X}"
            )

    @staticmethod
    def _parse_frame(raw: bytes) -> AirQualityReading:
        """Parse a validated 29-byte frame into an AirQualityReading."""
        # Unpack 13 big-endian uint16 values starting at byte 2
        (
            pm1_0_std, pm2_5_std, pm10_std,
            pm1_0_atm, pm2_5_atm, pm10_atm,
            cnt_03, cnt_05, cnt_10, cnt_25, cnt_50, cnt_100,
            _reserved,
        ) = struct.unpack_from(">13H", raw, offset=2)

        return AirQualityReading(
            pm1_0_std=pm1_0_std,
            pm2_5_std=pm2_5_std,
            pm10_std=pm10_std,
            pm1_0_atm=pm1_0_atm,
            pm2_5_atm=pm2_5_atm,
            pm10_atm=pm10_atm,
            count_0_3um=cnt_03,
            count_0_5um=cnt_05,
            count_1_0um=cnt_10,
            count_2_5um=cnt_25,
            count_5_0um=cnt_50,
            count_10um=cnt_100,
            sensor_num=raw[1],
        )
