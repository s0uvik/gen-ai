#!/bin/bash

export $(grep -v '^#' .env | xargs -d '\n') 
uv run rq worker --with-scheduler --worker-class rq.worker.SimpleWorker