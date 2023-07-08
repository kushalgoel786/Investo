import httpx
from datetime import datetime


async def fetch_scheme_data(scheme_code):
    base_url = "https://api.mfapi.in/mf/"

    if not scheme_code.isdigit() or len(scheme_code) != 6:
        return {"error": "Invalid Scheme ID"}

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

            del response_data["status"]

            return response_data

    except httpx.RequestError as e:
        return {"error": "Http Request Error"}

    except httpx.HTTPStatusError as e:
        return {"error": "Http Status Error"}

