<div align="center">
  <img src="./assets/dojo.png" alt="Dojo Logo" width="300">
  <h1 style="border-bottom: 0">Dojo Subnet</h1>
</div>

<div align="center">
  <a href="https://discord.gg/p8tg26HFQQ">
    <img src="https://img.shields.io/discord/1186416652955430932.svg" alt="Discord">
  </a>
  <a href="https://opensource.org/license/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  </a>
</div>

<br>

<div align="center">
  <a href="https://www.tensorplex.ai/">Website</a>
  ·
  <a href="https://docs.tensorplex.ai/tensorplex-docs/tensorplex-dojo-testnet">Docs</a>
  ·
  <a href="https://docs.tensorplex.ai/tensorplex-docs/tensorplex-dojo-testnet/whitepaper">Whitepaper</a>
  ·
  <a href="https://huggingface.co/tensorplex-labs">HuggingFace</a>
  ·
  <a href="#getting-started">Getting Started</a>
  ·
  <a href="https://twitter.com/TensorplexLabs">Twitter</a>
</div>

---

<details>
<summary>Table of Contents</summary>

- [Introduction](#introduction)
  - [Benefits to participants contributing through Dojo](#benefits-to-participants-contributing-through-dojo)
- [Prerequisites](#prerequisites)
  - [Validator](#validator)
  - [Miner](#miner)
- [System Requirements](#system-requirements)
  - [Miner](#miner-1)
  - [Validator](#validator-1)
- [Getting Started](#getting-started)
  - [Mining](#mining)
    - [Option 1: Self-hosting the miner backend services](#option-1-self-hosting-the-miner-backend-services)
    - [Option 2: Using our hosted Tensorplex backend](#option-2-using-our-hosted-tensorplex-backend)
    - [Setup Subscription Key for Labellers on UI to connect to Dojo Subnet for scoring](#setup-subscription-key-for-labellers-on-ui-to-connect-to-dojo-subnet-for-scoring)
  - [Validating](#validating)
- [Dojo CLI](#dojo-cli)
- [License](#license)

</details>

---

# Introduction

The development of open-source AI models is often hindered by the lack of high-quality human-generated datasets. Closed-source AI developers, aiming to reduce data collection costs, have created significant social and economic equity challenges, with workers being paid less than $2 per hour for mentally and emotionally taxing tasks. The benefits of these models have been concentrated among a select few, exacerbating inequalities among contributors.

Enter Tensorplex Dojo Subnet — an open platform designed to crowdsource high-quality human-generated datasets. Powered by Bittensor, the Dojo Subnet addresses these challenges by allowing anyone to earn TAO by labeling data or providing human-preference data. This approach democratizes the collection of human preference data, addressing existing equity issues and paving the way for more inclusive and ethical AI development.

Key Features

To ensure the quality and integrity of the data collected, Dojo introduces several novel features:

- Synthetic Task Generation: Unique tasks are generated by state-of-the-art Large Language Models (LLMs) to collect human feedback data, which can be used to improve open-source models.
- Synthetic Ground Truth Validation Mechanism: Validators can synthetically generate partial ground truths, allowing them to determine the quality of responses provided by individual participants.
- Obfuscation: Techniques to prevent sybil attacks and ensure contributions are genuinely human.

Use Cases

The Dojo Subnet offers multiple use cases:

- Synthetically Generated Tasks: These tasks can bootstrap the human participant pool and can be used for model training or fine-tuning from the outset.
- Cross-subnet Validation: Validators can use responses to rate the quality of outputs across other Bittensor subnets, thereby incentivizing miners to improve their performance.
- External Data Acquisition: Entities outside the Bittensor ecosystem can tap into the subnet to acquire high-quality human-generated data.

By creating an open platform for gathering human-generated datasets, Tensorplex Dojo Subnet aims to solve the challenges of quality control, human verification, and sybil attack prevention while promoting a more equitable distribution of benefits in AI development.

## Benefits to participants contributing through Dojo

- Open platform: Anyone capable can contribute, ensuring broad participation and diverse data collection.

- Flexible work environment: Participants enjoy the freedom to work on tasks at their convenience from any location.

- Quick payment: Rewards are streamed consistently to participants, as long as they complete sufficient tasks within a stipulated deadline and have them accepted by the subnet.

<br>

# Prerequisites

## Validator

- Python >=3.10
- PM2
- Docker
- Third party API Keys **(Validators Only)**
  - OpenRouter
  - wandb
  - Together **(Optional)**
  - OpenAI **(Optional)**

## Miner

- Python >=3.10
- PM2
- Docker

# System Requirements

## Miner

- 2 cores
- 4 GB RAM
- 32GB SSD

## Validator

- 4 cores
- 8 GB RAM
- 256 SSD

# Getting Started

To get started as a miner or validator, these are the common steps both a miner and validator have to go through.

> The following guide is tailored for distributions utilizing APT as the package manager. Adjust the installation steps as per the requirements of your system.
>
> We will utilize ~/opt directory as our preferred location in this guide.

Install PM2 (**If not already installed**)

```bash
cd dojo/scripts/setup/
./install_pm2.sh
```

Install Docker (**If not already installed**)

```bash
./install_docker.sh
```

Clone the project, set up and configure python virtual environment

```bash
# In this guide, we will utilize the ~/opt directory as our preferred location.
cd ~/opt

# Clone the project
git clone https://github.com/tensorplex-labs/dojo.git
cd dojo/

# Set up python virtual environment and pip packages
# Here we use venv for managing python versions

python3 -m venv env
source env/bin/activate
pip install -e .
# for developers, install the extras
pip install -e ".[dev]"
```

## Mining

### Option 1: Self-hosting the miner backend services

Activate the python virtual environment

```bash
source env/bin/activate
```

Create your wallets and register them to our subnet

```bash
# create your wallets
btcli wallet new_coldkey
btcli wallet new_hotkey

# register your wallet to our subnet
# Testnet
btcli s register --wallet.name coldkey --wallet.hotkey hotkey --netuid 98 --subtensor.network test
```

Create .env file with the following values first

```bash
# copy .env.miner.example
cp .env.miner.example .env
# fill in the following vars
DOJO_API_BASE_URL="http://localhost:8080"
WALLET_COLDKEY=your coldkey wallet name
WALLET_HOTKEY=your hotkey wallet name
AXON_PORT=port to serve requests over the public network for validators to call
```

Start the worker api which will be connected to the CLI later.

```bash
docker compose up -d worker-api
```

Now activate the python environment and run the CLI to generate an API key and subscription key, see [Dojo CLI](#dojo-cli) for usage.

```bash
source env/bin/activate
dojo
```

Grab the API key and add it to your .env file

Now, run the full miner service.

```bash
docker compose up -d miner-testnet
```

### Option 2: Using our hosted Tensorplex backend

Activate the python virtual environment

```bash
source env/bin/activate
```

Create your wallets and register them to our subnet

```bash
# create your wallets
btcli wallet new_coldkey
btcli wallet new_hotkey

# register your wallet to our subnet
# Testnet
btcli s register --wallet.name coldkey --wallet.hotkey hotkey --netuid 98 --subtensor.network test
```

Create .env file with the following values first.

```bash
# copy .env.miner.example
cp .env.miner.example .env

# ENV's that needs to be filled for miners:
DOJO_API_KEY="sk-<KEY>"
DOJO_API_BASE_URL="https://dojo-api-testnet.tensorplex.ai"
```

Retrieve the API Key and Subscription Key with Dojo CLI, see [Dojo CLI](#dojo-cli) for usage.

Start the miner by running the following commands:

```bash
# For Testnet
docker compose up -d miner-testnet
```

### Setup Subscription Key for Labellers on UI to connect to Dojo Subnet for scoring

Note: URLs are different for testnet and mainnet. Please refer to [docs](https://docs.tensorplex.ai/tensorplex-docs/tensorplex-dojo-testnet/official-links).

1. Head to https://dojo-testnet.tensorplex.ai and login and sign with your Metamask wallet.

- You'll see an empty homepage with no Tasks, and a "Connect" button on the top right ![image](./assets/ui/homepage.png)
- Click on "Connect" and you'll see a popup with different wallets for you to connect to ![image](./assets/ui/wallet_popup.jpg)
- Click "Next" and "Continue", then finally it will be requesting a signature from your wallet, please sign and it will be connected. ![image](./assets/ui/wallet_sign.jpg)
- Once connected, the top navigation bar should display your wallet address. ![image](./assets/ui/wallet_connected.png)

2. Once connected, please stay connected to your wallet and click on "Enter Subscription Key". ![image](./assets/subscription/enter_subscription.png)

- Give your subscription a name, and enter your subscription key generated earlier before running the miner. _*Refer to step 4 of "Getting Started" if you need to retrieve your key*_ ![image](./assets/subscription/enter_details.png)
- Click "Create" and your subscription will be saved. ![image](./assets/subscription/created_details.png)
- Confirmed your subscription is created properly, and that you can view your tasks! ![image](./assets/subscription/tasks_shown.png)

## Validating

Copy the validator .env file and set up the .env file

```bash
# copy .env.validator.example
cp .env.validator.example .env

# edit the .env file with vim, vi or nano
DOJO_API_BASE_URL="https://dojo-api-testnet.tensorplex.ai"
SYNTHETIC_API_URL="http://127.0.0.1:5003"
TOKENIZERS_PARALLELISM=true
WANDB_API_KEY="<wandb_key>"

# for dojo-synthetic-api
REDIS_PASSWORD=
REDIS_USER=
OPENROUTER_API_KEY="sk-or-v1-<KEY>"
E2B_API_KEY=

# Other LLM API providers, Optional or if you've chosen it
TOGETHER_API_KEY=
OPENAI_API_KEY=
```

Start the validator

```bash
# start the validator
# Testnet
docker compose up -d validator-testnet
```

To start with autoupdate for validators (**optional**)

```bash
# Testnet
pm2 start run.sh \
--interpreter bash \
--name dojo-autoupdater \
-- --wallet.name coldkey \
--wallet.hotkey hotkey \
--logging.debug \
--subtensor.network test \
--neuron.type validator
```

# Dojo CLI

We provide a CLI that allows miners to manage their API and subscription keys either when connecting to our hosted Tensorplex API services or their own self-hosted miner backend.

Features:

- Tab completion
- Prefix matching wallets

```bash
# Start the dojo cli tool
# Upon starting the CLI it will ask if you wanna use the default path for bittensor wallets, which is `~/.bittensor/wallets/`.
# If you want to use a different path, please enter 'n' and then specify the path when prompted.
dojo

# TIP: During the whole process, you could actually use tab-completion to display the options, so you don't have to remember them all. Please TAB your way guys! 🙇‍♂️
# It should be prompting you to enter you coldkey and hotkey
# After entering the coldkey and hotkey, you should be in the command line interface for dojo, please authenticate by running the following command.
# You should see a message saying "✅ Wallet coldkey name and hotkey name set successfully."
authenticate

# Afterwards, please generate an API Key with the following command.
# You should see a message saying:  "✅ All API keys: ['sk-<KEY>]". Displaying a list of your API Keys.
api_key generate

# Lastly, please generate a Subscription Key with the following command.
# You should see a message saying:  "✅ All Subscription keys: ['sk-<KEY>]". Displaying a list of your Subscription Keys.
subscription_key generate

# :rocket: You should now have all the required keys, and be able to start mining.

# Other commands available to the CLI:
# You can always run the following command to get your current keys.
api_key list
subscription_key list

# You can also delete your keys with the following commands.
api_key delete
subscription_key delete
```

# License

This repository is licensed under the MIT License.

```text
# The MIT License (MIT)
# Copyright © 2023 Yuma Rao

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
```
