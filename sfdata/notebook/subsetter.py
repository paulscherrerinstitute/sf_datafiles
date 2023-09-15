from sfdata.utils import dip, percentage_missing
from .widgets import Selector


class SubSetter(Selector):

    def __init__(self, sfd):
        self.sfd = sfd
        n_shared_pids, n_all_pids = get_general(sfd)
        names = [get_line(n, sfd,n_shared_pids, n_all_pids) for n in sfd.names]
        super().__init__(names, ["Name", "#valid", "#shared", "#total", "%"])

    def get(self):
        selection = self.get_filtered_list()
        return self.sfd[selection]





def get_general(sfd):
    shared_pids = sfd.pids
    all_pids    = sfd.all_pids

    n_shared_pids = len(shared_pids)
    n_all_pids    = len(all_pids)

    return n_shared_pids, n_all_pids


def get_line(name, sfd, n_shared_pids, n_all_pids):
    ch = sfd[name]
    n_valid = ch.nvalid
    perc = percentage_missing(n_valid, n_all_pids)
    blocks = dip(perc)
    return (name, n_valid, n_shared_pids, n_all_pids, blocks)



