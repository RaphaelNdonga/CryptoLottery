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
    uint256 internal winnings;

    constructor(
        address _vrfCoordinator,
        address _link,
        bytes32 _keyHash,
        uint256 _linkFee,
        address _deployer
    ) VRFConsumerBase(_vrfCoordinator, _link) {
        keyHash = _keyHash;
        linkFee = _linkFee;
        deployer = _deployer;
        winnings = 1000 * (10**18);
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
        lotCoin.transfer(winner, winnings);
        fundDeployer(lotCoin);
    }

    function fundDeployer(IERC20 lotCoin) private {
        lotCoin.transfer(deployer, lotCoin.balanceOf(address(this)));
    }
}
