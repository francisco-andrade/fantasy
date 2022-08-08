# sleeper-transactions
Sleeper data to csv container

## Docker build command
`docker build -t franciscoandrade/sleeper-draft -f Dockerfile .`

## Docker run example
`docker run -ti --name sleeper-data -ti --rm --net=host franciscoandrade/sleeper-draft -n ncaa -y 2022 -d 827718472812326913`

## Docker run example with ssh bash
`docker run -ti --entrypoint bash --name sleeper-data -v /tmp/docker:/tmp/data/ -ti --rm --net=host franciscoandrade/sleeper-draft`
