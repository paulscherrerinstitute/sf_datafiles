import ipywidgets as ipw


HB_LAYOUT = ipw.Layout(
    width="100%"
)


class HeaderButton(ipw.Button):

    def __init__(self, description, *args, layout=HB_LAYOUT, **kwargs):
        super().__init__(*args, description=description, layout=layout, **kwargs)



