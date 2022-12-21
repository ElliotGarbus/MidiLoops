from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.core.window import Window

kv = """
<ScrollButton>:
    size_hint_y: None
    height: dp(48)
    on_release: print(f'{self.text} pos: {self.pos}')
    
BoxLayout:
    orientation: 'vertical'
    # on_touch_down: print(f'Window{args[1].pos}')
    Label:
        text: 'Drop on ScrollView'
        size_hint_y: None
        height: dp(30)
    ScrollView:
        BoxLayout:
            id: scroll_box
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            # on_touch_down: print(f'BoxLayout: {args[1].pos} {self.to_widget(*args[1].pos, relative=True)=}')
"""


class ScrollButton(Button):
    pass


class ScrollDropApp(App):
    def build(self):
        Window.bind(on_drop_file=self.drop_file)
        return Builder.load_string(kv)

    def on_start(self):
        for i in range(128):
            self.root.ids.scroll_box.add_widget(ScrollButton(text=f'Button {i}'))

    def drop_file(self, window, filename, *_):
        # the x,y passed into the drop_file event are in sdl coordinates, use mouse_pos
        print(f'pos:{window.mouse_pos} {filename.decode("utf-8")}')
        x, y = window.mouse_pos
        for button in self.root.ids.scroll_box.children:
            if button.collide_point(*button.to_widget(x, y)):
                print(f'Drop on Button: {button.text} ')
                button.text = filename.decode("utf-8")
                break


ScrollDropApp().run()
