# bible_trivia

## Bible Trivia Web Application
A web application that provides a Bible trivia game, built using a modern tech stack including MySQL, FastAPI, and Docker Compose. This README will guide you through setting up the project on your local machine.


---

## Table of Contents

- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Setting Up the Environment Variables](#setting-up-the-environment-variables)
- [Setup Instructions](#setup-instructions)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Navigate to the Project Directory](#2-navigate-to-the-project-directory)
  - [3. Create the `.env` File](#3-create-the-env-file)
  - [4. Configure the `.env` File](#4-configure-the-env-file)
  - [5. Build and Run the Application](#5-build-and-run-the-application)
- [Accessing the Application](#accessing-the-application)
- [Stopping the Application](#stopping-the-application)
- [Troubleshooting](#troubleshooting)
- [Security Considerations](#security-considerations)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---


## Project Overview
This project is a Bible trivia web application consisting of:

- Database: MySQL 8.0
- Backend: FastAPI (Python)
- Frontend: FastAPI (Python)
- Database Management: phpMyAdmin
- Docker Compose: Orchestrates the multi-container application
- Dynamic DNS: Duck DNS service to handle dynamic IP addresses


---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)
- **Git**: [Install Git](https://git-scm.com/downloads)

---


## Setting Up the Environment Variables

The application requires certain environment variables to be set for configuration. These variables are stored in a `.env` file in the root directory of the project.

---

## Setup Instructions

### 1. Clone the Repository

Clone the project repository to your local machine:

```bash
git clone https://github.com/yourusername/bible-trivia.git
```

---

### Navigate to the Project Directory

```bash
cd bible-trivia
```

---

### Create the .env File

Create a file named .env in the root directory of the project:
```bash
touch .env
```

---

### Configure the .env File

Open the .env file in a text editor and add the following content:

```dotenv
# MySQL Database Configuration
MYSQL_ROOT_PASSWORD="admin"
MYSQL_USER="db_user"
MYSQL_PASSWORD="db_password"
SECRET_KEY="SECRET_KEY"

# Database URL
DATABASE_URL="mysql+pymysql://db_user:db_password2408@db:3306/bible_trivia_db"

# Website Admin Credentials
ADMIN_USERNAME="admin"
ADMIN_EMAIL="admin@example.com"
ADMIN_PASSWORD="admin123"

# Duck DNS Configuration
DUCKDNS_TOKEN="your_duckdns_token"
DUCKDNS_DOMAIN="bible-trivia"

# Network Configuration
NETWORK_SUBNET=172.21.0.0/16
NETWORK_GATEWAY=172.21.0.1
NETWORK_IPV4_ADDRESS_DB=172.21.0.2
NETWORK_IPV4_ADDRESS_PHP=172.21.0.3
NETWORK_IPV4_ADDRESS_BACKEND=172.21.0.4
NETWORK_IPV4_ADDRESS_FRONTEND=172.21.0.5
NETWORK_IPV4_ADDRESS_INIT_DB=172.21.0.6
NETWORK_IPV4_ADDRESS_DUCKDNS=172.21.0.7


```
---

#### Import Notes:

- MySQL Credentials: Set strong passwords for MYSQL_ROOT_PASSWORD and MYSQL_PASSWORD.
- SECRET_KEY: Replace "SECRET_KEY" with a securely generated secret key.
- Admin Credentials: Set the admin username, email, and password for the web application.
- Duck DNS Token: Obtain your Duck DNS token and replace "your_duckdns_token" with it.
- Duck DNS Domain: Ensure that DUCKDNS_DOMAIN matches the subdomain you have registered with Duck DNS.

---

#### Obtaining Duck DNS Token
- Go to Duck DNS.
- Sign in using one of the available options (Google, GitHub, Twitter, Reddit).
- Once logged in, you will see your token at the top of the page.
- Copy the token and paste it into your .env file as the value for DUCKDNS_TOKEN.

---

### Build and Run the Application
Run the following command to build and start all the services defined in the docker-compose.yml file:

```bash
docker-compose up -d --build
```
- -d: Runs the containers in detached mode.
- --build: Builds images before starting containers.

---

### Accessing the Application
Once all the services are up and running, you can access the application components via the following URLs:

- Frontend Application: http://localhost
- Backend API (Swagger UI): http://localhost:8000/docs
- phpMyAdmin: http://localhost:8080

Note: If you're accessing the application from another device or over the internet, replace localhost with your machine's IP address or your Duck DNS domain (bible-trivia.duckdns.org).

---

### Stopping the Application
To stop and remove all running containers, networks, and volumes created by docker-compose up:

```bash
docker-compose down
```
---

### Security Considerations
- Protect Sensitive Data: Do not commit the .env file to any public repositories. Add it to your .gitignore file.
- Use Strong Passwords: Ensure all passwords and secret keys are strong and securely generated.
- Firewall Settings: If hosting the application over the internet, configure your firewall to allow only necessary traffic.
- SSL/TLS Encryption: For secure connections, consider setting up HTTPS using Let's Encrypt certificates.


---

### License
This project is licensed under the MIT License.

---