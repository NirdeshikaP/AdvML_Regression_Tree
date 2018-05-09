import numpy as np

# TODO Remove if not used anywhere
feature_id_name_dict = {"CompPrice": 0, "Income": 1,	"Advertising": 2, "Population": 3, "Price":4, "ShelveLoc": 5,	"Age": 6, "Education": 7, "Urban": 8, "US": 9}


# Pre-process to replace Bad with 0, Medium with 1 and Good with 2.
def convertors():
    shelvloc_to_int = {'"Bad"': 0.0, '"Medium"': 1.0, '"Good"': 2.0}
    yes_no_int = {'"Yes"': 1.0, '"No"': 0.0}
    return  shelvloc_to_int, yes_no_int


# TODO Remove if not used anywhere
# Gets the id of the feature for the given feature name
def get_feature_id_for_name(feature_name):
    return feature_id_name_dict.get(feature_name)


def read_csv():
    data = np.genfromtxt('Carseats.csv', delimiter=',', names = True, converters={6: lambda s: convertors()[0].get(s), 9: lambda s: convertors()[1].get(s), 10: lambda s: convertors()[1].get(s)})
    return data


def get_data():
    data = read_csv()
    np.random.seed(10)
    np.random.shuffle(data)

    train_data = data[0:300]
    test_data = data[300:]

    return train_data, test_data


# Making it a dictionary and extract feature values and y_values i.e. Sales
def get_feature_values(train_data):
    feature_values = {}

    for feature_name in train_data.dtype.names:
        feature_values[feature_name] = train_data[feature_name]

    y_values = feature_values.pop('Sales')

    return feature_values, y_values


def find_split_point(train_data):
    rss = {}

    feature_values, y_values = get_feature_values(train_data)

    features = feature_values.keys()

    for feature in features:
        x_values = feature_values[feature]

        n = len(x_values)
        for i in range(1, n):
            r1 = []
            r2 = []
            y_r_1 = []
            y_r_2 = []
            for j in range(n):
                if x_values[j] < x_values[i]:
                    r1.append(train_data[j])
                    y_r_1.append(y_values[j])
                else:
                    r2.append(train_data[j])
                    y_r_2.append(y_values[j])

            y_1_hat = sum(y_r_1)/len(y_r_1) if len(y_r_1) > 0 else 0
            y_2_hat = sum(y_r_2)/len(y_r_2) if len(y_r_2) > 0 else 0

            # TODO: Can modify this using reduce.
            s_1 = [(y - y_1_hat)**2 for y in y_r_1]
            rss_1 = sum(s_1)

            s_2 = [(y - y_2_hat)**2 for y in y_r_2]
            rss_2 = sum(s_2)

            r = rss_1 + rss_2

            if feature not in rss:
                rss[feature] = (r, x_values[i], r1, r2)
            elif rss[feature][0] > r:
                rss[feature] = (r, x_values[i], r1, r2)

    key_min_rss = min(rss, key = rss.get)
    return key_min_rss, rss[key_min_rss]















