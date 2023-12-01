# -------------------------------------------------------
# Copyright (c) [2023] Nadege Lemperiere
# All rights reserved
# -------------------------------------------------------
# Keywords to create data for module test
# -------------------------------------------------------
# Nadège LEMPERIERE, @18 january 2021
# Latest revision: 18 january 2021
# -------------------------------------------------------

# System includes
from json import load, dumps

# Robotframework includes
from robot.libraries.BuiltIn import BuiltIn, _Misc
from robot.api import logger as logger
from robot.api.deco import keyword
ROBOT = False

# ip address manipulation
from ipaddress import IPv4Network

@keyword('Load Ubuntu Test Data')
def load_ubuntu_test_data(vpc, subnet, instance, interfaces, key, account) :

    if len(interfaces) != 1 : raise Exception(str(len(interfaces)) + ' interfaces created instead of 1')

    result = {}
    result['instances'] = []
    result['security_groups'] = []
    result['keys'] = []
    result['interfaces'] = []

    result['instances'].append({})
    result['instances'][0]['name'] = 'ubuntu'
    result['instances'][0]['data'] = {}
    result['instances'][0]['data']['ImageId'] = 'ami-08031206a0ff5a6ac'
    result['instances'][0]['data']['InstanceId'] = instance['id']
    result['instances'][0]['data']['InstanceType'] = 'c5.xlarge'
    result['instances'][0]['data']['Monitoring'] =  {'State': 'enabled'}
    result['instances'][0]['data']['PrivateDnsName'] = interfaces[0]['dns']
    result['instances'][0]['data']['State'] = {'Code': 16, 'Name': 'running'}
    result['instances'][0]['data']['SubnetId'] = subnet
    result['instances'][0]['data']['VpcId'] = vpc
    result['instances'][0]['data']['Architecture'] = 'x86_64'
    result['instances'][0]['data']['BlockDeviceMappings'] = [{'Ebs': {'DeleteOnTermination': True, 'Status': 'attached'}}]
    result['instances'][0]['data']['NetworkInterfaces'] = [{"Attachment": {'DeleteOnTermination' : False, 'DeviceIndex': 0, 'Status': 'attached', 'NetworkCardIndex': 0}, "Description": "", "Groups": [{"GroupName": "test-instance-test-subnet0", "GroupId": interfaces[0]['group']}], "NetworkInterfaceId": interfaces[0]['interface'], "OwnerId": account, "PrivateDnsName": interfaces[0]['dns'], "Status": "in-use", "SubnetId": interfaces[0]['subnet'], "VpcId": vpc, "InterfaceType": "interface"}]
    result['instances'][0]['data']['RootDeviceType'] = 'ebs'
    result['instances'][0]['data']['SecurityGroups'] = [{'GroupId': interfaces[0]['group']}]
    result['instances'][0]['data']['Tags'] = []
    result['instances'][0]['data']['Tags'].append({'Key'          : 'Version'     , 'Value' : 'test'})
    result['instances'][0]['data']['Tags'].append({'Key'          : 'Project'     , 'Value' : 'test'})
    result['instances'][0]['data']['Tags'].append({'Key'          : 'Module'      , 'Value' : 'test'})
    result['instances'][0]['data']['Tags'].append({'Key'          : 'Environment' , 'Value' : 'test'})
    result['instances'][0]['data']['Tags'].append({'Key'          : 'Owner'       , 'Value' : 'moi.moi@moi.fr'})
    result['instances'][0]['data']['Tags'].append({'Key'          : 'Name'        , 'Value' : 'test.test.test.instance.test'})

    result['security_groups'].append({})
    result['security_groups'][0]['name'] = 'ubuntu'
    result['security_groups'][0]['data'] = {}
    result['security_groups'][0]['data']['GroupName'] = 'test-instance-test-subnet0'
    result['security_groups'][0]['data']['IpPermissions'] = []
    result['security_groups'][0]['data']['GroupId'] = interfaces[0]['group']
    result['security_groups'][0]['data']['IpPermissionsEgress'] = []
    result['security_groups'][0]['data']['IpPermissionsEgress'].append({"FromPort": 443, "IpProtocol": "tcp", "IpRanges": [{"CidrIp": "0.0.0.0/0", "Description": "AllowInternetTlsAccess"}], "Ipv6Ranges": [], "PrefixListIds": [], "ToPort": 443, "UserIdGroupPairs": []})
    result['security_groups'][0]['data']['IpPermissionsEgress'].append({"FromPort": 53, "IpProtocol": "udp", "IpRanges": [{"CidrIp": "0.0.0.0/0", "Description": "AllowInternetDnsAccess"}], "Ipv6Ranges": [], "PrefixListIds": [], "ToPort": 53, "UserIdGroupPairs": []})
    result['security_groups'][0]['data']['VpcId'] = vpc
    result['security_groups'][0]['data']['Tags'] = []
    result['security_groups'][0]['data']['Tags'].append({'Key'          : 'Version'     , 'Value' : 'test'})
    result['security_groups'][0]['data']['Tags'].append({'Key'          : 'Project'     , 'Value' : 'test'})
    result['security_groups'][0]['data']['Tags'].append({'Key'          : 'Module'      , 'Value' : 'test'})
    result['security_groups'][0]['data']['Tags'].append({'Key'          : 'Environment' , 'Value' : 'test'})
    result['security_groups'][0]['data']['Tags'].append({'Key'          : 'Owner'       , 'Value' : 'moi.moi@moi.fr'})
    result['security_groups'][0]['data']['Tags'].append({'Key'          : 'Name'        , 'Value' : 'test.test.test.instance.test.subnet0.nsg'})

    result['interfaces'].append({})
    result['interfaces'][0]['name'] = 'ubuntu'
    result['interfaces'][0]['data'] = {}
    result['interfaces'][0]['data']['Attachment'] = { 'DeleteOnTermination': False, 'DeviceIndex': 0, 'NetworkCardIndex': 0, "InstanceId": instance['id'], "InstanceOwnerId": account, "Status": "attached"}
    result['interfaces'][0]['data']['Groups'] = [{"GroupName": "test-instance-test-subnet0", "GroupId": interfaces[0]['group']}]
    result['interfaces'][0]['data']['InterfaceType'] = "interface"
    result['interfaces'][0]['data']['NetworkInterfaceId'] = interfaces[0]['interface']
    result['interfaces'][0]['data']['OwnerId'] = account
    result['interfaces'][0]['data']['PrivateDnsName'] = interfaces[0]['dns']
    result['interfaces'][0]['data']['PrivateIpAddresses'] = [{"Primary": True, "PrivateDnsName": interfaces[0]['dns']}]
    result['interfaces'][0]['data']['SourceDestCheck'] = True
    result['interfaces'][0]['data']['Status'] = "in-use"
    result['interfaces'][0]['data']['SubnetId']= interfaces[0]['subnet']
    result['interfaces'][0]['data']['VpcId'] = vpc
    result['interfaces'][0]['data']['TagSet'] = []
    result['interfaces'][0]['data']['TagSet'].append({'Key'          : 'Version'     , 'Value' : 'test'})
    result['interfaces'][0]['data']['TagSet'].append({'Key'          : 'Project'     , 'Value' : 'test'})
    result['interfaces'][0]['data']['TagSet'].append({'Key'          : 'Module'      , 'Value' : 'test'})
    result['interfaces'][0]['data']['TagSet'].append({'Key'          : 'Environment' , 'Value' : 'test'})
    result['interfaces'][0]['data']['TagSet'].append({'Key'          : 'Owner'       , 'Value' : 'moi.moi@moi.fr'})
    result['interfaces'][0]['data']['TagSet'].append({'Key'          : 'Name'        , 'Value' : 'test.test.test.instance.test.subnet0.interface'})


    result['keys'].append({})
    result['keys'][0]['name'] = 'ubuntu'
    result['keys'][0]['data'] = {}
    result['keys'][0]['data']['KeyId']                   = key['id']
    result['keys'][0]['data']['Arn']                     = key['arn']
    result['keys'][0]['data']['Enabled']                 = True
    result['keys'][0]['data']['KeyUsage']                = 'ENCRYPT_DECRYPT'
    result['keys'][0]['data']['KeyState']                = 'Enabled'
    result['keys'][0]['data']['Origin']                  = 'AWS_KMS'
    result['keys'][0]['data']['CustomerMasterKeySpec']   = 'SYMMETRIC_DEFAULT'
    result['keys'][0]['data']['AWSAccountId']            = account
    result['keys'][0]['data']['Policy']                  = {"Version": "2012-10-17", "Statement": [{"Sid": "AllowKeyModificationToRootAndGod", "Effect": "Allow", "Principal": {"AWS": ["arn:aws:iam::833168553325:user/principal", "arn:aws:iam::833168553325:root"]}, "Action": "kms:*", "Resource": "*"}]}
    result['keys'][0]['data']['Tags']                    = []
    result['keys'][0]['data']['Tags'].append({'TagKey'        : 'Version'             , 'TagValue' : 'test'})
    result['keys'][0]['data']['Tags'].append({'TagKey'        : 'Project'             , 'TagValue' : 'test'})
    result['keys'][0]['data']['Tags'].append({'TagKey'        : 'Module'              , 'TagValue' : 'test'})
    result['keys'][0]['data']['Tags'].append({'TagKey'        : 'Environment'         , 'TagValue' : 'test'})
    result['keys'][0]['data']['Tags'].append({'TagKey'        : 'Owner'               , 'TagValue' : 'moi.moi@moi.fr'})
    result['keys'][0]['data']['Tags'].append({'TagKey'        : 'Name'                , 'TagValue' : 'test.test.test.instance.test'})

    logger.debug(dumps(result))

    return result


