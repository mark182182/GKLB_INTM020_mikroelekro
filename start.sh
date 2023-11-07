#!/bin/bash

host=$1

pythonBin="../bin/python"
pipBin="../bin/pip"
flaskBin="../bin/flask"

function checkIfExists {
  bin=$1
  if [[ $(test -f $bin && echo 1 || echo 0) == 0 ]]; then
    echo "$bin does not exist"
    exit 1
  else
    echo "$bin exists"
  fi
}


echo "------ checking pre-requisite files --------"
checkIfExists $pythonBin
checkIfExists $pipBin
checkIfExists $flaskBin

echo "------ installing pip requirements --------"
$pipBin install -r requirements.txt

echo "------ setting env vars for MySQL --------"

read -p "MYSQL_USERNAME: " mysqlUser
read -sp "MYSQL_PASSWORD: " mysqlPass
echo ""

export MYSQL_USERNAME=$mysqlUser
export MYSQL_PASSWORD=$mysqlPass

echo "------ starting docker container --------"
isMysqlRunning=$(docker ps -f 'name=some-mysql' | grep -o 'some-mysql' | wc -l)
if [[ $isMysqlRunning == 0 ]]; then
  echo "starting container"
  docker run --name some-mysql -p 3306:3306 -p 33060:33060 -e MYSQL_ROOT_PASSWORD=$MYSQL_PASSWORD -d mysql:latest
else
    echo "MySQL is already running"
fi

echo "------ starting webserver --------"
../bin/flask run --host=$host