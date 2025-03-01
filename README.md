# CPE106L-4_E01_3Q2425_Group10 and Project Instructions

Lab Report Codes and Project
The Lab Report Codes are named "LR" folders.

For the installation of the Project...

Open a directory
python3 -m venv venvs
source venvs/bin/activate

pip install flet==0.19.0

pip install uvicorn

pip install "fastapi[standard]"

sudo apt install -y curl





Installing Mongosh, if you wanna see databases outside terminal
For Jammy:

wget -qO- https://www.mongodb.org/static/pgp/server-8.0.asc | sudo tee /etc/apt/trusted.gpg.d/server-8.0.asc



echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list



sudo apt-get update



sudo apt-get install -y mongodb-mongosh



sudo apt-get install -y mongodb-mongosh-shared-openssl11



sudo apt-get install -y mongodb-mongosh-shared-openssl3



mongosh --version



For Noble:

wget -qO- https://www.mongodb.org/static/pgp/server-8.0.asc | sudo tee /etc/apt/trusted.gpg.d/server-8.0.asc



echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list



sudo apt-get update



sudo apt-get install -y mongodb-mongosh



sudo apt-get install -y mongodb-mongosh-shared-openssl11



sudo apt-get install -y mongodb-mongosh-shared-openssl3



mongosh --version




pip install flet==0.19
