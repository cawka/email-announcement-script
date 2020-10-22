#!/usr/bin/env python3

import sys
import yaml
import pathlib
import argparse
import ics

from ics import Calendar, Event
from datetime import datetime, timezone
from dateutil import parser
import pytz
import uuid

parser = argparse.ArgumentParser()
parser.add_argument('input', help='.yml file with announcement parameters')
parser.add_argument('command', nargs='?', help="'send' to actually send out, otherwise test run")
parser.add_argument('-s', nargs='?', default="", dest='subject_prefix', help='Prefix for the subject line, e.g., "Reminder: "')
parser.add_argument('--st', nargs='?', default="subject.txt", dest="subject_template", help='Subject template file')
parser.add_argument('-t', dest='template', default='template.html', help='HTML template for the email')
parser.add_argument('--from-name')
parser.add_argument('--from-email')
parser.add_argument('--emails')
parser.add_argument('--ical', default='ical-template.ics')
parser.add_argument('--info', default="")

args = parser.parse_args()

template = open(args.template).read()
subject = open(args.subject_template).read()

yml = pathlib.Path(args.input)

with yml.open(encoding='utf-8') as f:
    info = yaml.load(f, yaml.SafeLoader)

info = {k.lower(): v for k, v in info.items()}

date = datetime.strptime(info['date'], "%B %d, %Y")
info['date'] = date.strftime("%A, %B %d, %Y")
info['image'] = "images/" + info['photo']

infoOrig = {}

for key in info:
    infoOrig[key+"_orig"] = info[key].replace("\n", "\\n")
    info[key] = info[key].replace("\n", "\n<p style='margin-top: 0.4em'>")

info = {**info, **infoOrig}
    
for key in info:
    template = template.replace("@@%s@@" % key.upper(), info[key])
    subject = subject.replace("@@%s@@" % key.upper(), info[key])

outname = yml.parts[len(yml.parts)-1].replace('.yml', '.html')
out = open(outname, "wt", encoding="utf-8")
out.write(template)
out.close()

starttime, stoptime = info['time'].split('-')

begin = datetime.strptime("%s %s" % (info['date'], starttime), "%A, %B %d, %Y %I:%M%p")
end = datetime.strptime("%s %s" % (info['date'], stoptime), "%A, %B %d, %Y %I:%M%p")
duration = end - begin

def format(date, suffix=''):
    return date.strftime('%Y%m%dT%H%M%S' + suffix)

calparams = {
    'dtstamp': format(datetime.utcnow(), 'Z'),
    'created': format(datetime.utcnow(), 'Z'),
    'last-modified': format(datetime.utcnow(), 'Z'),
    'room': info['zoomlink'],
    'subject': subject.split(" on ")[0],
    'description': '%s\\n%s\\n\\nTitle: %s\\n\\nAbstract: %s\\n\\nBio: %s\\n%s' % (info['zoomlink_orig'], info['zoominfo_orig'], info['topic_orig'], info['abstract_orig'], info['bio_orig'], args.info),
    'begin': format(begin),
    'end': format(end),
    'uid': str(uuid.uuid1()).upper(),
    'uid1': str(uuid.uuid1()).upper(),
    }

outf_ical = 'ical-seminar-event-%s.ics' % str(uuid.uuid1()).upper()

with open(args.ical, 'rt', encoding='utf-8') as f:
    ics = f.read()
    for key in calparams:
        ics = ics.replace("@@%s@@" % key.upper(), calparams[key])
    with open(outf_ical, 'wt', newline='\r\n', encoding='utf-8') as outf:
        outf.write(ics)

from script import pymailer

class Args:
    test = True
    html = [outname]
    image = ['fiu-logo.png', info['image']]
    addresses = ['emails.csv']
    subject = ["%s%s" % (args.subject_prefix, subject)]
    txt = ''
    attach = [['text/calendar', outf_ical, 'ical-seminar-event.ics']]

pymailer_args = Args()

if args.from_name:
    pymailer_args.from_name = args.from_name

if args.from_email:
    pymailer_args.from_email = args.from_email

if args.emails:
    pymailer_args.addresses = args.emails

mailer = pymailer.PyMailer(pymailer_args)

if args.command == "send":
    mailer.send()
else:
    mailer.send_test()
