from datetime import datetime, timedelta


def get_start_date(date_range: str) -> datetime:
    end_date = datetime.now()

    if date_range == "30d":
        return end_date - timedelta(days=30)
    elif date_range == "90d":
        return end_date - timedelta(days=90)
    elif date_range == "1y":
        return end_date - timedelta(days=365)
    else:
        return datetime(2020, 1, 1)
