#! /usr/bin/env sh

export PYTHONPATH="${PYTHONPATH}:/app"

uvicorn src.api_main:app --reload --host 0.0.0.0 --port 8000
