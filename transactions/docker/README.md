# sleeper-transactions
Sleeper data to csv container

## Docker build command
`docker build -t franciscoandrade/sleeper-data -f Dockerfile .`

## Docker run example
`docker run -ti --name sleeper-data -ti --rm --net=host franciscoandrade/sleeper-data -o transactions -l 840062462177955840 -w 1`

## Docker run example with ssh bash
`docker run -ti --entrypoint bash --name sleeper-data -ti --rm --net=host franciscoandrade/sleeper-data`
