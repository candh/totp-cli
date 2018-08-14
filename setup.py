from setuptools import setup
import sys
import os

if sys.version_info.major < 3:
  raise Exception("python3 is required to run this script")

# also cleanup the info.json file before building
if os.path.exists('totpauth/database/info.json'):
  os.remove('totpauth/database/info.json')
open('totpauth/database/info.json', 'w')

setup(
  name='totp-cli',
  version='1.0',
  description='A CLI tool to generate Time-Based One Time Passwords (TOTP)',
  author='Haider Ali Khichi',
  author_email='khichihaider@gmail.com',
  license='MIT',
  url='https://github.com/candh/totp-cli',
  keywords='totp otp 2fa cli tools two factor authentication google authenticator',
  install_requires=['termcolor', 'tinydb', 'keyring', 'pyotp'],
  packages=['totpauth'],
  entry_points = {
    'console_scripts': [
      'totp=totpauth.totp:main'
    ]
  },
  package_data = {
    'totpauth': ['database/info.json']
  },
  classifiers = [
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Topic :: Security',
    'Topic :: Security :: Cryptography'
  ]
)