from .__typeclass import TypeClass


class Genre(TypeClass):
    def __init__(self, **kwargs):
        super(Genre, self).__init__(**kwargs)
