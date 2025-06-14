from Cryptodome.Hash import keccak

from dharitri_sdk_core.interfaces import IMessage


class Message:
    def __init__(self, data: bytes, signature: bytes = b"") -> None:
        self.data = data
        self.signature = signature


class MessageComputer:
    """
    Also see: 
     - https://github.com/TerraDharitri/drt-js-sdk-core/blob/v11.2.0/src/signableMessage.ts
     - https://eips.ethereum.org/EIPS/eip-712 (in the past, it served as a basis for the implementation)
    """

    def __init__(self) -> None:
        pass

    def compute_bytes_for_signing(self, message: IMessage) -> bytes:
        PREFIX = bytes.fromhex("174e756d626174205369676e6564204d6573736167653a0a")
        size = str(len(message.data)).encode()
        content = PREFIX + size + message.data
        content_hash = keccak.new(digest_bits=256).update(content).digest()

        return content_hash
