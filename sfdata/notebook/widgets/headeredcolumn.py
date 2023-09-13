import ipywidgets as ipw

from .headerbutton import HeaderButton
from .column import Column


FWD_ATTR_TO_COLUMN = ["get_order", "sort_by", "show_filtered"]


class HeaderedColumn(ipw.VBox):

    def __init__(self, header, children, *args, **kwargs):
        self.header = header = HeaderButton(header)
        self.column = column = Column(children, *args, **kwargs)
        super().__init__(children=[header, column])

    def __iter__(self):
        return iter(self.column.children)

    def __getattr__(self, name):
        if name not in FWD_ATTR_TO_COLUMN:
            tn = type(self).__name__
            raise AttributeError(f"'{tn}' object has no attribute '{name}'")
        return getattr(self.column, name)

    def on_header_click(self, callback):
        # wrap cb to re-wire argument from pressed button to respective Column
        def wrapper(_btn):
            return callback(self.column)
        return self.header.on_click(wrapper)



