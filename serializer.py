import uuid


class Serializer:
    def __init__(self):
        pass

    def serialize(self, obj):
        """Serialize an arbitrary object, but specifically support circular dictionaries."""

        # is this a dictionary?
        if isinstance(obj, dict):
            return self.serialize_dict(obj)
        if isinstance(obj, (str, int, float, bool, tuple)):
            return self.serialize_primitive(obj)
        return self.serialize_unknown(obj)

    def serialize_dict(self, d, seen={}):
        s = {"type": "dict", "value": repr(d), "values": [], "id": str(uuid.uuid4())}

        # store this dictionary's ID first
        seen[id(d)] = s["id"]

        for k, v in d.items():
            if isinstance(v, dict):
                if id(v) in seen:
                    val = {"type": "reference", "value": seen[id(v)], "key": repr(k)}
                else:
                    seen[id(v)] = s["id"]
                    val = self.serialize_dict(v, seen)
                    val["key"] = repr(k)
                s["values"].append(val)
            else:
                val = self.serialize(v)
                val["key"] = repr(k)
                s["values"].append(val)
        return s

    def serialize_primitive(self, p):
        return {"type": "primitive", "value": repr(p), "raw": p}

    def serialize_unknown(self, p):
        return {"type": "unknown", "value": repr(p)}
