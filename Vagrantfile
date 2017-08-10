# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.provision "shell", inline: <<-SHELL
    VAGRANT_HOME=/home/vagrant

    apt-get update

    apt-get install -y python3-pip
    pip3 install -r /vagrant/requirements.txt

    apt-get install -y zsh

    su vagrant

    wget --quiet https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | sh
    wget --quiet https://raw.githubusercontent.com/Bookmark-Novels/Resources/master/Configuration%20Files/.zshrc -O $VAGRANT_HOME/.zshrc
    chsh -s /bin/zsh vagrant
    zsh
  SHELL
end
