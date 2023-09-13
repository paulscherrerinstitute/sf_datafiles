from .widgets import Selector


class SubSetter(Selector):

    def __init__(self, sfd):
        self.sfd = sfd
        names = [[n] for n in sfd.names]
        super().__init__(names, ["Name"])

    def get(self):
        selection = self.get_filtered_list()
        return self.sfd[selection]



