class Region:
    r_id = 0

    def __init__(self, split_feature=None, split_point=None, left_region=None, right_region=None, data=None):
        self.region_id = Region.r_id
        self.split_feature = split_feature
        self.split_point = split_point
        self.left_region = left_region
        self.right_region = right_region
        self.data = data
        Region.r_id = Region.r_id + 1




