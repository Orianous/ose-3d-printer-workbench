import Part
from FreeCAD import Vector

from .axis_side_mount import AxisSideMount
from .corner import Corner, is_top_corner
from .rotate_and_translate_part import rotate_and_translate_part


class AngleFrameConnector:
    """
    Encapsulates the data (i.e. topography and shape)
    for an Angle Frame Connector,
    and is separate from the "view" or GUI representation.

    An angle frame connector is made up of three brackets.
    """

    bracket_height = 38.1

    # forms the outer-most corner of bracket
    bracket_outer_edge_thickness = 4.21

    # forms the outer edges of bracket
    bracket_end_thickness = 3.41

    axis_side_mount_width = 5
    axis_side_mount_length = 27.75

    @classmethod
    def make(cls, width, thickness, corner=Corner.BOTTOM_LEFT_FRONT):
        """Make an angle frame connector.

        :param width: Width of the angled frame.
        :type width: float
        :param thickness: Thickness of the angled frame.
        :type thickness: float
        :param corner: Which corner to orient the angle frame connector to.
                       Defaults to bottom left front corner.
        :type corner: str, optional
        :return: an angle frame connector
        :rtype: Part.Shape
        """
        bracket_length = cls.calculate_bracket_length(width)
        length = bracket_length + cls.bracket_height

        angle_frame_connector = cls._make_angle_frame_connector(
            bracket_length, thickness, length, corner)

        d = get_angle_frame_connector_rotation_and_translation(corner, length)
        rotate_and_translate_part(angle_frame_connector, d)

        return angle_frame_connector

    @classmethod
    def _make_angle_frame_connector(cls,
                                    bracket_length,
                                    thickness,
                                    length,
                                    corner):
        bracket_width = cls.calculate_bracket_width(thickness)

        angle_connector_corner = make_angle_connector_corner(
            bracket_length, bracket_width)

        tri_bracket = make_tri_bracket(
            bracket_length,
            bracket_width,
            cls.bracket_height,
            cls.bracket_outer_edge_thickness,
            cls.bracket_end_thickness,
            thickness)

        # Top tri-bracket
        top_bracket = tri_bracket.copy()
        top_bracket.translate(Vector(0, 0, bracket_length))

        # Right tri-bracket
        right_bracket = tri_bracket.copy()
        right_bracket.rotate(Vector(0, 0, 0), Vector(0, -1, 0), 90)
        right_bracket.translate(Vector(length, 0, 0))

        # Rear tri-bracket
        rear_bracket = tri_bracket.copy()
        rear_bracket.rotate(Vector(0, 0, 0), Vector(1, 0, 0), 90)
        rear_bracket.translate(Vector(0, length, 0))

        parts = [
            angle_connector_corner, top_bracket, right_bracket, rear_bracket
        ]

        if is_top_corner(corner):
            axis_side_mount = AxisSideMount.make(
                cls.axis_side_mount_width,
                cls.axis_side_mount_length,
                corner)

            parts.append(axis_side_mount)

        angle_frame_connector = reduce(
            lambda union, part: union.fuse(part), parts)

        # removeSplitter() refines shape
        return angle_frame_connector.removeSplitter()

    @classmethod
    def calculate_bracket_length(cls, width):
        return width + \
            cls.bracket_outer_edge_thickness + cls.bracket_end_thickness

    @classmethod
    def calculate_bracket_width(cls, thickness):
        return thickness + \
            cls.bracket_outer_edge_thickness + cls.bracket_end_thickness

    @classmethod
    def distance_between_axis_side_mount_holes_and_frame(cls):
        return AxisSideMount.calculate_distance_between_holes_and_connector(
            cls.axis_side_mount_length)

    @classmethod
    def calculate_y_axis_overhang_distance(cls):
        return AxisSideMount.calculate_overhang_distance(
            cls.axis_side_mount_length)


def make_tri_bracket(length,
                     width,
                     height,
                     outer_edge_thickness,
                     end_thickness,
                     thickness):
    outer_most_edge = make_outer_most_edge_of_tri_bracket(
        length,
        width,
        height,
        outer_edge_thickness,
        end_thickness)
    inner_most_edge = make_inner_most_edge_of_tri_bracket(
        length,
        width,
        height,
        outer_edge_thickness,
        thickness)
    return outer_most_edge.fuse(inner_most_edge)


def make_outer_most_edge_of_tri_bracket(length,
                                        width,
                                        height,
                                        outer_edge_thickness,
                                        end_thickness):
    box = Part.makeBox(length, length, height)
    inner_box_dimension = length - outer_edge_thickness - end_thickness
    inner_box = Part.makeBox(
        inner_box_dimension, inner_box_dimension, height)
    inner_box.translate(Vector(
        outer_edge_thickness, outer_edge_thickness, 0))

    subtraction_box = Part.makeBox(length, length, height)
    subtraction_box.translate(Vector(width, width, 0))

    return box.cut(inner_box).cut(subtraction_box)


def make_inner_most_edge_of_tri_bracket(length,
                                        width,
                                        height,
                                        outer_edge_thickness,
                                        thickness):
    inner_most_edge_offset = outer_edge_thickness + thickness
    box_dimension = length - inner_most_edge_offset
    box = Part.makeBox(box_dimension, box_dimension, height)
    box.translate(
        Vector(inner_most_edge_offset, inner_most_edge_offset, 0))

    subtraction_box = Part.makeBox(length, length, height)
    subtraction_box.translate(Vector(width, width, 0))

    return box.cut(subtraction_box)


def make_angle_connector_corner(bracket_length, bracket_width):
    box = Part.makeBox(bracket_length, bracket_length, bracket_length)

    inner_box = box.copy()
    inner_box.translate(Vector(bracket_width, bracket_width, bracket_width))

    return box.cut(inner_box)


def get_angle_frame_connector_rotation_and_translation(corner, length):
    d = get_rotation_and_translation_by_corner(length)
    return d[corner]


def get_rotation_and_translation_by_corner(length):
    return {
        Corner.BOTTOM_LEFT_FRONT: {
            'rotate_args': [Vector(), Vector(0, 0, 1), 0],
            'translation': Vector()
        },
        Corner.BOTTOM_LEFT_REAR: {
            'rotate_args': [Vector(), Vector(0, 0, -1), 90],
            'translation': Vector(0, length, 0)
        },
        Corner.BOTTOM_RIGHT_REAR: {
            'rotate_args': [Vector(), Vector(0, 0, 1), 180],
            'translation': Vector(length, length, 0)
        },
        Corner.BOTTOM_RIGHT_FRONT: {
            'rotate_args': [Vector(), Vector(0, 0, 1), 90],
            'translation': Vector(length, 0, 0)
        },
        Corner.TOP_LEFT_FRONT: {
            'rotate_args': [Vector(), Vector(0, 1, 0), 90],
            'translation': Vector(0, 0, length)
        },
        Corner.TOP_LEFT_REAR: {
            'rotate_args': [
                [Vector(), Vector(0, 1, 0), 90],
                [Vector(), Vector(0, 0, -1), 90]
            ],
            'translation': Vector(0, length, length)
        },
        Corner.TOP_RIGHT_REAR: {
            'rotate_args': [
                [Vector(), Vector(0, 1, 0), 180],
                [Vector(), Vector(0, 0, 1), 90]
            ],
            'translation': Vector(length, length, length)
        },
        Corner.TOP_RIGHT_FRONT: {
            'rotate_args': [Vector(), Vector(0, 1, 0), 180],
            'translation': Vector(length, 0, length)
        }
    }
