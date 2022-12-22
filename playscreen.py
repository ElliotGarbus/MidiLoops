from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty

from pathlib import Path

# todo next: Add Audio and get files playing

Builder.load_string("""
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
                size_hint_x: None
                width: 20
                disabled: tb.text == '<Empty>'
                on_release: root.clear()
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
            Button:
                id: play_toggle
                text: 'Stop'
                # on_state:
                #     if self.state == 'down': root.play()
                #     if self.state == 'normal': root.stop()
            Button:
                text: 'Next'
        Label:
            size_hint_y: None
            height: dp(24)
            # text: 'Spacebar to Toggle Play/Stop'
""")


class ContentControl(BoxLayout):
    pc = NumericProperty()
    title = StringProperty('<Empty>')
    path = StringProperty()
    volume = NumericProperty(64)  # a value from 0-127, note sound obj volume is from 0-1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound = None

    def play_stop(self, state):
        if state == 'normal':
            self.sound.stop()
        elif state == 'down':
            try:
                self.sound = SoundLoader.load(self.path)
                self.sound.loop = True
                self.sound.volume = self.volume/127
                self.sound.play()
            except OSError:
                print('file not found or bad format')

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


class PlayScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.track = None
        # self.track_path = None  # holds the name of the 1x speed track
        # self.track_stretched = None  # name of stretched track
        # self.time_stretch_processes = {}
        Window.bind(on_drop_file=self._drop_file_action)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def on_kv_post(self, base_widget):
        scroll_box = self.ids.scroll_box
        for i in range(128):
            scroll_box.add_widget(ContentControl(pc=i))

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'spacebar':  # Toggle between play and stop
            # self.ids.play_toggle.state = 'down' if self.ids.play_toggle.state == 'normal' else 'normal'
            pass
            # todo: add spacebar action here

    def _drop_file_action(self, window, filename, *_):
        # the x,y passed into the drop_file event are in sdl coordinates, use mouse_pos
        x, y = window.mouse_pos
        for button in self.ids.scroll_box.children:
            if button.collide_point(*button.to_widget(x, y)):
                button.path = filename.decode("utf-8")
                button.title = Path(button.path).stem
                break



    # def set_backing_track(self, path):
    #     self.ids.speed.text = 'Speed 1x'
    #     self.track = SoundLoader.load(path)
    #     if not self.track:
    #         self.ids.file.text = self.error_msg
    #         self.track_path = None
    #     else:
    #         self.track_path = path
    #         self.ids.file.text = Path(path).stem
    #         self.track.loop = True
    #         self.time_stretch(path)
    #
    # def play(self):
    #     try:
    #         self.track.play()
    #         self.ids.play_toggle.state = 'down'
    #     except AttributeError:
    #         self.ids.file.text = self.error_msg
    #
    # def stop(self):
    #     try:
    #         self.track.stop()
    #         self.ids.play_toggle.state = 'normal'
    #     except AttributeError:
    #         self.ids.file.text = self.error_msg

    # def restart(self):
    #     try:
    #         if self.track.state == 'stop':
    #             self.ids.play_toggle.state = 'down'  # change is state cause track to play
    #         else:
    #             self.track.seek(0)
    #             self.track.play()
    #     except AttributeError:
    #         self.file.text = self.error_msg
    #
    # def set_volume(self, v):  # v is from 0 to 127
    #     try:
    #         self.track.volume = v / 127
    #     except AttributeError:
    #         self.ids.file.text = self.error_msg
    #
    # def set_speed(self, value):
    #     #  value from midi cc message : 1, 2, 3, 4, 5 for speeds  1x, 0.5x, .75x, 1.25x, 1.5x respectively
    #     if value not in [1, 2, 3, 4, 5]:
    #         return
    #     m_speeds = ['Speed 1x', 'Speed 0.5x', 'Speed 0.75x', 'Speed 1.25x', 'Speed 1.5x']
    #     self.ids.speed.text = m_speeds[value - 1]




