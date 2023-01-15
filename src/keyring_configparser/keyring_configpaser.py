import configparser
from .keyring_interpolation import KeyringInterpolation

class KeyringConfigParser(configparser.ConfigParser):
    """ConfigParser that can read values with the keyring pypi library.
    
    Instantiates a ConfigParser instance configured with an interpolation 
    class that can read values via the keyring pypi library.

    For example, the following entry in an app.config file

    ```
    [EXAMPLE_SERVICE]
    username=$.
    ```

    would equate to the keyring call 
    `keyring.get_password('EXAMPLE_SERVICE', 'username')`
    """
    def __init__(self, token="$.", keyring=None):
        """
        Args:
            token (str, optional): Token to signal the value is stored in 
            keyring. Defaults to "$.".
            keyring (keyring, optional): a pre-configured instance of keyring.
            If not supplied, a new empty instance of keyring is created.  
            Defaults to None.
        """
        super().__init__(interpolation=KeyringInterpolation(token=token, keyring=keyring))