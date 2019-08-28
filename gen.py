#!/usr/bin/env python

import sys
import yaml
import pathlib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input', help='.yml file with announcement parameters')
parser.add_argument('command', nargs='?', help="'send' to actually send out, otherwise test run")
parser.add_argument('-s', nargs='?', dest='subject_prefix', help='Prefix for the subject line, e.g., "Reminder: "')

args = parser.parse_args()

template = open("template.html").read()
subject = open("subject.txt").read()

yml = pathlib.Path(args.input)

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
    subject = ["%s%s" % (args.subject_prefix, subject)]
    txt = ''

mailer = pymailer.PyMailer(Args())

if args.command == "send":
    mailer.send()
else:
    mailer.send_test()
