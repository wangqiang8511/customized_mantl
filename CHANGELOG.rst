Changelog
=========

0.3.2 (June 30, 2015)
---------------------

Features
^^^^^^^^

* Add Minecraft sample app #506
* Add documentation for all components that were missing it #520
* Add ElasticSearch output for Logstash #524 (see ``logstash_output_elasticsearch`` in :doc:`components/logstash`)
* Add filesystem-backed Marathon artifact store #525

Fixes
^^^^^

* Update docs to clarify required Python version #515
* Fix typo in the Nginx proxy setup for Mesos #521
* Explicitly specify PyYAML version in ``requirements.txt``
* Support SSH key passphrase and any key name in the Docker builder #517

0.3.1 (June 17, 2015)
---------------------

Features
^^^^^^^^

* Add Distributive system checker #434
* Add Chronos role  #437
* Add DigitalOcean terraform provider #449
* Add VMware vSphere terraform provider #471
* Support for terraform in Dockerfile #481

Fixes
^^^^^

* Use default security group in OpenStack #477
* Allow ``terraform.py`` to use configurable usernames #491
* Change "disable security" to "check security" in ``security-setup`` #494
* Stop logstash variables from showing up as a top-level component in docs #482

0.3.0 (June 8, 2015)
--------------------

Features
^^^^^^^^

* Performance + usage metrics Linux + Mesos + Marathon + Containers #53
* Multi OpenStack region support in Atlas (TF) #61
* Rotate all logs daily and perge weekly #158
* Add additional confirmation prompt for password in security-setup #173
* Make security-setup flags more granular #239
* Make Consul domain name configurable #100 & #156
* Deploy logstash 1.5 container to all nodes with rsyslog input and output support #164
* Enable mesos resource configurations for followers #194
* Generate SHA256 signed CA/certs by default #213
* Add support for Hashicorp Vault #225
* Add coarse-grained options to security-setup #247
* Improve readability of ``security-setup --help`` #248
* Add mesos-consul support #251
* Remove registrator for mesos-consul #263 
* Create a local host file #146
* Bootstrap Vagrant box with just 'git clone && vagrant up' #254
* Remove Registrator #255
* Clean up security-setup options #258 
* Operationalize Zookeeper #259
* Add GCE support #260
* Add AWS support #261
* Upgrade Consul to 0.5.2 #304
* Implement Consul ACL upserts #266
* Explicitly version project packages and containers #276
* Add marathon-consul support #264
* Add Logstash role #275
* Add Consul service active check script #287
* Add metadata to hosts in Openstack #290
* Update usage of argparse #296
* Move to ciscocloud/mesos-consul container #333
* Add collectd to system #335
* Remove NetworkManger dependency for dnsmasq #330
* Add Mesos collectd plugins #347
* Add docker collectd plugin. #352
* Use Consul DNS instead of .novalocal #363
* Allow different OpenStack flavors in terraform #367
* Use versioned haproxy container #369
* Add support to configure mesos-consul refresh #372
* Create OpenStack and Google Compute Engine clusters with Terraform #336
* Remove OpenStack-specific requirements and playbooks in favor of Terraform provisioning #402
* Remove ansible OpenStack playbook dependency #414
* Make logstash grab logs from ZooKeeper data volume #435
* Include collectd, logstash role in terraform sample playbook #438
* Use ``ciscocloud/logstash:0.2`` for logstash container #443
* Add command line argument for hostname to ``zookeeper-wait-for-listen.sh`` #416

Fixes
^^^^^

* Note Vagrant provider requirement #170
* Fix dnsmasq host #188
* Disable firewalld #193
* Have awk read /proc/uptime directly #216
* security-setup now uses proper common names #228
* serialize Consul restarts #262
* Remove use of sudo for local file modification #272
* Use CiscoCloud data volume for zookeeper container #282
* Consul requires restart on ``acl_master_token`` change #283
* Fix Vault restart #231
* Fix issue with Consul restart #293
* Fix Marathon race #305
* Ansible doesn't wait for Vault port to open #306
* Wait for Vault port to open #307
* Fix for "install nginx admin password" task in Consul role #313
* nginx update #317
* Updated Ansible version constraint #321
* Add ssl args to the haproxy container #370
* added openssh to image #341
* Remove ansible openstack playbooks. Fixes #402 #411
* remove inventory #424
* Bug in ansible collectd role #431
* authorize logstash syslog port when selinux enforcing #459

Deprecations
^^^^^^^^^^^^

* microservices-infrastructure now uses `Terraform <https://terraform.io>`_ for
  provisioning hosts, and `terraform.py
  <https://github.com/CiscoCloud/terraform.py>`_ instead of inventory files.
  Because of this change, you will need to use the new :doc:`Terraform-based
  Getting Started Guide </getting_started/index>`.

0.2.0 (April 10, 2015)
----------------------

Features
^^^^^^^^

* Security added across the board
* Moved Consul out of docker #66
* Added authentication & ssl support for marathon #67
* Add mesos-authentication #45
* Add haproxy role to dynamically configure haproxy from Consul. #42
* Add TLS to Consul #46
* Add basic ACL support to Consul
* Add Consul agent_token support
* Add Haproxy container #42, #48
* Add authentication setup script #65
* Add Zookeeper authentication and ACLs for mesos #86
* Add nginx proxy to authentiate Consul UI
* Removed hardcoding of marathon to 0.7.6
* Move Consul to install via rpm #90
* auth-setup: openssl has to prompt user #99
* Ease of use enhancements for security-setup #109
* Need to update example/hello-world to support Marathon auth #112
* Automatically redirect http requests to https #113
* security-setup refinements #128
* Use Centos docker package #141
* Move openstack security group to a variable #155

Fixes
^^^^^
* Mesos & Marathon Consul registration do not survive reboot #16
* Set preference for virtualbox provider for owners of vmware_fusion #73
* Fix Consul clients #30
* Remove consul-ui from agent nodes #93
* OpenSSL certificate fixes #95
* Fix ansible inventory metadata #96
* Deprecated checkpoint flag prevents mesos-slave startup #105
* Consul UI unavailable #111
* Networkmanager removing 127.0.0.1 from /etc/resolv.conf #122
* Consul "Failed connect to 127.0.0.1:8080; Connection refused" #131
* Remove duplicate definition of marathon_servers #101 
* Running reboot-hosts.yml causes Consul to lose quorum #132
* Missing or incorrect information in getting started documents #133
* Numerous other bug fixes
* Docker fails to start when using latest Docker RPM without latest CentOS7 updates #161
* Fix documentation for security group ports #154
* Security-setup script hangs on low entropy linux hosts due to /dev/random bug #153


0.1.0 (March 2, 2015)
---------------------

- Initial release.

Ansible Roles 
^^^^^^^^^^^^^

* Add common role for timezones, users and resolv.conf
* Add consul role
* Add dnsmasq role
* Add registrator role
* Add mesos-leader role
* Add mesos-follower role
* Add marathon role
* Add zookeeper role
* Add documentation

Ansible Playbooks
^^^^^^^^^^^^^^^^^

* Add consul-join-wan
* Add destroy-hosts
* Add provision-consul-gossip-key
* Add provision-hosts
* Add provision-nova-key
* Add reboot-hosts
* Add show-containers
* Add show-package-drift
* Add show-uptime
* Add trace-consul-wan-traffic
* Add upgrade-packages
