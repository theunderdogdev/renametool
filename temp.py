from datetime import datetime
import re
from re import Match
from rich.console import Console
from rich.traceback import install

install()
cns = Console()


def _validate_date(match_obj: Match) -> str:
    date_val = match_obj.group(2)
    try:
        datetime.strptime( date_val, "%Y-%m-%d")
        return date_val
    except ValueError:
        # launch tk message box here
        print("Invalid date", date_val)
        return f"!d{{{date_val}}}"


def _prefill(text: str) -> str | None:
    __empty_dt_fill = re.compile(r"(\!d\{\})")

    __value_dt_fill = re.compile(r"(\!d\{)(\d{4}-\d{2}-\d{2})(\})")
    # __empty_dt_fill
    today = datetime.now().date().strftime("%Y-%m-%d")
    filled = __value_dt_fill.sub(_validate_date, text)
    filled = __empty_dt_fill.sub(today, filled)
    print(filled)


_prefill("Hello-!d{2022-21-32}")
_prefill("!d{}Hello World !d{2022-01-09}")

# datetime.strptime("%Y-%m-%d", "2022-01-10")
