from datetime import date
from fastapi import FastAPI
from app import client
from app import master

app = FastAPI()


@app.get("/")
async def root():
    return "API is Live"


@app.get("/mf/{scheme_code}")
async def get_scheme_data(scheme_code: str):
    data = await client.fetch_scheme_data(scheme_code)
    if "error" not in data.keys():
        return data["meta"]
    else:
        return data


@app.get("/mf/{scheme_code}/nav_history")
async def get_nav_history(scheme_code: str):
    data = await client.fetch_scheme_data(scheme_code)
    if "error" not in data.keys():
        return data["data"]
    else:
        return data


@app.get("/mf/{scheme_code}/nav")
async def get_nav(scheme_code: str, on: date = date.today()):
    data = await client.fetch_scheme_data(scheme_code)
    if "error" not in data.keys():
        nav_data = data["data"]
        nav = master.get_nav_on(nav_data, on)
        return nav
    else:
        return data


@app.get("/mf/{scheme_code}/returns")
async def get_absolute_returns(scheme_code: str, start: date, end: date = date.today()):
    data = await client.fetch_scheme_data(scheme_code)
    if "error" not in data.keys():
        nav_data = data["data"]
        return master.get_returns(nav_data, start, end)


@app.get("/mf/{scheme_code}/absolute")
async def get_absolute(scheme_code: str, years: int):
    data = await client.fetch_scheme_data(scheme_code)
    if "error" not in data.keys():
        nav_data = data["data"]
        return master.get_absolute(nav_data, years)


@app.get("/mf/{scheme_code}/cagr")
async def get_cagr(scheme_code: str, years: int):
    data = await client.fetch_scheme_data(scheme_code)
    if "error" not in data.keys():
        nav_data = data["data"]
        return master.get_cagr(nav_data, years)

# TODO
# List of all schemes
# error handling
# enumerate
# formatting
# numpy, pandas, matplotlib, flask or django
