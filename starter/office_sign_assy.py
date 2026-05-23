# %%
import math
from cadbuildr.foundation import (
    Assembly,
    TFHelper,
    show,
)

from starter.cadbuildr_plate_part import CadbuildrPlate
from starter.spacer_part import Spacer


class CadbuildrSign(Assembly):
    """A simple office sign with a CADBuildr logo and text."""

    def __init__(self, spacer_radius=5, spacer_height=20, spacer_hole_radius=3):
        """
        Initialize the CADBuildrSign assembly.

        Args:
            spacer_radius (float): Radius of the spacer cylinder.
            spacer_height (float): Height of the spacer cylinder.
            spacer_hole_radius (float): Radius of the hole in the spacer.
        """
        super().__init__()
        self.spacer_radius = spacer_radius
        self.spacer_height = spacer_height
        self.spacer_hole_radius = spacer_hole_radius

        self._add_plate()
        self._add_spacers()

    def _add_plate(self):
        """Add the main plate to the assembly."""
        plate = CadbuildrPlate(spacer_hole_radius=self.spacer_hole_radius)
        self.add_component(plate)

    def _add_spacers(self):
        """Add the three spacers to the assembly."""
        radius = 130  # Same as hole positions in plate
        for angle_deg in [0, 120, 240]:
            angle_rad = math.radians(angle_deg)
            x = radius * math.cos(angle_rad)
            y = radius * math.sin(angle_rad)

            tf = TFHelper()
            tf.translate([x, y, -self.spacer_height])

            spacer = Spacer(
                radius=self.spacer_radius,
                height=self.spacer_height,
                hole_radius=self.spacer_hole_radius,
            )
            self.add_component(spacer, tf.get_tf())


if __name__ == "__main__":
    show(CadbuildrSign())

# %%
