import pytest
from pytest import fixture

from cron_parser import CronParser


@fixture(scope="module")
def parser_instance():
    yield CronParser()


def test_cron_expression_original(parser_instance):
    parser_instance.parse("*/15 0 1,15 * 1-5 /usr/bin/find")
    expected_parsed_expression = {
        "minute": [0, 15, 30, 45],
        "hour": 0,
        "day of month": [1, 15],
        "month": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "day of week": [1, 2, 3, 4, 5],
    }
    assert parser_instance.result_dict == expected_parsed_expression


def test_cron_expression_minute_15(parser_instance):
    parser_instance.parse("15 0 1,15 * 1-5 /usr/bin/find")
    expected_parsed_expression = {
        "minute": 15,
        "hour": 0,
        "day of month": [1, 15],
        "month": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "day of week": [1, 2, 3, 4, 5],
    }
    assert parser_instance.result_dict == expected_parsed_expression


def test_cron_expression_extra_day_of_month(parser_instance):
    parser_instance.parse("*/15 0 1,11,20,15 * 1-5 /usr/bin/find")
    expected_parsed_expression = {
        "minute": [0, 15, 30, 45],
        "hour": 0,
        "day of month": [1, 11, 20, 15],
        "month": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "day of week": [1, 2, 3, 4, 5],
    }
    assert parser_instance.result_dict == expected_parsed_expression


def test_cron_expression_month_1_month_2(parser_instance):
    parser_instance.parse("*/15 0 1,11,20,15 1,2 1-5 /usr/bin/find")
    expected_parsed_expression = {
        "minute": [0, 15, 30, 45],
        "hour": 0,
        "day of month": [1, 11, 20, 15],
        "month": [1, 2],
        "day of week": [1, 2, 3, 4, 5],
    }
    assert parser_instance.result_dict == expected_parsed_expression


def test_cron_expression_hour_10(parser_instance):
    parser_instance.parse("*/15 10 1,11,20,15 1,2 1-5 /usr/bin/find")
    expected_parsed_expression = {
        "minute": [0, 15, 30, 45],
        "hour": 10,
        "day of month": [1, 11, 20, 15],
        "month": [1, 2],
        "day of week": [1, 2, 3, 4, 5],
    }
    assert parser_instance.result_dict == expected_parsed_expression


def test_cron_expression_expected_string(parser_instance):
    parser_instance.parse("*/15 0 1,15 * 1-5 /usr/bin/find")
    expected_string = """\
minute         0, 15, 30, 45
hour           0
day of month   1, 15
month          1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
day of week    1, 2, 3, 4, 5
command        /usr/bin/find
    """.strip()
    assert parser_instance.logg_results().strip() == expected_string


def test_cron_expression_invalid_expression_extra_field(parser_instance):
    with pytest.raises(ValueError):
        parser_instance.parse("*/15 0 1,15 * 1-5 /usr/bin/find extra")


def test_cron_expression_invalid_expression_missing_command(parser_instance):
    with pytest.raises(ValueError):
        parser_instance.parse("*/15 0 1,15 * 1-5")


def test_cron_expression_invalid_expression_exceed_max(parser_instance):
    with pytest.raises(ValueError):
        parser_instance.parse("*/15 0 1,15 * 1-7 /usr/bin/find")


def test_cron_expression_logging_without_parsing():
    instance = CronParser()
    with pytest.raises(Exception):
        instance.logg_results()


def test_cron_expression_single_values(parser_instance):
    parser_instance.parse("15 0 1 1 1 /usr/bin/find")
    expected_parsed_expression = {
        "minute": 15,
        "hour": 0,
        "day of month": 1,
        "month": 1,
        "day of week": 1,
    }
    assert parser_instance.result_dict == expected_parsed_expression


def test_cron_expression_invalid_characters(parser_instance):
    with pytest.raises(ValueError):
        parser_instance.parse("*/15 0 1a,15 * 1-5 /usr/bin/find")


def test_cron_expression_invalid_punctuation(parser_instance):
    with pytest.raises(ValueError):
        parser_instance.parse("*>15 0 1,15 * 1-5 /usr/bin/find")


def test_cron_expression_invalid_range(parser_instance):
    with pytest.raises(ValueError):
        parser_instance.parse("*/15 0 10-5 * 1-5 /usr/bin/find")


def test_cron_expression_(parser_instance):
    parser_instance.parse("*/15 1-5 1,11,20,15 1,2 1-5 /usr/bin/find")
    expected_parsed_expression = {
        "minute": [0, 15, 30, 45],
        "hour": [1, 2, 3, 4, 5],
        "day of month": [1, 11, 20, 15],
        "month": [1, 2],
        "day of week": [1, 2, 3, 4, 5],
    }
    assert parser_instance.result_dict == expected_parsed_expression


def test_cron_expression_original_by_name_range(parser_instance):
    parser_instance.parse("*/15 0 1,15 JAN-JUN MON-FRI /usr/bin/find -mtime 5 -maxdepth 5")
    expected_parsed_expression = {
        "minute": [0, 15, 30, 45],
        "hour": 0,
        "day of month": [1, 15],
        "month": [1, 2, 3, 4, 5, 6],
        "day of week": [1, 2, 3, 4, 5],
    }
    assert parser_instance.result_dict == expected_parsed_expression


# */15 0 1,15 * FRI-MON /usr/bin/find -mtime 5 -maxdepth 5

def test_cron_expression_original_by_wrap_around(parser_instance):
    parser_instance.parse("*/15 0 1,15 * FRI-MON /usr/bin/find -mtime 5 -maxdepth 5")
    expected_parsed_expression = {
        "minute": [0, 15, 30, 45],
        "hour": 0,
        "day of month": [1, 15],
        "month": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "day of week": [5, 6, 0, 1],
    }
    assert parser_instance.result_dict == expected_parsed_expression
