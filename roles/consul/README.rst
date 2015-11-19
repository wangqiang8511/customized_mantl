Consul
======

.. versionadded:: 0.1

`Consul <https://www.consul.io/>`_ is used in the project to coordinate service
discovery, specifically using the inbuilt DNS server.

Variables
---------

You can use these variables to customize your Consul installation.

.. data:: consul_image

   Docker image name for consul

.. data:: consul_image_tag

   Docker image tag for consul

.. data:: consul_size

   cluster size for consul.

.. data:: consul_leader

   Leader for consul cluster

.. data:: consul_mode

   Mode of current consul instance.
