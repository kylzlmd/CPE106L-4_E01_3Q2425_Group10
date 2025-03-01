# CPE106L-4_E01_3Q2425_Group10

## Project Installation Guide

### 1. Setting Up the Virtual Environment
Open a terminal and navigate to your project directory, then run:
```bash
python3 -m venv venvs
source venvs/bin/activate
```

### 2. Installing Dependencies
Install the required Python packages:
```bash
pip install flet==0.19.0
pip install uvicorn
pip install "fastapi[standard]"
```

### 3. Installing Additional Tools
Install `curl` (if not already installed):
```bash
sudo apt install -y curl
```

---

## Installing Mongosh (MongoDB Shell)
Mongosh allows you to interact with MongoDB outside the terminal.

### **For Ubuntu Jammy (22.04)**
```bash
wget -qO- https://www.mongodb.org/static/pgp/server-8.0.asc | sudo tee /etc/apt/trusted.gpg.d/server-8.0.asc

echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list

sudo apt-get update

sudo apt-get install -y mongodb-mongosh
sudo apt-get install -y mongodb-mongosh-shared-openssl11
sudo apt-get install -y mongodb-mongosh-shared-openssl3

mongosh --version
```

### **For Ubuntu Noble (24.04)**
```bash
wget -qO- https://www.mongodb.org/static/pgp/server-8.0.asc | sudo tee /etc/apt/trusted.gpg.d/server-8.0.asc

echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list

sudo apt-get update

sudo apt-get install -y mongodb-mongosh
sudo apt-get install -y mongodb-mongosh-shared-openssl11
sudo apt-get install -y mongodb-mongosh-shared-openssl3

mongosh --version
```

---

### 4. Installing Flet (Again, if needed)
```bash
pip install flet==0.19.0
```

Now, your project should be fully set up and ready to use.
