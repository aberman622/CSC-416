import math
import csv
from collections import Counter

class Node:
    def __init__(self, feature=None, value=None, decision=None):
        self.feature = feature  
        self.value = value  
        self.decision = decision  
        self.children = {}  

def calculate_entropy(data):
    """Calculate the entropy of the data."""
    total = len(data)
    if total == 0:
        return 0
    
    label_counts = Counter(row[-1] for row in data)  
    entropy = 0
    for count in label_counts.values():
        proportion = count / total
        entropy -= proportion * math.log2(proportion)
    
    return entropy

def calculate_information_gain(feature_index, data):
    """Calculate information gain for a specific feature."""
    base_entropy = calculate_entropy(data)
    
    feature_values = Counter(row[feature_index] for row in data)
    total = len(data)
    
    weighted_entropy = 0
    for value, count in feature_values.items():
        subset = [row for row in data if row[feature_index] == value]
        weighted_entropy += (count / total) * calculate_entropy(subset)

    information_gain = base_entropy - weighted_entropy
    return information_gain

def load_csv(filename):
    """Load CSV data into a list of lists."""
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
    return data

def build_decision_tree(data, features):
    """Recursively build a decision tree."""
    decisions = set(row[-1] for row in data)
    if len(decisions) == 1:
        return Node(decision=decisions.pop())

    if not features:
        majority_decision = Counter(row[-1] for row in data).most_common(1)[0][0]
        return Node(decision=majority_decision)

    best_feature = max(features, key=lambda f: calculate_information_gain(f, data))
    root = Node(feature=best_feature)

    feature_values = set(row[best_feature] for row in data)
    for value in feature_values:
        subset = [row for row in data if row[best_feature] == value]
        if subset:
            child = build_decision_tree(subset, [f for f in features if f != best_feature])
            root.children[value] = child

    return root

data = load_csv('decision_tree_data.csv')
features = list(range(len(data[0]) - 1)) 
decision_tree = build_decision_tree(data, features)

def print_tree(node, depth=0):
    if node.decision is not None:
        print("  " * depth + f"Decision: {node.decision}")
    else:
        print("  " * depth + f"Feature {node.feature}")
        for value, child in node.children.items():
            print("  " * (depth + 1) + f"Value {value}:")
            print_tree(child, depth + 2)

print_tree(decision_tree)
