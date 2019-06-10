import uuid

from detector import Detector
from serializer import Serializer

detector = Detector()
serializer = Serializer()


class Session:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.globals = {}
        self.locals = {}

    def evaluate(self, new_input):
        """Returns tuple of output value and whether or not the statement evaluated to a value."""
        try:
            output = eval(new_input, self.globals, self.locals)
            return (output, True)
        except SyntaxError as e:
            exec(new_input, self.globals, self.locals)
            return (None, False)
        except Exception as e:
            return str(e), True


class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self):
        s = Session()
        self.sessions[s.id] = s
        return s.id

    def eval(self, session_id, new_input):
        s = self.sessions[session_id]
        output = s.evaluate(new_input)
        if output[1]:
            serialized = serializer.serialize(output[0])
            detector.detect(serialized)
            return serialized
        return None