@keyword('Load Subnets Test Data')
def load_subnets_test_data(vpc, subnet, instance, interfaces, key, account) :

    if len(interfaces) != 2 : raise Exception(str(len(interfaces)) + ' interfaces created instead of 2')

    result = {}
    result['instances'] = []
    result['security_groups'] = []
    result['keys'] = []
    result['interfaces'] = []

    result['instances'].append({})
    result['instances'][0]['name'] = 'subnets'
    result['instances'][0]['data'] = {}
    result['instances'][0]['data']['ImageId'] = 'ami-0b3a63a48e767cc82'
    result['instances'][0]['data']['InstanceId'] = instance['id']
    result['instances'][0]['data']['InstanceType'] = 't2.nano'
    result['instances'][0]['data']['Monitoring'] =  {'State': 'enabled'}
    result['instances'][0]['data']['PrivateDnsName'] = interfaces[0]['dns']
    result['instances'][0]['data']['State'] = {'Code': 16, 'Name': 'running'}
    result['instances'][0]['data']['SubnetId'] = subnet[0]
    result['instances'][0]['data']['VpcId'] = vpc
    result['instances'][0]['data']['Architecture'] = 'x86_64'
    result['instances'][0]['data']['BlockDeviceMappings'] = [{'Ebs': {'DeleteOnTermination': True, 'Status': 'attached'}}]
    result['instances'][0]['data']['NetworkInterfaces'] = [
        {"Attachment": {'DeleteOnTermination' : False, 'DeviceIndex': 0, 'Status': 'attached', 'NetworkCardIndex': 0}, "Description": "", "Groups": [{"GroupName": "test-instance-test-subnet0", "GroupId": interfaces[0]['group']}], "NetworkInterfaceId": interfaces[0]['interface'], "OwnerId": account, "PrivateDnsName": interfaces[0]['dns'], "Status": "in-use", "SubnetId": interfaces[0]['subnet'], "VpcId": vpc, "InterfaceType": "interface"},
        {"Attachment": {'DeleteOnTermination' : False, 'DeviceIndex': 1, 'Status': 'attached', 'NetworkCardIndex': 0}, "Description": "", "Groups": [{"GroupName": "test-instance-test-subnet1", "GroupId": interfaces[1]['group']}], "NetworkInterfaceId": interfaces[1]['interface'], "OwnerId": account, "PrivateDnsName": interfaces[1]['dns'], "Status": "in-use", "SubnetId": interfaces[1]['subnet'], "VpcId": vpc, "InterfaceType": "interface"}
    ]
    result['instances'][0]['data']['RootDeviceType'] = 'ebs'
    result['instances'][0]['data']['SecurityGroups'] = [{'GroupId': interfaces[0]['group']}]
    result['instances'][0]['data']['Tags'] = []
    result['instances'][0]['data']['Tags'].append({'Key'          : 'Version'     , 'Value' : 'test'})
    result['instances'][0]['data']['Tags'].append({'Key'          : 'Project'     , 'Value' : 'test'})
    result['instances'][0]['data']['Tags'].append({'Key'          : 'Module'      , 'Value' : 'test'})
    result['instances'][0]['data']['Tags'].append({'Key'          : 'Environment' , 'Value' : 'test'})
    result['instances'][0]['data']['Tags'].append({'Key'          : 'Owner'       , 'Value' : 'moi.moi@moi.fr'})
    result['instances'][0]['data']['Tags'].append({'Key'          : 'Name'        , 'Value' : 'test.test.test.instance.test'})


    for i in range(len(interfaces)) :

        result['security_groups'].append({})
        result['security_groups'][i]['name'] = 'subnet' + str(i)
        result['security_groups'][i]['data'] = {}
        result['security_groups'][i]['data']['GroupName'] = 'test-instance-test-subnet' + str(i)
        result['security_groups'][i]['data']['IpPermissions'] = []
        result['security_groups'][i]['data']['GroupId'] = interfaces[i]['group']
        result['security_groups'][i]['data']['IpPermissionsEgress'] = []
        if interfaces[i]['device'] == 0 :
            result['security_groups'][i]['data']['IpPermissionsEgress'].append({"FromPort": 443, "IpProtocol": "tcp", "IpRanges": [{"CidrIp": "0.0.0.0/0", "Description": "AllowInternetTlsAccess"}], "Ipv6Ranges": [], "PrefixListIds": [], "ToPort": 443, "UserIdGroupPairs": []})
            result['security_groups'][i]['data']['IpPermissionsEgress'].append({"FromPort": 53, "IpProtocol": "udp", "IpRanges": [{"CidrIp": "0.0.0.0/0", "Description": "AllowInternetDnsAccess"}], "Ipv6Ranges": [], "PrefixListIds": [], "ToPort": 53, "UserIdGroupPairs": []})
        elif interfaces[i]['device'] == 1 :
            result['security_groups'][i]['data']['IpPermissionsEgress'].append({"FromPort": 22, "IpProtocol": "tcp", "IpRanges": [{"CidrIp": "0.0.0.0/0", "Description": "AllowInternetSshAccess"}], "Ipv6Ranges": [], "PrefixListIds": [], "ToPort": 22, "UserIdGroupPairs": []})
        result['security_groups'][i]['data']['VpcId'] = vpc
        result['security_groups'][i]['data']['Tags'] = []
        result['security_groups'][i]['data']['Tags'].append({'Key'          : 'Version'     , 'Value' : 'test'})
        result['security_groups'][i]['data']['Tags'].append({'Key'          : 'Project'     , 'Value' : 'test'})
        result['security_groups'][i]['data']['Tags'].append({'Key'          : 'Module'      , 'Value' : 'test'})
        result['security_groups'][i]['data']['Tags'].append({'Key'          : 'Environment' , 'Value' : 'test'})
        result['security_groups'][i]['data']['Tags'].append({'Key'          : 'Owner'       , 'Value' : 'moi.moi@moi.fr'})
        result['security_groups'][i]['data']['Tags'].append({'Key'          : 'Name'        , 'Value' : 'test.test.test.instance.test.subnet' + str(i) + '.nsg'})

    for i in range(len(interfaces)) :
        result['interfaces'].append({})
        result['interfaces'][i]['name'] = 'subnet' + str(i)
        result['interfaces'][i]['data'] = {}
        result['interfaces'][i]['data']['Attachment'] = { 'DeleteOnTermination': False, 'DeviceIndex': i, 'NetworkCardIndex': 0, "InstanceId": instance['id'], "InstanceOwnerId": account, "Status": "attached"}
        result['interfaces'][i]['data']['Groups'] = [{"GroupName": "test-instance-test-subnet" + str(i), "GroupId": interfaces[i]['group']}]
        result['interfaces'][i]['data']['InterfaceType'] = "interface"
        result['interfaces'][i]['data']['NetworkInterfaceId'] = interfaces[i]['interface']
        result['interfaces'][i]['data']['OwnerId'] = account
        result['interfaces'][i]['data']['PrivateDnsName'] = interfaces[i]['dns']
        result['interfaces'][i]['data']['PrivateIpAddresses'] = [{"Primary": True, "PrivateDnsName": interfaces[i]['dns']}]
        result['interfaces'][i]['data']['SourceDestCheck'] = True
        result['interfaces'][i]['data']['Status'] = "in-use"
        result['interfaces'][i]['data']['SubnetId'] = interfaces[i]['subnet']
        result['interfaces'][i]['data']['VpcId'] = vpc
        result['interfaces'][i]['data']['TagSet'] = []
        result['interfaces'][i]['data']['TagSet'].append({'Key'          : 'Version'     , 'Value' : 'test'})
        result['interfaces'][i]['data']['TagSet'].append({'Key'          : 'Project'     , 'Value' : 'test'})
        result['interfaces'][i]['data']['TagSet'].append({'Key'          : 'Module'      , 'Value' : 'test'})
        result['interfaces'][i]['data']['TagSet'].append({'Key'          : 'Environment' , 'Value' : 'test'})
        result['interfaces'][i]['data']['TagSet'].append({'Key'          : 'Owner'       , 'Value' : 'moi.moi@moi.fr'})
        result['interfaces'][i]['data']['TagSet'].append({'Key'          : 'Name'        , 'Value' : 'test.test.test.instance.test.subnet' + str(i)+'.interface'})


    result['keys'].append({})
    result['keys'][0]['name'] = 'ubuntu'
    result['keys'][0]['data'] = {}
    result['keys'][0]['data']['KeyId']                   = key['id']
    result['keys'][0]['data']['Arn']                     = key['arn']
    result['keys'][0]['data']['Enabled']                 = True
    result['keys'][0]['data']['KeyUsage']                = 'ENCRYPT_DECRYPT'
    result['keys'][0]['data']['KeyState']                = 'Enabled'
    result['keys'][0]['data']['Origin']                  = 'AWS_KMS'
    result['keys'][0]['data']['CustomerMasterKeySpec']   = 'SYMMETRIC_DEFAULT'
    result['keys'][0]['data']['AWSAccountId']            = account
    result['keys'][0]['data']['Policy']                  = {"Version": "2012-10-17", "Statement": [{"Sid": "AllowKeyModificationToRootAndGod", "Effect": "Allow", "Principal": {"AWS": ["arn:aws:iam::833168553325:user/principal", "arn:aws:iam::833168553325:root"]}, "Action": "kms:*", "Resource": "*"}]}
    result['keys'][0]['data']['Tags']                    = []
    result['keys'][0]['data']['Tags'].append({'TagKey'        : 'Version'             , 'TagValue' : 'test'})
    result['keys'][0]['data']['Tags'].append({'TagKey'        : 'Project'             , 'TagValue' : 'test'})
    result['keys'][0]['data']['Tags'].append({'TagKey'        : 'Module'              , 'TagValue' : 'test'})
    result['keys'][0]['data']['Tags'].append({'TagKey'        : 'Environment'         , 'TagValue' : 'test'})
    result['keys'][0]['data']['Tags'].append({'TagKey'        : 'Owner'               , 'TagValue' : 'moi.moi@moi.fr'})
    result['keys'][0]['data']['Tags'].append({'TagKey'        : 'Name'                , 'TagValue' : 'test.test.test.instance.test'})

    logger.debug(dumps(result))

    return result