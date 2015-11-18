Prometheus
==========

.. versionadded:: 0.1

`Prometheus <http://prometheus.io/>`_  is an open-source service 
monitoring system and time series database. 

Variables
---------

You can use these variables to customize your swarm installation.

.. data:: prometheus_image

   Docker image of prometheus

.. data:: prometheus_image_tag

   Docker image tag of prometheus

.. data:: prometheus_image

   Docker image of prometheus consul exporter

.. data:: prometheus_image_tag

   Docker image tag of prometheus consul exporter

.. data:: consul_exporter_port

   Port for consul exporter.

.. data:: consul_hosts

   Consul hosts for monitoring.

.. data:: cluster_name

   Cluster name. Used as external label.
