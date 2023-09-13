import ipywidgets as ipw


CB_LAYOUT = ipw.Layout(
    justify_content="center",
    width="100%"
)

CB_STYLE = dict(
    description_width="0px"
)


# with indent=False, the checkbox is not centered correctly.
# with indent=True and description_width (which is the width of the indent) set to zero, it works.


class Checkbox(ipw.Checkbox):

    def __init__(self, *args, value=False, indent=True, layout=CB_LAYOUT, style=CB_STYLE, **kwargs):
        super().__init__(*args, value=value, indent=indent, layout=layout, style=style, **kwargs)

    @property
    def sorting_value(self):
        # sort True (checked) before False (unchecked)
        return 1 if self.value else 2



