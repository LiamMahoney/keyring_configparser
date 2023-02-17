# keyring_configparser

[![build](https://github.com/LiamMahoney/keyring_configparser/actions/workflows/python-package.yml/badge.svg)](https://github.com/LiamMahoney/keyring_configparser/actions/workflows/python-package.yml) ![PyPI](https://img.shields.io/pypi/v/keyring-configparser) ![PyPI - Downloads](https://img.shields.io/pypi/dm/keyring-configparser) ![PyPI - License](https://img.shields.io/pypi/l/keyring-configparser)

A ConfigParser subclass that can read values stored with the [keyring pypi package](https://pypi.org/project/keyring/).

## Installation

`pip install keyring_configparser`

## Usage

It is recommended to be familiar with the [ConfigParser](https://docs.python.org/3/library/configparser.html) module and the [keyring](https://pypi.org/project/keyring/) pypi package.

`KeryingConfigParser` is identical to `ConfigParser` except when it reads a specific token as a configuration value (`"$."` by default) it uses the keyring package to resolve the value. This enables using secret values in configuration files without storing the value as plain-text within the file.

### Basic Example

```
#/tmp/app.config
[EXAMPLE_SECTION]
non_secret = hello world
some_secret = $.
```

```python
import keyring

keyring.set_password("EXAMPLE_SECTION", "some_secret", "very_secret_value")
```

```python
from keyring_configparser import KeyringConfigParser

config = KeyringConfigParser()
config.read("/tmp/app.config")
config.get('EXAMPLE_SECTION', 'non_secret')
> "hello world"
sec = config.get('EXAMPLE_SECTION', 'some_secret')
> "very_secret_value"
```

### Additional Examples

#### Configured Keyring Instances

A configured keyring instance can be supplied to the `KeyringConfigParser` constructor. This allows using non-default backends or any other non-default keyring settings when looking up values in keyring.

For example, to use the [`keyrings.cryptfile`](https://pypi.org/project/keyrings.cryptfile/) backend:

```python
from keyrings.cryptfile.cryptfile import CryptFileKeyring

kr = CryptFileKeyring()
kr.keyring_key = "CRYPTFILE_PASSWORD"
kr.set_password("EXAMPLE_SECTION", "some_secret", "very_secret_value")
```

```python
from keyring_configparser import KeyringConfigParser
from keyrings.cryptfile.cryptfile import CryptFileKeyring

kr = CryptFileKeyring()
kr.keyring_key = "CRYPTFILE_PASSWORD"

config = KeyringConfigParser(keyring=kr)
config.read("/tmp/app.config")
config.get('EXAMPLE_SECTION', 'some_secret')
> "very_secret_value"
```

#### Custom Config Token

A token can be supplied to the `KeyringConfigParser` constructor to override the default token `"$."`. When the custom token is encountered in the configuration file the value will be resolved with keyring.

Given the following configuration file:

```
#/tmp/app.config
[EXAMPLE_SECTION]
non_secret = hello world
some_secret = !~!
default_token = $.
```

```python
from keyring_configparser import KeyringConfigParser

config = KeyringConfigParser(token="!~!")
config.read("/tmp/app.config")
config.get('EXAMPLE_SECTION', 'some_secret')
> "very_secret_value"
config.get('EXAMPLE_SECTION', 'default_token')
> "$."
```

## Questions / Issues

Please raise any questions in the [Discussions](https://github.com/LiamMahoney/keyring_configparser/discussions) page of the repository.

Please document any issues encountered in the [Issues](https://github.com/LiamMahoney/keyring_configparser/issues) page of the repository.