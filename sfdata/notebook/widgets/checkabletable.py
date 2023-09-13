import ipywidgets as ipw

from .checkbox import Checkbox
from .headeredcolumn import HeaderedColumn
from .statictext import StaticText


MAIN_LAYOUT = ipw.Layout(
    border="1px solid black"
)


class CheckableTable(ipw.HBox):

    def __init__(self, header, lines, *args, **kwargs):
        cols = transpose(lines)
        cols_lbls = mk_many_lbls(cols)

        col_names = cols[0]
        self.cbs = mk_cbs(col_names)

        cbs = self.cbs.values()
        cbs = list(cbs)
        self.box_cbs = box_cbs = HeaderedColumn("☑", cbs)

        lbls_boxes = mk_headered_columns(header, cols_lbls)
        self.names_box = lbls_boxes[0]

        self.boxes = boxes = [box_cbs] + lbls_boxes
        super().__init__(boxes, *args, **kwargs)


    def __iter__(self):
        return iter(self.boxes)


    def show_filtered(self, selected):
        for b in self.boxes:
            b.show_filtered(selected)

    def sort_by(self, order):
        for b in self.boxes:
            b.sort_by(order)


    def select_all(self):
        for cb in self.box_cbs:
            cb.value = True

    def clear_selection(self):
        for cb in self.box_cbs:
            cb.value = False

    def invert_selection(self):
        for cb in self.box_cbs:
            cb.value = not cb.value


    def get_list(self):
        items = self.get_dict().items()
        return [name for name, state in items if state]

    def get_filtered_list(self):
        items = self.get_filtered_dict().items()
        return [name for name, state in items if state]

    def get_dict(self):
        return {
            name: cb.value
            for name, cb in self.cbs.items()
        }

    def get_filtered_dict(self):
        return {
            name.value: cb.value
            for name, cb in zip(self.names_box, self.box_cbs)
        }





def transpose(lines):
    return list(zip(*lines))


def mk_cbs(entries):
    return {i: Checkbox() for i in entries}

def mk_lbls(entries):
    return [StaticText(i) for i in entries]

def mk_many_lbls(cols):
    return [mk_lbls(c) for c in cols]

def mk_headered_columns(headers, cols):
    return [HeaderedColumn(h, i) for h, i in zip(headers, cols)]



