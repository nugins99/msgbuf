#!/usr/bin/env python3

import yaml
import jinja2
import argparse
import os
import sys


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


def main():
    args = parse_args(sys.argv[1:])

    lang = get_lang(args)
    with open(args.in_file, 'r') as msg_stream:
        data = yaml.load(msg_stream, Loader=yaml.CLoader)
        data["desc"] = lang.comment_lines(split_lines(data["desc"]))

        for field in data["fields"]:
            field["desc"] = lang.comment_lines(split_lines(field["desc"]))
            field["type"] = lang.native_type(field["type"])

    with open(os.path.join(args.template_dir, lang.template_name), 'r') as template_stream:
        tm = jinja2.Template(template_stream.read())
        with open(os.path.join(args.out_dir, f"{data['name']}.hpp"), 'w') as out_stream:
            out_stream.write(tm.render(data=data))


if __name__ == '__main__':
    main()
