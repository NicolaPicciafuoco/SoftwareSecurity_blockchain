# Healthcare Application


## Table of Contents

- [Introduction](#introduction)
  - [Main Features](#main-features)
  - [How it Works](#how-it-works)
  - [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [Linux](#linux)
    - [Windows](#windows)
    - [macOS](#macos)
- [Usage](#usage)
  - [Running the Server](#running-the-server)
    - [Database Setup](#db-setup)
      - [Migrations](#migrations)
      - [Seeding](#seeding)
  - [Troubleshooting](#troubleshooting)
    - [Creating a Super User](#creating-a-super-user)
    - [Node Explorer](#node-explorer)
    - [Logs](#logs)
- [Credits](#credits)

## Introduction

This Healthcare application has been developed to harness the power of blockchain technology, more specifically
to ensure data integrity, security and privacy.

### Main Features

The application is designed to be used both by healthcare professionals and patients and/or their caregivers.
Some of the main features include:

- Checking the patient's medical history.
- Saving and modifying medical reports and services securely
- Checking the integrity of the saved data

All of this is achieved through the use of a private blockchain network and a smart contract, to ensure maximum security
and guarantee data integrity and safety for the end user.

### How it Works

Every user has a unique blockchain address and a private key, which are used to sign and verify the transactions.
Every time a new medical report or service is saved, a new transaction is created and signed by the user.

On the blockchain, the addresses of both the healthcare professional and the patient are stored in a smart contract, 
along with a hashed version of the data.

Every time a user tries to access the data, the smart contract checks the integrity of the data by comparing the
local hash with the one stored on the blockchain.

### Technologies Used

The Healthcare application is built using the following technologies:

- [Python](https://www.python.org/) as the main programming language
- [Django](https://www.djangoproject.com/) as the web framework
- [Gunicorn](https://gunicorn.org/) as the WSGI server
- [Nginx](https://www.nginx.com/) as the reverse proxy server
- [Hyperledger Besu](https://www.hyperledger.org/use/besu) for the blockchain network
- [ConsenSys Tessera](https://docs.tessera.consensys.io/) for private transact
- [Solidity](https://soliditylang.org/) for smart contract development
- [Web3.py](https://web3py.readthedocs.io/en/stable/) for interacting with the smart contracts
- [Docker](https://www.docker.com/) and [Compose](https://docs.docker.com/compose/) for containerization
- [PostgreSQL](https://www.postgresql.org/) as the database

## Getting Started

In order to run a local copy of the application, you need to follow the steps below.
  
### Prerequisites

The only real prerequisite needed for the project is to have a working installation of Docker and Docker Compose.
Based on your operating system, you can install Docker following [this link](https://www.docker.com/get-started/).

Otherwise, you can always install [Docker Desktop](https://www.docker.com/products/docker-desktop) for the GUI version.

To install Docker Compose, you can follow the instructions [here](https://docs.docker.com/compose/install/).

As far as hardware requirements go, running the blockchain network can be quite resource-intensive.
The application has been successfully tested on a machine with 8 GB of RAM and 4 cores, but performances may vary.

> :warning: **NOTE**: The official Quorum Dev article recommends to limit Docker's memory usage to 6GB when
> working with the blockhain. The method for doing this varies greatly based on the operating system.
> It is up to the user to decide whether to limit Docker's memory usage or not.

### Installation

The easiest way to install the application is to clone the repository on your local machine:

```bash
git clone https://github.com/NicolaPicciafuoco/SoftwareSecurity_blockchain
cd SoftwareSecurity_blockchain
```

Once cloned, you can build the images using Docker commands:

```bash
docker-compose build 
```

After successfully building the images, you should setup the environment variables.

In order to do so, place a `.env` file in the root directory and fill in the following variables:

- ```DATABASE_NAME```: the name for the database
- ```DATABASE_USER```: the name for the database user
- ```DATABASE_PASSWORD```: the password for the database user
- ```DATABASE_HOST```: the host for the database. 
Should be the same name as the PostgreSQL container in the `docker-compose.yaml` file. 
Default name should be `my-postgres`.
- ```DATABASE_PORT```: the port on which the database will run. 
Recommended to use the default PostgreSQL port `5432`.
Be sure to check that the port is not already in use and that it is able to accept TCP/IP connections.
- ```ADMIN_ADDRESS```: the blockchain address of the admin user.
Since this is a private blockchain network, the address is purely arbitrary.
- ```ADMIN_PRIVATE_KEY```: the private key of the admin user. Same as above, the key is arbitrary.
- ```LOG4J_CONFIGURATION_FILE```: the path to the log4j configuration file. 
Needed for besu to run properly.
Default path should be `/config/log-config.xml`.

#### Linux

The application has been tested and has been designed to run on Linux machines, and it is recommended to use a Linux distribution 
to run it.

More specifically, the application has been tested on these distributions:

- [EndeavourOS](https://endeavouros.com/)
- [Arch Linux](https://archlinux.org)
- [Ubuntu](https://ubuntu.com/).

#### Windows

The application has been tested both on Windows 10 and Windows 11, and it should work on both.

However, several problems may arise if you choose to run it on a Windows machine, especially with the blockchain network.

> :warning: **NOTE**: It is **heavily** recommended to have the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install) installed on your machine
> and to have Docker configured to use WSL2 as the default engine.

> :warning: **NOTE**: The official Besu Docker image should not run on Windows, as per its [documentation](https://besu.hyperledger.org/private-networks/get-started/install/run-docker-image).
> Despite this, all tests have worked succesfully on Windows machines.
> It is **still** recommended not to run the application on Windows.

#### macOS

The application has **NOT** been tested on macOS machines, neither on Intel nor ARM architectures.

Despite this, the application **should** still run on Mac, if the prerequisites are met.

## Usage

Once the setup has been completed, you can follow the steps below to get the application up and running.

### Running the Server

To run the application, simply run the respective Docker command:

```bash
docker-compose -p NAME up 
```

where `NAME` is the name you want to give to the project containers.

When you run the application for the first time, before you can access the application proper, 
you will need to wait for the deployment of the smart contract on the blockchain. 
This process can take up to a few minutes to complete.

> :warning: **NOTE**: Sometimes the smart contract is deployed twice on two separate adresses.
> This is harmless, as one of the two contracts will never get used by the application.

After the contract setup is complete, you should be able to access the application landing page on `http://localhost:1337`.

> :warning: **NOTE**: It is recommended to use Firefox as the preferred browser to access the application.
> This is due to some quirks with the request handling on Safari and Chromium-based browsers.
> Aside from that, all other features still work perfectly fine on the aforementioned browsers.

#### Database Setup

When the server has finished the deploy process and is ready to go, you need to setup the database.

##### Migrations

To run database migrations, you need to access the terminal in the `web` container:

```bash
docker-compose -p NAME exec web bash 
```

Once you've accessed the container terminal, you can proceed to run the commands.

First, you need to create the migration files using `manage.py`:

```bash
python manage.py makemigrations
```

To effectively run the migrations:

```bash
python manage.py migrate
```

##### Seeding

It is recommended to seed the database to setup the appropriate role permissions.
Seeding also sets up a few default users to test the application with.

```bash
python manage.py populate_db
```

Alternatively, you can run the above commands directly without accessing the container shell 
by using`docker-compose exec web <command>`.

### Troubleshooting

If you encounter any problems while running the application, 
you can follow the steps below to troubleshoot it.

#### Creating a Super User

In order to test out the server, you might want to create a Django super user to better debug the application.

To do so, access the `web` shell like in the above section and run the following command:

```bash
python manage.py createsuperuser
```

The user's parameters can be inserted as optional parameters while running the command, otherwise the program will ask
for them gradually. The parameters are as follows:

- `--email`: the superuser's email. Used for login.
- `--nome`: the superuser's name.
- `--cognome`: the superuser's surname.
- `--sesso`: the superuser's sex. Can be `0` (male) or `1` (female).
- `--data-nascita`: the superuser's birthdate. Follows the `YYYY-MM-MM` format.
- `--luogo-nascita`: the superuser's birthplace.
- `--indirizzo-residenza`: the superuser's home address.

Once prompted to choose a password, you can choose not to follow the standard requirements.

#### Node Explorer

To access the Hyperledger Besu node explorer, you can use the following URL:

```
http://localhost:25000
```

If you want to check the status of the blocks, transactions and deployed contracts, 
Explorer has an appropriate section, available at the following URL:

```
http://localhost:25000/explorer/explorer
```

#### Logs

Besu and Tessera logs can be found under `/besu-network/logs/`.
They contain information about the various instances of the blockchain and the signing of the transactions.

## Credits

This project has been developed as part of the Software Security and Blockchain course, held by Prof. Luca Spalazzi 
at the Università Politecnica delle Marche in Ancona, Italy.

The project has been developed by the following students:

- [Nicola Picciafuoco](https://github.com/NicolaPicciafuoco)
- [Alessandro Rossini](https://github.com/oathbound01)
- [Francesco Parisi](https://github.com/FrancescoParisi02)
- [Andrea Fiorani](https://github.com/125ade)
