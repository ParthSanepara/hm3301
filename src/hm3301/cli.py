"""Command-line interface for hm3301-read."""

import argparse
import json
import sys

from .driver import HM3301
from .exceptions import HM3301Error


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="hm3301-read",
        description="Read air quality data from the Seeed HM3301 sensor.",
    )
    parser.add_argument(
        "--bus",
        type=int,
        default=1,
        help="I2C bus number (default: 1)",
    )
    parser.add_argument(
        "--address",
        type=lambda x: int(x, 0),
        default=0x40,
        help="I2C address in hex (default: 0x40)",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=1,
        help="Number of readings to average (default: 1)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay in seconds between averaged readings (default: 1.0)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Output as JSON",
    )
    args = parser.parse_args()

    try:
        with HM3301(i2c_bus=args.bus, i2c_address=args.address) as sensor:
            if args.samples > 1:
                reading = sensor.read_average(
                    samples=args.samples, delay=args.delay
                )
            else:
                reading = sensor.read()

            if args.as_json:
                print(json.dumps(reading.to_dict(), indent=2))
            else:
                print(reading)
    except HM3301Error as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
