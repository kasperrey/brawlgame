from math import sqrt, floor


class Rect:
    @staticmethod
    def rect_and_rect(rect1_x1: int, rect1_y1: int, rect1_x2: int, rect1_y2: int, rect2_x1: int, rect2_y1: int, rect2_x2: int, rect2_y2: int) -> bool:
        if (rect1_x1 <= rect2_x2 <= rect1_x2) \
                or (rect1_x1 <= rect2_x1 <= rect1_x2):
            if (rect1_y1 <= rect2_y2 <= rect1_y2) \
                    or (rect1_y1 <= rect2_y1 <= rect1_y2):
                return True
        if (rect2_x1 <= rect1_x2 <= rect2_x2) \
                or (rect2_x1 <= rect1_x1 <= rect2_x2):
            if (rect2_y1 <= rect1_y2 <= rect2_y2) \
                    or (rect2_y1 <= rect1_y1 <= rect2_y2):
                return True
        return False

    @staticmethod
    def point_and_rect(point_x: int, point_y: int, rect_x1: int, rect_y1: int, rect_x2: int, rect_y2: int) -> bool:
        if rect_x1 <= point_x <= rect_x2:
            if rect_y1 <= point_y <= rect_y2:
                return True
        return False


class Circle:
    @staticmethod
    def circle_and_circle(cl1x: int, cl1y: int, cl1radius: int, cl2x: int, cl2y: int, cl2radius: int) -> bool:
        dist_x = cl1x - cl2x
        dist_y = cl1y - cl2y
        distance = sqrt((dist_x * dist_x) + (dist_y * dist_y))
        if distance <= cl1radius+cl2radius:
            return True
        return False

    @staticmethod
    def circle_and_rect(circlex: int, circley: int, circleradius: int, rect_x1: int, rect_y1: int, rect_x2: int, rect_y2: int):
        if Rect.rect_and_rect(circlex-floor(circleradius/4)*3, circley-floor(circleradius/4)*3, circlex+floor(circleradius/4)*3, circley+floor(circleradius/4)*3, rect_x1, rect_y1, rect_x2, rect_y2):
            return True
        if not Rect.rect_and_rect(circlex-circleradius, circley-circleradius, circlex+circleradius, circley+circleradius, rect_x1, rect_y1, rect_x2, rect_y2):
            return False
        mid_rect = (rect_x1+((rect_x2-rect_x1)/2), rect_y1+((rect_y2-rect_y1)/2))
        dist_x = (mid_rect[0] - circlex)
        dist_y = (mid_rect[1] - circley)
        distance = sqrt((dist_x * dist_x) + (dist_y * dist_y))
        een_x = dist_x/distance
        een_y = dist_y/distance
        piont_x = (circlex+(een_x*circleradius))
        piont_y = (circley+(een_y*circleradius))
        return Rect.point_and_rect(floor(piont_x), floor(piont_y), rect_x1, rect_y1, rect_x2, rect_y2)

    @staticmethod
    def circle_and_parallelogram(circlex: int, circley: int, circleradius: int,
                                 four_corners: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]):
        if Parallelogram.parallelogram_and_rect(four_corners, circlex - floor(circleradius / 4) * 3, circley - floor(circleradius / 4) * 3,
                              circlex + floor(circleradius / 4) * 3, circley + floor(circleradius / 4) * 3):
            return True
        if not Parallelogram.parallelogram_and_rect(four_corners, circlex - circleradius, circley - circleradius, circlex + circleradius,
                                  circley + circleradius):
            return False
        mid_para = (((four_corners[3][0] - four_corners[0][0])/2) + ((four_corners[1][0] - four_corners[0][0]) / 2), four_corners[3][1] + ((four_corners[0][1] - four_corners[3][1]) / 2))
        dist_x = (mid_para[0] - circlex)
        dist_y = (mid_para[1] - circley)
        distance = sqrt((dist_x * dist_x) + (dist_y * dist_y))
        een_x = dist_x / distance
        een_y = dist_y / distance
        piont_x = (circlex + (een_x * circleradius))
        piont_y = (circley + (een_y * circleradius))
        return Parallelogram.parallelogram_and_point(four_corners, floor(piont_x), floor(piont_y))

    @staticmethod
    def circle_and_triangleup(circlex: int, circley: int, circleradius: int,
                                 three_corners: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]):
        if TriangleUp.triangleup_and_rect(three_corners, circlex - floor(circleradius / 4) * 3,
                                                circley - floor(circleradius / 4) * 3,
                                                circlex + floor(circleradius / 4) * 3,
                                                circley + floor(circleradius / 4) * 3):
            return True
        if not TriangleUp.triangleup_and_rect(three_corners, circlex - circleradius, circley - circleradius,
                                                    circlex + circleradius,
                                                    circley + circleradius):
            return False
        mid_para = (three_corners[2][0] + ((three_corners[1][0]-three_corners[2][0])/2),
                    three_corners[0][1] + ((three_corners[1][1]-three_corners[0][1])/2))
        dist_x = (mid_para[0] - circlex)
        dist_y = (mid_para[1] - circley)
        distance = sqrt((dist_x * dist_x) + (dist_y * dist_y))
        een_x = dist_x / distance
        een_y = dist_y / distance
        piont_x = (circlex + (een_x * circleradius))
        piont_y = (circley + (een_y * circleradius))
        return TriangleUp.triangleup_and_point(three_corners, floor(piont_x), floor(piont_y))

    @staticmethod
    def circle_and_triangledown(circlex: int, circley: int, circleradius: int,
                              three_corners: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]):
        if TriangleDown.triangledown_and_rect(three_corners, circlex - floor(circleradius / 4) * 3,
                                        circley - floor(circleradius / 4) * 3,
                                        circlex + floor(circleradius / 4) * 3,
                                        circley + floor(circleradius / 4) * 3):
            return True
        if not TriangleDown.triangledown_and_rect(three_corners, circlex - circleradius, circley - circleradius,
                                            circlex + circleradius,
                                            circley + circleradius):
            return False
        mid_para = (three_corners[0][0] + ((three_corners[1][0] - three_corners[0][0]) / 2),
                    three_corners[0][1] + ((three_corners[1][1] - three_corners[0][1]) / 2))
        dist_x = (mid_para[0] - circlex)
        dist_y = (mid_para[1] - circley)
        distance = sqrt((dist_x * dist_x) + (dist_y * dist_y))
        een_x = dist_x / distance
        een_y = dist_y / distance
        piont_x = (circlex + (een_x * circleradius))
        piont_y = (circley + (een_y * circleradius))
        return TriangleDown.triangledown_and_point(three_corners, floor(piont_x), floor(piont_y))

    @staticmethod
    def circle_and_triangle(circlex: int, circley: int, circleradius: int,
                                three_corners: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]):
        min_x = min(three_corners[0][0], three_corners[1][0], three_corners[2][0])
        max_x = max(three_corners[0][0], three_corners[1][0], three_corners[2][0])
        min_y = min(three_corners[0][0], three_corners[1][0], three_corners[2][0])
        max_y = max(three_corners[0][0], three_corners[1][0], three_corners[2][0])
        mid_para = (min_x + ((max_x - min_x) / 2),
                    min_y + ((max_y - min_y) / 2))
        dist_x = (mid_para[0] - circlex)
        dist_y = (mid_para[1] - circley)
        distance = sqrt((dist_x * dist_x) + (dist_y * dist_y))
        een_x = dist_x / distance
        een_y = dist_y / distance
        piont_x = (circlex + (een_x * circleradius))
        piont_y = (circley + (een_y * circleradius))
        return Irregular.triangle_and_point(three_corners, floor(piont_x), floor(piont_y))

    @staticmethod
    def circle_and_lozenge(circlex: int, circley: int, circleradius: int, four_corners: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]):
        if Lozenge.lozenge_and_rect(four_corners, circlex - floor(circleradius / 4) * 3, circley - floor(circleradius / 4) * 3,
                              circlex + floor(circleradius / 4) * 3, circley + floor(circleradius / 4) * 3):
            return True
        if not Lozenge.lozenge_and_rect(four_corners, circlex - circleradius, circley - circleradius, circlex + circleradius,
                                  circley + circleradius):
            return False
        min_x = min(four_corners[0][0], four_corners[1][0], four_corners[2][0], four_corners[3][0])
        max_x = max(four_corners[0][0], four_corners[1][0], four_corners[2][0], four_corners[3][0])
        min_y = min(four_corners[0][0], four_corners[1][0], four_corners[2][0], four_corners[3][0])
        max_y = max(four_corners[0][0], four_corners[1][0], four_corners[2][0], four_corners[3][0])
        mid_rect = (min_x + ((max_x - min_x) / 2), min_y + ((max_y - min_y) / 2))
        dist_x = (mid_rect[0] - circlex)
        dist_y = (mid_rect[1] - circley)
        distance = sqrt((dist_x * dist_x) + (dist_y * dist_y))
        een_x = dist_x / distance
        een_y = dist_y / distance
        piont_x = floor(circlex + (een_x * circleradius))
        piont_y = floor(circley + (een_y * circleradius))
        return Lozenge.lozenge_and_point(four_corners, piont_x, piont_y)

    @staticmethod
    def circle_and_fourcorner(circlex: int, circley: int, circleradius: int,
                           four_corners: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]):
        if Irregular.fourcorner_and_rect(four_corners, circlex - floor(circleradius / 4) * 3,
                                    circley - floor(circleradius / 4) * 3,
                                    circlex + floor(circleradius / 4) * 3, circley + floor(circleradius / 4) * 3):
            return True
        if not Irregular.fourcorner_and_rect(four_corners, circlex - circleradius, circley - circleradius,
                                        circlex + circleradius,
                                        circley + circleradius):
            return False
        min_x = min(four_corners[0][0], four_corners[1][0], four_corners[2][0], four_corners[3][0])
        max_x = max(four_corners[0][0], four_corners[1][0], four_corners[2][0], four_corners[3][0])
        min_y = min(four_corners[0][0], four_corners[1][0], four_corners[2][0], four_corners[3][0])
        max_y = max(four_corners[0][0], four_corners[1][0], four_corners[2][0], four_corners[3][0])
        mid_rect = (min_x + ((max_x - min_x) / 2), min_y + ((max_y - min_y) / 2))
        dist_x = (mid_rect[0] - circlex)
        dist_y = (mid_rect[1] - circley)
        distance = sqrt((dist_x * dist_x) + (dist_y * dist_y))
        een_x = dist_x / distance
        een_y = dist_y / distance
        piont_x = floor(circlex + (een_x * circleradius))
        piont_y = floor(circley + (een_y * circleradius))
        return Irregular.fourcorner_and_point(four_corners, piont_x, piont_y)

    @staticmethod
    def point_and_circle(point_x, point_y, circlex: int, circley: int, circleradius: int):
        dist_x = point_x - circlex
        dist_y = point_y - circley
        distance = sqrt((dist_x * dist_x) + (dist_y * dist_y))

        if distance <= circleradius:
            return True
        return False


