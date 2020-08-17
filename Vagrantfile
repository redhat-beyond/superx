# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"	  
  # Flask
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  # config.vm.network "private_network", ip: "192.168.33.10"
  config.vm.provider "virtualbox" do |vb|
vb.name = "superx"
end
config.vm.provision "shell", path: "bootstrap.sh", privileged: false
end