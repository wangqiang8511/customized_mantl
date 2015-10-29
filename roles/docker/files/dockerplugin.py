#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Collectd plugin for collecting docker container stats
#
# Copyright © 2015 eNovance
#
# Authors:
#   Sylvain Baubeau <sylvain.baubeau@enovance.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Requirements: docker-py

import dateutil.parser
from distutils.version import StrictVersion
import docker
import json
import os
import threading
import time
import sys


def _c(c):
    """A helper method for representing a container in messages. If the given
    argument is a string, it is assumed to be the container's ID and only the
    first 7 digits will be returned. If it's a dictionary, the string returned
    is <7-digit ID>/<name>."""
    if type(c) == str or type(c) == unicode:
        return c[:7]
    return '{}/{}'.format(c['Id'][:7], c['Name'])


class Stats:
    @classmethod
    def emit(cls, container, type, value, t=None, type_instance=None):
        val = collectd.Values()
        val.plugin = 'docker'
        val.plugin_instance = container['Name']

        if type:
            val.type = type
        if type_instance:
            val.type_instance = type_instance

        if t:
            val.time = time.mktime(dateutil.parser.parse(t).timetuple())
        else:
            val.time = time.time()

        # With some versions of CollectD, a dummy metadata map must to be added
        # to each value for it to be correctly serialized to JSON by the
        # write_http plugin. See
        # https://github.com/collectd/collectd/issues/716
        val.meta = {'true': 'true'}

        val.values = value
        val.dispatch()

    @classmethod
    def read(cls, container, stats):
        raise NotImplementedError


class BlkioStats(Stats):
    @classmethod
    def read(cls, container, stats, t):
        for key, values in stats.items():
            # Block IO stats are reported by block device (with major/minor
            # numbers). We need to group and report the stats of each block
            # device independently.
            blkio_stats = {}
            for value in values:
                k = '{}-{}-{}'.format(key, value['major'], value['minor'])
                if k not in blkio_stats:
                    blkio_stats[k] = []
                blkio_stats[k].append(value['value'])

            for type_instance, values in blkio_stats.items():
                if len(values) == 5:
                    cls.emit(container, 'blkio', values,
                             type_instance=type_instance, t=t)
                elif len(values) == 1:
                    # For some reason, some fields contains only one value and
                    # the 'op' field is empty. Need to investigate this
                    cls.emit(container, 'blkio.single', values,
                             type_instance=key, t=t)
                else:
                    collectd.warn(('Unexpected number of blkio stats for '
                                   'container {}!'.format(_c(container))))


class CpuStats(Stats):
    @classmethod
    def read(cls, container, stats, t):
        cpu_usage = stats['cpu_usage']
        percpu = cpu_usage['percpu_usage']
        for cpu, value in enumerate(percpu):
            cls.emit(container, 'cpu.percpu.usage', [value],
                     type_instance='cpu%d' % (cpu,), t=t)

        items = sorted(stats['throttling_data'].items())
        cls.emit(container, 'cpu.throttling_data', [x[1] for x in items], t=t)

        values = [cpu_usage['total_usage'], cpu_usage['usage_in_kernelmode'],
                  cpu_usage['usage_in_usermode'], stats['system_cpu_usage']]
        cls.emit(container, 'cpu.usage', values, t=t)


class NetworkStats(Stats):
    @classmethod
    def read(cls, container, stats, t):
        items = stats.items()
        items.sort()
        cls.emit(container, 'network.usage', [x[1] for x in items], t=t)


class MemoryStats(Stats):
    @classmethod
    def read(cls, container, stats, t):
        values = [stats['limit'], stats['max_usage'], stats['usage']]
        cls.emit(container, 'memory.usage', values, t=t)

        for key, value in stats['stats'].items():
            cls.emit(container, 'memory.stats', [value],
                     type_instance=key, t=t)


class ContainerStats(threading.Thread):
    """
    A thread that continuously consumes the stats stream from a container,
    keeping the most recently read stats available for processing by CollectD.

    Such a mechanism is required because the first read from Docker's stats API
    endpoint can take up to one second. Hitting this endpoint for every
    container running on the system would only be feasible if the number of
    running containers was less than the polling interval of CollectD. Above
    that, and the whole thing breaks down. It is thus required to maintain open
    the stats stream and read from it, but because it is a continuous stream we
    need to be continuously consuming from it to make sure that when CollectD
    requests a plugin read, it gets the latest stats data from each container.

    The role of this thread is to keep consuming from the stats endpoint (it's
    a blocking stream read, getting stats data from the Docker daemon every
    second), and make the most recently read data available in a variable.
    """

    def __init__(self, container, client):
        threading.Thread.__init__(self)
        self.daemon = True
        self.stop = False

        self._container = container
        self._client = client
        self._feed = None
        self._stats = None

        # Automatically start stats reading thread
        self.start()

    def run(self):
        collectd.info('Starting stats gathering for {}.'
                      .format(_c(self._container)))

        while not self.stop:
            try:
                if not self._feed:
                    self._feed = self._client.stats(self._container)
                self._stats = self._feed.next()
            except Exception, e:
                collectd.warning('Error reading stats from {}: {}'
                                 .format(_c(self._container), e))
                # Marking the feed as dead so we'll attempt to recreate it and
                # survive transient Docker daemon errors/unavailabilities.
                self._feed = None

        collectd.info('Stopped stats gathering for {}.'
                      .format(_c(self._container)))

    @property
    def stats(self):
        """Wait, if needed, for stats to be available and return the most
        recently read stats data, parsed as JSON, for the container."""
        while not self._stats:
            pass
        return json.loads(self._stats)