class TriangleUp:
    @staticmethod
    def triangleup_and_point(three_corners: tuple[tuple[int, int], tuple[int, int], tuple[int, int]], point_x: int,
                             point_y: int):
        dist_x1 = three_corners[0][0] - three_corners[2][0]
        dist_x2 = three_corners[1][0] - three_corners[0][0]
        dist_y1 = three_corners[0][1] - three_corners[2][1]
        dist_y2 = three_corners[0][1] - three_corners[1][1]
        dist_pointy = three_corners[0][1] - point_y
        x1 = ((dist_x1 / dist_y1) * dist_pointy) + three_corners[2][0]
        x2 = ((dist_x2 / dist_y2) * dist_pointy) + three_corners[2][0]
        if x1 <= point_x <= x2:
            if three_corners[2][1] <= point_y <= three_corners[0][1]:
                return True
        return False

    @staticmethod
    def triangleup_and_triangleup(three_corners1: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
                                  three_corners2: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]):
        for hoek in three_corners1:
            if TriangleUp.triangleup_and_point(three_corners2, hoek[0], hoek[1]):
                return True
        for hoek in three_corners2:
            if TriangleUp.triangleup_and_point(three_corners1, hoek[0], hoek[1]):
                return True
        return False

    @staticmethod
    def triangleup_and_rect(
            three_corners1: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
            rect_x1: int, rect_y1: int, rect_x2: int, rect_y2: int):
        for hoek in three_corners1:
            if Rect.point_and_rect(hoek[0], hoek[1], rect_x1, rect_y1, rect_x2, rect_y2):
                return True
        for hoek in ((rect_x1, rect_y1), ((rect_x1+(rect_x2-rect_x1)), rect_y1), (rect_x1, rect_y1+(rect_y2-rect_y1)), (rect_x2, rect_y2)):
            if TriangleUp.triangleup_and_point(three_corners1, hoek[0], hoek[1]):
                return True
        return False

    @staticmethod
    def triangleup_and_triangledown(three_cornersup: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
                                  three_cornersdown: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]):
        for hoek in three_cornersup:
            if TriangleDown.triangledown_and_point(three_cornersdown, hoek[0], hoek[1]):
                return True
        for hoek in three_cornersdown:
            if TriangleUp.triangleup_and_point(three_cornersup, hoek[0], hoek[1]):
                return True
        return False

    @staticmethod
    def triangleup_and_triangle(three_cornersup: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
                                    three_corners: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]):
        for hoek in three_cornersup:
            if Irregular.triangle_and_point(three_corners, hoek[0], hoek[1]):
                return True
        for hoek in three_corners:
            if TriangleUp.triangleup_and_point(three_cornersup, hoek[0], hoek[1]):
                return True
        return False

    @staticmethod
    def triangleup_and_fourcorner(three_cornersup: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
                                four_corners: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]):
        for hoek in three_cornersup:
            if Irregular.fourcorner_and_point(four_corners, hoek[0], hoek[1]):
                return True
        for hoek in four_corners:
            if TriangleUp.triangleup_and_point(three_cornersup, hoek[0], hoek[1]):
                return True
        return False


