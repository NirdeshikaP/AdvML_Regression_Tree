from Main import *

data = test_data

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


def printCondition_preorder(tree = root):
    if tree.isLeaf:
        print(tree.region_id, tree.split_feature_id, tree.split_point, tree.isLeaf, tree.data)
        return

    print(tree.region_id, tree.split_feature_id, tree.split_point, tree.isLeaf)

    printCondition_preorder(tree.left_region)
    printCondition_preorder(tree.right_region)


def printCondition_inorder(tree = root):
    if tree.isLeaf:
        print(tree.region_id, tree.split_feature_id, tree.split_point, tree.isLeaf, tree.data)
        return

    printCondition_inorder(tree.left_region)
    print(tree.region_id, tree.split_feature_id, tree.split_point, tree.isLeaf)

    printCondition_inorder(tree.right_region)

calculate_mse(data)
print('**********Preorder traversal of tree************')
printCondition_preorder()
print('**********Inorder traversal of tree************')
printCondition_inorder()

