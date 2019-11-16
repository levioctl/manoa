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
from geometry import utils, segment, rotation, polygon


KEYCODE_A = 38
KEYCODE_D = 40
KEYCODE_H = 43
KEYCODE_J = 44
KEYCODE_K = 45
KEYCODE_L = 46
KEYCODE_W = 25
KEYCODE_S = 39
KEYCODE_C = 54


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
        #GLib.timeout_add(100, self._refresh_clock)

        # Keys
        self.connect("key-press-event", self._keypress_callback)
        np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})

    def _refresh_clock(self):
        self._darea.queue_draw()
        return True

    def _draw_frame(self, widget, ctx):

        try:
            # Draw
            objects = self._engine.render_next_frame_polygons()
            for _object in objects:
                if isinstance(_object, segment.Segment):
                    vertices = _object.vertices
                    self._draw_line(ctx,
                                    vertices[0][0],
                                    vertices[0][1],
                                    vertices[1][0],
                                    vertices[1][1],
                                    _object.color)
                elif isinstance(_object, polygon.Polygon):
                    #for _segment in _object.segments:
                    #    self._draw_line(ctx,
                    #                    _segment.vertices[0][0], _segment.vertices[0][1],
                    #                    _segment.vertices[1][0], _segment.vertices[1][1],
                    #                    _object.color,
                    #                    preserve=True)
                    seg = _object.segments
                    #self._draw_quad(ctx, _object.color,
                    #                v[0].vertices[0][0], v[0].vertices[0][1],
                    #                v[1].vertices[0][0], v[1].vertices[0][1],
                    #                v[2].vertices[0][0], v[2].vertices[0][1], 
                    #                v[3].vertices[0][0], v[3].vertices[0][1])
                    self._draw_quad(ctx, _object.color,
                                    seg)
                    ctx.move_to(seg[0].vertices[0][0], seg[0].vertices[0][1])
                    ctx.close_path()
                    ctx.fill()
                else:
                    assert False, type(_object)

            # To be moved to some 'Game' class or something
            self._engine.world.update()
            #self._engine._observer.position[0] += 0.01
            #self._engine._observer.direction = rotation.rotate(self._engine._observer.direction, axis_vector=np.array([0,0,1]),
            #                                                   theta=-.5 * np.pi / 180.)

            ctx.move_to(20, 30)
            ctx.set_font_size(20)
            ctx.set_source_rgba(255, 255, 255, 1)
            ctx.show_text("Position: {}; Direction: {}".format(self._engine._observer.position,
                                                               self._engine._observer.direction))

            def draw_polygon(x0, y0,x1,y1,x2,y2,x3,y3):
                ctx.move_to(x0,y0)
                ctx.line_to(x1,y1)
                ctx.stroke_preserve()

                #ctx.move_to(x1,y1)
                ctx.line_to(x2,y2)
                ctx.stroke_preserve()

                #ctx.move_to(x2,y2)
                ctx.line_to(x3,y3)
                ctx.stroke_preserve()

                #ctx.move_to(x3,y3)
                ctx.line_to(x0,y0)
                #ctx.close_path()
                ctx.stroke_preserve()

                ctx.fill()
            draw_polygon(100, 100, 200, 100, 200, 200, 100, 200)
        except:
            import traceback
            import sys;
            traceback.print_exc(file=sys.stdout)
            sys.exit(1)
        
        axis_size = 200
        origin_x = axis_size
        origin_y = self._height - 200
        self._draw_line(ctx, origin_x - axis_size / 2., origin_y, origin_x +  axis_size / 2., origin_y, "green")
        self._draw_line(ctx, origin_x, origin_y -  axis_size / 2., origin_x, origin_y +  axis_size / 2., "green")
        person_position_x =  origin_x - self._engine._observer.position[1] * 40.
        person_position_y =  origin_y - self._engine._observer.position[1] * 40.
        edge_x = person_position_x + self._engine._observer.direction[0] * 40.
        edge_y = person_position_y - self._engine._observer.direction[1] * 40.
        self._draw_line(ctx, person_position_x, person_position_y, edge_x, edge_y, "blue")

    def _color_name_to_rgb(self, color):
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
        return color

    def _draw_line(self, ctx, x0, y0, x1, y1, color, preserve=False):
        self.set_color(ctx, color)
        ctx.move_to(x0, y0)
        ctx.line_to(x1, y1)
        ctx.stroke()

    def set_color(self, ctx, name):
        color = self._color_name_to_rgb(name)
        ctx.set_source_rgba(color[0], color[1], color[2], 1)

    def _draw_quad(self, ctx, color, segments):
        self.set_color(ctx, color)

        ctx.move_to(segments[0].vertices[0][0], segments[0].vertices[0][1])

        ctx.line_to(segments[0].vertices[1][0], segments[0].vertices[1][1])
        ctx.stroke_preserve()

        ctx.line_to(segments[1].vertices[0][0], segments[1].vertices[0][1])
        ctx.stroke_preserve()

        ctx.line_to(segments[1].vertices[1][0], segments[1].vertices[1][1])
        ctx.stroke_preserve()

        ctx.line_to(segments[2].vertices[0][0], segments[2].vertices[0][1])
        ctx.stroke_preserve()

        ctx.line_to(segments[2].vertices[1][0], segments[2].vertices[1][1])
        ctx.stroke_preserve()

        ctx.line_to(segments[3].vertices[0][0], segments[3].vertices[0][1])
        ctx.stroke_preserve()

        ctx.line_to(segments[3].vertices[1][0], segments[3].vertices[1][1])
        ctx.stroke_preserve()

        ctx.line_to(segments[0].vertices[0][0], segments[0].vertices[0][1])
        ctx.stroke_preserve()

        #ctx.set_source_rgba(color[0], color[1], color[2], 1)
        ctx.close_path()
        ctx.fill()

    def _keypress_callback(self, *args):
        keycode = args[1].get_keycode()[1]
        if keycode == KEYCODE_J:
            axis_vector = np.array([self._engine._observer.direction[1], -self._engine._observer.direction[0], 0])
            theta = - 1. * np.pi / 180.

            new_direction = rotation.rotate(self._engine._observer.direction,
                                                                axis_vector=axis_vector,
                                                                theta=theta)
            if new_direction[2] > self._engine._observer.direction[2]:
                theta = -theta
                new_direction = rotation.rotate(self._engine._observer.direction,
                                                                    axis_vector=axis_vector,
                                                                    theta=theta)

            self._engine._observer.direction = new_direction
            self._engine._observer.direction = utils.normalized(self._engine._observer.direction)

        elif keycode == KEYCODE_K:
            axis_vector = np.array([self._engine._observer.direction[1], -self._engine._observer.direction[0], 0])
            theta = 1. * np.pi / 180.

            new_direction = self._engine._observer.direction = rotation.rotate(self._engine._observer.direction,
                                                                axis_vector=axis_vector,
                                                                theta=theta)
            if new_direction[2] < self._engine._observer.direction[2]:
                theta = -theta
                new_direction = rotation.rotate(self._engine._observer.direction,
                                                                    axis_vector=axis_vector,
                                                                    theta=theta)
            self._engine._observer.direction = new_direction
            self._engine._observer.direction = utils.normalized(self._engine._observer.direction)

        elif keycode == KEYCODE_H:
            axis_vector = np.array([0, 0, 1])
            theta = + 1. * np.pi / 180.
            self._engine._observer.direction = rotation.rotate(self._engine._observer.direction,
                                                                axis_vector=axis_vector,
                                                                theta=theta)
            self._engine._observer.direction = utils.normalized(self._engine._observer.direction)

        elif keycode == KEYCODE_L:
            axis_vector = np.array([0, 0, 1])
            theta = - 1. * np.pi / 180.
            self._engine._observer.direction = rotation.rotate(self._engine._observer.direction,
                                                                axis_vector=axis_vector,
                                                                theta=theta)
            self._engine._observer.direction = utils.normalized(self._engine._observer.direction)

        elif keycode == KEYCODE_W:
            self._engine._observer.position += self._engine._observer.direction * 0.3
        elif keycode == KEYCODE_S:
            self._engine._observer.position -= self._engine._observer.direction * 0.3
        elif keycode == KEYCODE_D:
            x, y, _ = self._engine._observer.direction
            diff = np.array((y, -x, 0))
            diff /= np.linalg.norm(diff)
            diff *= 0.1
            self._engine._observer.position += diff
        elif keycode == KEYCODE_A:
            x, y, _ = self._engine._observer.direction
            diff = np.array((y, -x, 0))
            diff /= np.linalg.norm(diff)
            diff *= 0.1
            self._engine._observer.position -= diff

        self._darea.queue_draw()

w = Screen()
Gtk.main()