class TriangleDown:
    @staticmethod
    def triangledown_and_point(three_corners: tuple[tuple[int, int], tuple[int, int], tuple[int, int]], point_x: int,
                               point_y: int):
        dist_x1 = three_corners[0][0] - three_corners[2][0]
        dist_x2 = three_corners[1][0] - three_corners[2][0]
        dist_y1 = three_corners[0][1] - three_corners[2][1]
        dist_y2 = three_corners[1][1] - three_corners[2][1]
        dist_pointy = point_y - three_corners[2][1]
        x1 = ((dist_x1 / dist_y1) * dist_pointy) + three_corners[0][0]
        x2 = ((dist_x2 / dist_y2) * dist_pointy) + three_corners[0][0]
        if x1 <= point_x <= x2:
            if three_corners[2][1] <= point_y <= three_corners[0][1]:
                return True
        return False

    @staticmethod
    def triangledown_and_triangledown(three_corners1: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
                                      three_corners2: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]):
        for hoek in three_corners1:
            if TriangleDown.triangledown_and_point(three_corners2, hoek[0], hoek[1]):
                return True
        return False

    @staticmethod
    def triangledown_and_rect(
            three_corners1: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
            rect_x1: int, rect_y1: int, rect_x2: int, rect_y2: int):
        for hoek in three_corners1:
            if Rect.point_and_rect(hoek[0], hoek[1], rect_x1, rect_y1, rect_x2, rect_y2):
                return True
        for hoek in ((rect_x1, rect_y1), ((rect_x1 + (rect_x2 - rect_x1)), rect_y1),
                     (rect_x1, rect_y1 + (rect_y2 - rect_y1)), (rect_x2, rect_y2)):
            if TriangleDown.triangledown_and_point(three_corners1, hoek[0], hoek[1]):
                return True
        return False

    @staticmethod
    def triangledown_and_parallelogram(
            three_corners1: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
            four_corners1: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]):
        for hoek in three_corners1:
            if Parallelogram.parallelogram_and_point(four_corners1, hoek[0], hoek[1]):
                return True
        for hoek in four_corners1:
            if TriangleDown.triangledown_and_point(three_corners1, hoek[0], hoek[1]):
                return True
        return False

    @staticmethod
    def triangledown_and_lozenge(
            three_corners1: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
            four_corners1: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]):
        for hoek in three_corners1:
            if Lozenge.lozenge_and_point(four_corners1, hoek[0], hoek[1]):
                return True
        for hoek in four_corners1:
            if TriangleDown.triangledown_and_point(three_corners1, hoek[0], hoek[1]):
                return True
        return False


