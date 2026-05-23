# %%
import math
from pathlib import Path
from cadbuildr.foundation import Part, Extrusion, Sketch, Circle, Point, SVGShape, show


class CadbuildrPlate(Part):
    """
    A plate component with the CADBuildr logo and text, featuring mounting holes.
    """

    def __init__(self, plate_radius=150, hole_radius=130, spacer_hole_radius=3):
        """
        Initialize the CADBuildr plate.

        Args:
            plate_radius (float): Radius of the main plate.
            hole_radius (float): Radius at which mounting holes are positioned.
            spacer_hole_radius (float): Radius of the mounting holes.
        """
        super().__init__()
        self.plate_radius = plate_radius
        self.hole_radius = hole_radius
        self.spacer_hole_radius = spacer_hole_radius

        # Load SVG files
        with open(Path(__file__).parent / "cadbuildr_logo.svg", "r") as file:
            self.logo_svg = file.read()

        self.text_svg = """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 50">
          <text x="0" y="40" font-family="poppins" font-size="40">CADBuildr</text>
        </svg>
        """

        self._create_plate()

    def _create_plate(self):
        """Create the plate with all its features."""
        self._create_base_plate()
        self._create_logo_cutout()
        self._create_text_cutout()
        self._create_mounting_holes()

    def _create_base_plate(self):
        """Create the main circular plate."""
        s = Sketch(self.xy())
        center_point = Point(s, 0, 0)
        circle = Circle(center_point, self.plate_radius)
        extrusion = Extrusion(circle, 2)
        self.add_operation(extrusion)

    def _create_logo_cutout(self):
        """Create the logo cutout in the plate."""
        s = Sketch(self.xy())
        logo_shape = SVGShape(
            s, self.logo_svg, xshift=0, yshift=-27, angle=0, scale=0.5
        )
        logo_extrusion = Extrusion(logo_shape, 2, cut=True)
        self.add_operation(logo_extrusion)

    def _create_text_cutout(self):
        """Create the text cutout in the plate."""
        s = Sketch(self.xy())
        text_shape = SVGShape(s, self.text_svg, xshift=0, yshift=80, angle=0, scale=1.0)
        text_extrusion = Extrusion(text_shape, 2, cut=True)
        self.add_operation(text_extrusion)

    def _create_mounting_holes(self):
        """Create the mounting holes in the plate."""
        s = Sketch(self.xy())
        for angle_deg in [0, 120, 240]:
            angle_rad = math.radians(angle_deg)
            x = self.hole_radius * math.cos(angle_rad)
            y = self.hole_radius * math.sin(angle_rad)
            hole_center = Point(s, x, y)
            hole_circle = Circle(hole_center, self.spacer_hole_radius)
            hole_extrusion = Extrusion(hole_circle, 2, cut=True)
            self.add_operation(hole_extrusion)


if __name__ == "__main__":
    show(CadbuildrPlate())

# %%
