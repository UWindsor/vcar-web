# This script was taken from https://github.com/railsgirls/installation-scripts and modified to meet the needs of the vcar-web project

set -e

echo "Installs Homebrew for installing other software"
/usr/bin/ruby -e "$(/usr/bin/curl -fsSkL raw.github.com/mxcl/homebrew/go)"

echo "Installs Git"
brew install git

echo "Updates Homebrew"
brew update


echo "Installs RVM (Ruby Version Manager) for handling Ruby installation"
curl -kL get.rvm.io | bash -s stable
source ~/.rvm/scripts/rvm

echo "Install Ruby"
rvm install 2.7.0
rvm use 2.7.0 --default

gem install bundler
gem install rails

echo -e "\n- - - - - -\n"
echo -e "Now we are going to print some information to check that everything is done:\n"

echo -n "Should be brew 0.8 or higher:       brew "
brew -v
echo -n "Should be git 1.7.7 or higher:           "
git --version
echo -n "Should be sqlite 3.7.3 or higher: sqlite "
sqlite3 --version
echo -n "Should be rvm 1.6.32 or higher:          "
rvm --version | sed '/^.*$/N;s/\n//g' | cut -c 1-10
echo -n "Should be ruby 2.7.0:                "
ruby -v | cut -d " " -f 2
echo -n "Should be Rails 6.0.1 or higher:         "
rails -v
echo -e "\n- - - - - -\n"

echo "If the versions match, everything is installed correctly. If the versions
don't match or errors are shown, something went wrong with the automated process
and we will help you do the installation the manual way at the event.
Congrats!"

echo "Now we install specific gems and setup database for the vcar-web application."
echo "Installing gems..."
bundle install

echo "Preparing database..."
rails db:setup
