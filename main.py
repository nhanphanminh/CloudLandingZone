#!/usr/bin/env python
from cdktf import App
from modules.vpc import awsVPC

app = App()

awsVPC(app, "awsVPC")

app.synth()

