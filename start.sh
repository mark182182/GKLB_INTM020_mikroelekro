#!/bin/bash

host=$1

pythonBin="../bin/python"
pipBin="../bin/pip"
flaskBin="../bin/flask"

function checkIfExists {
  local bin=$1
  if [[ $(test -f $bin && echo 1 || echo 0) == 0 ]]; then
    echo "$bin does not exist"
    exit 1
  else
    echo "$bin exists"
  fi
}

function check_if_env_var_exists {
  local envVar=$1
  if [[ -z $(grep -o $envVar .env) ]]; then
    echo "Environment variable '$envVar' is not defined!"
    exit 1
  fi
}


echo "------ checking pre-requisite files --------"
checkIfExists $pythonBin
checkIfExists $pipBin
checkIfExists $flaskBin

echo "------ installing pip requirements --------"
$pipBin install -r requirements.txt

echo "------ exporting env vars --------"

if [[ -f ".env" ]]; then
  check_if_env_var_exists MYSQL_USERNAME
  check_if_env_var_exists MYSQL_PASSWORD
  check_if_env_var_exists SMTP_USER
  check_if_env_var_exists SMTP_PASSWORD
  check_if_env_var_exists FROM_ADDRESS
  check_if_env_var_exists TO_ADDRESS

  envVars="$(cat .env)"
  for envVar in $envVars;
  do
    eval "export $envVar"
  done
else
  echo "Mandatory file .env does not exist!"
  exit 1
fi

echo "------ starting docker container --------"
mysqlContainer=$(docker ps -a -f 'name=some-mysql')
if [[ -n $mysqlContainer ]]; then
  if [[ $(echo $mysqlContainer | grep -o 'Exited') ]]; then
    echo "starting stopped container"
    docker start some-mysql
  else
    echo "MySQL is already running"
  fi
else
    echo "creating container"
    docker run --name some-mysql -p 3306:3306 -p 33060:33060 -e MYSQL_ROOT_PASSWORD=$MYSQL_PASSWORD -d mysql:latest
fi

echo "------ starting webserver --------"
../bin/flask run --host=$host