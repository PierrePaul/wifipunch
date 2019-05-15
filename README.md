# WifiPunch

## Dependencies

- for building: docker, docker-compose, envsubst
- for the code: see wifipunch/requirements.txt

## Docker

a script `docker.sh` wraps docker compose so it can pass $INTERFACE and $SUBNET
to compose. Those variables may change depending on the setup, they specify over
which network interface to bridge with and on what subnet.

### Build

- `./docker.sh build`: this will build the wifipunch container

### Run

- `./docker.sh up`: this runs the db container and wifipunch
