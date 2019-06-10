import uuid


class Serializer:
    def __init__(self):
        pass

    def serialize(self, obj):
        """Serialize an arbitrary object, but specifically support circular dictionaries."""

        # is this a dictionary?
        if isinstance(obj, dict):
            return self.serialize_dict(obj)
        return self.serialize_primitive(obj)

    def serialize_dict(self, d, seen={}):
        s = {"type": "dict", "values": [], "id": str(uuid.uuid4())}

        # store this dictionary's ID first
        seen[id(d)] = s["id"]

        for k, v in d.items():
            if isinstance(v, dict):
                if id(v) in seen:
                    val = {"type": "reference", "value": seen[id(v)], "key": k}
                else:
                    seen[id(v)] = s["id"]
                    val = self.serialize_dict(v, seen)
                s["values"].append(val)
            else:
                val = self.serialize(v)
                val["key"] = k
                s["values"].append(val)
        return s

    def serialize_primitive(self, p):
        return {"type": "primitive", "value": p}
