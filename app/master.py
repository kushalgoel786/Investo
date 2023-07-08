from datetime import date
from dateutil.relativedelta import relativedelta


def get_nav_on(nav_data, target_date):
    # For Weekends, return the NAV of Friday
    target_date = get_latest_weekday(target_date)

    # For dates that do not exist, return error
    if target_date > nav_data[0]["date"]:
        return {"error": "Invalid Date"}
    elif target_date < nav_data[-1]["date"]:
        return {"error": "Invalid Date"}

    low = 0
    high = len(nav_data) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_date = nav_data[mid]["date"]

        if mid_date == target_date:
            return nav_data[mid]
        elif mid_date > target_date:
            low = mid + 1
        else:
            high = mid - 1

    return {"error": "NAV Not Found"}


def get_returns(nav_data, start_date, end_date):
    if end_date < start_date:
        return {"error": "End date cannot be less than start date"}

    nav_start_date = get_nav_on(nav_data, start_date)
    nav_end_date = get_nav_on(nav_data, end_date)

    if "error" in nav_end_date:
        return {"error": "Invalid End Date"}
    elif "error" in nav_start_date:
        return {"error": "Invalid Start Date"}
    else:
        returns = ((nav_end_date["nav"] / nav_start_date["nav"]) - 1) * 100
        return {
            "return": returns,
            "to_date": nav_end_date["date"],
            "from_date": nav_start_date["date"],
        }


def get_cagr(nav_data, years):
    end_date = get_latest_weekday(date.today())
    # Calculate returns from latest weekday to latest weekday - no of years
    start_date = end_date - relativedelta(years=years)

    nav_start_date = get_nav_on(nav_data, start_date)
    nav_end_date = get_nav_on(nav_data, end_date)

    if "error" in nav_end_date:
        return {"error": "Could Not Calculate CAGR"}
    elif "error" in nav_start_date:
        return {"error": "Scheme is not existing from " + str(years) + " years"}
    else:
        cagr = (((nav_end_date["nav"] / nav_start_date["nav"]) ** (1/years)) - 1) * 100
        return {
            "return": cagr,
            "to_date": nav_end_date["date"],
            "from_date": nav_start_date["date"],
        }


def get_absolute(nav_data, years):
    end_date = get_latest_weekday(date.today())
    # Calculate returns from latest weekday to latest weekday - no of years
    start_date = end_date - relativedelta(years=years)

    nav_start_date = get_nav_on(nav_data, start_date)
    nav_end_date = get_nav_on(nav_data, end_date)

    if "error" in nav_end_date:
        return {"error": "Could Not Calculate CAGR"}
    elif "error" in nav_start_date:
        return {"error": "Scheme is not existing from " + str(years) + " years"}
    else:
        absolute_returns = ((nav_end_date["nav"] / nav_start_date["nav"]) - 1) * 100
        return {
            "return": absolute_returns,
            "to_date": nav_end_date["date"],
            "from_date": nav_start_date["date"],
        }


def get_latest_weekday(day):
    if day.weekday() == 5:
        return day - relativedelta(days=1)
    elif day.weekday() == 6:
        return day - relativedelta(days=2)
    else:
        return day