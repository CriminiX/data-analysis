#!/bin/bash
mkdir -p ./temp/dags ./temp/logs ./temp/plugins
bash ./scripts/deploy_to_airflow.sh
sudo docker compose up -d