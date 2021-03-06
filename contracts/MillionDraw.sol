//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract MillionDraw is VRFConsumerBase {
    bytes32 internal keyHash;
    uint256 internal linkFee;
    uint256 public randomNumber;
    address[] public participants;
    address public winner;
    address private deployer;

    uint256 private startTime;
    uint256 private drawDays;

    constructor(
        address _vrfCoordinator,
        address _link,
        bytes32 _keyHash,
        uint256 _linkFee,
        address _deployer,
        uint256 _drawDays
    ) VRFConsumerBase(_vrfCoordinator, _link) {
        keyHash = _keyHash;
        linkFee = _linkFee;
        deployer = _deployer;

        startTime = block.timestamp;
        drawDays = _drawDays;
    }

    function getRandomness() public returns (bytes32) {
        require(
            LINK.balanceOf(address(this)) >= linkFee,
            "Inadequate Link to fund this transaction"
        );
        return requestRandomness(keyHash, linkFee);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomness)
        internal
        override
    {
        randomNumber = randomness;
    }

    modifier drawEnded() {
        uint256 endTime = startTime + (drawDays * 1 days);
        require(block.timestamp < endTime, "The draw has ended");
        _;
    }

    function joinDraw() public drawEnded {
        participants.push(msg.sender);
    }

    function getParticipantsNum() public view returns (uint256) {
        return participants.length;
    }

    function getWinner() public returns (address) {
        uint256 winnerIndex = randomNumber % getParticipantsNum();
        winner = participants[winnerIndex];
        participants = new address[](0);
        return winner;
    }

    function fundWinner(IERC20 lotCoin) public {
        uint256 winnings = (lotCoin.balanceOf(address(this)) * 4) / 5;
        uint256 deployerFee = (lotCoin.balanceOf(address(this)) * 1) / 5;
        lotCoin.transfer(winner, winnings);
        lotCoin.transfer(deployer, deployerFee);
    }
}
