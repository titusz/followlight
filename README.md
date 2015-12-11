# followlight

Drive a DotStar LED strip from LIDAR Lite distance measurements connected via
2 Wipy´s and a hub (Raspberry PI)

**WORK IN PROGRESS**

## Getting started

- make sure you are on python 3.4+
- clone this repository
- pip install -r requirements.txt
- create a invoke.yaml configuration (see invoke.sample)
- deploy to sensor and actor Wipy devices with `invoke lidar deploy` and `invoke dotstar deploy`
