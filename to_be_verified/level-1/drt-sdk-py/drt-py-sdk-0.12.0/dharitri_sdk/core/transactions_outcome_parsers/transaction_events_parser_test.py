from pathlib import Path
from types import SimpleNamespace

import pytest

from dharitri_sdk.abi.abi import Abi
from dharitri_sdk.abi.abi_definition import AbiDefinition
from dharitri_sdk.converters import TransactionsConverter
from dharitri_sdk.core.address import Address
from dharitri_sdk.core.codec import encode_unsigned_number
from dharitri_sdk.core.transactions_outcome_parsers.resources import (
    SmartContractCallOutcome, SmartContractResult, TransactionEvent,
    TransactionLogs, TransactionOutcome, find_events_by_first_topic,
    find_events_by_identifier)
from dharitri_sdk.core.transactions_outcome_parsers.transaction_events_parser import \
    TransactionEventsParser
from dharitri_sdk.network_providers import ApiNetworkProvider

testdata = Path(__file__).parent.parent.parent / "testutils" / "testdata"


def test_parse_events_minimalistic():
    abi = Abi.load(testdata / "dcdt-safe.abi.json")
    parser = TransactionEventsParser(abi=abi)

    values = parser.parse_events(
        events=[
            TransactionEvent(
                identifier="transferOverMaxAmount",
                topics=["transferOverMaxAmount".encode(), bytes([0x2a]), bytes([0x2b])]
            )
        ]
    )

    assert len(values) == 1
    assert values[0] == SimpleNamespace(
        batch_id=42,
        tx_id=43
    )


def test_parse_dcdt_safe_deposit_event():
    abi = Abi.load(testdata / "dcdt-safe.abi.json")
    parser = TransactionEventsParser(abi=abi)

    transaction_outcome = TransactionOutcome()

    logs = TransactionLogs(
        events=[
            TransactionEvent(
                topics=[
                    bytes.fromhex("6465706f736974"),
                    bytes.fromhex("726cc2d4b46dd6bd74a4c84d02715bf85cae76318cab81bc09e7c261d4149a67"),
                    bytes.fromhex("0000000c57524557412d30316534396400000000000000000000000164")
                ],
                data_items=[bytes.fromhex("00000000000003db000000")]
            )
        ]
    )

    transaction_outcome.direct_smart_contract_call = SmartContractCallOutcome(return_code="ok", return_message="ok")
    transaction_outcome.transaction_results = [
        SmartContractResult(data=bytes.fromhex("4036663662"), logs=logs)
    ]

    events = find_events_by_first_topic(transaction_outcome, "deposit")
    parsed = parser.parse_events(events)

    assert len(parsed) == 1
    assert parsed[0] == SimpleNamespace(
        dest_address=Address.new_from_bech32("drt1wfkv9495dhtt6a9yepxsyu2mlpw2ua333j4cr0qfulpxr4q5nfns25nrld").get_public_key(),
        tokens=[SimpleNamespace(
            token_identifier="WREWA-01e49d",
            token_nonce=0,
            amount=100
        )],
        event_data=SimpleNamespace(
            tx_nonce=987,
            opt_function=None,
            opt_arguments=None,
            opt_gas_limit=None,
        )
    )


def test_parse_multisig_start_perform_action():
    abi = Abi.load(testdata / "multisig-full.abi.json")
    parser = TransactionEventsParser(abi=abi)

    transaction_outcome = TransactionOutcome(
        direct_smart_contract_call_outcome=SmartContractCallOutcome(return_code="ok", return_message="ok"),
        transaction_results=[SmartContractResult(data=bytes.fromhex("4036663662"))],
        transaction_logs=TransactionLogs(events=[TransactionEvent(
            identifier="performAction",
            topics=[bytes.fromhex("7374617274506572666f726d416374696f6e")],
            data_items=[bytes.fromhex("00000001000000000500000000000000000500d006f73c4221216fa679bc559005584c4f1160e569e100000000000000000361646400000001000000010700000001c782420144e8296f757328b409d01633bf8d09d8ab11ee70d32c204f6589bd24")]
        )])
    )

    events = find_events_by_first_topic(transaction_outcome, "startPerformAction")
    parsed = parser.parse_events(events)
    data = parsed[0].data

    assert data == SimpleNamespace(
        action_id=1,
        group_id=0,
        action_data=SimpleNamespace(
            **{
                "0": SimpleNamespace(
                    to=Address.new_from_bech32("drt1qqqqqqqqqqqqqpgq6qr0w0zzyysklfneh32eqp2cf383zc89d8ssk0pue3").get_public_key(),
                    rewa_amount=0,
                    opt_gas_limit=None,
                    endpoint_name=b'add',
                    arguments=[bytes.fromhex("07")]
                ),
                '__discriminant__': 5
            }
        ),
        signers=[Address.new_from_bech32("drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l").get_public_key()]
    )


