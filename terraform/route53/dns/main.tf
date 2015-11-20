variable control_private_ips {}
variable master_private_ips {}
variable worker_private_ips {}
variable control_public_ips {}
variable master_public_ips {}
variable worker_public_ips {}
variable control_count {}
variable master_count {}
variable worker_count {}
variable domain {}
variable short_name {}
variable hosted_zone_id {}

resource "aws_route53_record" "dns-private-control" {
  count = "${var.control_count}"
  zone_id = "${var.hosted_zone_id}"
  records = ["${element(split(\",\", var.control_private_ips), count.index)}"]
  name = "${var.short_name}-control-${format("%02d", count.index+1)}.${var.domain}"
  type = "A"
  ttl = 60
}

resource "aws_route53_record" "dns-private-master" {
  count = "${var.master_count}"
  zone_id = "${var.hosted_zone_id}"
  name = "${var.short_name}-master-${format("%03d", count.index+1)}.${var.domain}"
  records = ["${element(split(\",\", var.master_private_ips), count.index)}"]
  type = "A"
  ttl = 60
}

resource "aws_route53_record" "dns-private-worker" {
  count = "${var.worker_count}"
  zone_id = "${var.hosted_zone_id}"
  name = "${var.short_name}-worker-${format("%03d", count.index+1)}.${var.domain}"
  records = ["${element(split(\",\", var.worker_private_ips), count.index)}"]
  type = "A"
  ttl = 60
}

resource "aws_route53_record" "dns-public-control" {
  count = "${var.control_count}"
  zone_id = "${var.hosted_zone_id}"
  records = ["${element(split(\",\", var.control_public_ips), count.index)}"]
  name = "${var.short_name}-control-pub-${format("%02d", count.index+1)}.${var.domain}"
  type = "A"
  ttl = 60
}

resource "aws_route53_record" "dns-public-master" {
  count = "${var.master_count}"
  zone_id = "${var.hosted_zone_id}"
  name = "${var.short_name}-master-pub-${format("%03d", count.index+1)}.${var.domain}"
  records = ["${element(split(\",\", var.master_public_ips), count.index)}"]
  type = "A"
  ttl = 60
}

resource "aws_route53_record" "dns-public-worker" {
  count = "${var.worker_count}"
  zone_id = "${var.hosted_zone_id}"
  name = "${var.short_name}-worker-pub-${format("%03d", count.index+1)}.${var.domain}"
  records = ["${element(split(\",\", var.worker_public_ips), count.index)}"]
  type = "A"
  ttl = 60
}

resource "aws_route53_record" "dns-control-proxy" {
  zone_id = "${var.hosted_zone_id}"
  name = "*.${var.short_name}-control.${var.domain}"
  records = ["${split(\",\", var.control_private_ips)}"]
  type = "A"
  ttl = 60
}

resource "aws_route53_record" "dns-master-proxy" {
  zone_id = "${var.hosted_zone_id}"
  name = "*.${var.short_name}-master.${var.domain}"
  records = ["${split(\",\", var.master_private_ips)}"]
  type = "A"
  ttl = 60
}

resource "aws_route53_record" "dns-worker-proxy" {
  zone_id = "${var.hosted_zone_id}"
  name = "*.${var.short_name}-worker.${var.domain}"
  records = ["${split(\",\", var.worker_private_ips)}"]
  type = "A"
  ttl = 60
}
