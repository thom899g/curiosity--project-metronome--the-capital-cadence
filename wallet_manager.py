from web3 import Web3
import config

class WalletManager:
    def __init__(self, web3: Web3):
        self.w3 = web3
        self.accounts = []
        for private_key in config.FLOW_WALLET_PRIVATE_KEYS:
            if private_key:
                account = self.w3.eth.account.from_key(private_key)
                self.accounts.append(account)
        if not self.accounts:
            raise ValueError("No wallet private keys provided.")

    def get_account(self, index=0):
        if index < len(self.accounts):
            return self.accounts[index]
        else:
            return self.accounts[0]

    def sign_transaction(self, transaction, account_index=0):
        account = self.get_account(account_index)
        signed_txn = self.w3.eth.account.sign_transaction(transaction, account.key)
        return signed_txn