from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from functools import partial
import json

# Mappings for tabs
MAPPING = {
    "Device": "device_info",
    "Phone List": "phone_list",
    "Alive": "alive",
    "Din": "din",
    "Ain": "ain",
    "Dout": "dout",
    "Close": "Close",
}


class InfoPopup(Popup):
    def __init__(self, json_data, **kwargs):
        super(InfoPopup, self).__init__(**kwargs)
        self.title = "Information"
        self.size_hint = (1, 1)

        # Create BoxLayout for the popup content
        popup_layout = GridLayout(cols=1, spacing=10)

        # Create TabbedPanel
        tabbed_panel = TabbedPanel(
            do_default_tab=False, height=40, size_hint_y=None, tab_pos="bottom_mid"
        )
        tab_instances = []

        # Create tabs
        tabs = ["Device", "Phone List", "Alive", "Din", "Ain", "Dout", "Close"]
        for tab_text in tabs:
            tab = TabbedPanelItem(text=tab_text)
            tab_instances.append(tab)
            tab.bind(on_release=self.update_info)
            tabbed_panel.add_widget(tab)

        tabbed_panel.default_tab = tab_instances[0]

        # Text input to display information
        self.details_box = GridLayout(cols=1, spacing=10)
        popup_layout.add_widget(self.details_box)
        popup_layout.add_widget(tabbed_panel)

        # Add the BoxLayout to the popup
        self.content = popup_layout

        # Initial update of information
        self.json_data = json_data
        self.update_info(tabbed_panel.default_tab)

    def update_info(self, tab):
        # Get information based on the selected tab
        selected_tab_text = MAPPING[tab.text]
        self.details_box.clear_widgets()  # Clear existing
        self.current_obj_index = 0

        if tab.text == "Close":
            self.dismiss()
            return

        if selected_tab_text in self.json_data:
            self.details_obj = self.json_data[selected_tab_text]
            if isinstance(self.details_obj, dict):
                self.dictionary_parser(self.details_obj)
            else:
                current_obj = self.details_obj[0]
                self.dictionary_parser(current_obj)
                self.create_nav_buttons()
        else:
            text_input = TextInput(text="test2", multiline=False)
            self.details_box.add_widget(text_input)

    def dictionary_parser(self, details_dict):
        for key, value in details_dict.items():
            grid = GridLayout(cols=2, spacing=5, height=40, size_hint_y=None)
            if isinstance(value, dict):
                button = Button(text=f"{key} (See More)")
                button.bind(on_press=partial(self.on_expand_button, value))
                grid.add_widget(button)
            else:
                label = Label(text=key)
                grid.add_widget(label)
            text_input = TextInput(text=json.dumps(value), multiline=True, font_size=15)
            grid.add_widget(text_input)
            self.details_box.add_widget(grid)

    def on_next_button(self, instance):
        self.details_box.clear_widgets()
        if self.current_obj_index < len(self.details_obj) - 1:
            self.current_obj_index += 1
        else:
            self.current_obj_index == len(self.details_obj) - 1
        current_obj = self.details_obj[self.current_obj_index]
        self.dictionary_parser(current_obj)
        self.create_nav_buttons()

    def on_prev_button(self, instance):
        self.details_box.clear_widgets()
        self.current_obj_index -= 1 if self.current_obj_index > 0 else 0
        current_obj = self.details_obj[self.current_obj_index]
        self.dictionary_parser(current_obj)
        self.create_nav_buttons()

    def create_nav_buttons(self):
        button_box = GridLayout(cols=2, spacing=10, padding=10)

        if self.current_obj_index != 0:
            prev_button = Button(text="Prev", height=40, size_hint_y=None)
            prev_button.bind(on_press=self.on_prev_button)
            button_box.add_widget(prev_button)

        if self.current_obj_index != len(self.details_obj) - 1:
            next_button = Button(text="Next", height=40, size_hint_y=None)
            next_button.bind(on_press=self.on_next_button)
            button_box.add_widget(next_button)

        self.details_box.add_widget(button_box)

    def on_expand_button(self, value, instance):
        button_box = GridLayout(cols=2, spacing=10, padding=10)
        for k, v in value.items():
            label = Label(text=k)
            button_box.add_widget(label)
            text_input = TextInput(text=json.dumps(v), multiline=True, font_size=15)
            button_box.add_widget(text_input)
        popup = Popup(
            title="Test popup",
            content=button_box,
            auto_dismiss=True,
            size_hint=(0.8, 0.6),
        )
        popup.open()
