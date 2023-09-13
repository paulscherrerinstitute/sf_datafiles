import ipywidgets as ipw


CT_LAYOUT = ipw.Layout(
    width="30px"
)


class ClearableText(ipw.HBox):

    def __init__(self, *args, **kwargs):
        self.txt = txt = ipw.Text(*args, **kwargs)
        self.btn = btn = ipw.Button(description="✕", layout=CT_LAYOUT)
        super().__init__([txt, btn])

        @btn.on_click
        def on_button_clicked(_b):
            self.txt.value = ""


    def on_change(self, callback):
        # wrap cb to ignore _property_lock events
        def wrapper(change):
            if change["name"] == "value":
                return callback(change)
        return self.txt.observe(wrapper)



