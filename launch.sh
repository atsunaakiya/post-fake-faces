#!/usr/bin/env bash

cd "$(dirname $(dirname $0))"
task=script
timeout 60 /usr/local/bin/docker-compose run --rm $task >> out.log 2>> err.log