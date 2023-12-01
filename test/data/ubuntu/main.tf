# -------------------------------------------------------
# Copyright (c) [2023] Nadege Lemperiere
# All rights reserved
# -------------------------------------------------------
# Simple deployment for module testing
# -------------------------------------------------------
# Nadège LEMPERIERE, @18 january 2021
# Latest revision: 18 january 2021
# -------------------------------------------------------


# -------------------------------------------------------
# Create a network
# -------------------------------------------------------
resource "aws_vpc" "test" {

	cidr_block  			= "10.2.0.0/24"
	enable_dns_support  	= true
	enable_dns_hostnames	= true
   	tags 					= { Name = "test.instance" }

}

# -------------------------------------------------------
# Create the interface subnet
# -------------------------------------------------------
resource "aws_subnet" "test" {
	vpc_id 		= aws_vpc.test.id
	cidr_block  = "10.2.0.0/26"
   	tags 		= { Name = "test.instance" }
}
# -------------------------------------------------------
# Create instance using the current module
# -------------------------------------------------------
module "instance" {

	source 				= "../../../"
	email 				= "moi.moi@moi.fr"
	project 			= "test"
	environment 		= "test"
	module 				= "test"
	git_version 		= "test"
	name 				= "test"
	service_principal 	= var.service_principal
	account				= var.account
	region 			    = var.region
	size				= "c5.xlarge"
	os					= "Ubuntu-20.04"
	disk 				= {
		size	= 20
		type	= "gp3"
	}
	vpc 				= aws_vpc.test.id
	networks 			= [
		{
			subnet 	= aws_subnet.test.id
			egress = [
				{ description = "AllowInternetTlsAccess",    from = 443,	to = 443,   protocol = "tcp", cidr = "0.0.0.0/0"},
				{ description = "AllowInternetDnsAccess",    from = 53,		to = 53,    protocol = "udp", cidr = "0.0.0.0/0"}
			]
			ingress 	= [
			]
		}
	]
}

# -------------------------------------------------------
# Terraform configuration
# -------------------------------------------------------
provider "aws" {
	region		= var.region
	access_key 	= var.access_key
	secret_key	= var.secret_key
}

terraform {
	required_version = ">=1.0.8"
	backend "local"	{
		path="terraform.tfstate"
	}
}

# -------------------------------------------------------
# Region for this deployment
# -------------------------------------------------------
variable "region" {
	type    = string
}
variable "account" {
	type    = string
}
variable "service_principal" {
	type    = string
}

# -------------------------------------------------------
# AWS credentials
# -------------------------------------------------------
variable "access_key" {
	type    	= string
	sensitive 	= true
}
variable "secret_key" {
	type    	= string
	sensitive 	= true
}

# -------------------------------------------------------
# Test outputs
# -------------------------------------------------------
output "vpc" {
	value = {
		id 		= aws_vpc.test.id
	}
}

output "subnet" {
	value = aws_subnet.test.id
}

output "instance" {
	value = module.instance.instance
}

output "key" {
	value = module.instance.key
}

output "interfaces" {
	value = module.instance.interfaces
}
