
from numpy import sign
from solcx import compile_standard, install_solc

import json

from web3 import Web3
from dotenv import load_dotenv
load_dotenv()

import os
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)

# compile our solidity
install_solc("0.6.0")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)
# print(compiled_sol)

with open("compiled_code.json","w") as file:
    json.dump(compiled_sol,file)
    
# get bytecode 
bytecode =compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]  
# print(bytecode)

# we are doing in compiled_code file in which first is contract then SimpleStorage.sol then SimpleStorage then evm then bytecode then object 

# get abi
abi=compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

w3=Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id=1337
my_address="0xb94c1FBb6471ffBEA4B60F1960845DC889844632"
# private_key="0x135c3880f9fd9be89b6f195d32274ebaadc22b5f31538d03e74f4402bd2ec0f3"
private_key=os.getenv("PRIVATE_KEY")
# print(private_key)

#Create the contract in python
SimpleStorage=w3.eth.contract(abi=abi, bytecode=bytecode)
# print(SimpleStorage)

#We need to build our transaction 
#get the latest transaction
nonce=w3.eth.getTransactionCount(my_address)
# print(nonce)

# 1. Build the contract DEploy transaction
# 2. Sign the transaction
# 3. Send the transaction

transaction=SimpleStorage.constructor().buildTransaction({"gasPrice": w3.eth.gas_price,"chainId":chain_id,"from":my_address,"nonce":nonce})
# print(transaction)


signed_txn=w3.eth.account.sign_transaction(transaction,private_key=private_key)
# print(signed_txn)
print("Deploying Contract...")
tx_hash=w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt=w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")

# working with the contract
# Contract Address
# abi
simple_storage=w3.eth.contract(address=tx_receipt.contractAddress,abi=abi)

# Call -> Don't change states. return values
#Transact-> Actually make state change

# Initial value of favNum
print(simple_storage.functions.retrieve().call())


favNumInput = input("Enter your value: ")
print("Updating Contract...")
store_transaction=simple_storage.functions.store(int(favNumInput)).buildTransaction({
    "gasPrice": w3.eth.gas_price,"chainId":chain_id,"from":my_address,"nonce":nonce+1
})
signed_store_txn=w3.eth.account.sign_transaction(store_transaction,private_key=private_key)
send_store_tx_hash=w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt=w3.eth.wait_for_transaction_receipt(send_store_tx_hash)
print("Contract Updated!")
print(simple_storage.functions.retrieve().call())

n=input("Enter number of Persons adding in array: ")
nonce=nonce+1
for i in range(0,int(n)):
    PersonName = input("Enter Name: ")
    PersonFavNumInput=input("Enter the value: ")  
    print("Updating Contract...")
    addPerson_transaction=simple_storage.functions.addPerson(str(PersonName),int(PersonFavNumInput)).buildTransaction({
        "gasPrice": w3.eth.gas_price,"chainId":chain_id,"from":my_address,"nonce":nonce+i+1
    })
    signed_addPerson_txn=w3.eth.account.sign_transaction(addPerson_transaction,private_key=private_key)
    send_addPerson_tx_hash=w3.eth.send_raw_transaction(signed_addPerson_txn.rawTransaction)
    tx_receipt=w3.eth.wait_for_transaction_receipt(send_addPerson_tx_hash)
    print("Contract Updated!")

nonce=nonce+n

enquryName=input("Enter the string: ")
# NameMapping=input("Enter the string: ")
print(simple_storage.functions.nametofavNum(str(enquryName)).call())

