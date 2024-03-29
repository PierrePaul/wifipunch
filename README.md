# WifiPunch

`git clone --recurse-submodules git@github.com:PierrePaul/wifipunch.git`

## Dependencies

- for building: docker, docker-compose
- for the code: see wifipunch/requirements.txt

## Database

- `docker-compose exec wifipunch flask db migrate`
- `docker-compose exec wifipunch flask db update`

## API

- testing the API: `./test_api.sh [<IP:port (default: localhost)>]`

## ENV file

Copy one of the following file, depending on your shell : 

- `.env.sample` to `.env` if you are using bash
- `dev.env.fish` to `.env` if you are using fish

This file will be automatically loaded by `docker-composer` when you start the services.

There is also a `pi.env.fish` if you are deploying to a remote docker host.

## Docker

Configure the environment variables (see .env, dev.env.fish, pi.env.fish):

- `INTERFACE`: the network interface the container will bind on
- `IP_ADDR`: force assign an IP Address to the container
- `SUBNET`: the subnet the container will be connected to
- `GATEWAY`: gateway the container should use to communicate with the network
- `FLASK_ENV`: `production` or `development`
- `VOLUME_PATH`: set to `""` if deploying remotely, or `./` if using locally
- `SENDGRID_API_KEY`: Sendgrid API Key
- `FROM_EMAIL`: email to send from
- `TO_EMAIL`: email to send from
- `WIFIPUNCH_API_KEY`: api key to accept for sending reports

### Build

- `docker-compose build`: this will build the wifipunch container

### Run

- `docker-compose up`: this runs the db container and wifipunch

### Deploy to a remote RPi

- set `DOCKER_HOST` to `ssh://<user>@<rpi IP>`
- run `docker-compose up -d`
- create crons:
  - to send reports, ie `0 2 * * * http 172.16.238.3:5000/reports api_key=SomethingReallyCustom`
  - to scan the network, ie `0 2 * * * http post 172.16.238.3:5000/mac/log`


### Troubleshooting

- if the container cannot access internet (ie: can't send emails), it could be due to the `$GATEWAY` improperly set. To verify run `docker-compose exec wifipunch ip ro` and check that it matches. If not, you will have to `docker-compose down`, source the variable file and call `up` again.
