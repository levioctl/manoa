#!/usr/bin/python3
import world
import observer
import virtualscreen
import physicalscreen


class Engine:
    def __init__(self, world, observer, physical_sceen_width, physical_screen_height):
        self.world = world
        self.objects = world.objects
        self._observer = observer
        self._virtual_screen = virtualscreen.VirtualScreen(self._observer)
        self._physical_screen = physicalscreen.PhysicalScreen(physical_sceen_width,
                                                              physical_screen_height,
                                                              observer)

    def render_next_frame_polygons(self):
        self._render_frame()
        return self._physical_screen.get_polygons()

    def _render_frame(self):
        # Initialize virtual screen
        self._virtual_screen.start_new_frame()

        # Project objects on virtual screen
        for _object in self.objects:
            self._virtual_screen.project_object(_object)

        # Initialize virtual screen
        self._physical_screen.start_new_frame()

        # Transform virtual screen to physical screen
        for _object in self._virtual_screen.get_polygons():
            self._physical_screen.project_virtual_object(_object)


def factory(screen_width, screen_height):
    return Engine(world.World(), observer.Observer(), screen_width, screen_height)
