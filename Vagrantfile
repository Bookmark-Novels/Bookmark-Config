# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-16.04"

  config.vm.provision "shell", inline: <<-SHELL
    VAGRANT_HOME=/home/vagrant

    apt-get update

    apt-get install -y python3-pip
    pip3 install -r /vagrant/requirements.txt

    apt-get install -y zsh

    wget --quiet https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | sh
    wget --quiet https://gist.githubusercontent.com/xfanwu/18fd7c24360c68bab884/raw/f09340ac2b0ca790b6059695de0873da8ca0c5e5/xxf.zsh-theme -O $VAGRANT_HOME/.oh-my-zsh/themes/xxf.zsh-theme
    wget --quiet https://raw.githubusercontent.com/Bookmark-Novels/Resources/master/Configuration%20Files/.zshrc -O $VAGRANT_HOME/.zshrc
    chsh -s /bin/zsh vagrant
    zsh
  SHELL
end
