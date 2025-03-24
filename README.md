# Map Generator

[![GHA workflow badge](https://github.com/hojott/mapgenerator/workflows/CI/badge.svg)](https://github.com/hojott/mapgenerator/actions)
[![codecov](https://codecov.io/github/hojott/mapgenerator/graph/badge.svg?token=0N6B3YYDJ7)](https://codecov.io/github/hojott/mapgenerator)

Map generator with Fortune's algorithm at it's core

## Running
```
python -m mapgenerator
```

## Testing
```
poetry run coverage run --branch -m pytest

poetry run coverage html

poetry run pylint mapgenerator
```
