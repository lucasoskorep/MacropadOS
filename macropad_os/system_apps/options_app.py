import terminalio

from adafruit_display_text import label
from adafruit_display_text.scrolling_label import ScrollingLabel
from adafruit_displayio_layout.layouts.grid_layout import GridLayout

from macropad_os import App, Config
from macropad_os.app_utils import arrows_yes_no, arrows_with_enter, up_down_enter, clamp


class OptionsState(object):
    UNINIT = "uninit"
    VIEWING = "viewing"
    SELECTING = "selecting"


down_arrow_text = "vvvvvvvvvvvvvvvvvvvv"
down_arrow_not_shown = ""


class OptionsApp(App):
    def __init__(self, macropad, config: Config):
        super().__init__(macropad, config)
        self.send_keyboard_inputs = 0
        self.key_colors = arrows_yes_no
        self.possible_key_colors = [arrows_yes_no, arrows_with_enter, up_down_enter]
        self.counter = 0
        self.title = "Options"
        self.cursor_index = -1
        self.next_cursor_index = 0
        self.bottom_nav_label = label.Label(
            terminalio.FONT,
            text=down_arrow_text,
            background_tight=False,
            padding_left=100,
            padding_right=100
        )
        self.sorted_settings_keys = []
        self.state = OptionsState.UNINIT
        self.display_labels = [
            [ScrollingLabel(terminalio.FONT, text=" ", max_characters=11, animate_time=0.5) for _ in range(3)],
            [label.Label(terminalio.FONT, text="") for _ in range(3)]
        ]
        self.selected_item = None
        self.selected_item_new_value = None
        self.is_dev_mode_active = self.config.get_item_by_name("dev_mode_active").value

    def on_start(self):
        self.set_title(self.title)
        if not self.is_dev_mode_active:
            self.set_layout(GridLayout(x=0, y=9, width=128, height=54, grid_size=(3, 4), cell_padding=1))
            self._update_settings_items()
            self.update_settings_menu()
            self.set_colors(arrows_yes_no)
            self.register_on_key_pressed(self.on_key_pressed)
            self.register_on_encoder_changed(self.on_wheel_change)
        else:
            self.set_layout(GridLayout(x=0, y=9, width=128, height=54, grid_size=(1, 4), cell_padding=1))
            self._layout.add_content(label.Label(terminalio.FONT, text="Disabled in dev-mode"), grid_position=(0, 0),
                                     cell_size=(1, 1))
            self._layout.add_content(label.Label(terminalio.FONT, text="reboot device to exit"), grid_position=(0, 1),
                                     cell_size=(1, 1))

    def _update_settings_items(self):
        self.sorted_settings_keys = []
        for config_item_name in self.config.get_items().keys():
            dependency = self.config.get_item_by_name(config_item_name).dependency
            dep_check = True
            if dependency is not None:
                for k, v in dependency.items():
                    config_item = self.config.get_item_by_name(k)
                    if not config_item or config_item.value != v:
                        dep_check = False
                if dep_check:
                    self.sorted_settings_keys.append(config_item_name)
            else:
                self.sorted_settings_keys.append(config_item_name)
        print("SORTED KEYS")
        self.sorted_settings_keys = sorted(self.sorted_settings_keys)
        print(self.sorted_settings_keys)
        self._scroll()

    def _initialize_menu(self):
        for y in range(3):
            self._layout.add_content(self.display_labels[0][y], grid_position=(0, y), cell_size=(2, 1))
            self._layout.add_content(self.display_labels[1][y], grid_position=(2, y), cell_size=(1, 1))
        self._layout.add_content(self.bottom_nav_label, grid_position=(0, 3), cell_size=(3, 1))
        self.state = OptionsState.VIEWING

    def update_settings_menu(self):
        self.next_cursor_index = clamp(self.next_cursor_index, 0, len(self.sorted_settings_keys) - 1)
        if self.state == OptionsState.UNINIT:
            self._initialize_menu()
        if self.state == OptionsState.VIEWING and self.next_cursor_index != self.cursor_index:
            self._scroll()
        if self.state == OptionsState.SELECTING:
            self._update_selected_item()

    def _update_selected_item(self):
        if self.state == OptionsState.VIEWING:
            self.display_labels[1][0].background_color = None
            self.display_labels[1][0].color = 0xffffff
        if self.state == OptionsState.SELECTING:
            self.display_labels[1][0].background_color = 0xffffff
            self.display_labels[1][0].color = 0x000000

    def _up(self):
        if self.state == OptionsState.VIEWING:
            self.next_cursor_index -= 1
        elif self.state == OptionsState.SELECTING:
            if self.selected_item.available_values != None:
                avail_values = self.selected_item.available_values
                item_index = avail_values.index(self.selected_item_new_value) - 1
                item_index = clamp(item_index, 0, len(avail_values) - 1)
                self.selected_item_new_value = avail_values[item_index]
            elif self.selected_item.value_range != None:
                self.selected_item_new_value += 1
                self.selected_item_new_value = clamp(
                    self.selected_item_new_value,
                    self.selected_item.value_range.start,
                    self.selected_item.value_range.end
                )
            self.display_labels[1][0].text = f"{self.selected_item_new_value}"

    def _down(self):
        if self.state == OptionsState.VIEWING:
            self.next_cursor_index += 1
        elif self.state == OptionsState.SELECTING:
            if self.selected_item.available_values != None:
                avail_values = self.selected_item.available_values
                item_index = avail_values.index(self.selected_item_new_value) + 1
                item_index = clamp(item_index, 0, len(avail_values) - 1)
                self.selected_item_new_value = avail_values[item_index]
            elif self.selected_item.value_range != None:
                self.selected_item_new_value -= 1
                self.selected_item_new_value = clamp(
                    self.selected_item_new_value,
                    self.selected_item.value_range.start,
                    self.selected_item.value_range.end
                )
            self.display_labels[1][0].text = f"{self.selected_item_new_value}"

    def _select(self):
        if self.state == OptionsState.VIEWING:
            self.state = OptionsState.SELECTING
            self.selected_item = self.config.get_item_by_name(self.sorted_settings_keys[self.cursor_index])
            self.selected_item_new_value = self.selected_item.value
        elif self.state == OptionsState.SELECTING:
            self.state = OptionsState.VIEWING
            self.selected_item.value = self.selected_item_new_value
            self.config.set_item(self.selected_item)
            if not self.is_dev_mode_active:
                self.config.save()
                self._update_settings_items()
            self._update_selected_item()

    def _cancel(self):
        if self.state == OptionsState.VIEWING:
            print("Cancel called during viewing")
        elif self.state == OptionsState.SELECTING:
            self.state = OptionsState.VIEWING
            self.selected_item_new_value = self.selected_item.value
            self._update_selected_item()

    def _scroll(self):
        self.cursor_index = self.next_cursor_index
        keys = self.sorted_settings_keys[self.cursor_index:self.cursor_index + 3]
        print(keys)
        for y in range(3):
            if y < len(keys):
                self.display_labels[0][y].text = f">{keys[y]}" if y == 0 else keys[y]
                self.display_labels[1][y].text = f"{self.config.get_item_by_name(keys[y]).value}"
            else:
                self.display_labels[0][y].text = " "
                self.display_labels[1][y].text = " "
        if self.display_labels[0][2].text == " ":
            self.bottom_nav_label.text = down_arrow_not_shown
        else:
            self.bottom_nav_label.text = down_arrow_text

    def on_resume(self):
        print("resume from the options app!")

    def on_pause(self):
        print("Pausing")

    def on_stop(self):
        print("Stopping")

    def on_loop(self):
        pass

    def on_key_pressed(self, keyevent):
        print(keyevent)
        if keyevent == 4:
            self._down()
        elif keyevent == 1:
            self._up()
        elif keyevent == 5:
            self._select()
        elif keyevent == 3:
            self._cancel()
        self.update_settings_menu()

    def on_wheel_change(self, event):
        if event > 0:
            self._up()
        else:
            self._down()
        self.update_settings_menu()
