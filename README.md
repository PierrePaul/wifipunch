# WifiPunch

`git clone --recurse-submodules  git@git.fixrs.ca:evolvingweb/wifipunch.git`

## Dependencies

- for building: docker, docker-compose
- for the code: see wifipunch/requirements.txt

## Database

- `docker-compose exec wifipunch flask db migrate`
- `docker-compose exec wifipunch flask db update`

## API

- testing the API: `./test_api.sh [<IP:port (default: localhost)>]`

## Docker

Configure the environment variables (see .env, dev.env.fish, pi.env.fish):

- `INTERFACE`: the network interface the container will bind on
- `IP_ADDR`: force assign an IP Address to the container
- `SUBNET`: the subnet the container will be connected to
- `GATEWAY`: gateway the container should use to communicate with the network
- `FLASK_ENV`: `production` or `development`
- `VOLUME_PATH`: set to `""` if deploying remotely, or `./` if using locally

### Build

- `docker-compose build`: this will build the wifipunch container

### Run

- `docker-compose up`: this runs the db container and wifipunch

### Deploy to a remote RPi

- set `DOCKER_HOST` to `ssh://<user>@<rpi IP>`
- run `docker-compose up -d`
