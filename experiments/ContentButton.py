from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty

kv = """
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
                text: 'Song Title'
                group: 'track'
            Button:
                id: delete_button
                text: 'X'
                size_hint_x: None
                width: 20
        BoxLayout:
            Slider:
                id: volume
                max: 127
            Label:
                text: f'{volume.value:.0f}'
                size_hint_x: None
                width: 40

BoxLayout:
    orientation: 'vertical'
    padding: 10
    spacing: 10
    id: box
    

"""


class ContentControl(BoxLayout):
    pc = NumericProperty()


class ContentControlApp(App):
    def build(self):
        return Builder.load_string(kv)

    def on_start(self):
        for i in range(4):
            self.root.add_widget(ContentControl(pc=i))


ContentControlApp().run()
