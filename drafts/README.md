# sleeper-transactions
Sleeper data to csv container

## Docker build command
`docker build -t franciscoandrade/sleeper-draft -f Dockerfile .`

## Docker run example
`docker run -ti --name sleeper-data -ti --rm --net=host franciscoandrade/sleeper-draft -n fanbol -y 2024 -d 1065805259894792193`

## Docker run example with ssh bash
`docker run -ti --entrypoint bash --name sleeper-data -v /tmp/docker:/tmp/data/ -ti --rm --net=host franciscoandrade/sleeper-draft`



# STEP-BY-STEP
$ curl "https://api.sleeper.app/v1/players/nfl" > ./data/players.json

$ docker build -t franciscoandrade/sleeper-draft -f Dockerfile .

$ docker run -ti --entrypoint bash --name sleeper-data -v /tmp/docker:/tmp/data/ -ti --rm --net=host franciscoandrade/sleeper-draft

$ docker exec -ti sleeper-data python /root/sleeper/sleeper_parser.py --file /root/sleeper/data/players.json --option players > ~/Downloads/temp/players.csv

$ docker run -ti --name sleeper-data -ti --rm --net=host franciscoandrade/sleeper-draft -n palmers -y 2026 -d 1343790271325818880