def test_parse_event_with_multi_values():
    abi_definition = AbiDefinition.from_dict(
        {
            "events": [
                {
                    "identifier": "doFoobar",
                    "inputs": [
                        {
                            "name": "a",
                            "type": "multi<u8, utf-8 string, u8, utf-8 string>",
                            "indexed": True,
                        },
                        {
                            "name": "b",
                            "type": "multi<utf-8 string, u8>",
                            "indexed": True,
                        },
                        {
                            "name": "c",
                            "type": "u8",
                            "indexed": False,
                        },
                    ],
                },
            ]
        }
    )

    abi = Abi(abi_definition)
    parser = TransactionEventsParser(abi=abi)
    value = 42

    parsed = parser.parse_event(
        TransactionEvent(
            identifier="foobar",
            topics=[
                "doFoobar".encode(),
                encode_unsigned_number(value),
                "test".encode(),
                encode_unsigned_number(value + 1),
                "test".encode(),
                "test".encode(),
                encode_unsigned_number(value + 2),
            ],
            data_items=[encode_unsigned_number(value)]
        )
    )

    assert parsed == SimpleNamespace(
        a=[42, "test", 43, "test"],
        b=["test", 44],
        c=42
    )


def test_parse_dcdt_safe_deposit_event_without_first_topic():
    abi = Abi.load(testdata / "dcdt-safe.abi.json")
    parser = TransactionEventsParser(abi=abi)

    transaction_outcome = TransactionOutcome()

    logs = TransactionLogs(
        events=[
            TransactionEvent(
                identifier="deposit",
                topics=[
                    bytes.fromhex(""),
                    bytes.fromhex("726cc2d4b46dd6bd74a4c84d02715bf85cae76318cab81bc09e7c261d4149a67"),
                    bytes.fromhex("0000000c57524557412d30316534396400000000000000000000000164")
                ],
                data_items=[bytes.fromhex("00000000000003db000000")]
            )
        ]
    )

    transaction_outcome.direct_smart_contract_call = SmartContractCallOutcome(return_code="ok", return_message="ok")
    transaction_outcome.transaction_results = [
        SmartContractResult(data=bytes.fromhex("4036663662"), logs=logs)
    ]

    events = find_events_by_identifier(transaction_outcome, "deposit")
    parsed = parser.parse_events(events)

    assert len(parsed) == 1
    assert parsed[0] == SimpleNamespace(
        dest_address=Address.new_from_bech32("drt1wfkv9495dhtt6a9yepxsyu2mlpw2ua333j4cr0qfulpxr4q5nfns25nrld").get_public_key(),
        tokens=[SimpleNamespace(
            token_identifier="WREWA-01e49d",
            token_nonce=0,
            amount=100
        )],
        event_data=SimpleNamespace(
            tx_nonce=987,
            opt_function=None,
            opt_arguments=None,
            opt_gas_limit=None,
        )
    )


@pytest.mark.networkInteraction
def test_multisig_start_perform_action():
    api = ApiNetworkProvider("https://testnet-api.dharitri.org")
    converter = TransactionsConverter()

    transaction_on_network = api.get_transaction("69f63a246a65abad952fa052e105e2487fda98e765c318ed3a2af801efeb9818")
    transaction_outcome = converter.transaction_on_network_to_outcome(transaction_on_network)

    abi = Abi.load(testdata / "multisig-full.abi.json")
    events_parser = TransactionEventsParser(abi)

    events = find_events_by_first_topic(transaction_outcome, "startPerformAction")
    parsed_event = events_parser.parse_event(events[0])

    assert parsed_event.data == SimpleNamespace(
        action_id=1,
        group_id=0,
        action_data=SimpleNamespace(
            **{
                "0": SimpleNamespace(
                    **{
                        'to': Address.new_from_bech32("drt1kgxjlszkqcvccecuvl5r64c7cju7jqwp5kh22w4e6crf827peljqcvleft").get_public_key(),
                        'rewa_amount': 1000000000000000000,
                        'opt_gas_limit': None,
                        'endpoint_name': b'',
                        'arguments': []
                    }
                ),
                '__discriminant__': 5
            },
        ),
        signers=[Address.new_from_bech32("drt10xpcr2cqud9vm6q4axfv64ek63k7xywfcy8zyjp7pvx3kr4cnqlqv3scy7").get_public_key(),
                 Address.new_from_bech32("drt1kgxjlszkqcvccecuvl5r64c7cju7jqwp5kh22w4e6crf827peljqcvleft").get_public_key()]
    )
