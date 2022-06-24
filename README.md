# Chess.com Library Exporter

A command line utility that uses Selenium (Chess.com please improve API support!) to help you download your entire archive of games in `chess.com/library`.


## Usage

**Directly as a script:**

```bash
$ git clone https://github.com/manuelpepe/ChessComLibraryExporter
$ cd ChessComLibraryExporter
$ pip install -r requirements.txt
$ python chess_library_exporter.py -o ~/chess-library
Username: manuelpepe
Password: 

Found 6 collections
...
```

**From the Pip-installed entrypoint:**

```bash
$ pip install ChessComLibraryExport
$ chess_library_exporter -o ~/chess-library
Username: manuelpepe
Password: 

Found 6 collections
...
```


## Support

Firefox and Chrome are supported (use `-b firefox` or `-b chrome`, defaults to firefox). Headless mode can also be activated with the `-H` flag (Only seems to work on firefox).