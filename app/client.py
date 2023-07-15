import httpx
from datetime import datetime
from app.client_error import ClientError


# TODO: Convert to a dictionary?
# TODO: Add missing dates here only?
async def fetch_scheme_data(scheme_code):
    base_url = "https://api.mfapi.in/mf/"

    if not scheme_code.isdigit() or len(scheme_code) != 6:
        raise ClientError("Invalid Scheme ID")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(base_url + scheme_code)
            response.raise_for_status()
            response_data = response.json()

            if len(response_data["meta"]) == 0:
                raise ClientError("Scheme ID Not Found")

            if not response_data["status"] == "SUCCESS":
                raise ClientError("Failure in Fetching Data")

            for item in response_data["data"]:
                item["nav"] = float(item["nav"])
                item["date"] = datetime.strptime(item["date"], "%d-%m-%Y").date()

            del response_data["status"]

            return response_data

    except httpx.RequestError as e:
        raise ClientError("Http Request Error")

    except httpx.HTTPStatusError as e:
        raise ClientError("Http Status Error")

