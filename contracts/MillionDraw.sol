//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract MillionDraw is VRFConsumerBase {
    bytes32 internal keyHash;
    uint256 internal fee;
    uint256 public randomNumber;
    address[] public participants;
    address public winner;
    uint256 private linkFee = 0.0001 * (10**18);

    constructor(
        address _vrfCoordinator,
        address _link,
        bytes32 _keyHash,
        uint256 _fee
    ) VRFConsumerBase(_vrfCoordinator, _link) {
        keyHash = _keyHash;
        fee = _fee;
    }

    function getRandomness() public returns (bytes32) {
        require(
            LINK.balanceOf(address(this)) >= fee,
            "Inadequate Link to fund this transaction"
        );
        return requestRandomness(keyHash, fee);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomness)
        internal
        override
    {
        randomNumber = randomness;
    }

    function joinDraw() public {
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
        lotCoin.transfer(winner, lotCoin.balanceOf(address(this)));
    }
}
