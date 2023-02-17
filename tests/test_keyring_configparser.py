import pytest
import keyring
import os
import sys
import errno
import tempfile
from keyring_configparser import KeyringConfigParser
from configparser import NoOptionError, NoSectionError
from keyrings.cryptfile.cryptfile import CryptFileKeyring
from keyrings.alt.file import PlaintextKeyring

section_name = "keyring_configparser_testing"
secret_key = "secret_key"
secret_value = "very secret value"
non_secret_key = "non_secret_key"
non_secret_value = "not very secret"

@pytest.fixture
def config_str():
    return f"""
    [{section_name}]
    {secret_key}: $.
    {non_secret_key}: {non_secret_value}
    value_not_set: $.
    """.strip()

class TestDefaultKeyring:

    @pytest.fixture
    def default_keyring(self):
        keyring.set_keyring(PlaintextKeyring())
        keyring.set_password(section_name, secret_key, secret_value)
        yield
        keyring.delete_password(section_name, secret_key)

    @pytest.fixture
    def config(self, config_str, default_keyring):
        config = KeyringConfigParser()
        config.read_string(config_str)
        yield config

    def test_get_non_secret(self, config):
        val = config.get(section_name, non_secret_key)
        assert val == non_secret_value
    
    def test_get_secret(self, config):
        val = config.get(section_name, secret_key)
        assert val == secret_value

    def test_get_secret_with_custom_token(self, default_keyring):
        config_str = f"""
        [{section_name}]
        {secret_key}: !@
        """.strip()
        
        config = KeyringConfigParser(token="!@")
        config.read_string(config_str)
        
        val = config.get(section_name, secret_key)
        assert val == secret_value

    def test_key_not_in_keyring_error(self, config):
        with pytest.raises(KeyError):
            config.get(section_name, "value_not_set")
    
    def test_key_not_in_config_error(self, config):
        with pytest.raises(NoOptionError):
            config.get(section_name, "doesnt_exist")

    def test_sction_not_in_config_error(self, config):
        with pytest.raises(NoSectionError):
            config.get("doesnt_exist", "doesnt_exist")

class TestCryptFileKeyring:

    @pytest.fixture
    def cryptfile_keyring(self):
        kr = CryptFileKeyring()
        # changing file secrets / data stored in
        kr.file_path = tempfile.mktemp()
        kr.keyring_key = "cryptfile_password"
        # creating entry to test retrieving
        kr.set_password(section_name, secret_key, secret_value)
        
        yield kr

        # cleaning up temp keyring file
        try:
            os.remove(kr.file_path)
        except OSError:
            e = sys.exc_info()[1]
            if (e.errno != errno.ENOENT):
                raise

    @pytest.fixture
    def config(self, config_str, cryptfile_keyring):
        config = KeyringConfigParser(keyring=cryptfile_keyring)
        config.read_string(config_str)
        yield config

    def test_get_non_secret(self, config):
        val = config.get(section_name, non_secret_key)
        assert val == non_secret_value
    
    def test_get_secret(self, config):
        val = config.get(section_name, secret_key)
        assert val == secret_value

    def test_get_secret_with_custom_token(self, cryptfile_keyring):
        config_str = f"""
        [{section_name}]
        {secret_key}: !@
        """.strip()
        
        config = KeyringConfigParser(token="!@", keyring=cryptfile_keyring)
        config.read_string(config_str)
        
        val = config.get(section_name, secret_key)
        assert val == secret_value

    def test_key_not_in_keyring_error(self, config):
        with pytest.raises(KeyError):
            config.get(section_name, "value_not_set")
    
    def test_key_not_in_config_error(self, config):
        with pytest.raises(NoOptionError):
            config.get(section_name, "doesnt_exist")

    def test_sction_not_in_config_error(self, config):
        with pytest.raises(NoSectionError):
            config.get("doesnt_exist", "doesnt_exist")