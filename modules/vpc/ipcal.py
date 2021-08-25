egress = [
  {
    "protocol":"-1",
    "rule_no":200,
    "action":"allow",
    "cidr_block":"0.0.0.0/0",
    "from_port":0,
    "to_port":0
  }
]
print (egress.0.to_port)