#!/bin/bash

# This script was taken from https://github.com/railsgirls/installation-scripts and modified to meet the needs of the vcar-web project. Made for Ubuntu but hopefully works well on other distributions

if
  [[ "${USER:-}" == "root" ]]
then
  echo "This script works only with normal user, it wont work with root, please log in as normal user and try again." >&2
  exit 1
fi

set -e

echo "Updates packages. Asks for your password."
sudo apt-get update -y

echo "Installs Node 10"
sudo apt-get install -y snapd
sudo snap install node --classic --channel=10

echo "Installs packages. Give your password when asked."
sudo apt-get --ignore-missing install build-essential git-core curl openssl libssl-dev libcurl4-openssl-dev zlib1g zlib1g-dev libreadline6-dev libyaml-dev libsqlite3-dev libsqlite3-0 sqlite3 libxml2-dev libxslt1-dev libffi-dev software-properties-common libgdm-dev libncurses5-dev automake autoconf libtool bison postgresql postgresql-contrib libpq-dev pgadmin3 libc6-dev -y

echo "Installs ImageMagick for image processing"
sudo apt-get install imagemagick --fix-missing -y

echo "Installs RVM (Ruby Version Manager) for handling Ruby installation"
# Retrieve the GPG key.
curl -sSL https://rvm.io/pkuczynski.asc | gpg --import -
curl -sSL https://get.rvm.io | bash -s stable
source ~/.rvm/scripts/rvm

# Version used in vcar-web
echo "Installs Ruby"
rvm install 2.4.2
rvm use 2.4.2 --default

echo "gem: --no-ri --no-rdoc" > ~/.gemrc
gem install rails

echo "===> Installing bundler"
gem install bundler

echo -e "\n- - - - - -\n"
echo -e "Now we are going to print some information to check that everything is done:\n"


echo -n "Should be sqlite 3.22.0 or higher: sqlite "
sqlite3 --version
echo -n "Should be rvm 1.29.8 or higher:         "
rvm --version | sed '/^.*$/N;s/\n//g' | cut -c 1-11
echo -n "Should be ruby 2.4.2:                "
ruby -v | cut -d " " -f 2
echo -n "Should be Rails 5.2.3 or higher:         "
rails -v
echo -e "\n- - - - - -\n"

echo "If the versions match, everything is installed correctly. If the versions
don't match or errors are shown, something went wrong with the automated process
and we will help you do the installation the manual way at the event.
Congrats!
Make sure that all works well by running the application generator command:
    $ rails s
If you encounter the message:
    The program 'rails' is currently not installed.
It is just a hiccup with the shell, solutions:
    $ source ~/.rvm/scripts/rvm
    Allow login shell, example http://rvm.io/integration/gnome-terminal/"

echo "Now we install specific gems and setup database for the vcar-web application."
echo "Installing gems..."
bundle install

echo "Preparing database..."
rails db:setup
