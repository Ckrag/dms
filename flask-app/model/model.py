
class App:

    def __init__(self, app_id, description, created):
        self.app_id = app_id
        self.description = description
        self.created = created

    @staticmethod
    def from_tuple(t):
        return App(t[0], t[1], t[2])

    def json(self) -> dict:
        #TODO: test this
        return {
            "id": self.app_id,
            "description": self.description,
            "created": str(self.created)
        }


class Entry:

    def __init__(self, data, created):
        self.data = data
        self.created = created

    @staticmethod
    def from_tuple(t):
        return Entry(t[0], t[1])

    def json(self) -> dict:
        # TODO: test this
        return {
            "data": self.data,
            "created": self.created
        }