class Parallelogram:
    @staticmethod
    def parallelogram_and_parallelogram(four_corners1: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]],
                                four_corners2: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]):
        for hoek in four_corners2:
            if Parallelogram.parallelogram_and_point(four_corners1, hoek[0], hoek[1]):
                return True
        for hoek in four_corners1:
            if Parallelogram.parallelogram_and_point(four_corners2, hoek[0], hoek[1]):
                return True
        return False

    @staticmethod
    def parallelogram_and_rect(
            four_corners1: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]],
            rect_x1: int, rect_y1: int, rect_x2: int, rect_y2: int):
        for hoek in four_corners1:
            if Rect.point_and_rect(hoek[0], hoek[1], rect_x1, rect_y1, rect_x2, rect_y2):
                return True
        for hoek in ((rect_x1, rect_y1), ((rect_x1 + (rect_x2 - rect_x1)), rect_y1),
                     (rect_x1, rect_y1 + (rect_y2 - rect_y1)), (rect_x2, rect_y2)):
            if Parallelogram.parallelogram_and_point(four_corners1, hoek[0], hoek[1]):
                return True
        return False

    @staticmethod
    def parallelogram_and_point(four_corners: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]], point_x: int, point_y: int):
        dist_x = four_corners[3][0] - four_corners[0][0]
        dist_y = four_corners[0][1] - four_corners[3][1]
        dist_pointy = four_corners[0][1] - point_y
        x = ((dist_x/dist_y)*dist_pointy)+four_corners[0][0]
        if x <= point_x <= x+(four_corners[1][0] - four_corners[0][0]):
            if four_corners[0][1] <= point_y <= four_corners[3][1]:
                return True

    @staticmethod
    def triangleup_and_parallelogram(
            three_corners1: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
            four_corners1: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]):
        for hoek in three_corners1:
            if Parallelogram.parallelogram_and_point(four_corners1, hoek[0], hoek[1]):
                return True
        for hoek in four_corners1:
            if TriangleUp.triangleup_and_point(three_corners1, hoek[0], hoek[1]):
                return True
        return False

    @staticmethod
    def parallelogram_and_irregular(four_corners_irr: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]],
                                    four_corners2: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]):
        for hoek in four_corners2:
            if Irregular.fourcorner_and_point(four_corners_irr, hoek[0], hoek[1]):
                return True
        for hoek in four_corners_irr:
            if Parallelogram.parallelogram_and_point(four_corners2, hoek[0], hoek[1]):
                return True
        return False

    @staticmethod
    def parallelogram_and_lozenge(four_corners_lozenge: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]],
                                  four_corners2: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]):
        for hoek in four_corners2:
            if Lozenge.lozenge_and_point(four_corners_lozenge, hoek[0], hoek[1]):
                return True
        for hoek in four_corners_lozenge:
            if Parallelogram.parallelogram_and_point(four_corners2, hoek[0], hoek[1]):
                return True
        return False


