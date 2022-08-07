sudo apt install wget

wget https://dlm.mariadb.com/enterprise-release-helpers/mariadb_es_repo_setup

echo "957bc29576e8fd320fa18e35fa49b5733f3c8eeb4ca06792fb1f05e089c810ff mariadb_es_repo_setup" | sha256sum -c -

chmod +x mariadb_es_repo_setup

sudo ./mariadb_es_repo_setup --token="customer_download_token" --apply \
   --mariadb-server-version="10.5"

sudo apt update

sudo apt install libmariadb3 libmariadb-dev

pip3 install mariadb
