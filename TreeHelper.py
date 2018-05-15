import numpy as np

feature_id_name_dict = {"Sale":0, "CompPrice": 1, "Income": 2,	"Advertising": 3, "Population": 4, "Price": 5, "ShelveLoc": 6,	"Age": 7, "Education": 8, "Urban": 9, "US": 10}


# Pre-process to replace Bad with 0, Medium with 1 and Good with 2.
# Pre-process to replace Yes with 1 and No with 0.
def convertors():
    shelvloc_to_int = {'"Bad"': 0.0, '"Medium"': 1.0, '"Good"': 2.0}
    yes_no_int = {'"Yes"': 1.0, '"No"': 0.0}
    return  shelvloc_to_int, yes_no_int


# Gets the feature name for the given feature id
def get_name_for_id(feature_id):
    for r in feature_id_name_dict:
        if feature_id_name_dict.get(r) == feature_id:
            return r


# Read the csv and apply the pre-processing.
def read_csv():
    data = np.genfromtxt('Carseats.csv', delimiter=',', names=True, converters={6: lambda s: convertors()[0].get(s), 9: lambda s: convertors()[1].get(s), 10: lambda s: convertors()[1].get(s)})
    return data


# Get data by reading the csv. This provides an option to read all the data into one or
# if for_boot_strapping is set to True, then it returns only those number of points and
# number_of_samples number of sets of such points.
def get_data(for_boot_strapping=False, number_of_points_in_each_sample=0, number_of_samples=0):
    data = read_csv()
    np.random.seed(10)
    np.random.shuffle(data)
    train_data = data[0:275]
    test_data = data[275:]
    train_samples = []
    if for_boot_strapping:
        for i in range(number_of_samples):
            train_samples.append(np.random.choice(train_data, number_of_points_in_each_sample))
        return train_samples, test_data
    else:
        return train_data, test_data


# Calculate RSS by taking the sum of the squares of the difference between expected and actual values.
def calc_rss(y_values):
    rss = 0
    y_hat = sum(y_values)/len(y_values) if len(y_values) > 0 else 0

    for y in y_values:
        rss += (y - y_hat)**2

    return rss


# Calculate RSS by taking the sum of the squares of the difference between expected and actual values
# and also add a penalty term which is equal to alpha * number_of_leaves
def calc_rss_with_pruning(y_values, alpha, number_of_leaves):
    rss = 0
    y_hat = sum(y_values)/len(y_values) if len(y_values) > 0 else 0

    for y in y_values:
        rss += (y - y_hat)**2 + (alpha*number_of_leaves)

    return rss


# For each feature and point in the features, split the node and select the feature and point that gives
# the minimum RSS. Split the node only if after splitting, the RSS decreases.
def find_split_point(data, features, with_pruning=False, alpha=0.0, number_of_leaves=0):
    rss = {}
    y_values = [row[0] for row in data]

    for feature in features:
        x_values = [row[feature] for row in data]
        #print(len(x_values))
        n = len(x_values)
        for i in range(1, n):
            r1 = []
            r2 = []
            y_r_1 = []
            y_r_2 = []
            for j in range(n):
                if x_values[j] < x_values[i]:
                    r1.append(data[j])
                    y_r_1.append(y_values[j])
                else:
                    r2.append(data[j])
                    y_r_2.append(y_values[j])

            if with_pruning:
                rss_1 = calc_rss_with_pruning(y_r_1, alpha, number_of_leaves)
                rss_2 = calc_rss_with_pruning(y_r_2, alpha, number_of_leaves)
            else:
                rss_1 = calc_rss(y_r_1)
                rss_2 = calc_rss(y_r_2)

            r = rss_1 + rss_2

            if feature not in rss:
                rss[feature] = (r, x_values[i], r1, rss_1, r2, rss_2)
            elif rss[feature][0] > r:
                rss[feature] = (r, x_values[i], r1, rss_1, r2, rss_2)

    key_min_rss = min(rss, key=rss.get)
    return key_min_rss, rss[key_min_rss]














