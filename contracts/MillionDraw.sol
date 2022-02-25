//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MillionDraw{
    uint256 private tickets;
    string public name;
    address[] public participants;
    address public owner;
    // LotCoin private lotcoin;
    uint256 private entryFee = 1000000000000000000000000;
    constructor(){
        owner = msg.sender;
    }

    function joinDraw() public{
        participants.push(msg.sender);
    }
    function getParticipantsNum() view public returns(uint256){
        return participants.length;
    }
}