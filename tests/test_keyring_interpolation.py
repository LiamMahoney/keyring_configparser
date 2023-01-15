import pytest
import keyring
from keyring_configparser import KeyringInterpolation

class TestDefaultKeyring:
    secret_section = "keyring_configparser_testing"
    secret_key = "secret_key"
    secret_value = "hello world"

    @pytest.fixture
    def secret_storage(self):
        keyring.set_password(self.secret_section, self.secret_key, self.secret_value)
        yield
        keyring.delete_password(self.secret_section, self.secret_key)

    def test_get_normal_value(self):
        ki = KeyringInterpolation()
        val = ki.before_get(None, self.secret_section, "section_name", "normal value", None)
        assert val == "normal value"

    def test_get_secret(self, secret_storage):
        ki = KeyringInterpolation()
        val = ki.before_get(None, self.secret_section, self.secret_key, "$.", None)
        assert val == self.secret_value

    def test_get_secret_with_custom_token(self, secret_storage):
        ki = KeyringInterpolation(token="%$#")
        val = ki.before_get(None, self.secret_section, self.secret_key, "%$#", None)
        assert val == self.secret_value

    def test_key_not_found_error(self, secret_storage):
        ki = KeyringInterpolation()
        with pytest.raises(KeyError):
            ki.before_get(None, "section_doesnt_exist", "doesnt_exist", "$.", None)

#TODO: add TestCryptFileKeyring