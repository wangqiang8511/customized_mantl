Docker
======

.. versionadded:: 0.1

`Docker <https://www.docker.com/>`_ is a container manager and scheduler. In
their words, it "allows you to package an application with all of its
dependencies into a standardized unit for software development." Their site has
`more on what Docker is <https://www.docker.com/whatisdocker>`_. We use it in
microservices-infrastructure to ship units of work around the cluster, combined
with :doc:`marathon`'s scheduling.

See the `Marathon documentation
<https://mesosphere.github.io/marathon/docs/native-docker-private-registry.html>`_
for more information.

.. data:: etcd_client_port

   Port used for etcd api, default 2379

.. data:: docker_tcp_port

   Port used for docker tcp default 2375

.. data:: docker_advertise_port

   Port used for docker advertise opt default 2376
