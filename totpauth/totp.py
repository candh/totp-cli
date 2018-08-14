#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# MIT License
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from termcolor import cprint, colored
from tinydb import TinyDB, Query
import keyring
import pyotp
import time
import sys
import os

DATABASE_NAME = "info.json"
DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "database", DATABASE_NAME)
SERVICE_NAME = "totp-cli"


def help():
    """Display a small help guide"""
    help_str = """
    TOTP-cli. Generates TOTP from given secret
    usage: totp [COMMAND]
    and then follow instructions

    commands:
    - add (add secret to the keyring) 
    - show (show all the accounts)
    - get (generate TOTP of a account)
    - help (this)
  """
    print(help_str)


def clean_exit(func):
    def wrapper():
        try:
            func()
        except KeyboardInterrupt:
            sys.exit(0)

    return wrapper


@clean_exit
def add():
    """Ask for info and add secret to the system keyring"""
    # ask for secret key
    secret = str(input(colored("Enter secret: ", "red"))).strip()
    # clean it up a little
    secret = secret.replace(" ", "")
    name = str(input(colored("Enter name: ", "yellow"))).strip()
    issuer = str(input(colored("Enter issuer: ", "green"))).strip()
    email = str(input(colored("Enter email: ", "green"))).strip()

    # adding that to the keyring
    try:
        keyring.set_password(SERVICE_NAME, name, secret)
    except:
        print("Couldn't add secret to the keyring")

    # adding name, issuer and email to database for lookup
    with TinyDB(DATABASE) as db:
        db.insert({"name": name, "issuer": issuer, "email": email})


@clean_exit
def show():
    """Show all the available accounts"""
    with TinyDB(DATABASE) as db:
        for account in db:
            cprint(account.get("name"), "yellow")
            cprint("Issuer: ", "green", end="")
            print(account.get("issuer"))
            cprint("Email: ", "green", end="")
            print(account.get("email"))
            print()


@clean_exit
def get():
    """Get the secret for TOTP generation"""
    account = Query()
    name = str(input(colored("Enter name: ", "yellow"))).strip()

    with TinyDB(DATABASE) as db:
        result = db.search(account.name == name)
        if result:
            result = result[0]
            name = result.get("name")
            cprint(name, "yellow")
            issuer = result.get("issuer")
            cprint(issuer, "green")
            print()

            # get the secret from keychain
            try:
                secret = keyring.get_password(SERVICE_NAME, name)
            except:
                print("Couldn't find key from keyring")
                sys.exit()

            # the totp object
            totp = pyotp.TOTP(secret)

            while True:
                try:
                    time_elapsed = int(time.time()) % 30
                    now = str(totp.now())
                    print(
                        "\r[{}]  {} {}".format(
                            str(time_elapsed).zfill(2), now[:3], now[3:]
                        ),
                        end="",
                    )
                    time.sleep(1)
                    sys.stdout.flush()
                except KeyboardInterrupt:
                    print("\r[--]  --- ---  ")
                    sys.exit(0)

        else:
            cprint("No such account. Please run `show` to be sure.", "red")


def get_option(script="", option="help"):
    """arg parsing helper"""
    return option


def main():
    option = get_option(*sys.argv)

    if option == "help":
        help()
    elif option == "add":
        add()
    elif option == "show":
        show()
    elif option == "get":
        get()
    else:
        help()


if __name__ == "__main__":
    # for testing
    main()
