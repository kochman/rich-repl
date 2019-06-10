import re

from urllib.parse import urlparse


class Detector:
    def __init__(self):
        pass

    def detect(self, value):
        primitives = self.find_primitives(value)
        for p in primitives:
            p["detected"] = []
            for k, v in data_detectors.items():
                for detector in v:
                    if detector(p["raw"]):
                        p["detected"].append(k)

    def find_primitives(self, value):
        # find all primitives
        primitives = []
        if value["type"] == "primitive":
            primitives.append(value)
        elif value["type"] == "dict":
            for v in value["values"]:
                primitives += self.find_primitives(v)

        return primitives


def detect_data_uri_image(val):
    if not isinstance(val, (str, bytes)):
        return False
    if not re.search(r"data:image\/(\w+);base64", val):
        return False
    return True


data_detectors = {"image": [detect_data_uri_image]}

