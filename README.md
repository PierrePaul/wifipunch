# WifiPunch

## Dependencies

- for building: docker, docker-compose
- for the code: see wifipunch/requirements.txt

## Docker

Configure the environment variables:

- `INTERFACE`: the network interface the container will bind on
- `SUBNET`: the subnet the container will be connected to
- `FLASK_ENV`: `production` or `development`

### Build

- `docker-compose build`: this will build the wifipunch container

### Run

- `docker-compose up`: this runs the db container and wifipunch
