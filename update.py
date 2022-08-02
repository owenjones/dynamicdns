# DynamicDNS
# Reads current IP address from Home Assistant and then updates DNS records held by DigitalOcean.

from pathlib import Path
import yaml
import requests
import digitalocean

if Path("config.yml").is_file():
    with open("config.yml", "r") as f:
        config = yaml.safe_load(f)

else:
    print("Configuration file doesn't exist")
    exit(1)

try:
    url = config["homeassistant"]["url"]
    sensor = config["homeassistant"]["sensor"]

    request = requests.get(
        f"{ url }/api/states/sensor.{ sensor }",
        headers={
            "Authorization": "Bearer " + config["homeassistant"]["token"],
            "content-type": "application/json",
        },
    )

except Exception as e:
    print(f"Problem calling Home Assistant API: { e }")
    exit(1)

else:
    json = request.json()
    ip = json["state"]

if Path("state").is_file():
    with open("state", "r") as f:
        last = f.read()
        if ip == last:
            print("IP address hasn't changed, exiting")
            exit(0)

print("IP address has changed, updating DNS records")

for set in config["digitalocean"]["domains"]:
    domain = config["digitalocean"]["domains"][set]
    api = digitalocean.Domain(
        token=config["digitalocean"]["token"], name=domain["domain"]
    )
    records = api.get_records()

    for record in records:
        if record.name in domain["records"]:
            record.data = ip
            record.save()

with open("state", "w") as state:
    state.write(ip)

print("DNS records updated")
exit(0)
