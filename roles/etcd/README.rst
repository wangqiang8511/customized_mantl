etcd
====

.. versionadded:: 0.4

`etcd <https://github.com/coreos/etcd>`_ is used in the project by
:doc:`calico` to distribute information about workloads, endpoints, and policy
to each Docker host. It's run in a Docker container on each host and managed
by systemd.

Variables
---------

You can use these variables to customize your etcd installation. Beware,
you will need to update ``ETCD_AUTHORITY`` in the Calico role as well.

.. data:: etcd_client_port

   Port for etcd client communication

   Default: ``2379``

.. data:: etcd_peer_port

   Port for etcd server-to-server communication

   Default: ``2380``
   
.. data:: etcd_image

   Docker image of etcd

.. data:: etcd_image_tag

   Docker image tag of etcd

.. data:: etcd_browser_image

   Docker image of etcd browser

.. data:: etcd_browser_image_tag

   Docker image tag of etcd browser

.. data:: etcd_browser_port

   Port used for etcd browser

.. data:: etcd_client_port

   Port used for etcd api

.. data:: etcd_peer_port

   Port used for etcd discovery
