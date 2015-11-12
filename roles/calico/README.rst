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

.. data:: etcd_image

   Docker image of etcd

.. data:: etcd_image_tag

   Docker image tag of etcd

.. data:: etcd_client_port

   Port used for etcd api

.. data:: docker_advertise_port

   Port used for docker cluster-advertise option

.. data:: calico_subnet

   Subnet for calico
