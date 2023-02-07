from web3 import Web3
import json
from time import time
from time import sleep
from dotenv import load_dotenv
import os 

load_dotenv()

provider = os.getenv('PROVIDER')
w3 = Web3(Web3.HTTPProvider(provider))

address_weth = w3.toChecksumAddress("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2") 
address_dai = w3.toChecksumAddress("0x6B175474E89094C44Da98b954EedeAC495271d0F")
address_router = w3.toChecksumAddress("0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")

abi_router = open('abirouteruniswap.json')

router = w3.eth.contract(        #rooter uniswap
     address = address_router,
     abi = json.load(abi_router))

abi_dai = open('abidai.json')

contract_dai = w3.eth.contract(     #abi contract dai
     address = address_dai,
     abi = json.load(abi_dai))

decimals = 10**18 #number of decimals of eth and dai tokens

private_key = os.getenv('PRIVATE_KEY')
signer_wallet = w3.eth.account.from_key(private_key)

number_of_dai = 100 #os.getenv('NUMBER_OF_DAI') #number of dai that will be swap for eth at each transaction

#dai tokens must be approved because there are erc20
tx_approve = contract_dai.functions.approve(address_router, 2**256 - 1).buildTransaction({'nonce': w3.eth.getTransactionCount(signer_wallet.address)})
s_tx_approve = w3.eth.account.sign_transaction(tx_approve, private_key)

period = int(os.getenv('PERIOD')) #number of seconds you want to wait between each transaction 

while True :
     timestamp = int(time())

     #swap dai for weth
     tx_swap = router.functions.swapExactTokensForETH(number_of_dai*decimals, 0, [address_dai, address_weth], signer_wallet.address, timestamp+1000).buildTransaction({'nonce': w3.eth.getTransactionCount(signer_wallet.address), 'from': signer_wallet.address})
     s_tx_swap = w3.eth.account.sign_transaction(tx_swap, private_key)

     #print for testing
     balanceeth = w3.eth.get_balance(signer_wallet.address) / decimals
     balancedai = contract_dai.functions.balanceOf(signer_wallet.address).call() / decimals
     print(balancedai)
     print(balanceeth)
     sleep(period)
