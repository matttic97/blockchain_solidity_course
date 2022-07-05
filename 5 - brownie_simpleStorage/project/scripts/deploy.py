from brownie import accounts, config, SimpleStorage, network


def deploy_simple_storage():
    #account = accounts[0]                                    # take one of ganache test addresses
    #account = accounts.load("solidity-tutorial-account")     # take manualy added brownie account
    #account = accounts.add(config["wallets"]["from_key"])    # import from .env using config
    account = get_account()

    simple_storage = SimpleStorage.deploy({"from": account})

    transaction = simple_storage.addPerson("matic", "isovski", 25, {"from": account}) # when calling transact, we need the address
    transaction.wait(1)
    stored_value = simple_storage.getPerson(0)
    print(stored_value)

def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
    

def main():
    deploy_simple_storage()
