#!/usr/bin/env python

import sys
import yaml
import pathlib

template = open("template.html").read()
subject = open("subject.txt").read()

if len(sys.argv) < 2:
    sys.stderr.write("Usage: ./gen.py <input>.yml\n")
    exit(1)

yml = pathlib.Path(sys.argv[1])

with yml.open() as f:
    info = yaml.load(f, yaml.SafeLoader)


for key in info:
    template = template.replace("@@%s@@" % key.upper(), info[key])
    subject = subject.replace("@@%s@@" % key.upper(), info[key])

outname = yml.parts[len(yml.parts)-1].replace('.yml', '.html')
out = open(outname, "wt")
out.write(template.encode('utf-8'))
out.close()

from script import pymailer

class Args:
    test = True
    html = [outname]
    image = ['fiu-logo.png', info['image']]
    addresses = ['emails.csv']
    subject = [subject]
    txt = ''

mailer = pymailer.PyMailer(Args())

if len(sys.argv) > 2 and sys.argv[2] == "send":
    mailer.send()
else:
    mailer.send_test()
