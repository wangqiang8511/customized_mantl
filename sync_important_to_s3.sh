#!/usr/bin/env sh


mkdir -p important

cp -r ssl important/

cp_if_exisit() {
	if [ -f $1 ]
	then
		cp $1 important/
	fi
}

cp_if_exisit cluster.yml
cp_if_exisit security.yml
cp_if_exisit infra_ansible.yml
cp_if_exisit terraform.tfstate
cp_if_exisit terraform.tfstate.backup

aws s3 cp important $1 --recursive
