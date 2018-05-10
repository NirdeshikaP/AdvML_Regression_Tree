class Region:
    r_id = 0

    def __init__(self, split_feature_id=None, split_point=None, rss = 0, left_region=None, right_region=None, data=None, isLeaf= False):
        self.region_id = Region.r_id
        self.split_feature_id = split_feature_id
        self.split_point = split_point
        self.rss = rss
        self.left_region = left_region
        self.right_region = right_region
        self.data = data
        self.isLeaf = isLeaf
        Region.r_id = Region.r_id + 1




