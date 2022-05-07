[THE CONTENT OF THE TASK](https://github.com/MatSkot/StavaRT/raw/master/Python-routing.pdf)

# GeoDistance Calculator

Simple app that allow to calculate summary distance of path created up to 50 geo points.

## Installation

Instal requirements

```bash
pip install -r requirements.txt
```

Copy env_example as .env and update configurtion variables

```bash
cp env_example .env
```

## Runing

run aplication with run.sh script

```
./run.sh
```

application is listening on 9002 port,
during startup application will create database table to collect statistics

## Usage

[Live documentation](http://localhost:9002/docs)
[Web interface](http://localhost:9002/)
[API](http://localhost:9002/api)