class Irregular:
    @staticmethod
    def _knip(three_corners: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]):
        dist_x = three_corners[0][0] - three_corners[2][0]
        dist_y = three_corners[0][1] - three_corners[2][1]
        dist_pointy = three_corners[1][1] - three_corners[2][1]
        x = floor((dist_x / dist_y) * dist_pointy) + min(three_corners[0][0], three_corners[1][0], three_corners[2][0])
        three_corners_1 = (x, three_corners[1][1])
        return (three_corners[0], three_corners[1], three_corners_1), (three_corners[1], three_corners_1, three_corners[2])

    @staticmethod
    def triangle_and_point(three_corners: tuple[tuple[int, int], tuple[int, int], tuple[int, int]], point_x: int, point_y: int):
        driehoek1, driehoek2 = Irregular._knip(three_corners)
        if TriangleUp.triangleup_and_point(driehoek1, point_x, point_y):
            return True
        if TriangleDown.triangledown_and_point(driehoek2, point_x, point_y):
            return True
        return False

    @staticmethod
    def triangle_and_triangle(three_corners1: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
                              three_corners2: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]):
        for hoek in three_corners1:
            if Irregular.triangle_and_point(three_corners2, hoek[0], hoek[1]):
                return True
        for hoek in three_corners2:
            if Irregular.triangle_and_point(three_corners1, hoek[0], hoek[1]):
                return True
        return False

    @staticmethod
    def triangle_and_rect(
            three_corners1: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
            rect_x1: int, rect_y1: int, rect_x2: int, rect_y2: int):
        for hoek in three_corners1:
            if Rect.point_and_rect(hoek[0], hoek[1], rect_x1, rect_y1, rect_x2, rect_y2):
                return True
        for hoek in ((rect_x1, rect_y1), ((rect_x1 + (rect_x2 - rect_x1)), rect_y1),
                     (rect_x1, rect_y1 + (rect_y2 - rect_y1)), (rect_x2, rect_y2)):
            if Irregular.triangle_and_point(three_corners1, hoek[0], hoek[1]):
                return True
        return False

    @staticmethod
    def fourcorner_and_point(four_corners: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]],
                                  point_x: int, point_y: int):
        if Irregular.triangle_and_point((four_corners[0], four_corners[1], four_corners[2]), point_x, point_y):
            return True
        if Irregular.triangle_and_point((four_corners[1], four_corners[2], four_corners[3]), point_x, point_y):
            return True
        return False

    @staticmethod
    def fourcorner_and_fourcorner(
            four_corners1: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]],
            four_corners2: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]):
        for hoek in four_corners2:
            if Irregular.fourcorner_and_point(four_corners1, hoek[0], hoek[1]):
                return True
        for hoek in four_corners1:
            if Irregular.fourcorner_and_point(four_corners2, hoek[0], hoek[1]):
                return True
        return False

    @staticmethod
    def fourcorner_and_rect(
            four_corners1: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]],
            rect_x1: int, rect_y1: int, rect_x2: int, rect_y2: int):
        for hoek in four_corners1:
            if Rect.point_and_rect(hoek[0], hoek[1], rect_x1, rect_y1, rect_x2, rect_y2):
                return True
        for hoek in ((rect_x1, rect_y1), ((rect_x1 + (rect_x2 - rect_x1)), rect_y1),
                     (rect_x1, rect_y1 + (rect_y2 - rect_y1)), (rect_x2, rect_y2)):
            if Irregular.fourcorner_and_point(four_corners1, hoek[0], hoek[1]):
                return True
        return False


