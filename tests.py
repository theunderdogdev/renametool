from datetime import datetime
import re
from re import Match
from rich.console import Console
from rich.traceback import install
from tkinter import messagebox
install()
cns = Console()


def _validate_date(match_obj: Match) -> str:
    date_val = match_obj.group(2)
    try:
        datetime.strptime( date_val, "%Y-%m-%d")
        return date_val
    except ValueError:
        messagebox.showinfo("Invalid date", "The date format is invalid")
        print("Invalid date", date_val)
        return f"!d{{{date_val}}}"

def _vatlidate_date_time(match_obj: Match) -> str:
    date_time_val = match_obj.group(2)
    try:
        return datetime.strptime(date_time_val, "%Y-%m-%d|%H:%M:%S").isoformat()
    except ValueError:
        print('Invalid', date_time_val)
        return f"!d{{{date_time_val}}}"

def _prefill(text: str) -> str:
    __empty_dt_fill = re.compile(r"(\!d\{\})")
    __empty_dtt_fill = re.compile(r"(\!dt\{\})")

    __value_dt_fill = re.compile(r"(\!d\{)(\d{4}-\d{2}-\d{2})(\})")
    __value_dtt_fill = re.compile(r"(\!dt\{)(\d{4}-\d{2}-\d{2}\|\d{2}:\d{2}:\d{2})(\})")
    today = datetime.now()
    filled = __empty_dt_fill.sub(today.date().strftime("%Y-%m-%d"), text)
    filled = __empty_dtt_fill.sub(today.isoformat(), filled)
    filled = __value_dt_fill.sub(_validate_date, filled)
    filled = __value_dtt_fill.sub(_vatlidate_date_time, filled)
    return filled


# filled_date = _prefill("Empty date: !d{}\nFilled Date: !d{2022-01-32}\nEmpty Datetime: !dt{}\nFilled Datetime: !dt{2022-01-09|12:20:22}")
fill_match = re.compile(r"(?<=\!d|dt)(\{[0-9:|-]*\})?")
print(fill_match.findall("!-Hello"))