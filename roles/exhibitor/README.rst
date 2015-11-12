Exhibitor
=========

.. versionadded:: 0.1

`Exhibitor <https://www.consul.io/>`_ is used in the project to bootstrap
zookeeper.


Variables
---------

You can use these variables to customize your exhibitor installation. 

.. data:: exhibitor_image

   Docker image name for exhibitor

.. data:: exhibitor_image_tag

   Docker image tag for exhibitor 

.. data:: exhibitor_s3_region

   S3 region for exhibitor share config.

.. data:: exhibitor_s3_bucket

   S3 bucket for exhibitor share config.

.. data:: exhibitor_config_prefix

   Prefix for share config.

.. data:: exhibitor_size

   Size of exhibitor cluster.

.. data:: cluster_name

   Name for your exhibitor cluster.
