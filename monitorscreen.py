from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty

import re
import mido


Builder.load_string("""
<MidiLine>
    orientation: 'horizontal'
    size_hint: 1, None
    height: dp(12)
    Label:
        padding: 10, 0 
        text_size: self.size
        halign: 'left'
        valign: 'middle'
        text: root.raw
        
    Label:
        padding: 10, 0 
        text_size: self.size
        halign: 'left'
        valign: 'middle'
        text: root.action
    
<MidiMonitorScreen>:
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            size_hint_y: None
            height: dp(24)
            Label:
                text: 'MIDI Message'
            Label:
                padding: 20, 0
                text_size: self.size
                halign: 'left'
                valign: 'middle'
                text: 'Action'
        RecycleView:
            id: rv
            viewclass: 'MidiLine'
            data: root.rv_list
            scroll_type: ['bars','content']
            bar_width: dp(20)
            do_scroll_x: False
            RecycleBoxLayout:
                id: rbl
                orientation: 'vertical'
                size_hint_y: None
                default_size: None, dp(22)
                default_size_hint: 1, None
                height: self.minimum_height
""")


class MidiMonitorScreen(Screen):
    rv_list = ListProperty()

    def add_line(self, msg):
        re_search = re.compile(r' channel=(\d+)')
        midi_string = mido.format_as_string(msg, include_time=False)
        result = re_search.search(midi_string)
        if result:
            ch = int(result.group(1)) + 1
            raw = re_search.sub(f' channel={ch}', midi_string)
        else:
            raw = midi_string
        action = ''
        app = App.get_running_app()
        if msg.type == 'sysex':
            raw = 'SYSEX Message'
        try:
            midi_ch = int(app.root.ids.midi_ch.text) - 1
        except ValueError:
            midi_ch = -1  # if the channel has not been set, the int() conversion will fail
        if msg.type == 'control_change' and msg.channel == midi_ch and msg.control in [1, 2, 3]:
            if msg.control == 1:
                action = 'Stop'
            elif msg.control == 2:
                action = 'Play Next'
            elif msg.control == 3:
                action = f'Volume: {int(msg.value/127 * 100)}%'
        elif msg.type == 'program_change' and msg.channel == midi_ch:
            action = f'play loop {msg.program}'
        self.rv_list.append({'raw': raw, 'action': action})
        if self.ids.rv.height < self.ids.rbl.height:
            self.ids.rv.scroll_y = 0


class MidiLine(BoxLayout):
    raw = StringProperty()
    action = StringProperty()