class Lozenge:
    @staticmethod
    def lozenge_and_point(four_corners: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]], point_x: int, point_y: int):
        if TriangleUp.triangleup_and_point((four_corners[0], four_corners[1], four_corners[2]), point_x, point_y):
            return True
        if TriangleDown.triangledown_and_point((four_corners[1], four_corners[2], four_corners[3]), point_x, point_y):
            return True
        return False

    @staticmethod
    def lozenge_and_lozenge(
            four_corners1: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]],
            four_corners2: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]):
        for hoek in four_corners2:
            if Lozenge.lozenge_and_point(four_corners1, hoek[0], hoek[1]):
                return True
        for hoek in four_corners1:
            if Lozenge.lozenge_and_point(four_corners2, hoek[0], hoek[1]):
                return True
        return False

    @staticmethod
    def lozenge_and_rect(
            four_corners1: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]],
            rect_x1: int, rect_y1: int, rect_x2: int, rect_y2: int):
        for hoek in four_corners1:
            if Rect.point_and_rect(hoek[0], hoek[1], rect_x1, rect_y1, rect_x2, rect_y2):
                return True
        for hoek in ((rect_x1, rect_y1), ((rect_x1 + (rect_x2 - rect_x1)), rect_y1),
                     (rect_x1, rect_y1 + (rect_y2 - rect_y1)), (rect_x2, rect_y2)):
            if Lozenge.lozenge_and_point(four_corners1, hoek[0], hoek[1]):
                return True
        return False

    @staticmethod
    def lozenge_and_triangleup(
            four_corners1: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]],
            three_corners: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]):
        for hoek in three_corners:
            if Lozenge.lozenge_and_point(four_corners1, hoek[0], hoek[1]):
                return True
        for hoek in four_corners1:
            if TriangleUp.triangleup_and_point(three_corners, hoek[0], hoek[1]):
                return True
        return False

    @staticmethod
    def lozenge_and_irregular(
            four_cornersirr: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]],
            four_corners2: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]):
        for hoek in four_corners2:
            if Irregular.fourcorner_and_point(four_cornersirr, hoek[0], hoek[1]):
                return True
        for hoek in four_cornersirr:
            if Lozenge.lozenge_and_point(four_corners2, hoek[0], hoek[1]):
                return True
        return False
