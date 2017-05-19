# coding=utf-8
"""
Just for image, doesn't support any action in it.
It's just for testing velocity approach.
"""

from kivy.uix.stencilview import StencilView
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ListProperty
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.effects.kinetic import KineticEffect
from math import ceil

Builder.load_string("""
<VelocityCarousel>:
    RelativeLayout:
        id: container
        pos: root.pos
        height: root.height
""")


class VelocityCarousel(StencilView):
    slides = ListProperty()

    def __init__(self, **kwargs):
        self._container = None
        self._touch = None
        super(VelocityCarousel, self).__init__(**kwargs)

    def add_widget(self, widget, index=0):
        if self._container is None:
            self._container = widget
            super(VelocityCarousel, self).add_widget(self._container)
            return
        rl = RelativeLayout(size=self.size, size_hint=(None, None))
        rl.add_widget(widget)
        self.slides.append(widget)
        self._container.add_widget(rl)
        self._relayout()

    def remove_widget(self, widget, *args, **kwargs):
        if widget in self.slides:
            rl = widget.parent
            self.slides.remove(widget)
            return rl.remove_widget(widget, *args, **kwargs)
        super(VelocityCarousel, self).remove_widget(widget, *args, **kwargs)

    def clear_widgets(self):
        for slide in self.slides[:]:
            self.remove_widget(slide)
        super(VelocityCarousel, self).clear_widgets()

    def on_size(self, instance, size):
        self._relayout()

    def on_pos(self, instance, pos):
        self._relayout()

    @property
    def vuid(self):
        return "vc:{}".format(self.uid)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        if self._touch:
            return super(VelocityCarousel, self).on_touch_down(touch)
        Clock.unschedule(self._animate)
        self._touch = touch
        touch.grab(self)
        touch.ud[self.vuid] = ud = {
            "mode": None,
            "time": touch.time_start,
            "kx": KineticEffect()
        }
        ud["kx"].start(touch.x)
        return True

    def on_touch_move(self, touch):
        if touch != self._touch:
            return super(VelocityCarousel, self).on_touch_move(touch)
        if touch.grab_current is not self:
            return True
        ud = touch.ud[self.vuid]
        ud["kx"].update(touch.x)
        self._container.x += touch.dx
        return True

    def on_touch_up(self, touch):
        if touch != self._touch:
            return super(VelocityCarousel, self).on_touch_up(touch)
        if touch.grab_current is not self:
            return True
        self._touch = None
        touch.ungrab(self)
        ud = touch.ud[self.vuid]
        ud["kx"].stop(touch.x)
        v = ud["kx"].velocity
        index = ceil(self._container.x / float(self.width))
        minv = self.width * 2
        if v > 0:
            self.velocity = max(minv, v)
            self.stop_at = (index   ) * self.width
        else:
            self.velocity = min(-minv, v)
            self.stop_at = (index - 1) * self.width
        self.stop_at = max(-self._container.width, min(0, self.stop_at))
        Clock.schedule_interval(self._animate, 1 / 60.)
        return True

    def _animate(self, dt):
        container = self._container
        container.x += self.velocity * dt
        if container.x >= 0:
            container.x = 0
            return False
        if container.x <= -container.width + self.width:
            container.x = -container.width + self.width
            return False
        if self.velocity < 0 and container.x <= self.stop_at:
            container.x = self.stop_at
            return False
        if self.velocity > 0 and container.x >= self.stop_at:
            container.x = self.stop_at
            return False

    def _relayout(self):
        self._container.width = len(self.slides) * self.width
        for index, slide in enumerate(self.slides):
            slide.parent.x = index * self.width
            slide.parent.size = self.size
            print(self.y, slide.y, slide.parent.y, slide.parent.width)
