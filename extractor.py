import os
import json
import requests
import gspread


API_URL = "https://api.waterfallhunt.com/api/state"
SPREADSHEET_NAME = "Circle Movement and Shrinkage Data"
TARGET_RANGE = "B2:D10000"


def fetch_circle_data():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) "
            "Gecko/20100101 Firefox/151.0"
        ),
        "Accept": "*/*",
    }

    response = requests.get(API_URL, headers=headers, timeout=30)
    response.raise_for_status()

    return response.json()


def get_google_sheet_client():
    service_account_json = os.environ.get("GCP_SERVICE_ACCOUNT_JSON")

    if not service_account_json:
        raise RuntimeError("Missing GCP_SERVICE_ACCOUNT_JSON environment variable.")

    service_account_info = json.loads(service_account_json)

    return gspread.service_account_from_dict(service_account_info)


def main():
    data = fetch_circle_data()
    circles = data.get("circles", [])

    rows = []
    for c in circles:
        rows.append([
            c.get("lat"),
            c.get("lon"),
            c.get("radius_m"),
        ])

    if not rows:
        print("No circle data found. Sheet was not updated.")
        return

    gc = get_google_sheet_client()
    sheet = gc.open(SPREADSHEET_NAME).sheet1

    sheet.batch_clear([TARGET_RANGE])
    sheet.update("B2", rows)

    print(f"Successfully posted {len(rows)} rows.")


if __name__ == "__main__":
    main()