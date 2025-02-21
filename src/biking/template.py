import os

from jinja2 import Environment, FileSystemLoader


def write_file(file, content):
    with open(file, "w") as fh:
        fh.write(content)


def render(template_root, path, file, data, output_path, output_file):
    env = Environment(loader=FileSystemLoader(template_root))
    template_path = str(os.path.join(path, file))
    template = env.get_template(template_path)
    content = template.render(data)

    os.makedirs(output_path, exist_ok=True)
    out_file = os.path.join(output_path, output_file)
    write_file(out_file, content)
