from datetime import datetime

def ms_date_to_datetime(ms_date: str) -> datetime:
  return datetime.strptime(ms_date, "%Y-%m-%d %H:%M:%S.%f")
