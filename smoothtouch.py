# coding=utf-8

from kivy.uix.boxlayout import BoxLayout
from kivy.input.motionevent import MotionEvent
from kivy.clock import Clock
from kivy.core.window import Window as win
from kivy.utils import platform
from functools import partial
from time import time
from kivy.effects.kinetic import KineticEffect


class CustomKineticEffect(KineticEffect):
    def calculate_velocity(self):
        newest_sample = self.history[-1]
        old_sample = self.history[0]
        for sample in self.history:
            if (newest_sample[0] - sample[0]) < 10. / 60.:
                break
            old_sample = sample
        distance = newest_sample[1] - old_sample[1]
        duration = abs(newest_sample[0] - old_sample[0])
        self.velocity = (distance / max(duration, 0.0001))
        return self.velocity


class SmoothMotionEvent(MotionEvent):
    def depack(self, args):
        self.is_touch = True
        self.profile = ["pos"]
        self.sx, self.sy = args
        super(SmoothMotionEvent, self).depack(args)


class SmoothTouch(BoxLayout):
    def __init__(self, **kwargs):
        super(SmoothTouch, self).__init__(**kwargs)
        self.touches = {}

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        touch.grab(self)
        uid = "st:{}".format(touch.uid)

        x, y = self.to_window(*touch.pos)
        sx = x / win.width
        sy = y / win.height

        me = SmoothMotionEvent(None, uid, (sx, sy))
        if "button" in touch.profile:
            me.profile.append("button")
            me.button = touch.button
        me.target_sx = me.sx
        me.target_sy = me.sy
        me.got_a_move = False
        me.last_move = time()
        me.kx = CustomKineticEffect()
        me.ky = CustomKineticEffect()
        me.kx.start(me.sx)
        me.ky.start(me.sy)
        self.touches[touch] = me
        self.simulate_touch_down(me)
        return True

    def on_touch_move(self, touch):
        if touch in self.touches and touch.grab_current == self:
            me = self.touches[touch]
            x, y = self.to_window(*touch.pos)
            sx = x / win.width
            sy = y / win.height
            me.target_sx = sx
            me.target_sy = sy
            me.kx.update(sx)
            me.ky.update(sy)
            me.got_a_move = True
            me.last_move = time()
            return True

    def on_touch_up(self, touch):
        if touch in self.touches and touch.grab_current == self:
            touch.ungrab(self)
            self.simulate_touch_up(self.touches[touch])
            del self.touches[touch]
            return True

    def simulate_touch_down(self, me):
        me.sx = me.target_sx
        me.sy = me.target_sy
        me.simulate_func = partial(self.simulate_touch_move, me)
        Clock.schedule_interval(me.simulate_func, 1 / 60.)
        me.scale_for_screen(win.width, win.height)
        me.push()
        me.apply_transform_2d(self.to_widget)
        super(SmoothTouch, self).on_touch_down(me)
        me.pop()

    def simulate_touch_move(self, me, dt):
        # tx = (me.target_sx - me.sx)
        # ty = (me.target_sy - me.sy)
        # sx = me.sx + tx / 4.
        # sy = me.sy + ty / 4.
        w, h = win.system_size
        if platform == "ios" or win._density != 1:
            w, h = win.size

        self.update_touch(me, dt)
        me.scale_for_screen(w, h)
        me.push()
        me.apply_transform_2d(self.to_widget)
        super(SmoothTouch, self).on_touch_move(me)
        me.pop()
        self.dispatch_grab("update", me)

    def simulate_touch_up(self, me):
        Clock.unschedule(me.simulate_func)
        w, h = win.system_size
        if platform == "ios" or win._density != 1:
            w, h = win.size
        me.scale_for_screen(w, h)
        me.push()
        me.apply_transform_2d(self.to_widget)
        super(SmoothTouch, self).on_touch_up(me)
        me.pop()
        self.dispatch_grab("up", me)

    def update_touch(self, me, dt):
        if me.got_a_move:
            me.got_a_move = False
            me.kx.update(me.target_sx)
            me.ky.update(me.target_sy)
            # me.move((me.target_sx, me.target_sy))
            me.kx.calculate_velocity()
            me.ky.calculate_velocity()
        else:
            # after 0.1s, clear velocity asap
            if time() - me.last_move > 0.1:
                me.kx.velocity /= 2.
                me.ky.velocity /= 2.
        sx = me.sx + me.kx.velocity * dt
        sy = me.sy + me.ky.velocity * dt
        me.move((sx, sy))

    def dispatch_grab(self, etype, me):
        me.grab_state = True
        for _wid in me.grab_list[:]:
            wid = _wid()
            if wid is None:
                me.grab_list.remove(_wid)
                continue
            me.push()
            w, h = win.system_size
            if platform == "ios" or win._density != 1:
                w, h = win.size
            me.scale_for_screen(w, h)
            me.apply_transform_2d(wid.parent.to_widget)

            me.grab_current = wid
            if etype == "update":
                wid.dispatch("on_touch_move", me)
            elif etype == "up":
                wid.dispatch("on_touch_up", me)
            me.grab_current = None
            me.pop()
        me.grab_state = False
