"""Custom exceptions for the HM3301 sensor driver."""


class HM3301Error(Exception):
    """Base exception for all HM3301 errors."""


class HM3301ConnectionError(HM3301Error):
    """Raised when the I2C bus cannot be opened or the sensor is unreachable."""


class HM3301ReadError(HM3301Error):
    """Raised when a read from the sensor fails or returns unexpected data."""


class HM3301ChecksumError(HM3301ReadError):
    """Raised when the frame checksum does not match."""
