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


output "instance" {
    value = {
        id      = aws_instance.instance.id
        arn     = aws_instance.instance.arn
        status  = aws_instance.instance.instance_state
    }
}

output "interfaces" {
    value = null_resource.interfaces[*].triggers
}

output "key" {
    value = {
        arn     = aws_kms_key.key.arn
        id      = aws_kms_key.key.id
    }
}

