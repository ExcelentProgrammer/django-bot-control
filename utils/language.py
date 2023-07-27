import json
import os

from config.settings import BASE_DIR


class Language:

    def __init__(self, language):
        self.file_path = BASE_DIR.joinpath(f"languages/{language}.json")

        if not os.path.exists(self.file_path):
            with open(self.file_path, "wb") as file:
                json.dump({}, file)
                file.close()

    def get(self, key, default=None, **kwargs):
        data = self.read()

        try:
            return str(data[key]).format(**kwargs)
        except:
            return default

    def read(self):
        with open(self.file_path, "rb") as file:
            data = json.load(file)
            file.close()
            return data
