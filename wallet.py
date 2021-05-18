# Import dependencies
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3 import Web3, middleware, Account
from bit.network import NetworkAPI
from bit import PrivateKeyTestnet
import subprocess
import json
import os

# Import constants.py and necessary functions from bit and web3
from constants import BTC, BTCTEST, ETH
from pprint import pprint
from dotenv import load_dotenv


# Load and set environment variables
load_dotenv()

# connect Web3
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.eth.setGasPriceStrategy(medium_gas_price_strategy)
mnemonic = os.getenv("mnemonic")

# key = wif_to_key("")

# Create a function called `derive_wallets`


def derive_wallets(coin=BTC, mnemonic=mnemonic, depth=3):
    command = 'php ./derive -g --mnemonic="{mnemonic}" --cols=all --coin={coin} --numderive={depth} --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    return json.loads(output)


# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {
    ETH: derive_wallets(coin=ETH),
    BTCTEST: derive_wallets(coin=BTCTEST)

}

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.


def priv_key_to_account(coin, priv_key):
    private_key = os.getenv('PRIVATE_KEY')
    account_one = Account.from_key(private_key)

# w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
# w3.middleware_onion.inject(geth_poa_middleware, layer=0)
# private_key= "0x1f1a3d10a144aa22b8f7850e09f4032599d72162d48ac9d68df6684efc326c80"
# account_one = Account.from_key(private_key)

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.


def create_tx(coin, account, recipient, amount):

    gasEstimate = w3.eth.estimateGas(
        {"from": account.address, "to": recipient, "value": amount}
    )
    return {
        "from": account.address,
        "to": recipient,
        "account_one": Account.from_key(private_key),   
        "value": amount,
        "gasPrice": w3.eth.gasPrice,
        "gas": gasEstimate,
        "nonce": w3.eth.getTransactionCount(w3.toChecksumAddress(account.address))
    }

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.


def send_tx(coin, account, recipient, amount):
    tx = create_tx(coin, account, recipient, amount)
    signed_tx = account.sign_transaction(tx)
    result = w3.eth.send_raw_transaction(
        signed_tx.rawTransaction)  # Transaction Hash
    print(result.hex())
    return result.hex()


txHash = send_tx(account_one, "PUBLIC_KEY_OF_YOUR_WALLET", w3.toWei(12345, 'ether'))
print(w3.eth.get_transaction(txHash))

pprint(coins)
