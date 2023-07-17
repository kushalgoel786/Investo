from datetime import date
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app import service

app = FastAPI()


@app.get("/mf/{scheme_code}")
async def get_scheme_data(scheme_code: str):
    return await service.get_scheme_data(scheme_code)


@app.get("/mf/{scheme_code}/nav")
async def get_nav(scheme_code: str, on: date = date.today()):
    return await service.get_nav(scheme_code, on)


@app.get("/mf/{scheme_code}/nav/history")
async def get_nav_history(scheme_code: str):
    return await service.get_nav_history(scheme_code)


@app.get("/mf/{scheme_code}/returns")
async def get_returns(scheme_code: str, start: date, end: date = date.today()):
    return await service.get_returns(scheme_code, start, end)


@app.get("/mf/{scheme_code}/returns/yearly")
async def get_yearly_returns(scheme_code: str):
    return await service.get_yearly_returns(scheme_code)


@app.get("/mf/{scheme_code}/returns/cagr")
async def get_cagr(scheme_code: str, years: int):
    return await service.get_cagr(scheme_code, years)

app.mount("/", StaticFiles(directory="static", html=True))  # , name="home")


# get abs return for x years
# @app.get("/mf/{scheme_code}/absolute")
# async def get_absolute(scheme_code: str, years: int):
#     data = await client.fetch_scheme_data(scheme_code)
#     if "error" not in data.keys():
#         nav_data = data["data"]
#         return master.get_absolute(nav_data, years)

