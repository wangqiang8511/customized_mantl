Mesos
=====

.. versionadded:: 0.1

`Mesos <https://mesos.apache.org/>`_ is the distributed system kernel that
manages resources across multiple nodes. When combined with :doc:`marathon`, you
can basically think of it as a distributed init system.

Modes
-----

Mesos can be run in one of two "modes":

 - A server mode (called "master" or "leader")
 - A client mode (called "slave" or "follower")

Variables
---------

You can use these variables to customize your Mesos installation.

.. data:: mesos_mode

   Set to ``master`` for master mode, and ``slave`` for slave mode. 

.. data:: zk_hosts

   Zookeeper hosts, in format of "zk://host1:port1,host2:port2,host3:port3"

   default: ``zk://localhost:2181``

.. data:: cluster_name

   Name of the cluster. Used in zookeeper prefix

   default: ``mi``
