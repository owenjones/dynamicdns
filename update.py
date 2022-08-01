# DynamicDNS
# Reads current IP address from Home Assistant and then updates DNS records held by DigitalOcean.

# TODO:
# - add logging to this
# - use better path library

import os.path
import yaml
import requests
import digitalocean

with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

try:
    url = config["homeassistant"]["url"]
    sensor = config["homeassistant"]["sensor"]

    ro = requests.get(
        f"{ url }/api/states/sensor.{ sensor }",
        headers={
            "Authorization": "Bearer " + config["homeassistant"]["token"],
            "content-type": "application/json",
        },
    )

except:
    exit(0)

else:
    json = ro.json()
    ip = json["state"]

if os.path.isfile("state"):
    with open("state", "r") as f:
        last = f.read()
        if ip == last:
            exit(0)


for set in config["digitalocean"]["domains"]:
    domain = config["digitalocean"]["domains"][set]
    do = digitalocean.Domain(
        token=config["digitalocean"]["token"], name=domain["domain"]
    )
    rec = do.get_records()

    for r in rec:
        if r.name in domain["records"]:
            r.data = ip
            r.save()

with open("state", "w") as ipcheck:
    ipcheck.write(ip)

exit(0)
