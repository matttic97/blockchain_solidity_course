from brownie import SimpleStorage, accounts

def test_deploy():
    # arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})

    # act
    expected_value = ("matic", "isovski", 25)
    simple_storage.addPerson("matic", "isovski", 25, {"from": account})

    # assert
    assert expected_value == simple_storage.getPerson(0)