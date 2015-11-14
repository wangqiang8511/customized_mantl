Swarm
=====

.. versionadded:: 0.1

`Swarm <https://docs.docker.com/swarm/>`_ It allows you create 
and access to a pool of Docker hosts using the full suite of 
Docker tools. Because Docker Swarm serves the standard Docker API, 
any tool that already communicates with a Docker daemon can use 
Swarm to transparently scale to multiple hosts. 


Variables
---------

You can use these variables to customize your swarm installation.

.. data:: etcd_image

   Docker image of etcd

.. data:: etcd_image_tag

   Docker image tag of etcd

.. data:: etcd_client_port

   Port used for etcd api

.. data:: docker_tcp_port

   Port used for docker tcp default 2375

.. data:: swarm_manager_port

   Port used for swarm manager default 2374

.. data:: swarm_mode

   Swarm mode for current group. (agent|manager) Required.
