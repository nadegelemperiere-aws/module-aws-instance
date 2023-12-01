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
# Contact e-mail for this deployment
# -------------------------------------------------------
variable "email" {
    type = string
}

# -------------------------------------------------------
# Environment for this deployment (prod, preprod, ...)
# -------------------------------------------------------
variable "environment" {
    type = string
}
variable "region" {
    type = string
}
variable "service_principal" {
    type = string
}
variable "account" {
    type = string
}

# -------------------------------------------------------
# Topic context for this deployment
# -------------------------------------------------------
variable "project" {
    type = string
}
variable "module" {
    type = string
}
variable "name" {
    type = string
}

# -------------------------------------------------------
# Solution version
# -------------------------------------------------------
variable "git_version" {
    type    = string
    default = "unmanaged"
}

# -------------------------------------------------------
# Instance size
# -------------------------------------------------------
variable "size" {
    type = string
}
variable "os" {
    type = string
}

# -------------------------------------------------------
# Instance root disk settings
# -------------------------------------------------------
variable "disk" {
    type = object({
        size = number
        type = string
    })
    default = {
        size = 30
        type = "gp3"
    }
}

# --------------------------------------------------------
# Networks on which the instance shall be integrated with
# Access rules
# --------------------------------------------------------
variable "vpc" {
    type = string
}
variable "networks" {
    type = list(object({
        subnet     = string
        egress     = list(object({
            description = string,
            cidr        = string,
            from        = number,
            to          = number,
            protocol    = string
        })),
        ingress = list(object({
            description = string,
            cidr        = string,
            from        = number,
            to          = number,
            protocol    = string
        }))
    }))
    default = []
}
