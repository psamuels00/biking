import json


class Journal:
    def __init__(self, params):
        self.params = params

    def load_file(self):
        with open(self.params.journal_file) as fh:
            return json.load(fh)

    def remove_notes(self, data):
        # remove "note" and entries containing only "note"
        return {
            k: {
                k2: v2 for k2, v2 in v.items() if k2 != "note"
            }
            for k, v in data.items() if len(v) > 1 or "note" not in v
        }

    def load(self):
        data = self.load_file()
        data = self.remove_notes(data)

        return data