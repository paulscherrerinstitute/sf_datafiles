
class FileDemultiplexer(set):

    def close(self):
        for f in self:
            f.close()


