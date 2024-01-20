from media_processing import FrameData, Landmarks

class CoordTranslator:
    def __init__(self, dimensions):
        # a tuple
        self.dimensions = dimensions

    def translate_coords(self, frame_data: FrameData):
        # from perspective of person's holding up their palm to the camera
        wrist = frame_data.fetch(Landmarks.WRIST)
        palm_right = frame_data.fetch(Landmarks.INDEX_FINGER_MCP)
        palm_left = frame_data.fetch(Landmarks.PINKY_FINGER_MCP)

        x1 = wrist.x
        y1 = wrist.y
        x2 = palm_right.x
        y2 = palm_right.y
        x3 = palm_left.x
        y3 = palm_left.y

        # POV of camera is flipped horizontally compared to what the user would expect
        # so reverse x direction here
        centroid_x = 1 + (-1 * ((x1 + x2 + x3)/3))
        centroid_y = (y1 + y2 + y3)/3

        # factorize to dimensions
        centroid_x *= self.dimensions[0]
        centroid_y *= self.dimensions[1]

        centroid = (centroid_x, centroid_y)
        return centroid
