variable "datacenter" {}
variable "host" {}
variable "pool" {}
variable "template" {}
variable "ssh_user" {}
variable "ssh_key" {}
variable "consul_dc" {}

variable "short_name" {default = "mi"}
variable "long_name" {default = "microservices-infrastructure"}

variable "control_count" {default = 3}
variable "worker_count" {default = 2}
variable "control_cpu" { default = 1 }
variable "worker_cpu" { default = 1 }
variable "control_ram" { default = 4096 }
variable "worker_ram" { default = 4096 }

resource "vsphere_virtual_machine" "mi-control-nodes" {
  name = "${var.short_name}-control-${format("%02d", count.index+1)}"
  image = "${var.template}"

  datacenter = "${var.datacenter}"
  host = "${var.host}"
  resource_pool = "${var.pool}"

  cpus = "${var.control_cpu}"
  memory = "${var.control_ram}"

  configuration_parameters = {
    role = "control"
    ssh_user = "${var.ssh_user}"
    consul_dc = "${var.consul_dc}"
  }

  connection = {
      user = "${var.ssh_user}"
      key_file = "${var.ssh_key}"
      host = "${self.ip_address}"
  }

  provisioner "remote-exec" {
    inline = [ "sudo hostnamectl --static set-hostname ${self.name}" ]
  }

  count = "${var.control_count}"
}

resource "vsphere_virtual_machine" "mi-worker-nodes" {
  name = "${var.short_name}-worker-${format("%03d", count.index+1)}"
  image = "${var.template}"

  datacenter = "${var.datacenter}"
  host = "${var.host}"
  resource_pool = "${var.pool}"

  cpus = "${var.worker_cpu}"
  memory = "${var.worker_ram}"

  configuration_parameters = {
    role = "worker"
    ssh_user = "${var.ssh_user}"
    consul_dc = "${var.consul_dc}"
  }
  
  connection = {
      user = "${var.ssh_user}"
      key_file = "${var.ssh_key}"
      host = "${self.ip_address}"
  }

  provisioner "remote-exec" {
    inline = [ "sudo hostnamectl --static set-hostname ${self.name}" ]
  }

  count = "${var.worker_count}"
}

output "control_ips" {
  value = "${join(\",\", vsphere_virtual_machine.mi-control-nodes.*.network_interface.ip_address)}"
}

output "worker_ips" {
  value = "${join(\",\", vsphere_virtual_machine.mi-worker-nodes.*.network_interface.ip_address)}"
}
