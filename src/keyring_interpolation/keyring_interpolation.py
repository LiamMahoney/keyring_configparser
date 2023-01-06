import configparser
import keyring

class KeyringInterpolation(configparser.Interpolation):
    """Interpolation that uses keyring to retrieve values stored in a system's
    keyring.

    When the token specified is encountered, the interpolation looks up the
    value in the keyring. It uses the config file section as the keyring 
    'servicename' and the config file option as the 'username'.

    For example, the following entry in an app.config file

    ```
    [EXAMPLE_SERVICE]
    username=$.
    ```

    would equate to the keyring call 
    `keyring.get_password('EXAMPLE_SERVICE', 'username')`
    """

    def __init__(self, token="$."):
        """
        Args:
            token (str, optional): Token to signal the value is stored in keyring. Defaults to "$.".
        """
        self.token = token

    def before_get(self, parser, section, option, value, defaults):
        """If the value matches the token specified when creating an instance
        of the class, looks up the value using the keyring library. Otherwise
        returns the value specified in the config file. See ConfigParser
        documentation and source code (specificially the Interpolation class)
        for more details on the parameters.

        Returns:
            str: value stored in the configuration file or keyring
        """
        if (value == self.token):
            # TODO: figure out how to make it work with different keyring backends - need to research keyring more and different backends. **USE DOCKER** to learn more about keyring
            parsed_value = keyring.get_password(section, option)

            if (parsed_value == None):
                raise KeyError(f"entry in keyring with service '{section}' and username '{option}' not found")
            
            return parsed_value
        
        return value