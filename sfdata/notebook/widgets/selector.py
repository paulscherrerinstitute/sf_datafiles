from fnmatch import fnmatch
from IPython.display import display
import ipywidgets as ipw

from .buttonrow import ButtonRow
from .clearabletext import ClearableText
from .checkabletable import CheckableTable


class Selector(ipw.VBox):

    def __init__(self, entries, header, **kwargs):
        children = self.create_widgets(entries, header)
        super().__init__(children=children, **kwargs)
        self.set_callbacks()


    def __getattr__(self, name):
        if name not in ["get_list", "get_filtered_list", "get_dict", "get_filtered_dict"]:
            tn = type(self).__name__
            raise AttributeError(f"'{tn}' object has no attribute '{name}'")
        return getattr(self.table, name)


    def create_widgets(self, lines, header):
        self.filter_text = filter_text = ClearableText(placeholder="Filter")
        self.btns_select = btns_select = ButtonRow("Select All", "Clear Selection", "Invert Selection")
        self.table = table = CheckableTable(header, lines)
        return [filter_text, btns_select, table]


    def set_callbacks(self):
        @self.filter_text.on_change
        def cb_filter_changed(change):
            pattern = change["new"]
            pattern = f"*{pattern}*"
            selected = [fnmatch(i, pattern) for i in self.table.cbs]
            self.table.show_filtered(selected)


        btn_select_all, btn_clear_selection, btn_invert_selection = self.btns_select

        @btn_select_all.on_click
        def cb_select_all(_btn):
            self.table.select_all()

        @btn_clear_selection.on_click
        def cb_clear_selection(_btn):
            self.table.clear_selection()

        @btn_invert_selection.on_click
        def cb_invert_selection(_btn):
            self.table.invert_selection()


        for column in self.table:
            @column.on_header_click
            def cb_header_clicked(col):
                order = col.get_order()
                self.table.sort_by(order)



