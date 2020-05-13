import unittest

import FreeCAD as App
from ose3dprinter.app.enums import Side
from ose3dprinter.app.get_faces_for_side import \
    get_faces_for_side
from ose3dprinter.app.is_face_parallel_to_plane import (
    is_face_parallel_to_xy_plane, is_face_parallel_to_xz_plane,
    is_face_parallel_to_yz_plane)
from ose3dprinter.app.model import FrameModel

from .freecad_test_case import FreeCADTestCase


class GetFacesWithinBoundsOfSideForFrameWithCornersTest(FreeCADTestCase):

    @classmethod
    def setUpClass(cls):
        document = App.newDocument()
        cls.frame = document.addObject('Part::FeaturePython', 'Frame')
        FrameModel(cls.frame, has_corners=True)
        document.recompute()

    def test_get_faces_within_bounds_of_side_for_frame_with_corners_top_face(
            self):
        top_faces = get_faces_for_side(self.frame, Side.TOP)

        self.assertEqual(len(top_faces), 8)
        for top_face in top_faces:
            self.assertTrue(is_face_parallel_to_xy_plane(top_face))

    def test_get_faces_within_bounds_of_side_for_frame_with_corners_left_face(
            self):
        left_faces = get_faces_for_side(self.frame, Side.LEFT)

        self.assertEqual(len(left_faces), 8)
        for left_face in left_faces:
            self.assertTrue(is_face_parallel_to_yz_plane(left_face))

    def test_get_faces_within_bounds_of_side_for_frame_with_corners_right_face(
            self):
        right_faces = get_faces_for_side(self.frame, Side.RIGHT)

        self.assertEqual(len(right_faces), 8)
        for right_face in right_faces:
            self.assertTrue(is_face_parallel_to_yz_plane(right_face))

    def test_get_faces_within_bounds_of_side_for_frame_with_corners_front_face(
            self):
        front_faces = get_faces_for_side(self.frame, Side.FRONT)

        self.assertEqual(len(front_faces), 8)
        for front_face in front_faces:
            self.assertTrue(is_face_parallel_to_xz_plane(front_face))

    def test_get_faces_within_bounds_of_side_for_frame_with_corners_rear_face(
            self):
        rear_faces = get_faces_for_side(self.frame, Side.REAR)

        self.assertEqual(len(rear_faces), 8)
        for rear_face in rear_faces:
            self.assertTrue(is_face_parallel_to_xz_plane(rear_face))

    def test_get_faces_within_bounds_of_side_for_frame_with_corners_bottom_face(self):
        bottom_faces = get_faces_for_side(self.frame, Side.BOTTOM)
        self.assertEqual(len(bottom_faces), 0)


if __name__ == '__main__':
    unittest.main()
