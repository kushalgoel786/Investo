from datetime import date, datetime
import httpx
from fastapi import FastAPI
from dateutil.relativedelta import relativedelta

app = FastAPI()


async def fetch_scheme_data(scheme_code):
    base_url = "https://api.mfapi.in/mf/"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(base_url + scheme_code)
            response.raise_for_status()
            response_data = response.json()

            if len(response_data["meta"]) == 0:
                return {"error": "Scheme ID Not Found"}

            if not response_data["status"] == "SUCCESS":
                return {"error": "Failure in Fetching Data"}

            for item in response_data["data"]:
                item["nav"] = float(item["nav"])
                item["date"] = datetime.strptime(item["date"], "%d-%m-%Y").date()

            return response_data

    except httpx.RequestError as e:
        return {"error": "Http Request Error"}

    except httpx.HTTPStatusError as e:
        return {"error": "Http Status Error"}


def get_nav_on(nav_data, target_date):
    # For Weekends, return the NAV of Friday
    target_date = get_latest_weekday(target_date)

    # For dates that do not exist, return None
    if target_date > nav_data[0]["date"]:
        return None
    elif target_date < nav_data[-1]["date"]:
        return None

    low = 0
    high = len(nav_data) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_date = nav_data[mid]["date"]

        if mid_date == target_date:
            return nav_data[mid]["nav"]
        elif mid_date > target_date:
            low = mid + 1
        else:
            high = mid - 1

    return None


def get_latest_weekday(day):
    if day.weekday() == 5:
        return day - relativedelta(days=1)
    elif day.weekday() == 6:
        return day - relativedelta(days=2)
    else:
        return day


@app.get("/")
async def root():
    return "Live"


@app.get("/mf/{scheme_code}")
async def get_scheme_data(scheme_code: str):
    data = await fetch_scheme_data(scheme_code)
    if "error" not in data.keys():
        return data["meta"]


@app.get("/mf/{scheme_code}/nav_history")
async def get_nav_history(scheme_code: str):
    data = await fetch_scheme_data(scheme_code)
    if "error" not in data.keys():
        return data["data"]


@app.get("/mf/{scheme_code}/nav")
async def get_nav(scheme_code: str, on: date = date.today()):
    data = await fetch_scheme_data(scheme_code)
    if "error" not in data.keys():
        nav_data = data["data"]
        nav = get_nav_on(nav_data, on)
        if nav:
            return nav
        else:
            return {"error": "NAV not found"}


@app.get("/mf/{scheme_code}/absolute_returns")
async def get_absolute_returns(scheme_code: str, start: date, end: date = date.today()):
    if end < start:
        return {"error": "End date cannot be less than start date"}

    data = await fetch_scheme_data(scheme_code)

    if "error" not in data.keys():
        nav_data = data["data"]
        nav_on_start_date = await get_nav_on(nav_data, start)
        nav_on_end_date = await get_nav_on(nav_data, end)
        if nav_on_end_date and nav_on_start_date:
            return ((nav_on_end_date / nav_on_start_date) - 1) * 100


@app.get("/mf/{scheme_code}/cagr")
async def get_cagr(scheme_code, years: int):
    data = await fetch_scheme_data(scheme_code)

    if "error" not in data.keys():
        nav_data = data["data"]
        end_date = get_latest_weekday(date.today())
        start_date = end_date - relativedelta(years=years)
        nav_on_start_date = get_nav_on(nav_data, start_date)
        nav_on_end_date = get_nav_on(nav_data, end_date)
        if nav_on_end_date and nav_on_start_date:
            return (((nav_on_end_date/nav_on_start_date) ** (1/years)) - 1) * 100

# TODO
# List of all schemes
# error handling
# enumerate
# formatting
# numpy, pandas, matplotlib, flask or django
