#!/usr/bin/env python
from constructs import Construct
from cdktf import TerraformStack, TerraformOutput
from imports.aws import VpcPeeringConnection,SecurityGroup, NetworkAcl, NatGateway, Eip, AwsProvider, ShieldProtection, Vpc, InternetGateway, Subnet,DbSubnetGroup,RouteTable,RouteTableAssociation
#Project information 
PROJECT="LandingZone"
ENV="dev"
OWNER="DNC"
REGION="ap-northeast-1"
AVAILABILITY_ZONE = ["ap-northeast-1a","ap-northeast-1c"] 
VPC_CIDR_BLOCK="10.10.0.0/16"
PUBLIC_SUBNETS = ["10.10.1.0/24","10.10.2.0/24"]
PRIVATE_SUBNETS = ["10.10.2.0/24","10.10.3.0/24","10.10.4.0/24","10.10.5.0/24"]
#Network Access List Ingress Control
ALC_INGRESS_CIDR_BLOCK="0.0.0.0/0"
ALC_INGRESS_FROM_PORT=0
ALC_INGRESS_TO_PORT=0
ALC_INGRESS_RULE_NO=200
ALC_INGRESS_PROTOCOL="tcp"
#VPC Peer
PEER_VPC_ID=""
PEER_REGION=""
PEER_OWNER_ID=""
class awsVPC(TerraformStack):
  def __init__(self, scope: Construct, ns: str):
    super().__init__(scope, ns)
    AwsProvider(self, 'Aws', region=REGION)
    VPC = Vpc(self, 'VPC',
      cidr_block = VPC_CIDR_BLOCK,
      enable_dns_support   = True,
      enable_dns_hostnames = True,
      tags       = {
          "Name":"%s-%s-vpc" % (PROJECT, ENV),
          "CreatedBy":OWNER
      }
    )
    IGW = InternetGateway(self, 'InternetGateWay',
      vpc_id  = VPC.id,
      tags    = {
          "Name":"%s-%s-Igw" % (PROJECT, ENV),
          "CreatedBy":OWNER
      }
    )
    PRIVATE_SUBNET_01 = Subnet(self, 'privateSubnet01', 
      availability_zone       = AVAILABILITY_ZONE[0],
      vpc_id                  = VPC.id,
      cidr_block              = PRIVATE_SUBNETS[0],
      map_public_ip_on_launch = False,
      tags    = {
          "Name":"%s-%s-privateSubnet01" % (PROJECT, ENV),
          "CreatedBy":OWNER
      }
    )
    PRIVATE_SUBNET_02 = Subnet(self, 'privateSubnet02', 
      availability_zone       = AVAILABILITY_ZONE[1],
      vpc_id                  = VPC.id,
      cidr_block              = PRIVATE_SUBNETS[1],
      map_public_ip_on_launch = False,
      tags    = {
          "Name":"%s-%s-privateSubnet02" % (PROJECT, ENV),
          "CreatedBy":OWNER
      }
    )
    PRIVATE_SUBNET_03 = Subnet(self, 'privateSubnet03', 
      availability_zone       = AVAILABILITY_ZONE[0],
      vpc_id                  = VPC.id,
      cidr_block              = PRIVATE_SUBNETS[2],
      map_public_ip_on_launch = False,
      tags    = {
          "Name":"%s-%s-privateSubnet03" % (PROJECT, ENV),
          "CreatedBy":OWNER
      }
    )
    PRIVATE_SUBNET_04 = Subnet(self, 'privateSubnet04', 
      availability_zone       = AVAILABILITY_ZONE[1],
      vpc_id                  = VPC.id,
      cidr_block              = PRIVATE_SUBNETS[3],
      map_public_ip_on_launch = False,
      tags    = {
          "Name":"%s-%s-privateSubnet04" % (PROJECT, ENV),
          "CreatedBy":OWNER
      }
    )
    PUBLIC_SUBNET_01 = Subnet(self, 'publicSubnet01', 
      availability_zone       = AVAILABILITY_ZONE[0],
      vpc_id                  = VPC.id,
      cidr_block              = PUBLIC_SUBNETS[0],
      map_public_ip_on_launch = True,
      tags    = {
          "Name":"%s-%s-publicSubnet01" % (PROJECT, ENV),
          "CreatedBy":OWNER
      }
    )
    PUBLIC_SUBNET_02 = Subnet(self, 'publicSubnet02', 
      availability_zone       = AVAILABILITY_ZONE[1],
      vpc_id                  = VPC.id,
      cidr_block              = PUBLIC_SUBNETS[1],
      map_public_ip_on_launch = True,
      tags    = {
          "Name":"%s-%s-publicSubnet02" % (PROJECT, ENV),
          "CreatedBy":OWNER
      }
    )
    DB_SUBNET_GROUP = DbSubnetGroup(self, 'DatabaseSubnetGroup',
      name = "posgres_subnet_group",
      subnet_ids = [PRIVATE_SUBNET_03.id,PRIVATE_SUBNET_04.id],
      tags    = {
        "Name":"%s-%s-DatabaseSubnetGroup" % (PROJECT, ENV),
        "CreatedBy":OWNER
      }
    )
    ROUTE_PUBLIC_SUBNET = RouteTable(self, 'publicSubRouteTable',
      vpc_id = VPC.id,
      route = [{
        "cidr_block":"0.0.0.0/0",
        "gateway_id":IGW.id
      }],
      tags    = {
        "Name":"%s-%s-publicSubRouteTable" % (PROJECT, ENV),
        "CreatedBy":OWNER
      }
    )
    ROUTE_ASSOCIATION_PUBLIC_SUB_01 = RouteTableAssociation(self,'publicSubRouteAssociation01',
      subnet_id      = PUBLIC_SUBNET_01.id,
      route_table_id = ROUTE_PUBLIC_SUBNET.id
    )
    ROUTE_ASSOCIATION_PUBLIC_SUB_02 = RouteTableAssociation(self,'publicSubRouteAssociation02',
      subnet_id      = PUBLIC_SUBNET_02.id,
      route_table_id = ROUTE_PUBLIC_SUBNET.id
    )
    AWS_EIP_01 = Eip(self, 'aws_eip_01',
      vpc = True,
      tags    = {
        "Name":"%s-%s-eip-01" % (PROJECT, ENV),
        "CreatedBy":OWNER
      }
    )
    AWS_EIP_02 = Eip(self, 'aws_eip_02',
      vpc = True,
      tags    = {
        "Name":"%s-%s-eip-02" % (PROJECT, ENV),
        "CreatedBy":OWNER
      }
    )
    NAT_GATEWAY_01 = NatGateway(self, "natgateway-01",
      allocation_id = AWS_EIP_01.id,
      subnet_id  = PUBLIC_SUBNET_01.id,
      tags    = {
        "Name":"%s-%s-natgateway-01" % (PROJECT, ENV),
        "CreatedBy":OWNER
      }
    )
    NAT_GATEWAY_02 = NatGateway(self, "natgateway-02",
      allocation_id = AWS_EIP_02.id,
      subnet_id  = PUBLIC_SUBNET_02.id,
      tags    = {
        "Name":"%s-%s-natgateway-02" % (PROJECT, ENV),
        "CreatedBy":OWNER
      }
    )
    ROUTE_PRIVATE_SUBNET_01 = RouteTable(self, 'privateSubRouteTable01',
      vpc_id = VPC.id,
      route = [{
        "cidr_block":"0.0.0.0/0",
        "gateway_id":NAT_GATEWAY_01.id
      }],
      tags    = {
        "Name":"%s-%s-privateSubRouteTable01" % (PROJECT, ENV),
        "CreatedBy":OWNER
      }
    ) 
    ROUTE_ASSOCIATION_PRIVATE_SUB_01 = RouteTableAssociation(self,'privateSubRouteAssociation01',
      subnet_id      = PRIVATE_SUBNET_01.id,
      route_table_id = ROUTE_PRIVATE_SUBNET_01.id
    )
    ROUTE_PRIVATE_SUBNET_02 = RouteTable(self, 'privateSubRouteTable02',
      vpc_id = VPC.id,
      route = [{
        "cidr_block":"0.0.0.0/0",
        "gateway_id":NAT_GATEWAY_02.id
      }],
      tags    = {
        "Name":"%s-%s-privateSubRouteTable02" % (PROJECT, ENV),
        "CreatedBy":OWNER
      }
    ) 
    ROUTE_ASSOCIATION_PRIVATE_SUB_02 = RouteTableAssociation(self,'privateSubRouteAssociation02',
      subnet_id      = PRIVATE_SUBNET_02.id,
      route_table_id = ROUTE_PRIVATE_SUBNET_02.id
    )
    NET_ACLS_DATABASE = NetworkAcl(self, 'NetworkAclDatabase',
      vpc_id = VPC.id,
      subnet_ids = [PRIVATE_SUBNET_03.id, PRIVATE_SUBNET_04.id],
      egress = [
        {
          "protocol":"-1",
          "rule_no":ALC_INGRESS_RULE_NO,
          "action":"allow",
          "cidr_block":"0.0.0.0/0",
          "from_port":0,
          "to_port":0
        }
      ],
      ingress = [
        {
          "action":"allow",
          "cidr_block":ALC_INGRESS_CIDR_BLOCK,
          "protocol":ALC_INGRESS_PROTOCOL,
          "rule_no":ALC_INGRESS_RULE_NO,
          "from_port":ALC_INGRESS_FROM_PORT,
          "to_port":ALC_INGRESS_TO_PORT,
        }
      ]
    )
    SECURITY_GROUP_WEB_SERVICE = SecurityGroup(self,'SecurityGroupWebService',
      name        = "SecurityGroupWebService",
      description = "Allow access web services",
      vpc_id      = VPC.id,
      ingress = [{
        "description":"Allow 443 from anywhere",
        "from_port":443,
        "to_port":443,
        "protocol":"tcp",
        "cidr_blocks":"[0.0.0.0/0]"
      },
      {
        "description":"Allow 80 from anywhere for redirection",
        "from_port":80,
        "to_port":80,
        "protocol":"tcp",
        "cidr_blocks":["0.0.0.0/0"],
      }],
      egress = [{
        "from_port":0,
        "to_port":0,
        "protocol":"-1",
        "cidr_blocks":"[0.0.0.0/0]",
      }]
    )
    VPC_PEERING_CONNECTION = VpcPeeringConnection(self,'VpcPeeringConnection',
      peer_owner_id = PEER_OWNER_ID,
      peer_vpc_id   = PEER_VPC_ID,
      peer_region   = PEER_REGION,
      vpc_id        = VPC.id,
      auto_accept   = True,
      tags    = {
        "Name":"%s-%s-VpcPeeringConnection" % (PROJECT, ENV),
        "CreatedBy":OWNER
      }
    )
