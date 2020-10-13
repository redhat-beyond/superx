# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/bionic64"
    # Flask
    config.vm.network "forwarded_port", guest: 5000, host: 5000
    config.vm.provider "virtualbox" do |vb|
      vb.name = "super"
    end
config.vm.provision "shell", path: "bootstrap.sh", run: "always"
end
