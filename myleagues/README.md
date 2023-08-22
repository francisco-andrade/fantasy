# sleeper-transactions
Sleeper data to csv container

## Docker build command
`docker build -t franciscoandrade/sleeper-pr -f Dockerfile .`

## Docker run example
`docker run -ti --name sleeper-data -ti --rm --net=host franciscoandrade/sleeper-pr -o users -i $LEAGUE_ID`
`docker run -ti --name sleeper-data -ti --rm --net=host franciscoandrade/sleeper-pr -o power -w 17`
`docker run -ti --name sleeper-data -ti --rm --net=host franciscoandrade/sleeper-pr -o power -w 15 -i $LEAGUE_ID`

## Docker run example with ssh bash
`docker run -ti --entrypoint bash --name sleeper-data -v /tmp/docker:/tmp/data/ -ti --rm --net=host franciscoandrade/sleeper-pr`

Comandos:
```
# Gerar power ranking semanal
./power_rank.sh -o power -w 5
```

Dependencias:
```
- Python 2.7
- Python modules:
  - sys
  - json
  - argparse
```