import string


class CronParser:
    ANY_VALUE = "*"
    LIST_SEPERATOR_VALUE = ","
    RANGE_VALUE = "-"
    STEP_VALUE = "/"
    EXPRESSION_FIELDS = ["minute", "hour", "day of month", "month", "day of week"]
    FIELD_MIN_MAX = {
        "minute": [0, 59],
        "hour": [0, 23],
        "day of month": [1, 31],
        "month": [1, 12],
        "day of week": [0, 6],
    }

    DAYS_OF_WEEK = {
        "MON": 1,
        "TUE": 2,
        "WED": 3,
        "THU": 4,
        "FRI": 5,
        "SAT": 6,
        "SUN": 7,
    }

    MONTHS = {
        "JAN": 1,
        "FEB": 2,
        "MAR": 3,
        "APR": 4,
        "MAY": 5,
        "JUN": 6,
        "JUL": 7,
        "AUG": 8,
        "SEP": 9,
        "OCT": 10,
        "NOV": 11,
        "DEC": 12,
    }

    def __init__(self):
        self.expression = None
        self.expression_command = None
        self.result_dict = dict()

    def parse(self, expression):
        self.expression = expression
        split_expression = expression.split(" ")
        self.expression_command = " ".join(split_expression[5:])
        self.check_valid_expression(split_expression)

        for field, value in zip(self.EXPRESSION_FIELDS, split_expression[:-1]):
            field_max, field_min = self.field_max(field), self.field_min(field)
            self.parse_field_value(field, value, field_max, field_min)

    def parse_field_value(self, field, value, field_max, field_min):
        if value == self.ANY_VALUE:
            intervals = list(range(field_min, field_max + 1))
            self.result_dict[field] = intervals
        elif self.ANY_VALUE in value:
            self.parse_any_value(field, value, field_max, field_min)
        elif self.LIST_SEPERATOR_VALUE in value:
            self.parse_list_value(field, value, field_min, field_max)
        elif self.RANGE_VALUE in value:
            self.parse_range_value(field, value, field_min, field_max)
        else:
            self.result_dict[field] = int(value)

    def parse_any_value(self, field, value, field_max, field_min):
        if self.STEP_VALUE in value:
            step = int(value.split("/")[1])
            if step > field_max or step < field_min:
                raise ValueError(f"Field {field} incorrect, please try again.")
            else:
                self.result_dict[field] = list(range(field_min, field_max + 1, step)) if step != 0 else list(range(field_min, field_max + 1))
        else:
            raise ValueError(f"Field {field} incorrect, please try again.")

    def parse_list_value(self, field, value, field_min, field_max):
        days = list(map(int, value.split(self.LIST_SEPERATOR_VALUE)))
        if not self.check_valid_list(days, field_min, field_max):
            raise ValueError(f"Value {value} passed for field {field} is incorrect")
        self.result_dict[field] = days

    def parse_range_value(self, field, value, field_min, field_max):
        start, end = value.split("-")
        start, end = self.convert_range_value(start, field), self.convert_range_value(end, field)
        if not (field_min <= start <= field_max and field_min <= end <= field_max):
            raise ValueError(f"Value {value} passed for field {field} is incorrect")

        if field == "day of week" and start > end:
            self.result_dict[field] = list(range(start, field_max + 1)) + list(range(field_min, end + 1))
        else:
            self.result_dict[field] = list(range(start, end + 1))

    def convert_range_value(self, value, field):
        return self.DAYS_OF_WEEK.get(value, self.MONTHS.get(value, int(value)))

    def check_valid_expression(self, split_expression):
        for expression in split_expression[:5]:
            if any(char in string.punctuation and char not in ["-", ",", "/", "*"] for char in expression):
                raise ValueError(f"Invalid value in expression passed")

    def check_valid_list(self, _list, min_val, max_val):
        return all(min_val <= i <= max_val for i in _list)

    def field_min(self, field):
        return self.FIELD_MIN_MAX[field][0]

    def field_max(self, field):
        return self.FIELD_MIN_MAX[field][1]

    def log_results(self):
        if not self.expression:
            raise Exception("Please parse before attempting to log results.")

        return_str = "\n"
        for field, values in self.result_dict.items():
            if isinstance(values, list):
                return_str += f"{field:<14} {', '.join(map(str, values))}\n"
            else:
                return_str += f"{field:<14} {values}\n"
        return_str += f"{'command':<14} {self.expression_command}\n"
        return return_str
