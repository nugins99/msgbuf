#!/usr/bin/env python3

import importlib
import yaml
import jinja2
import argparse
import os
import sys
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


def get_lang(args):
    if args.lang == 'cpp':
        return CPP()
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

def get_template(lang):
    #print(importlib_resources.files(__name__))
    return importlib_resources.open_text(package=__package__+'.templates',
                                         resource=f"{lang.template_name}")



def main():
    args = parse_args(sys.argv[1:])
    if args.in_file is None:
        print("No input file specified.")
        return -1
    if not os.path.isfile(args.in_file):
        print(f"Input file does not exist: {args.in_file}")
        return -1


    lang = get_lang(args)
    with open(args.in_file, 'r') as msg_stream:
        data = yaml.load(msg_stream, Loader=yaml.CLoader)
        data["desc"] = lang.comment_lines(split_lines(data["desc"]))

        for field in data["fields"]:
            field["desc"] = lang.comment_lines(split_lines(field["desc"]))
            field["type"] = lang.native_type(field["type"])
    #with open(os.path.join(args.template_dir, lang.template_name), 'r') as template_stream:
    template_stream = get_template(lang)
    tm = jinja2.Template(template_stream.read())
    with open(os.path.join(args.out_dir, f"{data['name']}.hpp"), 'w') as out_stream:
        out_stream.write(tm.render(data=data))


if __name__ == '__main__':
    main()
