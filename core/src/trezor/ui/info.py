from trezor import res, ui
from trezor.ui.button import Button, ButtonConfirm
from trezor.ui.confirm import CONFIRMED
from trezor.ui.text import render_text, TEXT_MARGIN_LEFT, TEXT_LINE_HEIGHT


class DefaultInfoConfirm:

    bg_color = ui.BLACKISH

    class button(ButtonConfirm):
        class normal(ButtonConfirm.normal):
            border_color = ui.BLACKISH

        class disabled(ButtonConfirm.disabled):
            border_color = ui.BLACKISH


class InfoConfirm(ui.Layout):
    DEFAULT_CONFIRM = res.load(ui.ICON_CONFIRM)
    DEFAULT_STYLE = DefaultInfoConfirm

    def __init__(self, text, confirm=DEFAULT_CONFIRM, style=DEFAULT_STYLE):
        self.text = text.split()
        self.style = style
        panel_area = ui.grid(0, n_x=1, n_y=1)
        self.panel_area = panel_area
        confirm_area = ui.grid(4, n_x=1)
        self.confirm = Button(confirm_area, confirm, style.button)
        self.confirm.on_click = self.on_confirm
        self.repaint = True

    def dispatch(self, event, x, y):
        if event == ui.RENDER:
            self.on_render()
        self.confirm.dispatch(event, x, y)

    def on_render(self):
        if self.repaint:
            x, y, w, h = self.panel_area
            bg_color = self.style.bg_color

            # render the background panel
            ui.display.bar_radius(x, y, w, h, bg_color, ui.BG, ui.RADIUS)

            # render the info text
            render_text(
                self.text,
                new_lines=False,
                max_lines=6,
                offset_y=y + TEXT_LINE_HEIGHT,
                offset_x=x + TEXT_MARGIN_LEFT - ui.VIEWX,
                offset_x_max=x + w - ui.VIEWX,
                bg=bg_color,
            )

            self.repaint = False

    def on_confirm(self):
        raise ui.Result(CONFIRMED)