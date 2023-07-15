import app.client as client
from app.client_error import ClientError
from datetime import date
from app import master
from app.invalid_date_error import InvalidDateError


async def get_scheme_data(scheme_code: str):
    try:
        data = await client.fetch_scheme_data(scheme_code)
        scheme_data = data["meta"]
        return {
            "scheme_code": scheme_data["scheme_code"],
            "scheme_name": scheme_data["scheme_name"]
        }
    except ClientError as e:
        return {"error": e.message}


async def get_nav(scheme_code: str, on: date):
    try:
        data = await client.fetch_scheme_data(scheme_code)
        nav_data = data["data"]
        nav = master.get_nav_on(nav_data, on)
        return nav
    except ClientError as e:
        return {"error": e.message}
    except InvalidDateError as e:
        return {"error": e.message}


async def get_nav_history(scheme_code: str):
    try:
        data = await client.fetch_scheme_data(scheme_code)
        return data["data"]
    except ClientError as e:
        return {"error": e.message}


async def get_returns(scheme_code: str, start: date, end: date = date.today()):
    try:
        data = await client.fetch_scheme_data(scheme_code)
        nav_data = data["data"]
        return master.get_returns(nav_data, start, end)
    except ClientError as e:
        return {"error": e.message}
    except InvalidDateError as e:
        return {"error": e.message}


async def get_yearly_returns(scheme_code: str):
    try:
        data = await client.fetch_scheme_data(scheme_code)
        return master.get_yearly_returns(data["data"])
    except ClientError as e:
        return {"error": e.message}
