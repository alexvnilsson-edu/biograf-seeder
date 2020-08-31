from .__typeclass import TypeClass


class Movie(TypeClass):
    def __init__(self, **kwargs):
        super(Movie, self).__init__(**kwargs)
