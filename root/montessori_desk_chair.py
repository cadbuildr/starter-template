from cadbuildr.foundation import (
    Part,
    Assembly,
    Sketch,
    Point,
    Line,
    Axis,
    Rectangle,
    Circle,
    Extrusion,
    Lathe,
    Hole,
    TFHelper,
    show,
)

# ── Dimensions (mm) ──────────────────────────────────────────
# Desk
DESK_W          = 450   # tabletop width  (X)
DESK_D          = 300   # tabletop depth  (Y)
DESK_TOP_H      =  18   # tabletop thickness
DESK_LEG_W      =  22   # square leg side
DESK_HEIGHT     = 520   # floor → underside of top
DESK_APRON_H    =  40   # apron board height
DESK_APRON_T    =  15   # apron board thickness
DESK_INSET      =  30   # how far legs sit in from edge

# Chair
CHAIR_SEAT_W    = 260
CHAIR_SEAT_D    = 240
CHAIR_SEAT_T    =  16
CHAIR_LEG_W     =  18
CHAIR_SEAT_H    = 280   # floor → seat surface
CHAIR_BACK_H    = 220   # back above seat
CHAIR_BACK_T    =  14
CHAIR_BACK_W    = 220
CHAIR_APRON_H   =  35
CHAIR_APRON_T   =  14
CHAIR_INSET     =  25


# ═══════════════════════════════════════════════════════════════
#  DESK PARTS
# ═══════════════════════════════════════════════════════════════

class DeskTop(Part):
    def __init__(self):
        super().__init__()
        plane = self.xy()
        sk = Sketch(plane)
        cx, cy = DESK_W / 2, DESK_D / 2
        c = Point(sk, cx, cy)
        rect = Rectangle.from_center_and_sides(c, DESK_W, DESK_D)
        self.add_operation(Extrusion([rect], DESK_TOP_H))
        self.paint("plywood")


class DeskLeg(Part):
    def __init__(self):
        super().__init__()
        plane = self.xy()
        sk = Sketch(plane)
        c = Point(sk, 0, 0)
        rect = Rectangle.from_center_and_sides(c, DESK_LEG_W, DESK_LEG_W)
        self.add_operation(Extrusion([rect], DESK_HEIGHT))
        self.paint("reddish_brown")


class DeskApronLong(Part):
    """Front / back apron spanning the full width between legs."""
    def __init__(self):
        super().__init__()
        span = DESK_W - 2 * DESK_INSET
        plane = self.xy()
        sk = Sketch(plane)
        c = Point(sk, span / 2, 0)
        rect = Rectangle.from_center_and_sides(c, span, DESK_APRON_T)
        self.add_operation(Extrusion([rect], DESK_APRON_H))
        self.paint("reddish_brown")


class DeskApronShort(Part):
    """Left / right apron spanning the depth between legs."""
    def __init__(self):
        super().__init__()
        span = DESK_D - 2 * DESK_INSET
        plane = self.xy()
        sk = Sketch(plane)
        c = Point(sk, span / 2, 0)
        rect = Rectangle.from_center_and_sides(c, span, DESK_APRON_T)
        self.add_operation(Extrusion([rect], DESK_APRON_H))
        self.paint("reddish_brown")


class Desk(Assembly):
    def __init__(self):
        super().__init__()

        top = DeskTop()
        tf_top = TFHelper()
        tf_top.translate([0, 0, DESK_HEIGHT])
        self.add_component(top, tf_top.get_tf())

        # Four legs at corners
        leg_positions = [
            (DESK_INSET,          DESK_INSET),
            (DESK_W - DESK_INSET - DESK_LEG_W, DESK_INSET),
            (DESK_INSET,          DESK_D - DESK_INSET - DESK_LEG_W),
            (DESK_W - DESK_INSET - DESK_LEG_W, DESK_D - DESK_INSET - DESK_LEG_W),
        ]
        for (lx, ly) in leg_positions:
            leg = DeskLeg()
            tf = TFHelper()
            tf.translate([lx, ly, 0])
            self.add_component(leg, tf.get_tf())

        # Front apron (y = DESK_INSET, facing -Y)
        apron_z = DESK_HEIGHT - DESK_APRON_H - DESK_LEG_W
        front_apron = DeskApronLong()
        tf_fa = TFHelper()
        tf_fa.translate([DESK_INSET, DESK_INSET, apron_z])
        self.add_component(front_apron, tf_fa.get_tf())

        # Back apron (y = DESK_D - DESK_INSET)
        back_apron = DeskApronLong()
        tf_ba = TFHelper()
        tf_ba.translate([DESK_INSET, DESK_D - DESK_INSET - DESK_APRON_T, apron_z])
        self.add_component(back_apron, tf_ba.get_tf())

        # Left side apron  (x = DESK_INSET)
        left_apron = DeskApronShort()
        tf_la = TFHelper()
        tf_la.translate([DESK_INSET, DESK_INSET, apron_z])
        tf_la.rotate([0, 0, 1], 90)
        self.add_component(left_apron, tf_la.get_tf())

        # Right side apron
        right_apron = DeskApronShort()
        tf_ra = TFHelper()
        tf_ra.translate([DESK_W - DESK_INSET, DESK_INSET, apron_z])
        tf_ra.rotate([0, 0, 1], 90)
        self.add_component(right_apron, tf_ra.get_tf())


# ═══════════════════════════════════════════════════════════════
#  CHAIR PARTS
# ═══════════════════════════════════════════════════════════════

