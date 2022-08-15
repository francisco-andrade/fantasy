# sleeper-transactions
Sleeper data to csv container

## Docker build command
`docker build -t franciscoandrade/sleeper-transactions -f Dockerfile .`

## Docker run example
`docker run -ti --name sleeper-data -ti --rm --net=host franciscoandrade/sleeper-transactions  /root/sleeper/sleeper_data.py --league_id 840062462177955840 --week 1 --debug false`

## Docker run example with ssh bash
`docker run -ti --entrypoint bash --name sleeper-data -ti --rm --net=host franciscoandrade/sleeper-transactions`
