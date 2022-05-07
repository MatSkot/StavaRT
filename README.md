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

```bash
./run.sh
```

application is listening on 9002 port,
during startup application will create database table to collect statistics

## Usage

[Live documentation](http://localhost:9002/docs)

[Web interface](http://localhost:9002/)

Allow to create path on map, double click on last point on map will save path to calculation. Max length of path: 50 points

[API](http://localhost:9002/api/calc_distance)

Calculates distance between two geo points. Path must be between 2 and 50 geo points. Each point should contain valid latitude and longitude. eturns start and finish times, partial distance between consecutive points and total distance between all points.

### example request:

```
{
  "geo_path": [
    {
      "latitude": 12.5675,
      "longitude": 50.234534
    },
    {
      "latitude": 14.1375,
      "longitude": 51.200534
    }
  ],
  "request_id": "123"
}
```

### example response:

```
{
  "status": "ok",
  "request": {
    "geo_path": [
      {
        "latitude": 12.5675,
        "longitude": 50.234534
      },
      {
        "latitude": 14.1375,
        "longitude": 51.200534
      }
    ],
    "request_id": "123"
  },
  "distances": [
    263229.3166097935
  ],
  "start_time": "2022-05-07T19:33:47.655576+00:00",
  "finish_time": "2022-05-07T19:33:48.284631",
  "total_distance": 263229.3166097935
}
```






