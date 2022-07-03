// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;     // pragma solidity 0.6.1 for exact version, ^0.6.0 - every version of 0.6(.x)


/**
 * @title SimpleStorage
 * @dev addPerson, getPerson & sum
 */
contract SimpleStorage {
      
    struct People {
        uint32 id;
        string name;
        string surname;
        uint16 age;
    }

    uint32 private counter;
    People[] people;                                // array of struct People
    mapping(string => uint16) public nameToAge;     // dict with name as key and age as value


    /**
     * @dev addPerson person in variable
     * @param _name person name, _surname person surname and _age person age to store
     */
    function addPerson(string memory _name, string memory _surname, uint16 _age) public {
        people.push(People(counter, _name, _surname, _age));
        nameToAge[_name] = _age;
        counter++;
    }
    
    function getPerson(uint32 _id) public view returns(string memory _name, string memory _surname, uint16) {
        // cannot return struct or an array
        return (people[_id].name, people[_id].surname, people[_id].age);
    }

    function getOldestPerson() public view returns(string memory _name, string memory _surname, uint16) {
        uint16 max = 0;
        uint32 id = 0;
        for (uint32 i=0; i<counter; i++) {
            if (people[i].age >= max) {
                max = people[i].age;
                id = i;
            }
        }
        return (people[id].name, people[id].surname, people[id].age);
    }

    function sum(int a, int b) public pure returns (int) {
        return a + b;
    }

}