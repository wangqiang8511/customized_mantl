Traefik
=======

.. versionadded:: 0.1

`Traefik <https://github.com/emilevauge/traefik>`_ 
Træfɪk is a modern HTTP reverse proxy and load balancer made to 
deploy microservices with ease.

Variables
---------

.. data:: traefik_image

   Docker image of traefik

.. data:: traefik_image_tag

   Docker image tag of traefik

.. data:: traefik_api_port

   Port for traefik api

   Default: ``3001``

.. data:: traefik_port

   Port for traefik

   Default: ``80``

.. data:: traefik_log_level

   Log Level for traefik

   Default: ``ERROR``
   
.. data:: marathon_hosts

   HA hosts for marathon

   Default: ``localhost:8080``

.. data:: cluster_name

   Name of cluster, used for setup traefik domain

   Default: ``mi``

.. data:: domain

   Domain of cluster, used for setup traefik domain

   Default: ``localhost``
