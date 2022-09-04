sudo apt-get install apt-transport-https curl
sudo curl -o /etc/apt/trusted.gpg.d/mariadb_release_signing_key.asc 'https://mariadb.org/mariadb_release_signing_key.asc'
sudo sh -c "echo 'deb https://tw1.mirror.blendbyte.net/mariadb/repo/10.10/ubuntu jammy main' >>/etc/apt/sources.list"
sudo apt-get update
sudo apt-get install mariadb-server
