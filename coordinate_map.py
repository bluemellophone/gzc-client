class CoordinateMap:
    """
    Maps coordinates to pixels in an image. Does not account for
    curvature of Earth.
    """
    def __init__(self, ulcoord, brcoord, img):
        img_shape = img.shape
        self.width = img_shape[1]
        self.height = img_shape[0]
        self.ulcoord = ulcoord
        self.brcoord = brcoord
        self.dx, self.dy = self.get_pixel_difference()

    def get_pixel_difference(self):
        # Gets degree / pixel
        import math
        difference_x = math.fabs(self.brcoord[1] - self.ulcoord[1])
        difference_y = math.fabs(self.brcoord[0] - self.ulcoord[0])
        dx = (1.0 * self.width) / difference_x
        dy = (1.0 * self.height) / difference_y
        return dx, dy

    def map_point(self, coord):
        import math
        given_y, given_x = coord
        base_y, base_x = self.ulcoord
        difference_x = math.fabs(given_x - base_x)
        difference_y = math.fabs(given_y - base_y)
        x_loc = int(round((difference_x * self.dx)))
        y_loc = int(round((difference_y * self.dy)))
        print("(%r, %r)" % (x_loc, y_loc))
        if x_loc < 0 or x_loc >= self.width:
            print("Error: point outside image")
            #return (-1, -1)
        if y_loc < 0 or y_loc >= self.height:
            print("Error: point outside image")
            #return (-1, -1)
        return (x_loc, y_loc)

    def map_point_float(self, coord):
        import math
        given_y, given_x = coord
        base_y, base_x = self.ulcoord
        difference_x = math.fabs(given_x - base_x)
        difference_y = math.fabs(given_y - base_y)
        x_loc = (difference_x * self.dx)
        y_loc = (difference_y * self.dy)
        print("(%r, %r)" % (x_loc, y_loc))
        if x_loc < 0 or x_loc >= self.width:
            print("Error: point outside image")
            #return (-1, -1)
        if y_loc < 0 or y_loc >= self.height:
            print("Error: point outside image")
            #return (-1, -1)
        return (x_loc, y_loc)
