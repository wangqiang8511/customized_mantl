Calico
======

.. versionadded:: 0.1

`Calico <http://www.projectcalico.org>`_ is used in the project to add the IP
per container functionality. Calico connects Docker containers through IP no matter
which worker node they are on. Calico uses :doc:`etcd` to distribute information
about workloads, endpoints, and policy to each worker node.

Variables
---------

You can use these variables to customize your Calico installation. For more
information, refer to the :doc:`etcd` configuration.

.. data:: etcd_cluster_store
    
   ETCD cluster used for calico. Informat etcd://<ip1>:2379,<ip2>:2379,<ip3>:2379

.. data:: cluster_name

   cluster_name is used for network name
