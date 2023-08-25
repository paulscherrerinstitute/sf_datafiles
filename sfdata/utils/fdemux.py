
class FileDemultiplexer(set):

    def __init__(self, *args, name=None, substitute=None):
        self.name = name
        self.substitute = substitute
        super().__init__(*args)

    def __getitem__(self, key):
        if self.substitute:
            return self.substitute[key]
        else:
            raise ValueError("FileDemultiplexer without substitute is not subscriptable")

    def close(self):
        for f in self:
            f.close()
        if self.substitute:
            self.substitute.close()



