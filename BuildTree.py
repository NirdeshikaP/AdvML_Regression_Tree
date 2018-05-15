from TreeHelper import *
from Region import Region


# Get the features needed to estimate "Sales" If for_random_forests is set to True, it randomly selects the number of
# features = number_of_features.
def get_input_features(for_random_forests=False, number_of_features=10):
    input_features = feature_id_name_dict.values()
    input_features.remove(0)
    if for_random_forests:
        input_features = np.random.choice(input_features, number_of_features)
    return input_features


# The root contains all the data initially which is split in further steps. It also contains RSS as its property.
def build_root(data):
    y_values = [row[0] for row in data]
    root_rss = calc_rss(y_values)
    root = Region(data=data, rss=root_rss)
    return root


# It repeatedly splits the root node checking all the split points that are possible with the "input_features" and
# if the parent node's RSS is greater than the sum of children's RSS. If with_pruning is set to True,
# then RSS is calculated with an additional penalty term = alpha * number of leaves at that point.
# It also replaces the data in the leaves with the mean of its "Sales" values.
def build_tree(root, input_features, with_pruning=False, alpha=0.0):
    leaves = []
    leaves.append(root)

    while len(leaves) < 15:
        current_leaves = leaves[:]  # current_leaves = leaves does not work because it copies reference and changes made to leaves are shown in current_leaves as well.
        temp_rss_reduction = 0
        split_region = None
        # print('Current number of leaves: ' + str(len(current_leaves)))

        for region in current_leaves:
            # if there is no data, then there is no need for split
            if len(region.data) <= 1:
                continue

            split_point_feature, split_details = find_split_point(region.data, input_features, with_pruning, alpha, len(leaves))

            split_rss = split_details[0]

            region.split_feature_id = split_point_feature
            region.split_point = split_details[1]
            region.left_region = Region(data=split_details[2], rss=split_details[3])
            region.right_region = Region(data=split_details[4], rss=split_details[5])

            if region.rss > split_rss:
                if temp_rss_reduction <= region.rss - split_rss:
                    temp_rss_reduction = region.rss - split_rss
                    split_region = region

        if split_region is not None:
            split_region.data = None
            leaves.remove(split_region)
            leaves.append(split_region.left_region)
            leaves.append(split_region.right_region)
        else:  # There is nothing else to split. So, len(leaves) <= 25 always evaluates to true and becomes an infinite loop
            break

    for leaf in leaves:
         leaf.isLeaf = True
         y_values = [row[0] for row in leaf.data]
         leaf.data = sum(y_values) / len(y_values) if len(y_values) > 0 else 0
         # print(leaf.data)

    print('Number of regions ' + ('with pruning: ' if with_pruning else 'without pruning: ') + str(len(leaves)))



