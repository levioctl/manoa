#!/usr/bin/python3
import gi
gi.require_version('Gtk', '3.0')
#gi.require_foreign("cairo")
gi.require_version('GdkPixbuf', '2.0')
from gi.repository.GdkPixbuf import Pixbuf, InterpType
from gi.repository import Gtk, GdkX11, Gdk
from gi.repository import GLib

import engine
import segment


class Screen(Gtk.Window):
    def __init__(self):
        super(Screen, self).__init__()

        self._width = 1200
        self._height = 675

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

        self._a = False
        self._b = 100

    def _refresh_clock(self):
        self._darea.queue_draw()
        return True

    def _draw_frame(self, widget, ctx):
        # To be removed
        self._a = not self._a
        self._b += 1
        color = "red" if self._a else "blue"
        self._draw_quad(ctx, color, self._b, 100, self._b, 200, 200, 200, 200, 100)

        # Draw
        polygons = self._engine.render_next_frame_polygons()
        for polygon in polygons:
            if len(polygon.vertices) == 4:
                self._draw_quad(ctx,
                                polygon.color,
                                polygon.vertices[0][0],
                                polygon.vertices[0][1],
                                polygon.vertices[1][0],
                                polygon.vertices[1][1],
                                polygon.vertices[2][0],
                                polygon.vertices[2][1],
                                polygon.vertices[3][0],
                                polygon.vertices[3][1])
            elif isinstance(polygon, segment.Segment):
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
        self._engine._observer.position[0] += 0.1
        #import numpy as np
        #theta = -10./180 * np.pi
        #rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        #d = np.array(self._engine._observer.direction[0], self._engine._observer.direction[1])
        #d = rot.dot(d)
        #self._engine._observer.direction = np.array((d[0], d[1], 0.))

    def _draw_line(self, ctx, x0, y0, x1, y1, color):
        if color == "red":
            color = (255, 0, 0)
        elif color == "green":
            color = (0, 255, 0)
        elif color == "blue":
            color = (0, 0, 255)
        else:
            color = (255, 255, 255)
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

w = Screen()
Gtk.main()
