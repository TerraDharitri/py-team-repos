from dharitri_sdk_core.address import Address
from dharitri_sdk_core.contract_query_builder import ContractQueryBuilder


def test_contract_query_builder():
    contract = Address.from_bech32("drt1qqqqqqqqqqqqqpgquzmh78klkqwt0p4rjys0qtp3la07gz4d396qwgcss9")
    caller = Address.from_bech32("drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf")

    builder = ContractQueryBuilder(
        contract=contract,
        function="getFoobar",
        call_arguments=[42, "test"],
        caller=caller,
        value=1
    )

    query = builder.build()

    assert query.contract == contract
    assert query.function == "getFoobar"
    assert query.encoded_arguments == ["2a", "74657374"]
    assert query.caller == caller
    assert query.value == 1
