// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;


import './SimpleStorage.sol';


contract StorageFactory is SimpleStorage {

    SimpleStorage[] public simpleStorageArray;

    function createSimpleStorageContract() public {
        simpleStorageArray.push(new SimpleStorage());
    }
    
    function sfStore(uint256 _storageIndex, string memory _name, string memory _surname, uint16 _age) public {
        // for calling a different contract, we need address & abi
        SimpleStorage(address(simpleStorageArray[_storageIndex])).addPerson(_name, _surname, _age);
    }

    function sfGet(uint256 _storageIndex) public view returns(uint16) {
        ( , , uint16 age) = SimpleStorage(address(simpleStorageArray[_storageIndex])).getOldestPerson();
        return age;
    }
}