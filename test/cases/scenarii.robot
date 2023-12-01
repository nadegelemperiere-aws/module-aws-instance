# -------------------------------------------------------
# Copyright (c) [2023] Nadege Lemperiere
# All rights reserved
# -------------------------------------------------------
# Robotframework test suite for module
# -------------------------------------------------------
# Nadège LEMPERIERE, @18 january 2021
# Latest revision: 18 january 2021
# -------------------------------------------------------


*** Settings ***
Documentation   A test case to check instances creation using module
Library         aws_iac_keywords.terraform
Library         aws_iac_keywords.keepass
Library         aws_iac_keywords.ec2
Library         aws_iac_keywords.kms
Library         ../keywords/data.py
Library         OperatingSystem

*** Variables ***
${KEEPASS_DATABASE}                 ${vault_database}
${KEEPASS_KEY_ENV}                  ${vault_key_env}
${KEEPASS_PRINCIPAL_KEY_ENTRY}      /aws/aws-principal-access-key
${KEEPASS_ACCOUNT_ENTRY}            /aws/aws-account
${KEEPASS_PRINCIPAL_USERNAME}       /aws/aws-principal-credentials
${REGION}                           eu-west-1

*** Test Cases ***
Prepare Environment
    [Documentation]         Retrieve principal credential from database and initialize python tests keywords
    ${keepass_key}          Get Environment Variable          ${KEEPASS_KEY_ENV}
    ${principal_access}     Load Keepass Database Secret      ${KEEPASS_DATABASE}     ${keepass_key}  ${KEEPASS_PRINCIPAL_KEY_ENTRY}            username
    ${principal_secret}     Load Keepass Database Secret      ${KEEPASS_DATABASE}     ${keepass_key}  ${KEEPASS_PRINCIPAL_KEY_ENTRY}            password
    ${principal_name}       Load Keepass Database Secret      ${KEEPASS_DATABASE}     ${keepass_key}  ${KEEPASS_PRINCIPAL_USERNAME}     username
    ${ACCOUNT}              Load Keepass Database Secret      ${KEEPASS_DATABASE}     ${keepass_key}  ${KEEPASS_ACCOUNT_ENTRY}         password
    Initialize Terraform    ${REGION}   ${principal_access}   ${principal_secret}
    Initialize EC2          None        ${principal_access}   ${principal_secret}    ${REGION}
    Initialize KMS          None        ${principal_access}   ${principal_secret}    ${REGION}
    ${TF_PARAMETERS}=       Create Dictionary   region=${REGION}    account=${ACCOUNT}       service_principal=${principal_name}
    Set Global Variable     ${TF_PARAMETERS}
    Set Global Variable     ${ACCOUNT}

Create Ubuntu Instance
    [Documentation]         Create Ubuntu Instance And Check That The AWS Infrastructure Match Specifications
    Launch Terraform Deployment               ${CURDIR}/../data/ubuntu    ${TF_PARAMETERS}
    ${states}   Load Terraform States         ${CURDIR}/../data/ubuntu
    ${specs}    Load Ubuntu Test Data         ${states['test']['outputs']['vpc']['value']['id']}   ${states['test']['outputs']['subnet']['value']}     ${states['test']['outputs']['instance']['value']}    ${states['test']['outputs']['interfaces']['value']}    ${states['test']['outputs']['key']['value']}    ${ACCOUNT}
    Instances Shall Exist And Match           ${specs['instances']}
    Security Group Shall Exist And Match      ${specs['security_groups']}
    Key Shall Exist And Match                 ${specs['keys']}
    Network Interfaces Shall Exist And Match  ${specs['interfaces']}
    [Teardown]  Destroy Terraform Deployment  ${CURDIR}/../data/ubuntu    ${TF_PARAMETERS}


Create Multiple Subnet Instance
    [Documentation]         Create Multiple Network Interfaces Instance And Check That The AWS Infrastructure Match Specifications
    Launch And Refresh Terraform Deployment     ${CURDIR}/../data/subnets    ${TF_PARAMETERS}
    ${states}   Load Terraform States           ${CURDIR}/../data/subnets
    ${specs}    Load Subnets Test Data          ${states['test']['outputs']['vpc']['value']['id']}   ${states['test']['outputs']['subnets']['value']}     ${states['test']['outputs']['instance']['value']}    ${states['test']['outputs']['interfaces']['value']}    ${states['test']['outputs']['key']['value']}    ${ACCOUNT}
    Instances Shall Exist And Match             ${specs['instances']}
    Security Group Shall Exist And Match        ${specs['security_groups']}
    Key Shall Exist And Match                   ${specs['keys']}
    Network Interfaces Shall Exist And Match    ${specs['interfaces']}
    [Teardown]  Destroy Terraform Deployment    ${CURDIR}/../data/subnets    ${TF_PARAMETERS}

Do Not Delete Instance On Multiple Applies
    [Documentation]        Create Multiple Network Interfaces Instance And Check That Regeneration Does Not Destroy Instance
    Launch Terraform Deployment                 ${CURDIR}/../data/subnets    ${TF_PARAMETERS}
    ${states_begin}   Load Terraform States     ${CURDIR}/../data/subnets
    Launch Terraform Deployment                 ${CURDIR}/../data/subnets    ${TF_PARAMETERS}
    ${states_end}     Load Terraform States     ${CURDIR}/../data/subnets
    Should Be Equal As Strings                  ${states_begin['test']['outputs']['instance']['value']['id']}    ${states_end['test']['outputs']['instance']['value']['id']}
    [Teardown]  Destroy Terraform Deployment    ${CURDIR}/../data/subnets    ${TF_PARAMETERS}

