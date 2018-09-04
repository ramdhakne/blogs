#! /bin/sh
# Install cbc-* tools typically on container nodes running in k8s.
# [TIP] Can be used anywhere if tools are required (VM/Physical Machine, install steps
# are same)
# 
# This is for ubuntu OS 
# Short description: cb tools container/pods install script
# 
apt-get update
apt install -yq --reinstall base-files lsb-release lsb-base
wget http://packages.couchbase.com/releases/couchbase-release/couchbase-release-1.0-4-amd64.deb
dpkg -i couchbase-release-1.0-4-amd64.deb
apt-get install -yq libcouchbase-dev libcouchbase2-bin build-essential
apt-get install -yq vim
rm -f couchbase*.deb*
