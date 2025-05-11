import requests

url = "https://www.nfl.com/players/tua-tagovailoa/stats/logs/2023/"
res = requests.get(url)
print(f"Status: {res.status_code}")

with open("tua_page.html", "w") as f:
    f.write(res.text)

print("✅ Saved page as tua_page.html")