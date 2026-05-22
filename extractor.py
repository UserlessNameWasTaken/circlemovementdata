import requests
import gspread

url = "https://api.waterfallhunt.com/api/state"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) Gecko/20100101 Firefox/151.0",
    "Accept": "*/*" ,
}

response = requests.get(url=url, headers=headers)
data = response.json()



# 1. Setup the connection to Google Sheets
gc = gspread.oauth(
    credentials_filename="client_secret.json",
    authorized_user_filename="authorized_user.json"
)

# 2. Open the specific sheet
sheet = gc.open("Circle Movement and Shrinkage Data").sheet1 

# --- Assume 'data' is the JSON response from your API ---
circles = data.get("circles", [])

# 3. Format data for Google Sheets (List of Lists)
# Each internal list represents one row in the sheet
rows = []
for c in circles:
    rows.append([c.get("lat"), c.get("lon"), c.get("radius_m")])

# 4. Post the data
# append_rows adds multiple rows at once to the bottom of the sheet
sheet.batch_clear(["B2:D10000"])
sheet.update("B2", rows)

print("Data successfully posted!")
