# %%
from cadbuildr.foundation import Part, Sketch, Circle, Point, Extrusion, show


class Spacer(Part):
    """A cylindrical spacer with a center hole."""

    def __init__(self, radius=5, height=20, hole_radius=3):
        """
        Initialize the spacer.

        Args:
            radius (float): Outer radius of the spacer.
            height (float): Height of the spacer.
            hole_radius (float): Radius of the center hole.
        """
        super().__init__()
        self.radius = radius
        self.height = height
        self.hole_radius = hole_radius
        self._create_spacer()
        self.paint("grey")

    def _create_spacer(self):
        """Create the spacer with its center hole."""
        self._create_outer_cylinder()
        self._create_center_hole()

    def _create_outer_cylinder(self):
        """Create the main cylinder of the spacer."""
        s = Sketch(self.xy())
        center_point = Point(s, 0, 0)
        circle = Circle(center_point, self.radius)
        extrusion = Extrusion(circle, self.height)
        self.add_operation(extrusion)

    def _create_center_hole(self):
        """Create the center hole in the spacer."""
        s = Sketch(self.xy())
        center_point = Point(s, 0, 0)
        circle = Circle(center_point, self.hole_radius)
        extrusion = Extrusion(circle, self.height, cut=True)
        self.add_operation(extrusion)


if __name__ == "__main__":
    spacer = Spacer()
    show(spacer)

# %%
