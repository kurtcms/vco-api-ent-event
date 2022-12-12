# VMware VeloCloud SD-WAN Orchestrator API: Automated Enterprise Events Retrieval for Network SLM, SIEM and SOAR Integration

This Python app is containerised with [Docker Compose](https://docs.docker.com/compose/) for a modular and cloud native deployment that fits in any microservice architecture.

It does the following:

1. Call the [VMware VeloCloud Orchestrator (VCO) API](#reference) to retrieve the enterprise events in the last 15 minutes;
2. Append the enterprise events, with each in a new line, in a JSON file on a `Docker volume` that is mounted in the same directory of the `docker-compose.yml` file on the Docker host, or in the same directory of the Python script if it is run as a standalone service, in a directory by the name of the enterprise; and
3. Repeat the process every 15 minutes on the hour and at :15, :30 and :45 past for an automated enterprise events retrieval.

For a list of the enterprise events along with severity and description, please refer to the [Supported VMware SD-WAN Edge Events](#reference) page in the VMware SD-WAN Documentation.

A detailed walk-through is available [here](https://kurtcms.org/vmware-velocloud-sd-wan-orchestrator-api-automated-enterprise-events-retrieval-for-network-slm-siem-and-soar-integration/).

## Table of Content

- [Getting Started](#getting-started)
  - [Git Clone](#git-clone)
  - [Environment Variable](#environment-variables)
  - [Crontab](#crontab)
  - [Docker Container](#docker-container)
	  - [Docker Compose](#docker-compose)
	  - [Build and Run](#build-and-run)
  - [Standalone Python Script](#standalone-python-script)
    - [Dependencies](#dependencies)
    - [Cron](#cron)
- [Enterprise Event in JSON](#enterprise-event-in-json)
- [Reference](#reference)

## Getting Started

Get started in three simple steps:

1. [Download](#git-clone) a copy of the app;
2. Create the [environment variables](#environment-variables) for the VCO authentication and modify the [crontab](#crontab) if needed; and
3. [Docker Compose](#docker-compose) or [build and run](#build-and-run) the image manually to start the app, or alternatively run the Python script as a standalone service.

### Git Clone

Download a copy of the app with `git clone`.

```shell
$ git clone https://github.com/kurtcms/vco-api-ent-event /app/vco-api-ent-event/
```

### Environment Variables

The app expects the hostname, the API token or the username and password for the VCO, as environment variables in a `.env` file in the same directory.

Should both the API token, and the username and password, for the VCO be present, the app will always use the API token.

Be sure to create the `.env` file.

```shell
$ nano /app/vco-api-ent-event/.env
```

And define the credentials accordingly.

```
VCO_HOSTNAME = 'vco.managed-sdwan.com/'

# Either the API token
VCO_TOKEN = '(redacted)'

# Or the username and password
VCO_USERNAME = 'kurtcms'
VCO_PASSWORD = '(redacted)'
```

### Crontab

By default the app is scheduled with [cron](https://linux.die.net/man/8/cron) to retrieve the enterprise events every 15 minutes, with `stdout` and `stderr` redirected to the main process for `Docker logs`.

Modify the `crontab` if a different schedule is required.

```shell
$ nano /app/vco-api-ent-event/crontab
```

### Docker Container

Packaged as a container, the app is a standalone, executable package that may be run on Docker Engine. Be sure to have [Docker](https://docs.docker.com/engine/install/) installed.

#### Docker Compose

With Docker Compose, the app may be provisioned with a single command.

Install [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/) with the [Bash](https://github.com/gitGNU/gnu_bash) script that comes with app.

```shell
$ chmod +x /app/vco-api-ent-event/docker-compose/docker-compose.sh \
    && /app/vco-api-ent-event/docker-compose/docker-compose.sh
```

Start the containers with Docker Compose.

```shell
$ docker-compose up -d
```

Stopping the container is as simple as a single command.

```shell
$ docker-compose down
```

#### Build and Run

Otherwise the Docker image can also be built manually.

```shell
$ docker build -t vco_api_ent_event /app/vco-api-ent-event/
```

Run the image with Docker once it is ready.

```shell
$ docker run -it --rm --name vco_api_ent_event vco_api_ent_event
```

### Standalone Python Script

Alternatively the `vco_api_ent_event.py` script may be deployed as a standalone service.

#### Dependencies

In which case be sure to install the following required libraries for the `vco_api_main.py`:

1. [Requests](https://github.com/psf/requests)
2. [Python-dotenv](https://github.com/theskumar/python-dotenv)
3. [NumPy](https://github.com/numpy/numpy)
4. [pandas](https://github.com/pandas-dev/pandas)

Install them with [`pip3`](https://github.com/pypa/pip):

```shell
$ pip3 install requests python-dotenv numpy pandas
```

#### Cron

The script may then be executed with a task scheduler such as [cron](https://linux.die.net/man/8/cron) that runs it once every 15 minutes for example.

```shell
$ (crontab -l; echo "*/15 * * * * /usr/bin/python3 /app/vco-api-ent-event/vco_api_ent_event.py") | crontab -
```

## Enterprise Event in JSON

The enterprise events will be appended to a JSON file, with each in a new line, on a `Docker volume` that is mounted in the same directory of the `docker-compose.yml` file on the Docker host. If the Python script is run as a standalone service, the JSON file will be in the same directory of the script instead.

```
{"id": 2913202, "eventTime": "2021-10-23T06:48:57.000Z", "event": "VPN_DATACENTER_STATUS", "category": "SYSTEM", "severity": "NOTICE", "message": "Tunnel to [Azure-SIN] - Failed to negotiate child SA IKEv2_I with 13.76.153.194. Error: ERR_IKE_TIMEOUT", "detail": "{\"enterpriseLogicalId\": \"24676352-23ed-4cdd-a0db-52f61810de1b\", \"dataCenterLogicalId\": \"bb395d4c-5963-4d14-8e6d-c2822c9dfadc\", \"ipAddress\": \"13.76.153.194\", \"ikeState\": \"DOWN\", \"numberP2SA\": 0, \"Hint\": \"No response from peer or no proposal chosen; check VPN type, GWIP, DH Group, IKE-ID, subnets.\"}", "enterpriseUsername": null, "edgeName": null, "segmentName": null}
```

In any case, the JSON file is stored under a directory by the enterpriseName to ease access.

```
.
└── enterpriseName/
    └── events.json
```

## Reference

- [VMware SD-WAN Orchestrator API v1 Release 4.0.1](https://code.vmware.com/apis/1045/velocloud-sdwan-vco-api)
- [VMware SD-WAN Documentation - Supported VMware SD-WAN Edge Events](https://docs.vmware.com/en/VMware-SD-WAN/4.0/VMware-SD-WAN-by-VeloCloud-Administration-Guide/GUID-0A41BC6A-5D8D-412A-BB87-A6B782997574.html)