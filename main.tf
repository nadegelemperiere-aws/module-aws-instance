# -------------------------------------------------------
# Copyright (c) [2023] Nadege Lemperiere
# All rights reserved
# -------------------------------------------------------
# Module to deploy an aws instance with all the secure
# components required
# -------------------------------------------------------
# Nadège LEMPERIERE, @18 january 2021
# Latest revision: 18 january 2021
# -------------------------------------------------------

# -------------------------------------------------------
# Matching os with associated ami
# -------------------------------------------------------
locals {
    images = {
        eu-west-1 = [
            { os = "Ubuntu-22.04", ami = "ami-0694d931cee176e7d", owner = "099720109477" },
            { os = "Ubuntu-20.04", ami = "ami-08031206a0ff5a6ac", owner = "099720109477" },
            { os = "Ubuntu-18.04", ami = "ami-0e42de9d667b232f7", owner = "099720109477" },
            { os = "Ubuntu-16.04", ami = "ami-0e9e0275fc0a4050a", owner = "099720109477" },
            { os = "Suze-15sp5", ami = "ami-0dde8123969953c19", owner = "013907871322" },
            { os = "Suze-15sp4", ami = "ami-06f9e8371de219664", owner = "013907871322" },
            { os = "Suze-15sp3", ami = "ami-02be7a0d5d4276ce2", owner = "013907871322" },
            { os = "RedHat-9", ami = "ami-049b0abf844cab8d7", owner = "309956199498" },
            { os = "RedHat-8", ami = "ami-04b82270e2c61ea45", owner = "124009662561" },
            { os = "Debian-12", ami = "ami-0eb11ab33f229b26c", owner = "136693071363" },
            { os = "Debian-11", ami = "ami-0b16162eb3d30b397", owner = "136693071363" },
            { os = "Debian-10", ami = "ami-07f258ab44d55e5db", owner = "136693071363"},
            { os = "Amazon-2023", ami = "ami-07355fe79b493752d", owner = "137112412989" },
            { os = "Amazon-5.10", ami = "ami-04489d9094a6a7a5f", owner = "137112412989" },
            { os = "Microsoft-2019", ami = "ami-06b88a17e7ff03ac1", owner = "801119661308"},
            { os = "Microsoft-2022", ami = "ami-0b3a63a48e767cc82", owner = "801119661308"},
            { os = "Microsoft-2016", ami = "ami-017f77c19842749bd", owner = "801119661308"}
        ]
    }


    region_images      = lookup(local.images, var.region, local.images.eu-west-1)
    points_map         = { for i, ept in local.region_images : tostring(i) => ept }
    images_map         = compact([for i, ept in local.region_images : ept.os == var.os ? i : ""])
    selected_images    = [for key in local.images_map : lookup(local.points_map, key, local.images.eu-west-1[0])]
    image              = local.selected_images[0].ami
    owner              = local.selected_images[0].owner
}

# -------------------------------------------------------
# Load an official aws image
# -------------------------------------------------------
data    "aws_ami"     "instance" {

    owners             = [local.owner]

    filter {
        name         = "image-id"
        values         = [local.image]
    }

    tags = {
        Name                = "${var.project}.${var.environment}.${var.module}.instance.${var.name}"
        Environment         = var.environment
        Owner               = var.email
        Project             = var.project
        Version             = var.git_version
        Module              = var.module
    }

}

# -------------------------------------------------------
# Create instance
# -------------------------------------------------------
locals {
    subnets = [ for i, sub in var.networks : {index = i}]
}
resource "aws_instance" "instance" {

    depends_on         = [aws_network_interface.subnet]

    ami                = data.aws_ami.instance.id
    instance_type      = var.size

    monitoring         = true
    hibernation        = false

    dynamic "network_interface" {
        for_each = local.subnets
        content {
            device_index             = network_interface.value.index
            network_interface_id     = aws_network_interface.subnet[network_interface.value.index].id
        }
    }

    metadata_options {
        http_tokens = "required"
    }

    root_block_device {
        encrypted     = true
        kms_key_id     = aws_kms_key.key.arn
        volume_size    = var.disk.size
        volume_type    = var.disk.type

        tags = {
            Name                = "${var.project}.${var.environment}.${var.module}.instance.${var.name}"
            Environment         = var.environment
            Owner               = var.email
            Project             = var.project
            Version             = var.git_version
            Module              = var.module
        }
    }

    tags = {
        Name                = "${var.project}.${var.environment}.${var.module}.instance.${var.name}"
        Environment         = var.environment
        Owner               = var.email
        Project             = var.project
        Version             = var.git_version
        Module              = var.module
    }
}

