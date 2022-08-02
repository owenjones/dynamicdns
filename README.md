# DynamicDNS
Fetches the current IP address from a Home Assistant sensor, and updates DNS records held by DigitalOcean with it.

## Setup
Copy `config.yml` and `ddns.service` files.

Add Home Assistant URL, API token, and sensor name (from `sensor.{name}`).

Add DigitalOcean API token and DNS records in the form:
```
{reference}:
  domain: {domain}
  records:
    - {record 1}
    - {record 2}
    - etc
```
