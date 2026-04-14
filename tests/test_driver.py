"""Tests for HM3301 driver (mocked I2C)."""

import struct
from unittest.mock import MagicMock, patch

import pytest

from hm3301.driver import HM3301
from hm3301.exceptions import HM3301ChecksumError, HM3301ConnectionError


def _build_frame(
    pm1_std=5, pm25_std=8, pm10_std=9,
    pm1_atm=5, pm25_atm=8, pm10_atm=9,
    c03=100, c05=50, c10=20, c25=10, c50=5, c100=2,
    sensor_num=0x4D,
):
    """Build a valid 29-byte HM3301 frame with correct checksum."""
    header = bytes([0x42, sensor_num])
    payload = struct.pack(
        ">13H",
        pm1_std, pm25_std, pm10_std,
        pm1_atm, pm25_atm, pm10_atm,
        c03, c05, c10, c25, c50, c100,
        0,  # reserved
    )
    data = header + payload
    checksum = sum(data) & 0xFF
    return data + bytes([checksum])


@pytest.fixture
def mock_smbus():
    """Patch smbus2 so HM3301 can be instantiated without real hardware."""
    mock_bus = MagicMock()
    mock_module = MagicMock()
    mock_module.SMBus.return_value = mock_bus

    with patch.dict("sys.modules", {"smbus2": mock_module}):
        yield mock_bus, mock_module


def test_read_valid_frame(mock_smbus):
    mock_bus, mock_module = mock_smbus
    frame = _build_frame()

    mock_msg = MagicMock()
    mock_msg.__iter__ = lambda self: iter(frame)
    mock_msg.__len__ = lambda self: len(frame)
    mock_module.i2c_msg.read.return_value = mock_msg

    # Make bytes(msg) return the frame
    mock_msg.__bytes__ = lambda self: frame

    with patch("hm3301.driver.smbus2", mock_module, create=True):
        sensor = HM3301(i2c_bus=1)
        # Patch _read_raw to return our frame directly
        sensor._read_raw = MagicMock(return_value=frame)
        reading = sensor.read()

    assert reading.pm2_5_atm == 8
    assert reading.pm10_atm == 9
    assert reading.aqi_category == "Good"


def test_checksum_error(mock_smbus):
    mock_bus, _ = mock_smbus
    frame = _build_frame()
    # Corrupt the checksum
    bad_frame = frame[:-1] + bytes([frame[-1] ^ 0xFF])

    sensor = HM3301(i2c_bus=1)
    with pytest.raises(HM3301ChecksumError):
        sensor._validate_checksum(bad_frame)


def test_connection_error_no_smbus():
    with patch.dict("sys.modules", {"smbus2": None}):
        with pytest.raises(HM3301ConnectionError):
            HM3301(i2c_bus=1)


def test_read_average(mock_smbus):
    mock_bus, mock_module = mock_smbus
    frame = _build_frame(pm25_atm=10)

    sensor = HM3301(i2c_bus=1)
    sensor._read_raw = MagicMock(return_value=frame)

    reading = sensor.read_average(samples=3, delay=0)
    assert reading.pm2_5_atm == 10


def test_close(mock_smbus):
    mock_bus, _ = mock_smbus
    sensor = HM3301(i2c_bus=1)
    sensor.close()
    assert sensor._bus is None


def test_context_manager(mock_smbus):
    mock_bus, _ = mock_smbus
    with HM3301(i2c_bus=1) as sensor:
        assert sensor._bus is not None
    assert sensor._bus is None
