import uuid


class Session:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.globals = {}
        self.locals = {}

    def evaluate(self, new_input):
        output = eval(new_input, self.globals, self.locals)
        return output


class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self):
        s = Session()
        self.sessions[s.id] = s
        return s.id

    def eval(self, session_id, new_input):
        s = self.sessions[session_id]
        return s.evaluate(new_input)
