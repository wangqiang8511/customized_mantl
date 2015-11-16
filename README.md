This is mirror of [MANTL](https://github.com/CiscoCloud/microservices-infrastructure)

# Changes from the original repo:

* instance group, separate coordination services with mesos
  Now have control, master, worker
* use ubuntu as base
* mainly focus on aws

# Setup the the infra

* Make sure you have following package installed

  * ansible
  * terraform

* Clone the code

* Run env setup

```bash
$ make buildenv
```

* Config you cluster 

```bash
cp infra.sample.yml infra.yml
# Modify infra.yml accordingly
```

* Run setup scripts

```bash
$ source bin/activate
$ ./security-setup
$ ./flocker-security-setup $YOUR_CLUSTER_NAME
$ python infra/infra-setup.py infra.yml
```

* Setup infra with terraform

```bash
$ terraform get
$ terraform plan
$ terraform apply
```

* Provisioning your infra with ansible

```bash
ansible-playbook \
  -i plugins/inventory/terraform.py \
  -e @security.yml \
  -e @cluster.yml \
  infra_ansible.yml 
```

# Destroy created infra

```bash
$ terraform destroy
```
