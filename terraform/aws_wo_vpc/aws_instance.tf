variable "availability_zone" {}
variable "control_count" {default = "3"}
variable "control_type" {default = "m1.small"}
variable "datacenter" {default = "aws"}
variable "addtional_volume_size" {default = "100"} # size is in gigabytes
variable "shared_volume_size" {default = "100"} # size is in gigabytes
variable "long_name" {default = "microservices-infastructure"}
variable "short_name" {default = "mi"}
variable "source_ami" { }
variable "ssh_key" {default = "~/.ssh/id_rsa.pub"}
variable "ssh_username"  {default = "centos"}
variable "master_count" {default = "3"}
variable "master_type" {default = "m1.small"}
variable "worker_count" {default = "1"}
variable "worker_type" {default = "m1.small"}
variable "control_volume_size" {default = "20"} # size is in gigabytes
variable "master_volume_size" {default = "20"} # size is in gigabytes
variable "worker_volume_size" {default = "20"} # size is in gigabytes
variable "control_iam_profile" { default = "" }
variable "master_iam_profile" { default = "" }
variable "worker_iam_profile" { default = "" }
variable "subnet_id" { default = "" }
variable "security_groups_ids" { default = [] }


resource "aws_ebs_volume" "mi-control-addtional" {
  availability_zone = "${var.availability_zone}"
  count = "${var.control_count}"
  size = "${var.addtional_volume_size}"
  type = "gp2"

  tags {
    Name = "${var.short_name}-control-addtional-${format("%02d", count.index+1)}"
  }
}

resource "aws_ebs_volume" "mi-control-share" {
  availability_zone = "${var.availability_zone}"
  count = "${var.control_count}"
  size = "${var.addtional_volume_size}"
  type = "gp2"

  tags {
    Name = "${var.short_name}-control-share-${format("%02d", count.index+1)}"
  }
}

resource "aws_instance" "mi-control-nodes" {
  ami = "${var.source_ami}"
  availability_zone = "${var.availability_zone}"
  instance_type = "${var.control_type}"
  count = "${var.control_count}"
  vpc_security_group_ids = "${var.security_groups_ids}"

  key_name = "${aws_key_pair.deployer.key_name}"

  associate_public_ip_address=true

  iam_instance_profile = "${var.control_iam_profile}"

  subnet_id = "${var.subnet_id}"

  root_block_device {
    delete_on_termination = true
    volume_size = "${var.control_volume_size}"
  }

  tags {
    Name = "${var.short_name}-control-${format("%02d", count.index+1)}"
    sshUser = "${var.ssh_username}"
    role = "control"
    dc = "${var.datacenter}"
  }
}

resource "aws_volume_attachment" "mi-control-nodes-addtional-attachment" {
  count = "${var.control_count}"
  device_name = "xvdh"
  instance_id = "${element(aws_instance.mi-control-nodes.*.id, count.index)}"
  volume_id = "${element(aws_ebs_volume.mi-control-addtional.*.id, count.index)}"
  force_detach = true
}

resource "aws_volume_attachment" "mi-control-nodes-share-attachment" {
  count = "${var.control_count}"
  device_name = "xvdi"
  instance_id = "${element(aws_instance.mi-control-nodes.*.id, count.index)}"
  volume_id = "${element(aws_ebs_volume.mi-control-share.*.id, count.index)}"
  force_detach = true
}

resource "aws_ebs_volume" "mi-master-addtional" {
  availability_zone = "${var.availability_zone}"
  count = "${var.master_count}"
  size = "${var.addtional_volume_size}"
  type = "gp2"

  tags {
    Name = "${var.short_name}-master-addtional-${format("%02d", count.index+1)}"
  }
}

resource "aws_instance" "mi-master-nodes" {
  ami = "${var.source_ami}"
  availability_zone = "${var.availability_zone}"
  instance_type = "${var.master_type}"
  count = "${var.master_count}"

  vpc_security_group_ids = "${var.security_groups_ids}"

  key_name = "${aws_key_pair.deployer.key_name}"

  associate_public_ip_address=true

  iam_instance_profile = "${var.master_iam_profile}"

  subnet_id = "${var.subnet_id}"

  root_block_device {
    delete_on_termination = true
    volume_size = "${var.master_volume_size}"
  }

  tags {
    Name = "${var.short_name}-master-${format("%03d", count.index+1)}"
    sshUser = "${var.ssh_username}"
    role = "master"
    dc = "${var.datacenter}"
  }
}

resource "aws_volume_attachment" "mi-master-nodes-addtional-attachment" {
  count = "${var.master_count}"
  device_name = "xvdh"
  instance_id = "${element(aws_instance.mi-master-nodes.*.id, count.index)}"
  volume_id = "${element(aws_ebs_volume.mi-master-addtional.*.id, count.index)}"
  force_detach = true
}

resource "aws_ebs_volume" "mi-worker-addtional" {
  availability_zone = "${var.availability_zone}"
  count = "${var.worker_count}"
  size = "${var.addtional_volume_size}"
  type = "gp2"

  tags {
    Name = "${var.short_name}-worker-addtional-${format("%02d", count.index+1)}"
  }
}

resource "aws_instance" "mi-worker-nodes" {
  ami = "${var.source_ami}"
  availability_zone = "${var.availability_zone}"
  instance_type = "${var.worker_type}"
  count = "${var.worker_count}"

  vpc_security_group_ids = "${var.security_groups_ids}"

  key_name = "${aws_key_pair.deployer.key_name}"

  associate_public_ip_address=true

  iam_instance_profile = "${var.worker_iam_profile}"

  subnet_id = "${var.subnet_id}"

  root_block_device {
    delete_on_termination = true
    volume_size = "${var.worker_volume_size}"
  }

  tags {
    Name = "${var.short_name}-worker-${format("%03d", count.index+1)}"
    sshUser = "${var.ssh_username}"
    role = "worker"
    dc = "${var.datacenter}"
  }
}

resource "aws_volume_attachment" "mi-worker-nodes-addtional-attachment" {
  count = "${var.worker_count}"
  device_name = "xvdh"
  instance_id = "${element(aws_instance.mi-worker-nodes.*.id, count.index)}"
  volume_id = "${element(aws_ebs_volume.mi-worker-addtional.*.id, count.index)}"
  force_detach = true
}

resource "aws_key_pair" "deployer" {
  key_name = "key-${var.short_name}"
  public_key = "${file(var.ssh_key)}"
}

output "control_private_ips" {
  value = "${join(\",\", aws_instance.mi-control-nodes.*.private_ip)}"
}

output "master_private_ips" {
  value = "${join(\",\", aws_instance.mi-master-nodes.*.private_ip)}"
}

output "worker_private_ips" {
  value = "${join(\",\", aws_instance.mi-worker-nodes.*.private_ip)}"
}

output "control_public_ips" {
  value = "${join(\",\", aws_instance.mi-control-nodes.*.public_ip)}"
}

output "master_public_ips" {
  value = "${join(\",\", aws_instance.mi-master-nodes.*.public_ip)}"
}

output "worker_public_ips" {
  value = "${join(\",\", aws_instance.mi-worker-nodes.*.public_ip)}"
}
