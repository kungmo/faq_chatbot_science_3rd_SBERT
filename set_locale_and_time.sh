sudo apt install language-pack-ko
sudo locale-gen ko_KR.UTF-8
sudo dpkg-reconfigure locales
sudo update-locale LANG=ko_KR.UTF-8 LC_MESSAGES=POSIX
sudo timedatectl set-timezone Asia/Seoul
sudo timedatectl
