# sleeper-transactions
Sleeper data to csv container

## Docker build command
`docker build -t franciscoandrade/sleeper-powerranking -f Dockerfile .`

## Docker run example
`docker run -ti --name sleeper-data -ti --rm --net=host franciscoandrade/sleeper-powerranking  /root/sleeper/sleeper_data.py --league_id 792189515207925760 --week 1 --debug true`

## Docker run example with ssh bash
`docker run -ti --entrypoint bash --name sleeper-data -ti --rm --net=host franciscoandrade/sleeper-powerranking`
