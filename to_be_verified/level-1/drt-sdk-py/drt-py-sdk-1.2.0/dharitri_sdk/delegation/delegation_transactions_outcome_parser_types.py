from dataclasses import dataclass

from dharitri_sdk.core.address import Address


@dataclass
class CreateNewDelegationContractOutcome:
    contract_address: Address
