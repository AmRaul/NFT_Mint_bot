// SPDX-License-Identifier: MIT
// Compatible with OpenZeppelin Contracts ^5.0.0
pragma solidity ^0.8.22;

import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

contract TheCryptoLogs is ERC721, Ownable {
    uint256 private _nextTokenId;
    uint256 private _priceInWei;
    uint256 private _maxSupply;

    error SupplyEnded();
    error NotEnoughtFunds();
    error YouAreHaveNFT();

constructor(address initialOwner, uint256 _price, uint256 _supply)
        ERC721("TheCryptoLogs", "TCL")
        Ownable(initialOwner)
    {
        _priceInWei = _price;
        _maxSupply = _supply;
    }

function setPriceInWei(uint256 _price) public onlyOwner {
        _priceInWei = _price;
    } 

    function _baseURI() internal pure override returns (string memory) {
        return "ipfs://bafybeicmaatolgm5vcj7qelygbrntmrces57by2uorkbgsnfk2xegqz3k4/";
    }

    function safeMint(address to) public onlyOwner {
        require(_nextTokenId < _maxSupply, SupplyEnded());
        require(super.balanceOf(to) == 0, YouAreHaveNFT());
        uint256 tokenId = _nextTokenId++;
        _safeMint(to, tokenId);
    }

    function buy() public payable {
        require(_nextTokenId < _maxSupply, SupplyEnded());
        require(super.balanceOf(msg.sender) == 0, YouAreHaveNFT());
        require(msg.value >= _priceInWei, NotEnoughtFunds());

        uint256 tokenId = _nextTokenId++;
        _safeMint(msg.sender, tokenId);
    }

    function withdraw() public onlyOwner {
        uint256 balance = address(this).balance;
        require(balance > 0, NotEnoughtFunds());
        payable(owner()).transfer(balance);
    }
}
