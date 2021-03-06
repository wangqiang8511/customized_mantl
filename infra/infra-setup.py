#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Setup infra config files

* aws.tf
* cluster.yml
* xxx_ansible.yml
* openvpn_ansible.yml
"""
import os

import requests
import yaml
import click
from jinja2 import Environment
from jinja2 import FileSystemLoader


current_dir = os.path.dirname(__file__)
tmpl_dir = os.path.join(current_dir, "templates")

required_fields_yaml = os.path.join(current_dir, "required_fields.yml")
out_dir = os.path.dirname(current_dir)


def echo_error(msg):
    click.echo(click.style(msg, fg="red"))


def echo_msg(msg):
    click.echo(click.style(msg, fg="green"))


def load_infra_config(filename):
    config = yaml.load(open(filename, "r").read())
    return config


def check_cluster_type(config):
    supported = ["swarm", "mesos"]
    if not config["cluster_type"] in supported:
        return False, "Cluster type is not supported"
    return True, "OK"


def get_required_fields(config):
    required_fields = yaml.load(open(required_fields_yaml, "r").read())
    required_keys = []
    required_keys += required_fields["aws"]
    required_keys += required_fields[config["cluster_type"]]
    if "openvpn_enabled" in config.keys() and config["openvpn_enabled"]:
        required_keys += required_fields["openvpn"]
    return required_keys


def check_required_fields(config):
    required_keys = get_required_fields(config)
    for k in required_keys:
        if k not in config:
            return False, "missing %s" % k
    return True, "OK"


def valid_config(config):
    # Config validation
    ok, msg = check_cluster_type(config)
    if not ok:
        return ok, msg
    ok, msg = check_required_fields(config)
    return ok, msg


def generate_ectd_discovery(config):
    url = "https://discovery.etcd.io/new"
    params = {
        "size": config["control_count"]
    }
    r = requests.get(url, params=params)
    config["etcd_discovery"] = r.text
    return config


def generate_zk_hosts(config):
    control_count = int(config["control_count"])
    zk_hosts = []
    for i in range(1, control_count + 1):
        zk_hosts.append("%s-control-%s.%s:2181" %
                        (config["cluster_name"],
                         str(i).zfill(2),
                         config["domain"]))
    config["zk_hosts"] = "zk://" + ",".join(zk_hosts)
    return config


def generate_marathon_hosts(config):
    master_count = int(config["master_count"])
    marathon_hosts = []
    for i in range(1, master_count + 1):
        marathon_hosts.append("%s-master-%s.%s:8080" %
                              (config["cluster_name"],
                               str(i).zfill(3),
                               config["domain"]))
    config["marathon_hosts"] = ",".join(marathon_hosts)
    return config


def generate_mesos_hosts(config):
    mesos_hosts = "%s-master-%s.%s:5050" % (
        config["cluster_name"],
        str(1).zfill(3),
        config["domain"])
    config["mesos_hosts"] = mesos_hosts
    return config


def generate_consul_hosts(config):
    consul_hosts = "%s-control-%s.%s:8500" % (
        config["cluster_name"],
        str(1).zfill(2),
        config["domain"])
    config["consul_hosts"] = consul_hosts
    return config


def generate_prometheus_host(config):
    prometheus_host_tag = "%s-control-%s" % (
        config["cluster_name"],
        str(1).zfill(2))
    config["prometheus_host"] = prometheus_host_tag
    return config


def generate_more_settings(config):
    remains = {}
    presented = []
    with open(os.path.join(tmpl_dir, "cluster.yml.j2")) as f:
        for line in f:
            if ':' in line:
                presented.append(line.split(":")[0])
    for k, v in config.iteritems():
        if k not in presented:
            remains[k] = v
    config["more_settings"] = yaml.dump(remains, default_flow_style=False)
    return config


def generate_openvpn_settings(config):
    if "openvpn_host" not in config.keys():
        config["openvpn_deploy_host"] = "%s-control-01" \
            % config["cluster_name"]
        config["openvpn_host"] = "%s-control-pub-01.%s" \
            % (config["cluster_name"], config["domain"])
    config["openvpn_push_routes"] = ["route 10.0.0.0 255.255.0.0"]
    return config


def render_template(config, template_name, outfile):
    env = Environment(loader=FileSystemLoader(tmpl_dir))
    template = env.get_template(template_name)
    with open(outfile, 'w') as f:
        f.write(template.render(config))


@click.command()
@click.argument("config_file")
def infra_setup(config_file):
    echo_msg("generating infra settings with %s" % config_file)
    config = load_infra_config(config_file)
    ok, msg = valid_config(config)
    if not ok:
        echo_error(msg)
        exit(1)
    out_aws_tf = os.path.join(out_dir, "aws.tf")
    render_template(config, "aws.tf.j2", out_aws_tf)
    config = generate_ectd_discovery(config)
    config = generate_zk_hosts(config)
    config = generate_mesos_hosts(config)
    config = generate_marathon_hosts(config)
    config = generate_consul_hosts(config)
    config = generate_prometheus_host(config)
    config = generate_openvpn_settings(config)
    config = generate_more_settings(config)
    out_cluster_yml = os.path.join(out_dir, "cluster.yml")
    render_template(config, "cluster.yml.j2", out_cluster_yml)
    out_infra_ansible_yml = os.path.join(out_dir, "infra_ansible.yml")
    render_template(config, "%s.yml.j2" % config["cluster_type"],
                    out_infra_ansible_yml)
    if "openvpn_enabled" in config.keys() and config["openvpn_enabled"]:
        out_openvpn_yml = os.path.join(out_dir, "openvpn_ansible.yml")
        render_template(config, "openvpn.yml.j2", out_openvpn_yml)


if __name__ == '__main__':
    infra_setup()
