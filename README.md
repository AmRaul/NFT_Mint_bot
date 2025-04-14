# NFT_Mint_bot

Name: NFT Mint Bot (Telegram + Solidity)
Description:
This is my first pet project using Solidity and Web3.

I built a Telegram bot that lets users mint a free NFT on the Arbitrum network. The bot is written in Python using aiogram, and it connects to a smart contract through Web3.py.

What’s working:
	•	Smart contract written in Solidity with a safeMint and buy function
	•	Telegram bot with a simple interface to request NFTs
	•	Limit on how many NFTs can be minted (e.g. 25 total)
	•	Address validation (checks if the wallet is valid)
	•	Logs all errors and important actions to a file
	•	Sends me (admin) a message when someone tries to mint
	•	Uses .env for safe private key storage

Coming soon:
	•	DeepLink feature: a simple website that opens MetaMask and lets the user buy an NFT through their wallet

Why I built this:
I wanted to learn how Solidity smart contracts work, how to interact with them from the backend, and how to use tools like Web3.py and Telegram bots. This project helped me understand how blockchain apps are built and deployed.
