from configstartup import window_width, window_top, window_left, window_height
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform
from kivy.metrics import Metrics
from kivy.properties import ListProperty

from midi_control import MidiControl
from pathlib import Path
import functools
import playscreen
import monitorscreen

#  todo: midi functionality
#  todo: Update midi monior
#  todo: update cc popup


kv = """
#:import Factory kivy.factory.Factory
<MidiCCPopup@Popup>
    title: 'Midi Assignments'
    size_hint: None, None
    size: dp(640), dp(340)
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)
        GridLayout:
            size_hint_y: None
            height: 30 * 4
            cols: 3
            LeftLabel:
                text: 'Action'
                halign: 'center'
                bold: True
            CCLabel:
                text: 'CC#'
                bold: True
            RightLabel:
                text: 'Value & Description'
                halign: 'center'
                bold: True
            
            LeftLabel:
                text: 'Stop'
            CCLabel:
                text: 'CC# 1'
            RightLabel:
                text: 'Any, Stop Playing'
                
            LeftLabel:
                text: 'Next'
            CCLabel:
                text: 'CC# 2'
            RightLabel:
                text: 'Any, Stop current loop, start the next loop'
            
            LeftLabel:
                text: 'Volume'
            CCLabel:
                text: 'CC# 3'
            RightLabel:
                text: '0 - 127, set volume for playing loop'
        Label:
            text: 'When a PC message associated with one of the loops is received the selected loop begins to play. ' \
                  'If a different loop is playing when the PC message is received, the playing loop will stop, ' \
                  'then the selected loop plays' 
            text_size: self.size

        Button:
            size_hint_y: None
            height: dp(48)
            text: 'OK'
            on_release:
                print(root.size) 
                root.dismiss()


<LeftLabel@Label>:
    size_hint_x: None
    width: dp(75)
    padding: dp(5), dp(5)
    canvas:
        Color:
            rgb: 1, 1, 1
        Line:
            width: dp(1)
            rectangle: (*self.pos, *self.size)
    
<CCLabel@Label>:
    size_hint_x: None
    width: dp(60)
    canvas:
        Color:
            rgb: 1, 1, 1
        Line:
            width: dp(1)
            rectangle: (*self.pos, *self.size)

<RightLabel@Label>:
    text_size: self.size
    halign: 'left'
    valign: 'center' 
    padding: dp(5), dp(5)
    canvas:
        Color:
            rgb: 1, 1, 1
        Line:
            width: dp(1)
            rectangle: (*self.pos, *self.size)

BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: None
        height: dp(48)
        Label:
            text: 'Midi Device & Channel'
            size_hint_x: None
            width: dp(200)
        Spinner:
            id: midi_devices
            text: 'Select Midi Device'
            on_text: app.mc.set_midi_port(self.text)
        Spinner:
            id: midi_ch
            size_hint_x: None
            width: dp(200)
            text: 'Select Midi Channel'
            values: [str(n) for n in range(1, 17)]
            on_text: app.mc.set_midi_channel(self.text)
    ScreenManager:
        id: sm
        PlayScreen:
            name: 'play_screen'
        MidiMonitorScreen:
            name: 'midi_monitor'
    BoxLayout:
        size_hint_y: None
        height: dp(48)
        Button:
            text: 'Play Mode'
            on_release: sm.current = 'play_screen'
        Button:
            text: 'Midi Commands'
            on_release: Factory.MidiCCPopup().open()
        Button:
            text: 'Midi Monitor Mode'
            on_release: sm.current = 'midi_monitor'
"""


class MidiLoopsApp(App):
    recent_track_names = ListProperty()  # used to display names in most recent spinner

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mc = MidiControl()
        self.recent_track_paths = []  # holds full path to the track

    def build(self):
        self.title = 'MidiLoops V0'
        self.use_kivy_settings = False
        Window.minimum_width = window_width
        Window.minimum_height = window_height
        Window.bind(on_request_close=self.window_request_close)
        return Builder.load_string(kv)


    def on_start(self):
        names = self.mc.get_midi_ports()
        self.root.ids.midi_devices.values = names
        m_input = self.config.getdefault('MIDI', 'input', 'None')
        ch = self.config.get('MIDI', 'channel')
        if m_input in names:
            self.mc.set_midi_port(m_input)
            self.mc.midi_channel = int(ch)
            self.root.ids.midi_devices.text = m_input
            self.root.ids.midi_ch.text = str(int(ch) + 1)
        self.root.ids.sm.get_screen('play_screen').load_playlist(self.user_data_dir)
        Clock.schedule_interval(self.mc.read_midi_callback, .1)

    def open_settings(self, *largs):  # kivy control panel will not open
        pass

    def build_config(self, config):
        config.setdefaults('MIDI', {'input': 'None',
                                    'channel': 'None'})
        config.setdefaults('Window', {'width': window_width,
                                      'height': window_height,
                                      'top': window_top,
                                      'left': window_left})

    def get_application_config(self, defaultpath='%(appdir)s/%(appname)s.ini'):
        if platform in ['win', 'macosx']:    # mac will not write into app folder
            s = self.user_data_dir + '/%(appname)s.ini'  # puts ini in AppData on Windows
        else:
            s = defaultpath
        return super().get_application_config(defaultpath=s)

    def window_request_close(self, _):
        # Window.size is automatically adjusted for density, must divide by density when saving size
        config = self.config
        config.set('Window', 'width', int(Window.size[0]/Metrics.density))
        config.set('Window', 'height', int(Window.size[1]/Metrics.density))
        config.set('Window', 'top', Window.top)
        config.set('Window', 'left', Window.left)
        self.config.write()
        return False

    def on_stop(self):
        # Save config file here
        if self.mc.midi_in_port and self.mc.midi_channel is not None:
            self.config.set('MIDI', 'input', self.mc.midi_in_port.name)
            self.config.set('MIDI', 'channel', self.mc.midi_channel)
            self.config.write()
        # Save playlist
        self.root.ids.sm.get_screen('play_screen').save_playlist(self.user_data_dir)


MidiLoopsApp().run()
