from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from parsed_output_info import InfoPopup
from kivy.config import Config
from kivy.core.window import Window

Config.set("input", "mouse", "mouse,multitouch_on_demand")
Window.size = (530, 900)

import json


class MyApp(App):
    def build(self):
        # Main layout
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Text Input
        text_input = TextInput(
            hint_text="Enter JSON text here", font_size=15, size_hint=(1, 0.95)
        )
        layout.add_widget(text_input)

        # Button
        button = Button(text="Submit", size_hint=(1, 0.05))
        button.bind(on_press=self.on_button_press)
        layout.add_widget(button)

        return layout

    def on_button_press(self, instance):
        # Retrieve the JSON text from the TextInput
        json_text = self.root.children[1].text  # Assuming TextInput is the second child

        # Check if the JSON text is empty
        if not json_text.strip():
            self.show_error_popup("Error!", "JSON text cannot be empty.")
        else:
            # Parse the JSON text
            try:
                json_data = json.loads(json_text)
                # Open the InfoPopup with the parsed JSON data
                InfoPopup(json_data=json_data).open()
            except json.JSONDecodeError as e:
                self.show_error_popup("Error", f"Invalid JSON format: {e}")

    def show_error_popup(self, title, message):
        # Display an error popup
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(None, None),
            size=(500, 100),
        )
        popup.open()


if __name__ == "__main__":
    MyApp().run()
