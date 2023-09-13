import ipywidgets as ipw


class ButtonRow(ipw.HBox):

    def __init__(self, *names):
        self.buttons = buttons = [
            ipw.Button(description=n) for n in names
        ]
        super().__init__(buttons)

    def __iter__(self):
        return iter(self.buttons)



