# coding=utf-8

from kivy.uix.image import Image
from kivy.properties import AliasProperty
from kivy.lang import Builder

Builder.load_string("""
<-CoverImage>:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            texture: root.texture
            size: self.size
            tex_coords: root.tex_coords
""", filename=__file__)


class CoverImage(Image):

    def on_source(self, instance, source):
        # this is a fix to force refreshing the cover image
        # when the source change (otherwise it flicker or behave badly)
        # when used in a recycleview
        self.texture = None

    def get_tex_coords(self):
        if not self.texture:
            return [0, 0, 1, 0, 1, 1, 0, 1]
        w, h = self.size
        tw, th = self.texture_size
        if not w or not h or not tw or not th:
            return [0, 0, 1, 0, 1, 1, 0, 1]
        u, v = self.texture.uvpos
        uw, vh = self.texture.uvsize

        r_viewport = w / float(h)
        r_image = tw / float(th)
        if r_image < r_viewport:
            ih = w / r_image
            vhn = vh * (h / float(ih))
            v = (vh - vhn) / 2.
            if vh < 0:
                v = abs(vh) + v
            vh = vhn
        else:
            iw = h * r_image
            uwn = uw * (w / float(iw))
            u = (uw - uwn) / 2.
            uw = uwn

        ret = (u, v, u + uw, v, u + uw, v + vh, u, v + vh)
        return ret

    tex_coords = AliasProperty(get_tex_coords, None, bind=(
        "texture_size", "size", "texture", "parent"))
