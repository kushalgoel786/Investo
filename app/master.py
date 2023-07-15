from datetime import date
from app.invalid_date_error import InvalidDateError
from dateutil.relativedelta import relativedelta
import numpy as np

# Rolling Returns


# # Good ----------------------------------
def get_nav_on(nav_data, target_date):
    if target_date > date.today() or target_date < nav_data[-1]["date"]:
        raise InvalidDateError(str(date) + " is an Invalid Date")

    # Improving efficiency, handle case for latest NAV
    if target_date >= nav_data[0]["date"]:
        return nav_data[0]

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

    return nav_data[low]


def get_returns(nav_data, start_date, end_date):
    if end_date < start_date:
        raise InvalidDateError("End date cannot be less than Start date")

    nav_start_date = get_nav_on(nav_data, start_date)
    nav_end_date = get_nav_on(nav_data, end_date)
    returns = ((nav_end_date["nav"] / nav_start_date["nav"]) - 1) * 100
    return {
        "return": returns,
        "end_date": nav_end_date["date"],
        "start_date": nav_start_date["date"],
    }


def get_yearly_returns(nav_data):
    start_year = nav_data[-1]["date"].year
    current_year = date.today().year
    yearly_returns = []

    for i in range(start_year, current_year + 1):
        first_date = date(i - 1, 12, 31)
        last_date = date(i, 12, 31)
        print(first_date)
        print(last_date)

        # Change first/last date for first/last year
        if i == start_year:
            first_date = nav_data[-1]["date"]

        if i == current_year:
            last_date = date.today()

        returns = get_returns(nav_data, first_date, last_date)
        yearly_returns.append({str(i): returns})
    return yearly_returns
# # Good ----------------------------------


# def get_cagr(nav_data, years):
#     end_date = get_latest_weekday(date.today())
#     nav_end_date = get_nav_on(nav_data, end_date)
#     # Calculate returns from latest weekday to (latest weekday - no of years)
#     start_date = nav_end_date["date"] - relativedelta(years=years)
#
#     # nav_start_date = get_nav_on(nav_data, start_date)
#     nav_start_date = get_nav_on(nav_data, date(2018,7,7))
#
#     print(nav_end_date)
#     print(nav_start_date)
#
#     if "error" in nav_end_date:
#         return {"error": "Could Not Calculate CAGR"}
#     elif "error" in nav_start_date:
#         return {"error": "Scheme is not existing from " + str(years) + " years"}
#     else:
#         diff = end_date - date(2018, 7, 7)
#         cagr = (((nav_end_date["nav"] / nav_start_date["nav"]) ** (1 / ((diff.days-2) / 365))) - 1) * 100
#         return {
#             "return": cagr,
#             "to_date": nav_end_date["date"],
#             "from_date": nav_start_date["date"],
#         }
#
#
# def get_standard_deviation(nav_data):
#     nav_values = np.array([item["nav"] for item in nav_data])
#     std_dev = np.std(nav_values)
#     return std_dev
#
# def get_absolute(nav_data, years):
#     end_date = get_latest_weekday(date.today())
#     # Calculate returns from latest weekday to latest weekday - no of years
#     start_date = end_date - relativedelta(years=years)
#
#     nav_start_date = get_nav_on(nav_data, start_date)
#     nav_end_date = get_nav_on(nav_data, end_date)
#
#     if "error" in nav_end_date:
#         return {"error": "Could Not Calculate CAGR"}
#     elif "error" in nav_start_date:
#         return {"error": "Scheme is not existing from " + str(years) + " years"}
#     else:
#         absolute_returns = ((nav_end_date["nav"] / nav_start_date["nav"]) - 1) * 100
#         return {
#             "return": absolute_returns,
#             "to_date": nav_end_date["date"],
#             "from_date": nav_start_date["date"],
#         }
#
#
# def get_latest_weekday(day):
#     if day.weekday() == 5:
#         return day - relativedelta(days=1)
#     elif day.weekday() == 6:
#         return day - relativedelta(days=2)
#     else:
#         return day

# def get_rolling(nav_data, start_date, years):
#     rolling_returns = []
#     # if date.today() - relativedelta(years=years) < start_date:
#     #     return {"error": "Invalid Start Date"}
#     # elif start_date < nav_data[-1]["date"]:
#     #     return {"error": "Invalid Start Date"}
#
#
#     nav_start = nav_data[i]["nav"]
#     nav_end =
