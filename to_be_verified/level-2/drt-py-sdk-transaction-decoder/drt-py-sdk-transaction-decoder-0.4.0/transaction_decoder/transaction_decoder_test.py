from transaction_decoder.transaction_decoder import TransactionDecoder, TransactionToDecode


class TestTransactionDecoder:
    def test_nft_smart_contract_call(self) -> None:
        tx_to_decode = TransactionToDecode()
        tx_to_decode.sender = (
            "drt18w6yj09l9jwlpj5cjqq9eccfgulkympv7d4rj6vq4u49j8fpwzws36f6y2"
        )
        tx_to_decode.receiver = (
            "drt18w6yj09l9jwlpj5cjqq9eccfgulkympv7d4rj6vq4u49j8fpwzws36f6y2"
        )
        tx_to_decode.value = "0"
        tx_to_decode.data = "RVNEVE5GVFRyYW5zZmVyQDRjNGI0ZDQ1NTgyZDYxNjE2MjM5MzEzMEAyZmI0ZTlAZTQwZjE2OTk3MTY1NWU2YmIwNGNAMDAwMDAwMDAwMDAwMDAwMDA1MDBkZjNiZWJlMWFmYTEwYzQwOTI1ZTgzM2MxNGE0NjBlMTBhODQ5ZjUwYTQ2OEA3Mzc3NjE3MDVmNmM2YjZkNjU3ODVmNzQ2ZjVmNjU2NzZjNjRAMGIzNzdmMjYxYzNjNzE5MUA="

        decoder = TransactionDecoder()
        metadata = decoder.get_transaction_metadata(tx_to_decode)

        assert (
            metadata.sender
            == "drt18w6yj09l9jwlpj5cjqq9eccfgulkympv7d4rj6vq4u49j8fpwzws36f6y2"
 drt1wcn58spj6rnsexugjq3p2fxxq4t3l3kt7np078zwkrxu70ul69fq3c9sr5       )
        assert (
            metadata.receiver
            == "drt1qqqqqqqqqqqqqpgqmua7hcd05yxypyj7sv7pffrquy9gf86s535qmyujkw"
        )
        assert metadata.value == 1076977887712805212893260
        assert metadata.function_name == "swap_lkmoa_to_rewa"
        assert metadata.function_args == ["0b377f261c3c7191", ""]
        if metadata.transfers:
            assert metadata.transfers[0].value == 1076977887712805212893260
            if metadata.transfers[0].properties:
                assert metadata.transfers[0].properties.collection == "LKMOA-aab910"
                assert (
                    metadata.transfers[0].properties.identifier == "LKMOA-aab910-2fb4e9"
                )
    
    def test_sc_call(self):
        tx_to_decode = TransactionToDecode()

        tx_to_decode.sender = (
            ""
        )
        tx_to_decode.receiver = (
            "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
        )
        tx_to_decode.value = "0"
        tx_to_decode.data = (
            "d2l0aGRyYXdHbG9iYWxPZmZlckAwMTczZDA="
        )

        decoder = TransactionDecoder()
        metadata = decoder.get_transaction_metadata(tx_to_decode)

        assert (
            metadata.sender
            == "drt1wcn58spj6rnsexugjq3p2fxxq4t3l3kt7np078zwkrxu70ul69fq3c9sr5"
        )
        assert (
            metadata.receiver
            == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
        )
        assert (
            metadata.function_name
            == "withdrawGlobalOffer"
        )
        assert (
            metadata.function_args
            == ['0173d0']
        )

    def test_multi_dcdt_nft_transfer(self):
        tx_to_decode = TransactionToDecode()
        tx_to_decode.sender = (
            "drt1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqmwzjqm"
        )
        tx_to_decode.receiver = (
            "drt1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqmwzjqm"
        )
        tx_to_decode.value = "0"
        tx_to_decode.data = "TXVsdGlFU0RUTkZUVHJhbnNmZXJAMDAwMDAwMDAwMDAwMDAwMDA1MDBkZjNiZWJlMWFmYTEwYzQwOTI1ZTgzM2MxNGE0NjBlMTBhODQ5ZjUwYTQ2OEAwMkA0YzRiNGQ0NTU4MmQ2MTYxNjIzOTMxMzBAMmZlM2IwQDA5Yjk5YTZkYjMwMDI3ZTRmM2VjQDRjNGI0ZDQ1NTgyZDYxNjE2MjM5MzEzMEAzMTAyY2FAMDEyNjMwZTlhMjlmMmY5MzgxNDQ5MUA3Mzc3NjE3MDVmNmM2YjZkNjU3ODVmNzQ2ZjVmNjU2NzZjNjRAMGVkZTY0MzExYjhkMDFiNUA="

        decoder = TransactionDecoder()
        metadata = decoder.get_transaction_metadata(tx_to_decode)

        assert (
            metadata.sender
            == "drt1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqmwzjqm"
        )
        assert (
            metadata.receiver
            == "drt1qqqqqqqqqqqqqpgqmua7hcd05yxypyj7sv7pffrquy9gf86s535qmyujkw"
        )
        assert metadata.value == 0
        assert metadata.function_name == "swap_lkmoa_to_rewa"
        assert metadata.function_args == [
            "0ede64311b8d01b5",
            "",
        ]
        if metadata.transfers:
            assert len(metadata.transfers) == 2
            assert metadata.transfers[0].value == 45925073746530627023852
            if metadata.transfers[0].properties:
                assert metadata.transfers[0].properties.collection == "LKMOA-aab910"
                assert (
                    metadata.transfers[0].properties.identifier == "LKMOA-aab910-2fe3b0"
                )
            assert metadata.transfers[1].value == 1389278024872597502641297
            if metadata.transfers[1].properties:
                assert metadata.transfers[1].properties.collection == "LKMOA-aab910"
                assert (
                    metadata.transfers[1].properties.identifier == "LKMOA-aab910-3102ca"
                )

    def test_dcdt_transfer(self):
        tx_to_decode = TransactionToDecode()

        tx_to_decode.sender = (
            "drt1wcn58spj6rnsexugjq3p2fxxq4t3l3kt7np078zwkrxu70ul69fq3c9sr5"
        )
        tx_to_decode.receiver = (
            "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
        )
        tx_to_decode.value = "0"
        tx_to_decode.data = (
            "RVNEVFRyYW5zZmVyQDU0NDU1MzU0MmQzMjY1MzQzMDY0MzdAMDI1NDBiZTQwMA=="
        )

        decoder = TransactionDecoder()
        metadata = decoder.get_transaction_metadata(tx_to_decode)

        assert (
            metadata.sender
            == "drt1wcn58spj6rnsexugjq3p2fxxq4t3l3kt7np078zwkrxu70ul69fq3c9sr5"
        )
        assert (
            metadata.receiver
            == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
        )
        assert metadata.value == 10000000000
        assert metadata.function_args is None
        if metadata.transfers:
            assert metadata.transfers[0].value == 10000000000
            if metadata.transfers[0].properties:
                assert metadata.transfers[0].properties.collection == "TEST-2e40d7"
                assert metadata.transfers[0].properties.identifier == "TEST-2e40d7"
    
    def test_multi_transfer_fungible_and_meta_dcdt(self):
        tx_to_decode = TransactionToDecode()

        tx_to_decode.sender = (
            "drt1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqmwzjqm"
        )
        tx_to_decode.receiver = (
            "drt1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqmwzjqm"
        )
        tx_to_decode.value = "0"
        tx_to_decode.data = (
            "TXVsdGlFU0RUTkZUVHJhbnNmZXJAMDAwMDAwMDAwMDAwMDAwMDA1MDBkZjNiZWJlMWFmYTEwYzQwOTI1ZTgzM2MxNGE0NjBlMTBhODQ5ZjUwYTQ2OEAwMkA0YzRiNGQ0NTU4MmQ2MTYxNjIzOTMxMzBAMmZlM2IwQDA5Yjk5YTZkYjMwMDI3ZTRmM2VjQDU1NTM0NDQzMmQzMzM1MzA2MzM0NjVAMDBAMDEyNjMwZTlhMjlmMmY5MzgxNDQ5MUA3MDYxNzk1ZjZkNjU3NDYxNWY2MTZlNjQ1ZjY2NzU2ZTY3Njk2MjZjNjVAMGVkZTY0MzExYjhkMDFiNUA="
        )

        decoder = TransactionDecoder()
        metadata = decoder.get_transaction_metadata(tx_to_decode)

        assert (
            metadata.sender
            == "drt1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqmwzjqm"
        )
        assert (
            metadata.receiver
            == "drt1qqqqqqqqqqqqqpgqmua7hcd05yxypyj7sv7pffrquy9gf86s535qmyujkw"
        )

        assert metadata.value == 0
        assert metadata.function_name == "pay_meta_and_fungible"
        assert metadata.function_args == ["0ede64311b8d01b5", ""]

        if metadata.transfers:
            assert metadata.transfers[0].value == 45925073746530627023852
            if metadata.transfers[0].properties:
                assert metadata.transfers[0].properties.collection == "LKMOA-aab910"
                assert metadata.transfers[0].properties.identifier == "LKMOA-aab910-2fe3b0"
            
            assert metadata.transfers[1].value == 1389278024872597502641297
            if metadata.transfers[1].properties:
                assert metadata.transfers[1].properties.token == "USDC-350c4e"

    def test_multi_transfer_fungible_dcdt(self):
        tx_to_decode = TransactionToDecode()

        tx_to_decode.sender = (
            "drt1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqmwzjqm"
        )
        tx_to_decode.receiver = (
            "drt1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqmwzjqm"
        )
        tx_to_decode.value = "0"
        tx_to_decode.data = (
            "TXVsdGlFU0RUTkZUVHJhbnNmZXJAMDAwMDAwMDAwMDAwMDAwMDA1MDBkZjNiZWJlMWFmYTEwYzQwOTI1ZTgzM2MxNGE0NjBlMTBhODQ5ZjUwYTQ2OEAwMkA1MjQ5NDQ0NTJkMzAzNTYyMzE2MjYyQDAwQDA5Yjk5YTZkYjMwMDI3ZTRmM2VjQDU1NTM0NDQzMmQzMzM1MzA2MzM0NjVAQDAxMjYzMGU5YTI5ZjJmOTM4MTQ0OTE="
        )

        decoder = TransactionDecoder()
        metadata = decoder.get_transaction_metadata(tx_to_decode)

        assert (
            metadata.sender
            == "drt1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqmwzjqm"
        )
        assert (
            metadata.receiver
            == "drt1qqqqqqqqqqqqqpgqmua7hcd05yxypyj7sv7pffrquy9gf86s535qmyujkw"
        )
        assert metadata.value == 0

        if metadata.transfers:
            assert metadata.transfers[0].value == 45925073746530627023852
            if metadata.transfers[0].properties:
                assert metadata.transfers[0].properties.token == "RIDE-05b1bb"
            
            assert metadata.transfers[1].value == 1389278024872597502641297
            if metadata.transfers[1].properties:
                assert metadata.transfers[1].properties.token == "USDC-350c4e"
