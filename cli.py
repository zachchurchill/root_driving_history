"""CLI to create driving reports given input files"""

import io
import sys
import logging

import click

from root_driving_history import parse_input_log
from root_driving_history import create_driving_report


logging.basicConfig(
    level=logging.INFO,
    format="%(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
LOGGER = logging.getLogger(__file__)
LOGGER.setLevel(logging.ERROR)


@click.command()
@click.option(
    "--file", "-f",
    required=True,
    help="Input file with driving records",
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    default=False,
    help="If verbose, then outputs INFO log items",
    show_default=True,
)
def cli(file, verbose):
    if verbose:
        LOGGER.setLevel(logging.INFO)
    try:
        LOGGER.info("Attempting to open and read {}...".format(file))
        with open(file, "r") as f:
            file_buffer = io.StringIO(f.read())
    except FileNotFoundError:
        LOGGER.error("'{}' does not exist".format(file))
        sys.exit(1)
    else:
        LOGGER.info("Contents received from {}".format(file))

    LOGGER.info("Parsing input file for data...")
    try:
        parsed_data = parse_input_log(file_buffer)
    except Exception as e:
        LOGGER.error(e)
    else:
        LOGGER.info("Input data parsed")

    LOGGER.info("Creating a driving summary report...")
    try:
        report = create_driving_report(parsed_data)
    except Exception as e:
        LOGGER.error(e)
        sys.exit(1)
    else:
        LOGGER.info("Summary report created")

    print(report)


if __name__ == "__main__":
    cli()