# -------------------------------------------------------
# Create a network interface for each network
# -------------------------------------------------------
resource "aws_network_interface" "subnet" {

    count                = length(var.networks)
    subnet_id            = var.networks[count.index].subnet
      security_groups    = [aws_security_group.subnet[count.index].id]

    tags = {
        Name            = "${var.project}.${var.environment}.${var.module}.instance.${var.name}.subnet${count.index}.interface"
        Environment     = var.environment
        Owner           = var.email
        Project         = var.project
        Version         = var.git_version
        Module          = var.module
    }
}

# -------------------------------------------------------
# Create a security group for instance network interface
# -------------------------------------------------------
resource "aws_security_group" "subnet" {

    count         = length(var.networks)

    name          = "${var.project}-instance-${var.name}-subnet${count.index}"
    description   = "security group for instance ${var.name}"
    vpc_id      = var.vpc

    tags = {
        Name            = "${var.project}.${var.environment}.${var.module}.instance.${var.name}.subnet${count.index}.nsg"
        Environment     = var.environment
        Owner           = var.email
        Project         = var.project
        Version         = var.git_version
        Module          = var.module
    }
}

# -------------------------------------------------------
# Add rules in nsg to enable instance access to resources
# -------------------------------------------------------
locals {
    egress  = flatten([ for i, sub in var.networks : [ for j, rule in sub.egress : merge(rule,{index = i, sg = aws_security_group.subnet[i].id})]])
    ingress = flatten([ for i, sub in var.networks : [ for j, rule in sub.ingress : merge(rule,{index = i, sg = aws_security_group.subnet[i].id})]])
}
resource "aws_security_group_rule" "egress" {

    count = length(local.egress)

    depends_on                   = [aws_security_group.subnet]
    description                  = local.egress[count.index].description
    security_group_id            = local.egress[count.index].sg
    type                         = "egress"
    protocol                     = local.egress[count.index].protocol
    cidr_blocks                  = [local.egress[count.index].cidr]
    ipv6_cidr_blocks             = []
    prefix_list_ids              = []
    from_port                    = local.egress[count.index].from
    to_port                      = local.egress[count.index].to
}
resource "aws_security_group_rule" "ingress" {

    count = length(local.ingress)

    depends_on                   = [aws_security_group.subnet]
    description                  = local.ingress[count.index].description
    security_group_id            = local.ingress[count.index].sg
    type                         = "ingress"
    protocol                     = local.ingress[count.index].protocol
    cidr_blocks                  = [local.ingress[count.index].cidr]
    ipv6_cidr_blocks             = []
    prefix_list_ids              = []
    from_port                    = local.ingress[count.index].from
    to_port                      = local.ingress[count.index].to
}

# -------------------------------------------------------
# Formatting data for output
# -------------------------------------------------------
resource "null_resource" "interfaces" {

    count = length(var.networks)

    triggers = {
        group = aws_security_group.subnet[count.index].id
        subnet = var.networks[count.index].subnet
        interface = aws_network_interface.subnet[count.index].id
        device = count.index
        dns = aws_network_interface.subnet[count.index].private_dns_name
    }
}

# -------------------------------------------------------
# Instance disk encryption key
# -------------------------------------------------------
resource "aws_kms_key" "key" {

    description                 = "EC2 Instance encryption key"
    key_usage                   = "ENCRYPT_DECRYPT"
    customer_master_key_spec    = "SYMMETRIC_DEFAULT"
    deletion_window_in_days     = 7
    enable_key_rotation         = true
    policy                      = jsonencode({
          Version = "2012-10-17",
          Statement = [
            {
                Sid             = "AllowKeyModificationToRootAndGod"
                Effect          = "Allow"
                Principal       = {
                    "AWS" : [
                        "arn:aws:iam::${var.account}:root",
                        "arn:aws:iam::${var.account}:user/${var.service_principal}"
                    ]
                }
                Action          = [ "kms:*" ],
                Resource        = "*"
               }
          ]
    })

    tags = {
        Name            = "${var.project}.${var.environment}.${var.module}.instance.${var.name}"
        Environment     = var.environment
        Owner           = var.email
        Project         = var.project
        Version         = var.git_version
        Module          = var.module
    }
}
