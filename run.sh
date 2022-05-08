#!/bin/sh

gunicorn -k uvicorn.workers.UvicornWorker app.main:app -b :9002
