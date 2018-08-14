# totp-cli
A simple utility to help store secrets in keyring and generate TOTPs based on those secrets.
[Read here](https://en.wikipedia.org/wiki/One-time_password)

Basically does what the Google Authenticator app does on the phone. Except you look much cooler and also helpful when you don't have your phone.

[![asciicast](https://asciinema.org/a/J97WpvLhG00ekGjEOhUDUqedW.png)](https://asciinema.org/a/J97WpvLhG00ekGjEOhUDUqedW)

# Installation
pip installation coming soon once i register the package. For now you could just run setup.py.

# Usage
Get secrets from 2FA settings page of the website that you're trying to add.

Choose any of these options
```bash
$ totp [add, show, get, help]
```
and then follow instructions.

# Security
All the secrets are stored in system keyring so they remain safe.
Information like name, issuer and email are stored in plaintext locally. Name is used for look up in the keyring. Email and Issuer are only there to help you distinguish.

# Notes
Tested with facebook & bitbucket.
Tested only on MacOS. Should work on other platforms too..