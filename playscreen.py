from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.utils import platform

from pathlib import Path
import subprocess
import shlex

Builder.load_string("""
<PlayScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            id: file
            text: 'Background Track Player'  # Replace with filename
            font_size: sp(20)
        Label:
            size_hint_y: None
            height: dp(24)
            text: 'Drop File in Window'
        BoxLayout:
            size_hint_y: None
            height: dp(48)
            Button:
                text: 'Restart'
                # on_release: root.restart()
            ToggleButton:
                id: play_toggle
                text: {'normal': 'Play', 'down': 'Stop'} [self.state]
                # on_state:
                #     if self.state == 'down': root.play()
                #     if self.state == 'normal': root.stop()
            Spinner:
                id: speed
                # text: root.speeds[2]
                # values: root.speeds
                # on_text: root.set_file(self.text)
        Label:
            size_hint_y: None
            height: dp(24)
            text: 'Spacebar to Toggle Play/Stop'
""")


class PlayScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.track = None
        # self.track_path = None  # holds the name of the 1x speed track
        # self.track_stretched = None  # name of stretched track
        # self.time_stretch_processes = {}
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'spacebar':  # Toggle between play and stop
            # self.ids.play_toggle.state = 'down' if self.ids.play_toggle.state == 'normal' else 'normal'
            pass
            # todo: add spacebar action here

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




