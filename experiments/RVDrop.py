from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.properties import NumericProperty, ListProperty
from kivy.core.window import Window

kv = """
<ScrollButton>:
    size_hint_y: None
    height: dp(48)
    on_release: print(f'{self.text} pos: {self.pos}')

BoxLayout:
    orientation: 'vertical'
    Label:
        text: 'Drop on ScrollView'
        size_hint_y: None
        height: dp(30)
    RV:
        id: rv
        viewclass: 'ScrollButton'
        RecycleBoxLayout:
            id: scroll_box
            orientation: 'vertical'
            default_size: None, dp(48)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
"""


class ScrollButton(Button):
    index = NumericProperty()


class RV(RecycleView):
    def on_kv_post(self, base_widget):
        self.data = [{'text': f'Button {i}', 'index': i} for i in range(128)]


class ScrollDropApp(App):
    def build(self):
        Window.bind(on_drop_file=self.drop_file)
        return Builder.load_string(kv)

    def drop_file(self, window, filename, *_):
        # the x,y passed into the drop_file event are in sdl coordinates, use mouse_pos
        print(f'pos:{window.mouse_pos} {filename.decode("utf-8")}')
        x, y = window.mouse_pos
        for button in self.root.ids.scroll_box.children:
            if button.collide_point(*button.to_widget(x, y)):
                print(f'Drop on Button: {button.text} ')
                self.root.ids.rv.data[button.index]['text'] = filename.decode("utf-8")
                self.root.ids.rv.refresh_from_data()
                break


ScrollDropApp().run()
