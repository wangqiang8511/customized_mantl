Marathon
========

.. versionadded:: 0.1

`Marathon <http://mesosphere.github.io/marathon/>`_ is a scheduler for
:doc:`mesos` - it takes specifications for apps to run and lets you scale them
up and down, and deploy new versions or roll back. Like Mesos' leader mode,
Marathon can run on as many servers as you like and will elect a leader among
nodes using :doc:`zookeeper`.

Keep Marathon servers close to Mesos leaders for best performance; they talk
back and forth quite a lot to keep the services in the cluster in a good state.
Placing them on the same machines would work.

Variables
---------
.. data:: marathon_version

   Version of marathon.

   default: ``0.11.1``

.. data:: zk_hosts

   Zookeeper hosts, in format of "zk://host1:port1,host2:port2,host3:port3"

   default: ``zk://localhost:2181``

.. data:: cluster_name

   Name of the cluster. Used in zookeeper prefix

   default: ``mi``
