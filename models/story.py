from . import Mongua


class Story(Mongua):
    __fields__ = Mongua.__fields__ + [
        ('story_name', str, ''),
        ('title', str, ''),
        ('content', str, ''),
        ('page', int, -1),
    ]
