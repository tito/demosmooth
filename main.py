# coding=utf-8

from kivy.lang import Builder
from kivy.app import App
from kivy.factory import Factory

KV = """
#:import SmoothTouch smoothtouch.SmoothTouch
#:import SwitchContainer switchcontainer.SwitchContainer
#:import CoverImage coverimage.CoverImage
#:import MapView mapview.MapView

<Contact@BoxLayout>:
    index: 0
    text: ""
    source: ""
    padding: dp(4)
    spacing: dp(4)
    RelativeLayout:
        size_hint_x: None
        width: self.height
        CoverImage:
            source: "data/image{}.jpg".format(1 + root.index % 5)
    Image:
        size_hint_x: None
        width: self.height
        source: root.source
    Label:
        text: root.text
        text_size: self.width, None

GridLayout:
    cols: 1
    Label:
        text: "Smooth touch demonstration"
        size_hint_y: None
        height: dp(48)

    Spinner:
        text: "Carousel"
        values: ["Carousel", "MapView", "RecycleView"]
        size_hint_y: None
        height: dp(48)
        on_text: sc.index = self.values.index(self.text)


    RelativeLayout:
        SwitchContainer:
            id: sc

            BoxLayout:
                orientation: "vertical"
                Carousel:
                    CoverImage:
                        source: "data/image1.jpg"
                    CoverImage:
                        source: "data/image2.jpg"
                    CoverImage:
                        source: "data/image3.jpg"
                    CoverImage:
                        source: "data/image4.jpg"
                    CoverImage:
                        source: "data/image5.jpg"

                SmoothTouch:
                    Carousel:
                        CoverImage:
                            source: "data/image1.jpg"
                        CoverImage:
                            source: "data/image2.jpg"
                        CoverImage:
                            source: "data/image3.jpg"
                        CoverImage:
                            source: "data/image4.jpg"
                        CoverImage:
                            source: "data/image5.jpg"

            BoxLayout:
                orientation: "vertical"
                MapView:
                    zoom: 5

                SmoothTouch:
                    MapView:
                        zoom: 5

            BoxLayout:
                orientation: "vertical"
                RecycleView:
                    id: rv
                    viewclass: "Contact"
                    RecycleBoxLayout:
                        default_size_hint: 1, None
                        default_size: None, dp(96)
                        padding: dp(4)
                        size_hint_y: None
                        height: self.minimum_height
                        orientation: "vertical"

                SmoothTouch:
                    RecycleView:
                        id: rv2
                        viewclass: "Contact"
                        RecycleBoxLayout:
                            default_size_hint: 1, None
                            default_size: None, dp(96)
                            padding: dp(4)
                            size_hint_y: None
                            height: self.minimum_height
                            orientation: "vertical"

        BoxLayout:
            orientation: "vertical"
            RelativeLayout:
                Label:
                    text: "Raw touch"
                    size_hint: None, None
                    size: dp(150), dp(32)
                    canvas.before:
                        Color:
                            rgba: .4, .4, .4, .6
                        Rectangle:
                            pos: self.pos
                            size: self.size

            RelativeLayout:
                Label:
                    text: "Smooth touch"
                    size_hint: None, None
                    size: dp(150), dp(32)
                    canvas.before:
                        Color:
                            rgba: .4, .4, .4, .6
                        Rectangle:
                            pos: self.pos
                            size: self.size

"""


class DemoSmooth(App):
    def build(self):
        self.root = Builder.load_string(KV)

        # populate rvs
        data = []
        for index in range(100):
            data.append({
                "text": "Contact {}".format(index),
                "source": "data/contact-image{}.png".format(1 + index % 2),
                "index": index
            })
        self.root.ids.rv.data = data
        self.root.ids.rv2.data = data



if __name__ == "__main__":
    DemoSmooth().run()
