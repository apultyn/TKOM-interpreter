# README - TKOM 2025L

## Autor

- Andrzej Pultyn
- 325213
- andrzej.pultyn.stud@pw.edu.pl

## Useful commands

- run parser with example input and output files:
```bash
python -m src.parser.main -i src/parser/input/file -o src/parser/output/file.json
```
- run pytest with coverage:
```bash
pytest --cov-report term-missing --cov
```
- run specific unit test with debug:
```bash
pytest <plik>::<nazwa_funkcji> --trace
```
- install `psc` command:
```bash
pip install -e .
```
- uninstall `psc` command:
```bash
pip uninstall pyscript-compiler -y
```
