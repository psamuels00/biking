import yaml


class NoDatesSafeLoader(yaml.SafeLoader):
    pass


def no_automatic_date_constructor(loader, node):
    return loader.construct_scalar(node)


NoDatesSafeLoader.add_constructor("tag:yaml.org,2002:timestamp", no_automatic_date_constructor)


class Journal:
    def __init__(self, params):
        self.params = params

    def load_file(self):
        with open(self.params.journal_file) as fh:
            data = yaml.load(fh, Loader=NoDatesSafeLoader)
        return data

    def remove_notes(self, data):
        # remove "note", "skipped", and "timeline" and entries containing only those fields
        return {
            k: {k2: v2 for k2, v2 in v.items() if k2 not in ("note", "skipped", "timeline")}
            for k, v in data.items()
            if len(v) > 1 or "note" not in v
        }

    def load(self):
        data = self.load_file()
        data = self.remove_notes(data)

        return data
