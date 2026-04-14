"""Tests for AirQualityReading model."""

from hm3301.models import AirQualityReading


def test_aqi_good():
    r = AirQualityReading(pm2_5_atm=10)
    assert r.aqi_category == "Good"


def test_aqi_moderate():
    r = AirQualityReading(pm2_5_atm=20)
    assert r.aqi_category == "Moderate"


def test_aqi_unhealthy_sensitive():
    r = AirQualityReading(pm2_5_atm=40)
    assert r.aqi_category == "Unhealthy for Sensitive Groups"


def test_aqi_unhealthy():
    r = AirQualityReading(pm2_5_atm=100)
    assert r.aqi_category == "Unhealthy"


def test_aqi_very_unhealthy():
    r = AirQualityReading(pm2_5_atm=200)
    assert r.aqi_category == "Very Unhealthy"


def test_aqi_hazardous():
    r = AirQualityReading(pm2_5_atm=300)
    assert r.aqi_category == "Hazardous"


def test_to_dict_keys():
    r = AirQualityReading(pm1_0_atm=5, pm2_5_atm=8, pm10_atm=9)
    d = r.to_dict()
    assert d["pm1_0_atm"] == 5
    assert d["pm2_5_atm"] == 8
    assert d["pm10_atm"] == 9
    assert d["aqi_category"] == "Good"
    assert "timestamp" in d


def test_repr():
    r = AirQualityReading(pm1_0_atm=5, pm2_5_atm=8, pm10_atm=9)
    s = repr(r)
    assert "PM2.5=8" in s
    assert "Good" in s


def test_equality():
    a = AirQualityReading(pm2_5_atm=10, pm10_atm=20)
    b = AirQualityReading(pm2_5_atm=10, pm10_atm=20)
    assert a == b


def test_inequality():
    a = AirQualityReading(pm2_5_atm=10)
    b = AirQualityReading(pm2_5_atm=20)
    assert a != b
