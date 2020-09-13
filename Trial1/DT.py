import math

def test_split(dataset, f_index, value):
    left, right = [], []
    for row in dataset:
        if row[f_index] < value:
            left.append(row)
        else:
            right.append(row)
    return left, right

def split_entropy(groups, classes):
    entropy = 0
    totes_size = float(sum(len(group) for group in groups))
    for group in groups:
        size = len(group)
        if size == 0:
            continue
        group_sum = 0
        for class_typ in classes:
            temp1 = ([item[-1] for item in group].count(class_typ)) / float(size)
            if (temp1 == 0):
                continue
            group_sum = group_sum - (temp1*math.log(temp1, 2))
        entropy += (size/totes_size)*group_sum
    return entropy

def get_best_split(dataset):
    class_typ = list(set(item[-1] for item in dataset))
    best_index = 0
    best_value = 0
    best_score = 999
    best_groups = None
    for index in range(len(dataset[0]) - 1):
        for row in dataset:
            groups = test_split(dataset, index, row[index])
            entropy = split_entropy(groups, class_typ)
            if entropy < best_score:
                best_index, best_value, best_score, best_groups = index, row[index], entropy, groups
    return {'index': best_index, 'value': best_value, 'groups': best_groups}


def termination(group):
    outcomes = [row[-1] for row in group]
    return max(set(outcomes), key=outcomes.count)

def split(rlgroup, max_depth, min_size, depth):
    left, right = rlgroup['groups']
    del(rlgroup['groups'])
    if not left or not right:
        rlgroup['left'] = rlgroup['right'] = termination(left+right)
        return
    if depth>= max_depth:
        rlgroup['left'] = termination(left)
        rlgroup['right'] = termination(right)
        return
    if len(left)<=min_size:
        rlgroup['left'] = termination(left)
    else:
        rlgroup['left'] = get_best_split(left)
        split(node['left'], max_depth, min_size, depth+1)
    if len(right)<=min_size:
        rlgroup['right'] = termination(right)
    else:
        rlgroup['right'] = get_best_split(right)
        split(rlgroup['right'], max_depth, min_size, depth+1)

def build_tree(train, max_depth, min_size):
    root = get_best_split(train)
    split(root, max_depth, min_size, 1)
    return root

def predict(rlgroup, row):
    if row[rlgroup['index']] < rlgroup['value']:
        if isinstance(rlgroup['left'], dict):
            return predict(rlgroup['left'], row)
        else:
            return rlgroup['left']
    else:
        if isinstance(rlgroup['right'], dict):
            return predict(rlgroup['right'], row)
        else:
            return rlgroup['right']

def efficiency(test, tree):
    count=0
    for row in test:
        prediction = predict(tree, row)
        if prediction==row[-1]:
            count += 1
    eff = count/float(len(test))
    per_eff = eff*100
    return per_eff