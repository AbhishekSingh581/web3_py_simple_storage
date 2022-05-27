// SPDX-Licence-Identifier : MIT
pragma solidity >=0.6.0 <0.9.0;   //in range between these two

contract SimpleStorage{

    struct People{
        uint256 favNum;
        string name;
    }

    People public person=People({favNum:2,name:"Abhishek"}); 

    //array
    People[] public people;  //dynamic array

    mapping(string =>uint256) public nametofavNum;

    function addPerson(string memory _name,uint256 _favNumber) public{    //1. storage   2.memory //in memory it will store only during execute
        people.push(People({favNum:_favNumber,name:_name}));
        nametofavNum[_name]=_favNumber;
    } 

    //mapping
    uint256 public favNum;  //size of 256 bits
    // bool favBool=true;
    // string favString= "String";
    // int256 favInt=-5;
    // address favAddress=0x54Ae0C23a8B25BD7F305B6a2402fcB7A61521e27;
    // bytes32 favBytes="cat";

    //functions
    function store(uint256 _favNumber) public{   //calling this function will lead to change in state or transaction
        favNum=_favNumber;
    }

    function retrieve() public view returns(uint256){    //view :read the state of blockchain that means we are not changing states or transactions so no transaction fee cut from account

        return favNum;
    }
    function retrieve2(uint256 _favNumber) public pure{  // pure also not change states of block
        _favNumber+_favNumber;
    }
}
