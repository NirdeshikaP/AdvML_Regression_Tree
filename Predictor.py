from Main import *
import matplotlib.pyplot as mpl


def predict(tree, data_row):
    if tree.isLeaf:
        return tree.data
    elif data_row[tree.split_feature_id] < tree.split_point:
        return predict(tree.left_region, data_row)
    else:
        return predict(tree.right_region, data_row)


# def calculate_mse(data):
#     n = len(data)
#     sum = 0
#     for d in data:
#         value = predict(root, d)
#         sum += (d[0] - value)**2
#
#     mse = sum/n
#
#     print('MSE on test data is: ' + str(mse))
#     return mse


def calculate_mse(actual, expected):
    n = len(actual)
    sum = 0
    for i in range(n):
        sum += (actual[i] - expected[i])**2

    mse = sum/n
    print('MSE on test data is: ' + str(mse))
    return mse


# def print_condition_preorder(tree):
#     if tree.isLeaf:
#         print(tree.region_id, tree.split_feature_id, tree.split_point, tree.isLeaf, tree.data)
#         return
#
#     print(tree.region_id, tree.split_feature_id, tree.split_point, tree.isLeaf)
#
#     print_condition_preorder(tree.left_region)
#     print_condition_preorder(tree.right_region)
#
#
# def print_condition_inorder(tree):
#     if tree.isLeaf:
#         print(tree.region_id, tree.split_feature_id, tree.split_point, tree.isLeaf, tree.data)
#         return
#
#     print_condition_inorder(tree.left_region)
#     print(tree.region_id, tree.split_feature_id, tree.split_point, tree.isLeaf)
#
#     print_condition_inorder(tree.right_region)

 # print('**********Preorder traversal of tree************')
 #    print_condition_preorder()
 #    print('**********Inorder traversal of tree************')
 #    print_condition_inorder()

def case_1_build_tree():
    train_data, test_data = get_data()
    expected = [d[0] for d in test_data]
    root = build_root(train_data)
    input_features = get_input_features()
    build_tree(root, input_features)
    actual = [predict(root, row) for row in test_data]
    calculate_mse(actual=actual, expected=expected)



def case_2_build_tree_with_pruning():
    x = []
    y = []

    train_data, test_data = get_data()
    expected = [d[0] for d in test_data]
    input_features = get_input_features()

    for a in np.arange(0.1, 1, 0.1):
        print ('alpha = '+ str(a))
        root = build_root(train_data)
        build_tree(root=root, input_features=input_features, with_pruning=True, alpha=a)
        actual = [predict(root, row) for row in test_data]
        y.append(calculate_mse(actual=actual, expected=expected))
        x.append(a)

    mpl.plot(y)
    mpl.show()


def case_3_build_tree_with_bagging():
    number_of_samples = 100
    number_of_points_in_each_sample = 100
    train_data, test_data = get_data(for_boot_strapping=True, number_of_points_in_each_sample = number_of_points_in_each_sample, number_of_samples = number_of_samples)
    expected = [d[0] for d in test_data]
    actual = []
    input_features = get_input_features()

    for i in range(number_of_samples):
        root = build_root(train_data[i])
        build_tree(root, input_features)
        calculated_output = []
        for d in test_data:
            calculated_output.append(predict(root, d))
        actual.append(calculated_output)

    actual = map(sum, zip(*actual))
    actual = [a/number_of_samples for a in actual]
    calculate_mse(actual=actual, expected=expected)


def case_4_build_tree_for_random_forest():
    number_of_features = 5
    train_data, test_data = get_data()
    expected = [d[0] for d in test_data]
    number_of_trees = 100
    actual = []

    for i in range(number_of_trees):
        root = build_root(train_data)
        input_features = get_input_features(for_random_forests=True, number_of_features=number_of_features)
        build_tree(root=root, input_features=input_features)
        calculated_output = []
        for d in test_data:
            calculated_output.append(predict(root,d))
        actual.append(calculated_output)

    actual = map(sum, zip(*actual))
    actual = [a / number_of_trees for a in actual]
    calculate_mse(actual=actual, expected=expected)




# case_1_build_tree()
# case_2_build_tree_with_pruning()
# case_3_build_tree_with_bagging()
case_4_build_tree_for_random_forest()