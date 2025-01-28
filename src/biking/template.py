import os

from jinja2 import Environment, FileSystemLoader


def write_file(file, content):
    with open(file, "w") as fh:
        fh.write(content)


def render(path, file, data, output_path, output_file):
    env = Environment(loader=FileSystemLoader(path))
    template = env.get_template(file)
    content = template.render(data)

    out_file = os.path.join(output_path, output_file)
    write_file(out_file, content)
