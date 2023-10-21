#!/bin/sh
echo "Starting"
uvicorn main:app --reload --port "$UVICORN_PORT" --host "$UVICORN_HOST"