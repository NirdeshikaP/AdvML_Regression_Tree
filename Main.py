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

while len(leaves) <= 10:
    current_leaves = leaves[:] # current_leaves = leaves does not work because it copies reference and changes made to leaves are shown in current_leaves as well.
    temp = []
    temp_rss_reduction = 0
    split_region = None
    split_region_details = None
    print('Current number of leaves: ' + str(len(current_leaves)))

    for region in current_leaves:
        split_point_feature, split_details = find_split_point(region.data, input_features)
        split_rss = split_details[0]

        region.split_feature = split_point_feature
        region.split_point = split_details[1]
        region.left_region = Region(data=split_details[2], rss=split_details[3])
        region.right_region = Region(data=split_details[4], rss=split_details[5])

        if region.rss > split_rss:
            if temp_rss_reduction <= region.rss - split_rss:
                temp_rss_reduction = region.rss - split_rss
                split_region = region

    split_region.data = None

    leaves.remove(split_region)
    leaves.append(split_region.left_region)
    leaves.append(split_region.right_region)
