import ipywidgets as ipw


class Column(ipw.VBox):

    def __init__(self, children, *args, **kwargs):
        self.entries = children
        super().__init__(*args, children=children, **kwargs)

    def get_order(self):
        entries = [i.sorting_value for i in self.children]
        indices = range(len(self.children))
        new_indices = dsu(entries, indices)
        new_indices = dsu(new_indices, indices)
        return new_indices

    def sort_by(self, order):
        # if it is already ordered, reverse the order
        if order == tuple(range(len(order))):
            order = order[::-1]
        self.children = dsu(order, self.children)

    def show_filtered(self, state):
        self.children = [i for i, s in zip(self.entries, state) if s]





def dsu(a, b, key=None):
    return list(zip(*sorted(zip(a, b), key=key)))[1]



