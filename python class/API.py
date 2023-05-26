import requests
import json
import sqlite3
from win10toast import ToastNotifier

# API
url = 'https://api.nasa.gov/planetary/apod'
params = {
    'api_key': 'zX8z1Pl7ZfCjZJKess156cEdxoPxIMmOtnjjVcBr'
}

# Fetch APOD data from API
response = requests.get(url, params=params)
data = {}
if response.status_code == 200:
    data = response.json()
else:
    print("Failed to fetch APOD data")
    exit()


print(f"Title: {data['title']}")
print(f"Explanation: {data['explanation']}")
print(f"Image URL: {data['url']}")

# Save APOD data to JSON file
with open("apod.json", "w") as f:
    json.dump(data, f)

# Save APOD data to SQLite database
conn = sqlite3.connect("apod.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS apod (
    id INTEGER PRIMARY KEY,
    title TEXT,
    explanation TEXT,
    image_url TEXT
)
""")
c.execute("INSERT INTO apod (title, explanation, image_url) VALUES (?, ?, ?)", (
    data["title"],
    data["explanation"],
    data["url"]
))
conn.commit()
conn.close()

# desktop notification
toaster = ToastNotifier()
toaster.show_toast(data["title"], data["explanation"])
