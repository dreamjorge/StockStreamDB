#!/bin/bash

if [ "$1" == "windows" ]; then
  export DOCKER_HOST="tcp://localhost:2375"
  echo "Switched to Docker on Windows"
elif [ "$1" == "wsl" ]; then
  export DOCKER_HOST="unix:///var/run/docker.sock"
  echo "Switched to Docker on WSL"
else
  echo "Usage: source switch-docker.sh [windows|wsl]"
fi
