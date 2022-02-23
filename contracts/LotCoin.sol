//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract LotCoin is ERC20{
    constructor(address founder1, address founder2 , address founder3,uint256 initialSupply) ERC20("LOTCOIN","LOT"){
        _mint(founder1,initialSupply/3);
        _mint(founder2,initialSupply/3);
        _mint(founder3,initialSupply/3);
    }
}