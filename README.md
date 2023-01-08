# keyring_configparser

A ConfigParser subclass that can read configuration values stored with the [keyring pypi package](https://pypi.org/project/keyring/).

## Installation

`pip install keyring_configparser`

## Usage

### Default Keyring Backend

```python
from keyring_configparser import KeyringConfigParser

config = KeyringConfigParser()
config.read("/tmp/app.config")
config.get('EXAMPLE_SECTION', 'non_secret')
> hello world
sec = config.get('EXAMPLE_SECTION', 'some_secret')
> very_secret_value
```

where `/tmp/app.config` is

```
#/tmp/app.config
[EXAMPLE_SECTION]
non_secret = hello world
some_secret = $.
```

and the following has been ran in python

```python
import keyring

keyring.set_password("EXAMPLE_SECTION", "some_secret", "very_secret_value")
```

### Non-Default Keyring Backend

You can pass a configured keyring instance to the KeyringConfigParser constructor.

For example, to use the [`keyrings.cryptfile`](https://pypi.org/project/keyrings.cryptfile/) backend:

```python
from keyring_configparser import KeyringConfigParser
from keyrings.cryptfile.cryptfile import CryptFileKeyring

kr = CryptFileKeyring()
kr.keyring_key = "CRYPTFILE_PASSWORD"

config = KeyringConfigParser(keyring=kr)
config.get('section', 'username')
```