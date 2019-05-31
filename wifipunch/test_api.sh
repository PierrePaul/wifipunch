#!/bin/sh
host=$1
if [ "x_$host" = "x_" ]; then
    host="localhost:5000"
fi
get="http -b GET $host"
post="http -b POST $host"

commands=$(echo "
# Testing User API
$get/user
$post/user username=test
$post/user username=test
$get/user/test

# Testing Link API
$get/link
$post/link username=test
$post/link mac_address=12:23:34:22:65 username=test
$post/link mac_address=12:23:34:22:65 username=nobody

# Testing Mac API
$get/mac
$get/mac/mine

# Testing Log API
$post/mac/log
$get/mac/log

# Testing reporting
$get/report
"|grep -v -e '^#' -e '^ *$')

oIFS=$IFS
nIFS=$'\n'
IFS=$nIFS
for com in $commands; do
	IFS=$oIFS
	echo "// $com"
	$com
done
