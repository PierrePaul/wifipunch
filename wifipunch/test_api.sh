#!/bin/sh -x
host=$1
if [ "x_$host" = "x_" ]; then
    host="localhost:5000"
fi

# Testing User API
http GET $host/user
http POST $host/user username=test
http POST $host/user username=test
http GET $host/user/test

# Testing Link API
http GET $host/link
http POST $host/link username=test
http POST $host/link mac_address=12:23:34:22:65 username=test
http POST $host/link mac_address=12:23:34:22:65 username=nobody

# Testing Mac API
http GET $host/mac
http GET $host/mac/mine

# Testing Log API
http POST $host/mac/log
http GET $host/mac/log
