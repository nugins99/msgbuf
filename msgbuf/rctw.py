#!/usr/bin/env python3

import importlib
import yaml
import jinja2
import argparse
import os
import sys
import json
import logging

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)

try:
    import importlib.resources as importlib_resources
except ImportError:
    # In PY<3.7 fall-back to backported `importlib_resources`.
    import importlib_resources


def split_lines(desc):
    return desc.split("\n")


class CPP:
    def comment_lines(self, desc):
        return "\n".join([f"/// {line}" for line in desc])

    def native_type(self, typedef):
        return typedef

    @property
    def template_name(self):
        return 'hpp.template'

class HTML:
    def comment_lines(self, desc):
        return desc

    def native_type(self, typedef):
        return typedef

    @property
    def template_name(self):
        return 'html.template'


def get_lang(args):
    log.debug("Getting language: %s", args.lang)
    if args.lang == 'cpp':
        return CPP()
    elif args.lang == 'html':
        return HTML()
    else:
        raise RuntimeError(f'Invalid language/not implemented: {args.lang}')


def parse_args(args):
    parser = argparse.ArgumentParser(description="Message Buffer Compiler")
    parser.add_argument('--in-file', nargs='?', type=str)
    parser.add_argument('--template-dir', nargs='?',
                        type=str, default='templates')
    parser.add_argument('--out-dir', nargs='?', default='.', type=str)
    parser.add_argument('--lang', nargs='?', default='cpp', type=str)
    return parser.parse_args(args)

def get_template(lang, template_dir):
    #print(importlib_resources.files(__name__))
    #return importlib_resources.open_text(package=__package__+'.templates',
    #                                     resource=f"{lang.template_name}")
    return open(os.path.join(template_dir, lang.template_name), 'r')

def process_udp(service, lang, template_dir, out_dir):
    log.debug("Processing UDP Service: %s", service['name'])
    log.debug("\tpublishing: %s", service['publish'])

def process_tcp(service, lang, template_dir, out_dir):
    log.debug("Processing TCP Service: %s", service['name'])

def processDocument(doc, lang, template_dir, out_dir):
    
    for service_name, service in doc['services'].items():
        log.debug("Processing Service: %s", service_name)
        log.debug("\tDesc: %s", service['desc'])
        if service['protocol'] == 'udp':
            process_udp(service, lang, template_dir, out_dir)
        elif service['protocol'] == 'tcp':
            process_tcp(service, lang, template_dir, out_dir)

    msg = doc['message']
    print("Message: ", json.dumps(msg, indent=2))
    if "desc" in msg:
        msg["desc"] = lang.comment_lines(split_lines(msg["desc"]))
    for name, prop in msg["properties"].items():
        print(name)
    for field in msg["properties"]:
        if "desc" in field:
            field["desc"] = lang.comment_lines(split_lines(field["desc"]))
        if 'type' in field:
            field["type"] = lang.native_type(field["type"])
    #with open(os.path.join(args.template_dir, lang.template_name), 'r') as template_stream:
    template_stream = get_template(lang, template_dir)
    tm = jinja2.Template(template_stream.read())
    with open(os.path.join(out_dir, f"{msg['name']}.hpp"), 'w') as out_stream:
        out_stream.write(tm.render(msg=msg))


def main():
    args = parse_args(sys.argv[1:])
    if args.in_file is None:
        print("No input file specified.")
        return -1
    if not os.path.isfile(args.in_file):
        print(f"Input file does not exist: {args.in_file}")
        return -1

    lang = get_lang(args)

    log.debug(f"Reading in: {args.in_file}")

    with open(args.in_file, 'r') as msg_stream:
        doc = yaml.full_load(msg_stream)
        print("Processing document: ", doc)
        processDocument(doc, lang, args.template_dir, args.out_dir)

if __name__ == '__main__':
    main()
