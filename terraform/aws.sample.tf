provider "aws" {
	  region = "us-east-1"
}

module "aws-dc" {
  source = "./terraform/aws"
  availability_zone = "us-east-1d"
  control_type = "t2.small"
  master_type = "t2.small"
  worker_type = "t2.small"
  ssh_username = "ubuntu"
  source_ami = "ami-d05e75b8"
  control_count = 3
  master_count = 3
  worker_count = 1
}

# Example setup for DNS with dnsimple;
# module "dnsimple-dns" {
#   source = "./terraform/dnsimple/dns"
#   short_name = "mi"
#   control_count = 3
#   worker_count = 3
#   domain = "example.com"
#   control_ips = "${module.aws-dc.control_ips}"
#   worker_ips = "${module.aws-dc.worker_ips}"
# }

# Example setup for DNS with dnsimple;
module "route53-dns" {
  source = "./terraform/route53/dns"
  short_name = "mi"
  control_count = 3
  master_count = 3
  worker_count = 1
  domain = "razerdata.com"
  hosted_zone_id = "Z1AJSP2MFMQX3K"
  control_ips = "${module.aws-dc.control_ips}"
  master_ips = "${module.aws-dc.master_ips}"
  worker_ips = "${module.aws-dc.worker_ips}"
}

