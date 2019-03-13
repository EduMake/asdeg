# A* and Dijkstra Example Generator (ASDEG)
# Copyright (C) 2018 EduMake Limited and Stephen Parry
#
# This file is part of ASDEG (the A* and Dikstra Example Generator)
#
# ASDEG is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ASDEG is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ASDEG.  If not, see <https://www.gnu.org/licenses/>.

#
# intersections.py
#
# Python for finding line intersections
#   intended to be easily adaptable for line-segment intersections
#

import math


DET_TOLERANCE = 0.00000001


def intersect_lines(pt_1, pt_2, pt_a, pt_b):
    """ this returns the intersection of Line(pt_1, pt_2) and Line(pt_a, pt_b)

        returns a tuple: (xi, yi, valid, r, s), where
        (xi, yi) is the intersection
        r is the scalar multiple such that (xi, yi) = pt_1 + r*(pt_2-pt_1)
        s is the scalar multiple such that (xi, yi) = pt_1 + s*(ptB-pt_a)
            valid == 0 if there are 0 or inf. intersections (invalid)
            valid == 1 if it has a unique intersection ON the segment    """

    # the first line is pt_1 + r*(pt_2-pt_1)
    # in component form:
    x1, y1 = pt_1
    x2, y2 = pt_2
    dx12 = x2 - x1
    dy12 = y2 - y1

    # the second line is ptA + s*(ptB-ptA)
    x_a, y_a = pt_a
    x_b, y_b = pt_b
    dx_ab = x_b - x_a
    dy_ab = y_b - y_a

    # we need to find the (typically unique) values of r and s
    # that will satisfy
    #
    # (x1, y1) + r(dx12, dy12) = (x_a, y_a) + s(dx_ab, dy_ab)
    #
    # which is the same as
    #
    #    [ dx12  -dx_ab ][ r ] = [ x_a-x1 ]
    #    [ dy12  -dy_ab ][ s ] = [ y_a-y1 ]
    #
    # whose solution is
    #
    #    [ r ] = _1_  [ -dy_ab  dx_ab ] [ x_a-x1 ]
    #    [ s ] = det  [ -dy12  dx12 ] [ y_a-y1 ]
    #
    # where det = (-dx12 * dy_ab + dy12 * dx_ab)
    #
    # if det is too small, they're parallel
    #
    det = (-dx12 * dy_ab + dy12 * dx_ab)

    if math.fabs(det) < DET_TOLERANCE:
        if x1 == x_a and y1 == y_a or x1 == x_b and y1 == y_b or x2 == x_a and y2 == y_a or x2 == x_b and y2 == y_b:
            colinear = True
        else:
            d_gap_x = x_a - x1
            d_gap_y = y_a - y1
            det2 = -dx12 * d_gap_y + dy12 * d_gap_x
            colinear = (math.fabs(det2) < DET_TOLERANCE)
        if colinear:
            if x1 <= min(x_a, x_b) and x2 <= min(x_a, x_b) and y1 <= min(x_a, x_b) and y2 <= min(x_a, x_b) or \
              x1 >= max(x_a, x_b) and x2 >= max(x_a, x_b) and y1 >= max(x_a, x_b) and y2 >= max(x_a, x_b):
                return 0, 0, 0, 0, 0
            else:
                return 0, 0, 1, 0.5, 0.5
        else:
            return 0, 0, 0, 0, 0

    # now, the determinant should be OK
    det_inv = 1.0/det

    # find the scalar amount along the "self" segment
    r = det_inv * (-dy_ab * (x_a-x1) + dx_ab * (y_a-y1))

    # find the scalar amount along the input line
    s = det_inv * (-dy12 * (x_a-x1) + dx12 * (y_a-y1))

    # return the average of the two descriptions
    xi = (x1 + r*dx12 + x_a + s*dx_ab)/2.0
    yi = (y1 + r*dy12 + y_a + s*dy_ab)/2.0
    return xi, yi, 1, r, s


def test_intersection(test_pt_1, test_pt_2, test_pt_a, test_pt_b):
    """ prints out a test for checking by hand... """
    print("Line segment #1 runs from", test_pt_1, "to", test_pt_2)
    print("Line segment #2 runs from", test_pt_a, "to", test_pt_b)

    result = intersect_lines(test_pt_1, test_pt_2, test_pt_a, test_pt_b)
    print("    Intersection result =", result)
    print()


if __name__ == "__main__":

    test2_pt_1 = (10, 10)
    test2_pt_2 = (20, 20)

    test2_pt_3 = (10, 20)
    test2_pt_4 = (20, 10)

    test2_pt_5 = (40, 20)

    test2_pt_6 = (10, 20)
    test2_pt_7 = (50, 40)
    test2_pt_8 = (20, 25)
    test2_pt_9 = (30, 30)

    test_intersection(test2_pt_1, test2_pt_2, test2_pt_3, test2_pt_4)
    test_intersection(test2_pt_1, test2_pt_3, test2_pt_2, test2_pt_4)
    test_intersection(test2_pt_1, test2_pt_2, test2_pt_4, test2_pt_5)
    test_intersection(test2_pt_6, test2_pt_7, test2_pt_8, test2_pt_9)


def check_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    i_l_res = intersect_lines((x1, y1), (x2, y2), (x3, y3), (x4, y4))
    rv = i_l_res[2] and 0.0 <= i_l_res[3] <= 1.0 and 0.0 <= i_l_res[4] <= 1.0
    rv = rv and i_l_res[3] * i_l_res[4] != 0.0 and i_l_res[3] * i_l_res[4] != 1.0
    return rv
