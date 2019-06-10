class Detector:
    def __init__(self):
        pass

    def detect(self, value):
        primitives = self.find_primitives(value)
        for p in primitives:
            p["detected"] = ["lol"]

    def find_primitives(self, value):
        # find all primitives
        primitives = []
        if value["type"] == "primitive":
            primitives.append(value)
        elif value["type"] == "dict":
            for v in value["values"]:
                primitives += self.find_primitives(v)

        return primitives
