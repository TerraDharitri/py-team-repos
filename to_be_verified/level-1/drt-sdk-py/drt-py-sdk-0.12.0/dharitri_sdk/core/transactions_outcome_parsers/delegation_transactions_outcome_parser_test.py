import base64

from dharitri_sdk.core.address import Address
from dharitri_sdk.core.transactions_outcome_parsers.delegation_transactions_outcome_parser import \
    DelegationTransactionsOutcomeParser
from dharitri_sdk.core.transactions_outcome_parsers.resources import (
    SmartContractResult, TransactionEvent, TransactionLogs, TransactionOutcome)
from dharitri_sdk.testutils.utils import base64_topics_to_bytes


class TestDelegationTransactionsOutcomeParser:
    parser = DelegationTransactionsOutcomeParser()

    def test_parse_create_new_delegation_contract(self):
        contract_address = Address.new_from_bech32("drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqlllllsuqfmuj")

        encodedTopics = [
            "Q8M8GTdWSAAA",
            "Q8M8GTdWSAAA",
            "AQ==",
            "Q8M8GTdWSAAA",
            "IzMAAAAAAAAAAAAAAAAAAAACMzAAAAAAAAAAAAP///8=",
        ]

        delegate_event = TransactionEvent(
            address="drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5",
            identifier="delegate",
            topics=base64_topics_to_bytes(encodedTopics)
        )

        encodedTopics = [
            "IzMAAAAAAAAAAAAAAAAAAAACMzAAAAAAAAAAAAP///8=",
            "PDXX6ssamaSgzKpTfvDMCuEJ9B9sK0AiA+Yzv7sHH1w=",
        ]

        sc_deploy_event = TransactionEvent(
            address="drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqlllllsuqfmuj",
            identifier="SCDeploy",
            topics=base64_topics_to_bytes(encodedTopics)
        )

        logs = TransactionLogs(events=[delegate_event, sc_deploy_event])

        encoded_topics = ["b2g6sUl6beG17FCUIkFwCOTGJjoJJi5SjkP2077e6xA="]
        sc_result_event = TransactionEvent(
            address="drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5",
            identifier="completedTxEvent",
            topics=base64_topics_to_bytes(encoded_topics)
        )

        sc_result_log = TransactionLogs(
            address="drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5",
            events=[sc_result_event]
        )

        sc_result = SmartContractResult(
            sender="drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqyllls4jxmwv",
            receiver="drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5",
            data=base64.b64decode("QDZmNmJAMjMzMzAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAyMzMzMDAwMDAwMDAwMDAwMDAwMDAxMGZmZmZmZg=="),
            logs=sc_result_log
        )

        tx_outcome = TransactionOutcome(transaction_results=[sc_result], transaction_logs=logs)

        outcome = self.parser.parse_create_new_delegation_contract(tx_outcome)

        assert len(outcome) == 1
        assert outcome[0].contract_address == contract_address.to_bech32()
