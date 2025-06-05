from pathlib import Path

import pytest
from dharitri_sdk import Account


def test_load_account_from_keystore_without_kind():
    alice_json = Path(__file__).parent / "testdata" / "alice.json"
    account = Account.new_from_keystore(file_path=alice_json, password="password")
    assert account.address.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"

    with pytest.raises(Exception):
        _ = Account.new_from_keystore(file_path=alice_json, password="wrong_password")


def test_load_account_from_keystore_with_kind_secret_key():
    keystore_path = Path(__file__).parent / "testdata" / "aliceWithKindSecretKey.json"
    account = Account.new_from_keystore(file_path=keystore_path, password="password")
    assert account.address.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"

    with pytest.raises(Exception):
        _ = Account.new_from_keystore(file_path=keystore_path, password="wrong_password")


def test_load_account_from_keystore_with_kind_mnemonic():
    keystore_path = Path(__file__).parent / "testdata" / "withDummyMnemonic.json"
    account = Account.new_from_keystore(file_path=keystore_path, password="password")
    assert account.address.to_bech32() == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"

    with pytest.raises(Exception):
        _ = Account.new_from_keystore(file_path=keystore_path, password="wrong_password")
