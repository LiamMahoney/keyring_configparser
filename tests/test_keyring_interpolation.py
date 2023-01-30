import pytest
import keyring
import os
import sys
import errno
import tempfile
from keyring_configparser import KeyringInterpolation
from keyrings.cryptfile.cryptfile import CryptFileKeyring
from keyrings.alt.file import PlaintextKeyring

class TestDefaultKeyring:
    secret_section = "keyring_configparser_testing"
    secret_key = "secret_key"
    secret_value = "hello world"

    @pytest.fixture
    def default_keyring(self):
        keyring.set_keyring(PlaintextKeyring())
        keyring.set_password(self.secret_section, self.secret_key, self.secret_value)
        yield
        keyring.delete_password(self.secret_section, self.secret_key)

    def test_get_normal_value(self):
        ki = KeyringInterpolation()
        val = ki.before_get(None, self.secret_section, "section_name", "normal value", None)
        assert val == "normal value"

    def test_get_secret(self, default_keyring):
        ki = KeyringInterpolation()
        val = ki.before_get(None, self.secret_section, self.secret_key, "$.", None)
        assert val == self.secret_value

    def test_get_secret_with_custom_token(self, default_keyring):
        ki = KeyringInterpolation(token="%$#")
        val = ki.before_get(None, self.secret_section, self.secret_key, "%$#", None)
        assert val == self.secret_value

    def test_key_not_found_error(self, default_keyring):
        ki = KeyringInterpolation()
        with pytest.raises(KeyError):
            ki.before_get(None, "section_doesnt_exist", "doesnt_exist", "$.", None)

class TestCryptFileKeyring:
    secret_section = "keyring_configparser_testing"
    secret_key = "secret_key"
    secret_value = "hello world"
    cryptfile_password = "s0s3cure"

    @pytest.fixture
    def cryptfile_keyring(self):
        kr = CryptFileKeyring()
        # changing file secrets / data stored in
        kr.file_path = tempfile.mktemp()
        kr.keyring_key = self.cryptfile_password
        # creating entry to test retrieving
        kr.set_password(self.secret_section, self.secret_key, self.secret_value)
        
        yield kr
        # cleaning up temp keyring file
        try:
            os.remove(kr.file_path)
        except OSError:
            e = sys.exc_info()[1]
            if (e.errno != errno.ENOENT):
                raise

    @pytest.fixture
    def instantiated_keyring_interpolation(self, cryptfile_keyring):
        return KeyringInterpolation(keyring=cryptfile_keyring)

    def test_get_normal_value(self, instantiated_keyring_interpolation):
        val = instantiated_keyring_interpolation.before_get(None, self.secret_section, "section_name", "normal value", None)
        assert val == "normal value"
    
    def test_get_secret(self, instantiated_keyring_interpolation):
        val = instantiated_keyring_interpolation.before_get(None, self.secret_section, self.secret_key, "$.", None)
        assert val == self.secret_value

    def test_get_secret_with_custom_token(self, cryptfile_keyring):
        kr = KeyringInterpolation(token="%$#", keyring=cryptfile_keyring)
        val = kr.before_get(None, self.secret_section, self.secret_key, "%$#", None)
        assert val == self.secret_value
    
    def test_key_not_found_error(self, instantiated_keyring_interpolation):
        with pytest.raises(KeyError):
            instantiated_keyring_interpolation.before_get(None, self.secret_section, "non_existent_key", "$.", None)