class ChairSeat(Part):
    def __init__(self):
        super().__init__()
        plane = self.xy()
        sk = Sketch(plane)
        c = Point(sk, CHAIR_SEAT_W / 2, CHAIR_SEAT_D / 2)
        rect = Rectangle.from_center_and_sides(c, CHAIR_SEAT_W, CHAIR_SEAT_D)
        self.add_operation(Extrusion([rect], CHAIR_SEAT_T))
        self.paint("plywood")


class ChairLeg(Part):
    def __init__(self):
        super().__init__()
        plane = self.xy()
        sk = Sketch(plane)
        c = Point(sk, 0, 0)
        rect = Rectangle.from_center_and_sides(c, CHAIR_LEG_W, CHAIR_LEG_W)
        self.add_operation(Extrusion([rect], CHAIR_SEAT_H))
        self.paint("reddish_brown")


class ChairApronLong(Part):
    def __init__(self):
        super().__init__()
        span = CHAIR_SEAT_W - 2 * CHAIR_INSET
        plane = self.xy()
        sk = Sketch(plane)
        c = Point(sk, span / 2, 0)
        rect = Rectangle.from_center_and_sides(c, span, CHAIR_APRON_T)
        self.add_operation(Extrusion([rect], CHAIR_APRON_H))
        self.paint("reddish_brown")


class ChairApronShort(Part):
    def __init__(self):
        super().__init__()
        span = CHAIR_SEAT_D - 2 * CHAIR_INSET
        plane = self.xy()
        sk = Sketch(plane)
        c = Point(sk, span / 2, 0)
        rect = Rectangle.from_center_and_sides(c, span, CHAIR_APRON_T)
        self.add_operation(Extrusion([rect], CHAIR_APRON_H))
        self.paint("reddish_brown")


class ChairBack(Part):
    """Simple slab back panel."""
    def __init__(self):
        super().__init__()
        plane = self.xy()
        sk = Sketch(plane)
        c = Point(sk, CHAIR_BACK_W / 2, 0)
        rect = Rectangle.from_center_and_sides(c, CHAIR_BACK_W, CHAIR_BACK_T)
        self.add_operation(Extrusion([rect], CHAIR_BACK_H))
        self.paint("plywood")


class Chair(Assembly):
    def __init__(self):
        super().__init__()

        # Seat
        seat = ChairSeat()
        tf_seat = TFHelper()
        tf_seat.translate([0, 0, CHAIR_SEAT_H])
        self.add_component(seat, tf_seat.get_tf())

        # Four legs
        leg_positions = [
            (CHAIR_INSET,                            CHAIR_INSET),
            (CHAIR_SEAT_W - CHAIR_INSET - CHAIR_LEG_W, CHAIR_INSET),
            (CHAIR_INSET,                            CHAIR_SEAT_D - CHAIR_INSET - CHAIR_LEG_W),
            (CHAIR_SEAT_W - CHAIR_INSET - CHAIR_LEG_W, CHAIR_SEAT_D - CHAIR_INSET - CHAIR_LEG_W),
        ]
        for (lx, ly) in leg_positions:
            leg = ChairLeg()
            tf = TFHelper()
            tf.translate([lx, ly, 0])
            self.add_component(leg, tf.get_tf())

        apron_z = CHAIR_SEAT_H - CHAIR_APRON_H - CHAIR_LEG_W

        # Front apron
        fa = ChairApronLong()
        tf_fa = TFHelper()
        tf_fa.translate([CHAIR_INSET, CHAIR_INSET, apron_z])
        self.add_component(fa, tf_fa.get_tf())

        # Back apron
        ba = ChairApronLong()
        tf_ba = TFHelper()
        tf_ba.translate([CHAIR_INSET, CHAIR_SEAT_D - CHAIR_INSET - CHAIR_APRON_T, apron_z])
        self.add_component(ba, tf_ba.get_tf())

        # Left side apron
        la = ChairApronShort()
        tf_la = TFHelper()
        tf_la.translate([CHAIR_INSET, CHAIR_INSET, apron_z])
        tf_la.rotate([0, 0, 1], 90)
        self.add_component(la, tf_la.get_tf())

        # Right side apron
        ra = ChairApronShort()
        tf_ra = TFHelper()
        tf_ra.translate([CHAIR_SEAT_W - CHAIR_INSET, CHAIR_INSET, apron_z])
        tf_ra.rotate([0, 0, 1], 90)
        self.add_component(ra, tf_ra.get_tf())

        # Back panel – sits at rear of seat, rises above
        back = ChairBack()
        tf_back = TFHelper()
        tf_back.translate([
            (CHAIR_SEAT_W - CHAIR_BACK_W) / 2,
            CHAIR_SEAT_D - CHAIR_INSET - CHAIR_BACK_T,
            CHAIR_SEAT_H + CHAIR_SEAT_T,
        ])
        self.add_component(back, tf_back.get_tf())


# ═══════════════════════════════════════════════════════════════
#  FULL SCENE
# ═══════════════════════════════════════════════════════════════

class MontessoriSet(Assembly):
    def __init__(self):
        super().__init__()

        desk = Desk()
        self.add_component(desk)

        # Chair sits in front of the desk, offset on X to centre it
        chair = Chair()
        tf_chair = TFHelper()
        chair_x = (DESK_W - CHAIR_SEAT_W) / 2
        chair_y = -(CHAIR_SEAT_D + 60)          # 60 mm gap from desk front
        tf_chair.translate([chair_x, chair_y, 0])
        self.add_component(chair, tf_chair.get_tf())


scene = MontessoriSet()
show(scene)
