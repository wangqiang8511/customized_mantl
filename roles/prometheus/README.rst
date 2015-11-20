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

.. data:: cluster_name

   Cluster name. Used as external label.

.. data:: host_domain

   Domain used for hosts.

.. data:: promdash_image

   Docker image of promdash

.. data:: promdash_image_tag

   Docker image tag of promdash

.. data:: promdash_port

   Port for promdash.

.. data:: prometheus_consul_exporter_image

   Docker image of prometheus consul exporter

.. data:: prometheus_consul_exporter_image_tag

   Docker image tag of prometheus consul exporter

.. data:: consul_exporter_port

   Port for consul exporter.

.. data:: consul_hosts

   Consul hosts for monitoring.

.. data:: etcd_size

   Size of etcd cluster. Default 1.

.. data:: etcd_client_port

   Etcd client port. Default 2379.

.. data:: prometheus_mesos_exporter_image

   Docker image of prometheus mesos exporter

.. data:: prometheus_mesos_exporter_image_tag

   Docker image tag of prometheus mesos exporter

.. data:: mesos_exporter_port

   Port for mesos exporter.

.. data:: mesos_hosts

   Mesos master endpoint for monitoring.

.. data:: consul_hosts 

   Consul hosts for node exporter service discovery.
