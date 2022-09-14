Comandos:
```
# Capturar os dados dos rosters da liga
./sleeper_tool.sh -o rosters -w 1

# Gerar o csv com os dados de matchups
./sleeper_tool.sh -o matchups -w 1
```

## Docker build command
`docker build -t franciscoandrade/sleeper-brasileirao -f Dockerfile .`

## Docker run example
`docker run -ti --name sleeper-data -ti --rm --net=host -v /tmp/docker:/tmp/data/ franciscoandrade/sleeper-brasileirao -f ./data/leagues_2022.txt -o matchups -w 1`

## Docker run example with ssh bash
`docker run -ti --entrypoint bash --name sleeper-data -v /tmp/docker:/tmp/data/ -ti --rm --net=host franciscoandrade/sleeper-brasileirao`

Dependencias:
```
- Python 2.7
- Python modules:
  - sys
  - json
  - argparse
```