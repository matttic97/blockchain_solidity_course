from cv2 import add
import numpy as np
from solcx import compile_standard, install_solc
from dotenv import load_dotenv
from web3 import Web3
import json
import os

load_dotenv()

install_solc("0.8.0")


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# compile solidity file
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)
print("Contracts successfully compiled.")

# save compiled file
with open("output/compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode & abi
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]


w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/fadd9c491393498bad676f43811172d8"))
chain_id = 4
address = "0x60c85d5e1705B470980844CBb92a27dde20BBe39"
private_key = os.getenv("ACCOUNT_PRIVATE_KEY")


# create the contract
print("Creating contracts to deploy...")
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get latest transaction
nonce = w3.eth.getTransactionCount(address)


# Deploy a contract
## 1. build a transaction
print("Preparing contracts for deploy...")
transaction = SimpleStorage.constructor().buildTransaction(
    {"gasPrice": w3.eth.gas_price, "chainId": chain_id, "from": address, "nonce": nonce}
)

## 2. sign a transaction
signed_transaction = w3.eth.account.sign_transaction(
    transaction, private_key=private_key
)

## 3. send a transaction
print("Deploying...")
transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
print("Successfully deployed.")


# Working with the contract
## for this we always need abi and address of the contract
simple_storage = w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)

print(simple_storage.functions.addPerson("matic", "isovski", 25).call())      # simulate function call and get response without changing the blockchain state
#print(simple_storage.functions.addPerson("matic", "isovski", 25).transact())  # simulate function call with the blockchain state change
addPersonTransaction = simple_storage.functions.addPerson("matic", "isovski", 25).buildTransaction(
    {"gasPrice": w3.eth.gas_price, "chainId": chain_id, "from": address, "nonce": nonce+1}
)
addPersonTransaction = w3.eth.account.sign_transaction(addPersonTransaction, private_key=private_key)
addPersonTrxHash = w3.eth.send_raw_transaction(addPersonTransaction.rawTransaction)
addPersonTrxReceipt = w3.eth.wait_for_transaction_receipt(addPersonTrxHash)
print(simple_storage.functions.getPerson(0).call()) 
