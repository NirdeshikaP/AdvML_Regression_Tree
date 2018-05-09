from Region import Region
from RegressionTree import *

input_features = feature_id_name_dict.values()
input_features.remove(0) # Removing 'Sales'
leaves = []
regions = []

train_data, test_data = get_data()
root = Region(data=train_data)
leaves.append(root)
regions.append(root)

for region in regions:
    #  print('Splitting region ' + str(region.region_id))
    split_point_feature, split_details = find_split_point(region.data, input_features)
    print(split_details[0])
    region.split_feature = split_point_feature
    region.split_point = split_details[1]
    region.left_region = Region(data=split_details[2])
    region.right_region = Region(data=split_details[3])
    region.data = None
    leaves.remove(region)
    leaves.append(region.left_region)
    leaves.append(region.right_region)
    regions.append(region.left_region)
    regions.append(region.right_region)
    if len(leaves) == 2:
        break

l = [leaf.region_id for leaf in leaves]
print(l)

print(root.split_feature)
print(root.split_point)
print(root.left_region.region_id)
print(root.right_region.region_id)
