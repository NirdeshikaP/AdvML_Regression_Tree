from Region import Region
from RegressionTree import *

leaves = []

train_data, test_data = get_data()
root = Region(data=train_data)
leaves.append(root)

for region in leaves:
    count = 1
    split_point_feature, split_details = find_split_point(region.data)
    region.split_feature = split_point_feature
    region.split_point = split_details[1]
    region.left_region = Region(data=split_details[2])
    region.right_region = Region(data=split_details[3])
    region.data = None
    leaves.remove(region)
    leaves.append(region.left_region)
    leaves.append(region.right_region)
    if len(leaves) == 2:
        break

print(leaves[0].data)
