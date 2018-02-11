class MissingParameter(Exception):
    def __init__(self, arg):
        self.msg = arg

    def __unicode__(self):
        return str(self.msg)

    def __str__(self):
        return str(self.msg)
