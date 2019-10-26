#!/usr/bin/python3
import numpy as np
import gi
gi.require_version('Gtk', '3.0')
#gi.require_foreign("cairo")
gi.require_version('GdkPixbuf', '2.0')
from gi.repository.GdkPixbuf import Pixbuf, InterpType
from gi.repository import Gtk, GdkX11, Gdk
from gi.repository import GLib

import engine
from geometry import segment, rotation


KEYCODE_J = 44
KEYCODE_K = 45
KEYCODE_L = 46
KEYCODE_W = 25
KEYCODE_S = 39
KEYCODE_C = 54
KEYCODE_D = 40
KEYCODE_H = 43


class Screen(Gtk.Window):
    def __init__(self):
        super(Screen, self).__init__()

        self._width = 1600
        self._height = 900

        # Game
        self._engine = engine.factory(self._width, self._height)

        self.set_size_request(self._width, self._height)
        self.set_position(Gtk.WindowPosition.CENTER)

        # Set background color to black
        col = Gdk.Color(0, 0, 0)
        self.modify_bg(Gtk.StateFlags.NORMAL, col)
        self.connect("delete-event", Gtk.main_quit)

        # Add drawing area
        self._darea = Gtk.DrawingArea()
        self._darea.connect("draw", self._draw_frame)
        self.add(self._darea)
        self.show_all()

        # Set clock
        GLib.timeout_add(100, self._refresh_clock)

        # Keys
        self.connect("key-press-event", self._keypress_callback)

    def _refresh_clock(self):
        self._darea.queue_draw()
        return True

    def _draw_frame(self, widget, ctx):

        # Draw
        polygons = self._engine.render_next_frame_polygons()
        for polygon in polygons:
            if isinstance(polygon, segment.Segment):
                vertices = polygon.vertices
                self._draw_line(ctx,
                                vertices[0][0],
                                vertices[0][1],
                                vertices[1][0],
                                vertices[1][1],
                                polygon.color)
            else:
                assert False

        # To be moved to some 'Game' class or something
        self._engine.world.update()
        #self._engine._observer.position[0] += 0.01
        import numpy as np
        #self._engine._observer.direction = rotation.rotate(self._engine._observer.direction, axis_vector=np.array([0,0,1]),
        #                                                   theta=-.5 * np.pi / 180.)

        ctx.move_to(20, 30)
        ctx.set_font_size(20)
        ctx.show_text("Position: {}; Direction: {}".format(self._engine._observer.position,
                                                           self._engine._observer.direction))

    def _draw_line(self, ctx, x0, y0, x1, y1, color):
        if color == "red":
            color = (255, 0, 0)
        elif color == "green":
            color = (0, 255, 0)
        elif color == "blue":
            color = (0, 0, 255)
        elif color == "white":
            color = (255, 255, 255)
        elif color == "yellow":
            color = (255, 255, 0)
        else:
            assert False, color
        ctx.move_to(x0, y0)
        ctx.line_to(x1, y1)
        ctx.set_source_rgba(color[0], color[1], color[2], 1)
        ctx.stroke()

    def _draw_quad(self, ctx, color, x0, y0, x1, y1, x2, y2, x3, y3):
        self._draw_line(ctx, x0, y0, x1, y1, color)
        self._draw_line(ctx, x1, y1, x2, y2, color)
        self._draw_line(ctx, x2, y2, x3, y3, color)
        self._draw_line(ctx, x3, y3, x0, y0, color)
        #ctxr.arc(x, y, 2, 0, 2 * pi)
        #ctx.fill()

    def _keypress_callback(self, *args):
        keycode = args[1].get_keycode()[1]
        if keycode == KEYCODE_J:
            axis_vector = np.array([self._engine._observer.direction[1], -self._engine._observer.direction[0], 0])
            theta = - .5 * np.pi / 180.
            self._engine._observer.direction = rotation.rotate(self._engine._observer.direction,
                                                                axis_vector=axis_vector,
                                                                theta=theta)
        elif keycode == KEYCODE_K:
            axis_vector = np.array([self._engine._observer.direction[1], -self._engine._observer.direction[0], 0])
            theta = .5 * np.pi / 180.
            self._engine._observer.direction = rotation.rotate(self._engine._observer.direction,
                                                                axis_vector=axis_vector,
                                                                theta=theta)
        elif keycode == KEYCODE_H:
            axis_vector = np.array([0, 0, 1])
            theta = - .5 * np.pi / 180.
            self._engine._observer.direction = rotation.rotate(self._engine._observer.direction,
                                                                axis_vector=axis_vector,
                                                                theta=theta)
        elif keycode == KEYCODE_L:
            axis_vector = np.array([0, 0, 1])
            theta = + .5 * np.pi / 180.
            self._engine._observer.direction = rotation.rotate(self._engine._observer.direction,
                                                                axis_vector=axis_vector,
                                                                theta=theta)

        elif keycode == KEYCODE_W:
            self._engine._observer.position += self._engine._observer.direction * 0.1
        elif keycode == KEYCODE_S:
            self._engine._observer.position -= self._engine._observer.direction * 0.1

w = Screen()
Gtk.main()
