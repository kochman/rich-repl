class Serializer:
    def __init__(self):
        pass

    def serialize(self, obj):
        """Serialize an arbitrary object, but specifically support circular dictionaries."""

        # is this a dictionary?
        if isinstance(obj, dict):
            return self.serialize_dict(obj)
        return self.serialize_primitive(obj)

    def serialize_dict(self, d, seen=[]):
        s = {}
        for k, v in d.items():
            if isinstance(v, dict):
                if v in seen:
                    val = {"type": "reference", "value": seen.index(v)}
                else:
                    seen.append(v)
                    val = self.serialize_dict(v, seen)
                s[k] = val
            else:
                val = self.serialize(v)
                s[k] = val
        return s

    def serialize_primitive(self, p):
        return {"type": "primitive", "value": p}
