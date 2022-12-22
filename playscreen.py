from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty, ObjectProperty

from pathlib import Path

# todo: Play Next

Builder.load_string("""
<ConfirmPopup>:
    size_hint: None, None
    size: 400, 200
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: root.message
        BoxLayout:
            size_hint_y: None
            height: dp(48)
            Button:
                text: 'Cancel'
                on_release: root.dismiss()
            Button:
                text: root.action_text
                on_release: root.action()
    

<ContentControl>:
    padding: dp(20)
    size_hint_y: None
    height: 130
    canvas:
        Color:
            rgb: .5, .5, .5
        RoundedRectangle:
            size: self.size
            pos: self.pos
    Label:
        text: f'{root.pc}'
        size_hint_x: None
        width: 50
        font_size: 20
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            size_hint_y: None
            height: dp(48)
            ToggleButton:
                id: tb
                text: root.title
                group: 'track'
                on_state: root.play_stop(self.state)
                disabled: self.text == '<Empty>' 
            Button:
                id: delete_button
                text: 'X'
                color: 'red'
                size_hint_x: None
                width: 20
                disabled: tb.text == '<Empty>'
                on_release: root.request_clear()
        BoxLayout:
            Slider:
                id: volume
                max: 127
                value: root.volume
                on_value: root.set_volume(self.value)
            Label:
                text: f'{volume.value:.0f}'
                size_hint_x: None
                width: 40

<PlayScreen>:
    BoxLayout:
        orientation: 'vertical'
        ScrollView:
            do_scroll_x: False
            scroll_type: ['bars', 'content']
            bar_width: dp(20)
            bar_inactive_color:  [.7, .7, .7, .5]
            BoxLayout:
                id: scroll_box
                padding: dp(10)
                spacing: dp(10)
                orientation: 'vertical'
                size_hint: None, None
                width: self.parent.width - dp(20)
                height: self.minimum_height
                
        Label:
            size_hint_y: None
            height: dp(24)
            text: 'Drop File on Loop Block'
        BoxLayout:
            size_hint_y: None
            height: dp(48)
            Button:
                text: 'Clear All'
                on_release: root.clear_all_request()
            Button:
                id: play_toggle
                text: 'Stop'
                on_release: root.stop()
            Button:
                text: 'Play Next'
        Label:
            size_hint_y: None
            height: dp(24)
            # text: 'Spacebar to Toggle Play/Stop'
""")


class ConfirmPopup(Popup):
    message = StringProperty()
    action_text = StringProperty()
    action = ObjectProperty()


class ContentControl(BoxLayout):
    pc = NumericProperty()
    title = StringProperty('<Empty>')
    path = StringProperty()
    volume = NumericProperty(64)  # a value from 0-127, note sound obj volume is from 0-1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound = None
        self.popup = None # see clear_request

    def play_stop(self, state):
        if state == 'normal':
            if self.sound:
                self.sound.stop()
        elif state == 'down':
            if self.sound:
                self.sound.loop = True
                self.sound.volume = self.volume/127
                self.sound.play()
            else:
                self.clear()

    def set_volume(self, vol):
        if self.sound and self.sound.state == 'play':
            self.volume = int(vol)
            self.sound.volume = vol/127
        else:
            self.volume = int(vol)

    def clear(self):
        self.ids.tb.state = 'normal'
        self.title = '<Empty>'
        self.path = ''
        self.volume = 64

    def clear_dismiss(self):
        self.clear()
        self.popup.dismiss()

    def request_clear(self):
        self.popup = ConfirmPopup(title='Confirm to clear',
                                  message= f'Clear: {self.title}',
                                  action_text='Clear',
                                  action=self.clear_dismiss)
        self.popup.open()


class PlayScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_drop_file=self._drop_file_action)
        # self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        # self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.popup = None  # holds confirmation popup, see clear_all_request()

    def on_kv_post(self, base_widget):
        scroll_box = self.ids.scroll_box
        for i in range(128):
            scroll_box.add_widget(ContentControl(pc=i))

    # def _keyboard_closed(self):
    #     self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    #     self._keyboard = None
    #
    # def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    #     if keycode[1] == 'spacebar':  # Toggle between play and stop
    #         # self.ids.play_toggle.state = 'down' if self.ids.play_toggle.state == 'normal' else 'normal'
    #         pass
    #         # todo: add spacebar action here

    def _drop_file_action(self, window, filename, *_):
        # the x,y passed into the drop_file event are in sdl coordinates, use mouse_pos
        x, y = window.mouse_pos
        for button in self.ids.scroll_box.children:
            if button.collide_point(*button.to_widget(x, y)):
                button.path = filename.decode("utf-8")
                button.title = Path(button.path).stem
                button.sound = SoundLoader.load(button.path)
                if not button.sound:
                    button.clear()
                break

    def stop(self):
        for button in self.ids.scroll_box.children:
            if button.sound and button.sound.state == 'play':
                button.ids.tb.state = 'normal'

    def clear_all_request(self):
        self.popup = ConfirmPopup(title='Confirm to clear',
                                  message='Confirm to clear all loops',
                                  action_text= 'Clear All',
                                  action=self.clear_all)
        self.popup.open()

    def clear_all(self):
        for button in self.ids.scroll_box.children:
            button.clear()
        self.popup.dismiss()


