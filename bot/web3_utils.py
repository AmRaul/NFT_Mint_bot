from web3 import Web3
from web3.exceptions import InvalidAddress
import json
import os
from dotenv import load_dotenv
import logging
load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("ALCHEMY_URL")))

with open("contract_abi.json") as f:
    abi = json.load(f)

contract_address = Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS"))
contract = w3.eth.contract(address=contract_address, abi=abi)


def create_add_arbitrum_link():
    arbitrum_network = {
        "chainId": "0xa4b1",  # Арбитрум One
        "chainName": "Arbitrum One",
        "rpcUrls": ["https://arb1.arbitrum.io/rpc"],
        "nativeCurrency": {
            "name": "Ether",
            "symbol": "ETH",
            "decimals": 18
        },
        "blockExplorerUrls": ["https://arbiscan.io"]
    }

    # Преобразуем объект в строку JSON
    arbitrum_network_json = json.dumps(arbitrum_network)

    # Формируем ссылку для добавления сети в MetaMask
    link = f"metamask://add-chain/{arbitrum_network_json}"

    return link

def create_buy_link():
    price_in_wei = w3.to_wei(0.000015, 'ether')  # Цена NFT
    hex_price = hex(price_in_wei)
    # Получаем hex-код вызова функции buy()
    data_hex = contract.functions.buy()._encode_transaction_data()

    # Формируем deep-link для MetaMask
    buy_link = f"metamask://eth_sendTransaction?to={contract_address}&value={hex_price}&data={data_hex}"

    return buy_link



def mint_nft(to_address: str):
    if not Web3.is_address(to_address):
        raise InvalidAddress("Неверный формат адреса")

    sender = w3.eth.account.from_key(os.getenv("PRIVATE_KEY"))
    nonce = w3.eth.get_transaction_count(sender.address)

    try:
        txn = contract.functions.safeMint(to_address).build_transaction({
            'chainId': 42161,
            'gas': 300000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })

        signed_txn = w3.eth.account.sign_transaction(txn, private_key=os.getenv("PRIVATE_KEY"))
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        return tx_hash.hex()
    except Exception as e:
        # Логирование ошибки
        logging.error(f"Ошибка при отправке NFT: {e}")
        raise  # Повторно выбрасываем ошибку, если нужно

