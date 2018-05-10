from Main import *
import matplotlib.pyplot as mpl


def predict(tree, data_row):
    if tree.isLeaf:
        return tree.data
    elif data_row[tree.split_feature_id] < tree.split_point:
        return predict(tree.left_region, data_row)
    else:
        return predict(tree.right_region, data_row)


def calculate_mse(data):
    n = len(data)
    sum = 0
    for d in data:
        value = predict(root, d)
        sum += (d[0] - value)**2

    mse = sum/n

    print('MSE on test data is: ' + str(mse))
    return mse


def print_condition_preorder(tree=root):
    if tree.isLeaf:
        print(tree.region_id, tree.split_feature_id, tree.split_point, tree.isLeaf, tree.data)
        return

    print(tree.region_id, tree.split_feature_id, tree.split_point, tree.isLeaf)

    print_condition_preorder(tree.left_region)
    print_condition_preorder(tree.right_region)


def print_condition_inorder(tree=root):
    if tree.isLeaf:
        print(tree.region_id, tree.split_feature_id, tree.split_point, tree.isLeaf, tree.data)
        return

    print_condition_inorder(tree.left_region)
    print(tree.region_id, tree.split_feature_id, tree.split_point, tree.isLeaf)

    print_condition_inorder(tree.right_region)


data = test_data


initialize()
build_tree()
calculate_mse(data)
x = []
y = []
for a in np.arange(0.1,1,0.1):
    print ('alpha = '+ str(a))
    initialize()
    build_tree(with_pruning=True, alpha=a)
    y.append(calculate_mse(data))
    x.append(a)

# mpl.plot(y)
# mpl.show()

# print('**********Preorder traversal of tree************')
# print_condition_preorder()
# print('**********Inorder traversal of tree************')
# print_condition_inorder()
#
