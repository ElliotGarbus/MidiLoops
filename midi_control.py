import mido
import mido.backends.rtmidi  # required for pyinstaller to create an exe
from kivy.app import App
from kivy.logger import Logger


class MidiControl:
    def __init__(self):
        self.midi_channel = None
        self.midi_in_names = None  # Names of all midi input ports
        self.midi_in_port = None

    def get_midi_ports(self):
        try:
            self.midi_in_names = mido.get_input_names()
        except RuntimeError as e:
            Logger.exception(f'APPLICATION: get_midi_ports(): {e}')
            self.midi_in_names = None
        return self.midi_in_names

    def set_midi_port(self, input_port: str):
        """Set up midi input port and channel"""
        if input_port not in self.midi_in_names:
            self.midi_in_port = None
            return
        if self.midi_in_port:
            self.midi_in_port.close()
            self.midi_in_port = None
        try:
            self.midi_in_port = mido.open_input(input_port)
        except (RuntimeError, OSError) as e:
            Logger.exception(f'APPLICATION: set_midi_port(): {e}')

    def set_midi_channel(self, ch: str):
        self.midi_channel = int(ch) - 1

    def read_midi_callback(self, _):  # called from Clock.schedule_interval, does not use dt
        """
        | Action | CC# | CC Value | Notes                                  |
        |--------|-----|----------|----------------------------------------|
        | Stop   | 1   | any      | Stop playing                           |
        | Next   | 2   | any      | stop current loop, start the next loop |
        | Volume | 3   | 0-127    | set the volume for the playing loop    |
        """
        app = App.get_running_app()
        p = app.root.ids.sm.get_screen('play_screen')
        if self.midi_in_port:
            for msg in self.midi_in_port.iter_pending():
                if app.root.ids.sm.current == 'midi_monitor':
                    app.root.ids.sm.get_screen('midi_monitor').add_line(msg)
                if msg.type == 'control_change' and msg.channel == self.midi_channel:
                    if msg.control == 1:  # play or stop
                        p.stop()
                    elif msg.control == 2:
                        p.play_next()
                    elif msg.control == 3:  # Adjust playback volume
                        p.set_volume(msg.value)
                elif msg.type == 'program_change' and msg.channel == self.midi_channel:
                    p.play_pc(msg.program)
