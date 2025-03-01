# 🌱 Seedie Project - Installation Guide

Welcome to the **Seedie Project**!  
All installation files are located in **`PROJ/FletApp`**.

---

## 📌 1. Setting Up the Virtual Environment  
Open a terminal and navigate to the **FletApp** directory:  

```bash
cd PROJ/FletApp
python3 -m venv venvs
source venvs/bin/activate
```

---

## 📌 2. Installing Dependencies  
Install the required Python packages:

```bash
pip install flet==0.19.0
pip install uvicorn
pip install "fastapi[standard]"
```

---

## 📌 3. Installing Additional Tools  

If you need `curl`, install it with:

```bash
sudo apt install -y curl
```

---

## 📌 4. Installing Mongosh (MongoDB Shell)  [OPTIONAL!!!!]

### 🔹 For Ubuntu Jammy (22.04)  

```bash
wget -qO- https://www.mongodb.org/static/pgp/server-8.0.asc | sudo tee /etc/apt/trusted.gpg.d/server-8.0.asc
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list
sudo apt-get update
sudo apt-get install -y mongodb-mongosh mongodb-mongosh-shared-openssl11 mongodb-mongosh-shared-openssl3
mongosh --version
```

### 🔹 For Ubuntu Noble (24.04)  

```bash
wget -qO- https://www.mongodb.org/static/pgp/server-8.0.asc | sudo tee /etc/apt/trusted.gpg.d/server-8.0.asc
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list
sudo apt-get update
sudo apt-get install -y mongodb-mongosh mongodb-mongosh-shared-openssl11 mongodb-mongosh-shared-openssl3
mongosh --version
```

---

## 📌 5. Running the Application  

Once everything is installed, you can run the app using:  

```bash
python seedApp.py
```

Now, you're all set to start using **Seedie Project**! 🚀  
