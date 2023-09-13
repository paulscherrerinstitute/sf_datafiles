import ipywidgets as ipw


ST_PADDING = "0 0 0 10px"

ST_LAYOUT_LEFT = ipw.Layout(
    justify_content="flex-start",
    padding=ST_PADDING
)

ST_LAYOUT_RIGHT = ipw.Layout(
    justify_content="flex-end",
    padding=ST_PADDING
)


class StaticText(ipw.Label):

    def __init__(self, value, *args, **kwargs):
        # store the raw value for sorting
        # if converted to str, 55 is next to 555
        self.sorting_value = value

        if isinstance(value, str):
            layout = ST_LAYOUT_LEFT
        else:
            value = str(value)
            layout = ST_LAYOUT_RIGHT

        kwargs.setdefault("layout", layout)

        super().__init__(*args, value=value, **kwargs)



