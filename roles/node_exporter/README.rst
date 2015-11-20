Node Exporter
=============

.. versionadded:: 0.1

`Node Exporter <https://github.com/prometheus/node_exporter>`_  is used
together with prometheus. It can be used to replace collectd to collect
local instance metrics. Prometheus can pull metrics from node exporter.

Variables
---------

.. data:: node_exporter_port

   Port of node_exporter listen to.

   default: ``9109``
