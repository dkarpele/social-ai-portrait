#!/bin/sh
echo "Waiting for volume $APP_HOME/test_apps/ ..."

while [ ! -d "$APP_HOME"/test_apps/ ]
do
  echo "volume $APP_HOME/test_apps/ is still creating ..."
  sleep 1
done

echo "volume $APP_HOME/test_apps/ created"

pytest -s -v --disable-warnings "$APP_HOME"/test_apps/end_to_end/src
