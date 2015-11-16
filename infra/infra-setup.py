#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Setup infra config files

* aws.tf
* swarm.yml
"""
import os

import requests
import yaml
import click
from jinja2 import Environment
from jinja2 import FileSystemLoader


def load_infra_config(filename):
    config = yaml.load(open(filename, "r").read())
    return config


def valid_config(config):
    # Config validation
    pass


def generate_ectd_discovery(config):
    url = "https://discovery.etcd.io/new"
    params = {
        "size": config["control_count"]
    }
    r = requests.get(url, params=params)
    config["etcd_discovery"] = r.text
    return config


def render_template(config, template_name):
    current_dir = os.path.dirname(__file__)
    tmpl_dir = os.path.join(current_dir, "templates")
    env = Environment(loader=FileSystemLoader(tmpl_dir))
    template = env.get_template(template_name)
    print template.render(config)


@click.command()
@click.argument("config_file")
def infra_setup(config_file):
    click.echo("generating infra settings with %s" % config_file)
    config = load_infra_config(config_file)
    valid_config(config)
    # render_template(config, "aws.tf.j2")
    config = generate_ectd_discovery(config)
    render_template(config, "cluster.yml.j2")


if __name__ == '__main__':
    infra_setup()
