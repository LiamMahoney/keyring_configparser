# keyring_interpolation

A [configparser.Interpolation][https://docs.python.org/3/library/configparser.html#interpolation-of-values] subclass that configures ConfigParser instances to read values from a system's keyring via the [keyring pypi package](https://pypi.org/project/keyring/).

## Installation

`pip install keyring_interpolation`

## Usage

```python
from keyring_interpolation import KeyringInterpolation

config = configparser.ConfigParser(interpolation=KeyringInterpolation())
config.read("/tmp/app.config")
non_sec = config.get('SECTION_1', 'value1')
sec = config.get('SECRET_SECTION', 'some_secret')
```

where `/tmp/app.config` is

```
#/tmp/app.config
[SECTION_1]
value1 = hello world

[SECRET_SECTION]
some_secret = $.
not_set_secret = $.
```

and the following has been ran in python

```python
import keyring

keyring.set_password("SECRET_SECTION", "some_secret", "very_secret_value")
```