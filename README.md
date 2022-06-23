# Chess.com Library Exporter

A command line utility that uses Selenium (Chess.com please improve API support!) to help you download your entire archive of games in `chess.com/library`.

## Support

Currently, the utility only supports the Chrome selenium driver, but that could be easily extended to other browsers.

## Usage

Due to Chess.com not exposing an API to retrieve games from Library, we are forced into using Selenium. This means that you must have a valid browser driver installed (see [Support](#support))

For info on drivers, [see this](https://selenium-python.readthedocs.io/installation.html#drivers).

With a valid driver installed and in your PATH, just run the utility and complete the Username and Password prompts.


```bash
$ python exporter.py
Username: manuelpepe
Password: 

Found 6 collections
...
````