class DockerPlugin:
    """
    CollectD plugin for collecting statistics about running containers via
    Docker's remote API /<container>/stats endpoint.
    """

    DEFAULT_BASE_URL = 'unix://var/run/docker.sock'
    DEFAULT_DOCKER_TIMEOUT = 5

    # The stats endpoint is only supported by API >= 1.17
    MIN_DOCKER_API_VERSION = '1.17'

    CLASSES = {'network': NetworkStats,
               'blkio_stats': BlkioStats,
               'cpu_stats': CpuStats,
               'memory_stats': MemoryStats}

    def __init__(self, docker_url=None):
        self.docker_url = docker_url or DockerPlugin.DEFAULT_BASE_URL
        self.timeout = DockerPlugin.DEFAULT_DOCKER_TIMEOUT
        self.capture = False
        self.stats = {}

    def configure_callback(self, conf):
        for node in conf.children:
            if node.key == 'BaseURL':
                self.docker_url = node.values[0]
            elif node.key == 'Timeout':
                self.timeout = int(node.values[0])

    def init_callback(self):
        self.client = docker.Client(
                base_url=self.docker_url,
                version=DockerPlugin.MIN_DOCKER_API_VERSION)
        self.client.timeout = self.timeout

        # Check API version for stats endpoint support.
        try:
            version = self.client.version()['ApiVersion']
            if StrictVersion(version) < \
                    StrictVersion(DockerPlugin.MIN_DOCKER_API_VERSION):
                raise Exception
        except:
            collectd.warning(('Docker daemon at {} does not '
                              'support container statistics!')
                             .format(self.docker_url))
            return False

        collectd.register_read(self.read_callback)
        collectd.info(('Collecting stats about Docker containers from {} '
                       '(API version {}; timeout: {}s).')
                      .format(self.docker_url, version, self.timeout))
        return True

    def read_callback(self):
        containers = [c for c in self.client.containers()
                      if c['Status'].startswith('Up')]

        # Terminate stats gathering threads for containers that are not running
        # anymore.
        for cid in set(self.stats) - set(map(lambda c: c['Id'], containers)):
            self.stats[cid].stop = True
            del self.stats[cid]

        for container in containers:
            try:
                container['Name'] = container['Names'][0][1:]

                # Start a stats gathering thread if the container is new.
                if container['Id'] not in self.stats:
                    self.stats[container['Id']] = ContainerStats(container,
                                                                 self.client)

                # Get and process stats from the container.
                stats = self.stats[container['Id']].stats
                for key, value in stats.items():
                    klass = self.CLASSES.get(key)
                    if klass:
                        klass.read(container, value, stats['read'])
            except Exception, e:
                collectd.warning('Error getting stats for container {}: {}'
                                 .format(_c(container), e))


# Command-line execution
if __name__ == '__main__':
    class ExecCollectdValues:
        def dispatch(self):
            if not getattr(self, 'host', None):
                self.host = os.environ.get('COLLECTD_HOSTNAME', 'localhost')
            identifier = '%s/%s' % (self.host, self.plugin)
            if getattr(self, 'plugin_instance', None):
                identifier += '-' + self.plugin_instance
            identifier += '/' + self.type
            if getattr(self, 'type_instance', None):
                identifier += '-' + self.type_instance
            print 'PUTVAL', identifier, \
                  ':'.join(map(str, [int(self.time)] + self.values))

    class ExecCollectd:
        def Values(self):
            return ExecCollectdValues()

        def warning(self, msg):
            print 'WARNING:', msg

        def info(self, msg):
            print 'INFO:', msg

    collectd = ExecCollectd()
    plugin = DockerPlugin()
    if len(sys.argv) > 1:
        plugin.docker_url = sys.argv[1]

    if plugin.init_callback():
        plugin.read_callback()

# Normal plugin execution via CollectD
else:
    import collectd
    plugin = DockerPlugin()
    collectd.register_config(plugin.configure_callback)
    collectd.register_init(plugin.init_callback)
