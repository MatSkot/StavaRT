#!/bin/sh

uvicorn --reload app.main:app --host 0.0.0.0 --port 9002 --log-level debug --no-access-log
