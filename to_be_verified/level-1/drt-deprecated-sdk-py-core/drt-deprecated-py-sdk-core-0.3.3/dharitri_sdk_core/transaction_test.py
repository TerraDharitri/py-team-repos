
from dharitri_sdk_core.address import Address
from dharitri_sdk_core.token_payment import TokenPayment
from dharitri_sdk_core.transaction import Transaction
from dharitri_sdk_core.transaction_payload import TransactionPayload


def test_serialize_for_signing():
    sender = Address.from_bech32("drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf")
    receiver = Address.from_bech32("drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c")

    transaction = Transaction(
        nonce=89,
        sender=sender,
        receiver=receiver,
        value=0,
        gas_limit=50000,
        gas_price=1000000000,
        chain_id="D",
        version=1
    )

    assert transaction.serialize_for_signing().decode() == r"""{"nonce":89,"value":"0","receiver":"drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c","sender":"drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf","gasPrice":1000000000,"gasLimit":50000,"chainID":"D","version":1}"""

    transaction = Transaction(
        nonce=90,
        sender=sender,
        receiver=receiver,
        value=TokenPayment.rewa_from_amount("1.0"),
        data=TransactionPayload.from_str("hello"),
        gas_limit=70000,
        gas_price=1000000000,
        chain_id="D",
        version=1
    )

    assert transaction.serialize_for_signing().decode() == r"""{"nonce":90,"value":"1000000000000000000","receiver":"drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c","sender":"drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf","gasPrice":1000000000,"gasLimit":70000,"data":"aGVsbG8=","chainID":"D","version":1}"""
