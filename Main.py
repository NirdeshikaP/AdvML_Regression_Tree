from Region import Region
from RegressionTree import *

input_features = feature_id_name_dict.values()
input_features.remove(0) # Removing 'Sales'
leaves = []
regions = []

train_data, test_data = get_data()
y_values = [row[0] for row in train_data]
root_rss = calc_rss(y_values)
root = Region(data=train_data, rss=root_rss)
leaves.append(root)
regions.append(root)

for region in regions:
    #  print('Splitting region ' + str(region.region_id))
    split_point_feature, split_details = find_split_point(region.data, input_features)
    print(split_details[0])
    split_rss = split_details[0]

    region.split_feature = split_point_feature
    region.split_point = split_details[1]
    region.left_region = split_details[2]
    region.right_region = split_details[3]

    if region.rss > split_rss:
        region.data = None
        leaves.remove(region)
        leaves.append(region.left_region)
        leaves.append(region.right_region)

    regions.append(region.left_region)
    regions.append(region.right_region)
    if len(leaves) == 10:
        break

print(root.split_feature)
print(root.split_point)
