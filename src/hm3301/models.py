"""Data models for HM3301 sensor readings."""

from datetime import datetime
from typing import Any, Dict


class AirQualityReading:
    """
    Represents a single air quality reading from the HM3301 sensor.

    Attributes
    ----------
    pm1_0_std, pm2_5_std, pm10_std : int
        PM concentrations in ug/m3 (standard particle).
    pm1_0_atm, pm2_5_atm, pm10_atm : int
        PM concentrations in ug/m3 (atmospheric environment).
    count_0_3um .. count_10um : int
        Particle counts per 0.1 L for each size bin.
    sensor_num : int
        Sensor number byte from the frame header.
    timestamp : datetime
        Time when the reading was created.
    """

    __slots__ = (
        "pm1_0_std", "pm2_5_std", "pm10_std",
        "pm1_0_atm", "pm2_5_atm", "pm10_atm",
        "count_0_3um", "count_0_5um", "count_1_0um",
        "count_2_5um", "count_5_0um", "count_10um",
        "sensor_num", "timestamp",
    )

    def __init__(
        self,
        pm1_0_std: int = 0,
        pm2_5_std: int = 0,
        pm10_std: int = 0,
        pm1_0_atm: int = 0,
        pm2_5_atm: int = 0,
        pm10_atm: int = 0,
        count_0_3um: int = 0,
        count_0_5um: int = 0,
        count_1_0um: int = 0,
        count_2_5um: int = 0,
        count_5_0um: int = 0,
        count_10um: int = 0,
        sensor_num: int = 0,
        timestamp: datetime = None,  # type: ignore[assignment]
    ) -> None:
        self.pm1_0_std = pm1_0_std
        self.pm2_5_std = pm2_5_std
        self.pm10_std = pm10_std
        self.pm1_0_atm = pm1_0_atm
        self.pm2_5_atm = pm2_5_atm
        self.pm10_atm = pm10_atm
        self.count_0_3um = count_0_3um
        self.count_0_5um = count_0_5um
        self.count_1_0um = count_1_0um
        self.count_2_5um = count_2_5um
        self.count_5_0um = count_5_0um
        self.count_10um = count_10um
        self.sensor_num = sensor_num
        self.timestamp = timestamp or datetime.now()

    @property
    def aqi_category(self) -> str:
        """Return the US EPA AQI category based on PM2.5 atmospheric concentration."""
        pm = self.pm2_5_atm
        if pm <= 12:
            return "Good"
        elif pm <= 35:
            return "Moderate"
        elif pm <= 55:
            return "Unhealthy for Sensitive Groups"
        elif pm <= 150:
            return "Unhealthy"
        elif pm <= 250:
            return "Very Unhealthy"
        else:
            return "Hazardous"

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serialisable dictionary of the reading."""
        return {
            "pm1_0_std": self.pm1_0_std,
            "pm2_5_std": self.pm2_5_std,
            "pm10_std": self.pm10_std,
            "pm1_0_atm": self.pm1_0_atm,
            "pm2_5_atm": self.pm2_5_atm,
            "pm10_atm": self.pm10_atm,
            "count_0_3um": self.count_0_3um,
            "count_0_5um": self.count_0_5um,
            "count_1_0um": self.count_1_0um,
            "count_2_5um": self.count_2_5um,
            "count_5_0um": self.count_5_0um,
            "count_10um": self.count_10um,
            "sensor_num": self.sensor_num,
            "aqi_category": self.aqi_category,
            "timestamp": self.timestamp.isoformat(),
        }

    def __repr__(self) -> str:
        return (
            f"AirQualityReading("
            f"PM1.0={self.pm1_0_atm}\u00b5g/m\u00b3, "
            f"PM2.5={self.pm2_5_atm}\u00b5g/m\u00b3, "
            f"PM10={self.pm10_atm}\u00b5g/m\u00b3, "
            f"AQI='{self.aqi_category}')"
        )

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AirQualityReading):
            return NotImplemented
        return (
            self.pm1_0_std == other.pm1_0_std
            and self.pm2_5_std == other.pm2_5_std
            and self.pm10_std == other.pm10_std
            and self.pm1_0_atm == other.pm1_0_atm
            and self.pm2_5_atm == other.pm2_5_atm
            and self.pm10_atm == other.pm10_atm
            and self.count_0_3um == other.count_0_3um
            and self.count_0_5um == other.count_0_5um
            and self.count_1_0um == other.count_1_0um
            and self.count_2_5um == other.count_2_5um
            and self.count_5_0um == other.count_5_0um
            and self.count_10um == other.count_10um
        )
