from ml.node import Node
from utils import CARTMath
import pandas as pd
import numpy as np
import pickle, os

class DecisionTree():
    def __init__(self, max_depth=5):
        self.max_depth = max_depth
        self.root = None
        self.mh = CARTMath()

        self.bsdir = os.path.join(os.path.expanduser("~"), "Documents", "flappy-rf")
        self.tree_path = os.path.join(self.bsdir, "models", "tree_root.pkl")

    def split(self, node, min_sample_leaf=6, min_sample_split=10):
        total_len = len(node)
        if total_len < min_sample_split * min_sample_leaf:
            return None

        # Counts class frequencies allowing for further calculation of Gini
        total_counts = {}
        for val in node:
            total_counts[val] = total_counts.get(val, 0) + 1

        # Calculate the gini of the parent Node
        original_gini = 1.0 - sum((c / total_len) ** 2 for c in total_counts.values())

        max_reduction = 0.0
        best_split = None

        left_counts = {}
        right_counts = total_counts.copy()

        # Step through array in single pass (O(N))
        for i in range(1, total_len):
            val = node[i - 1]

            # Update left/right frequencies incrementally
            left_counts[val] = left_counts.get(val, 0) + 1
            right_counts[val] -= 1

            # Enforce minimum leaf size constraint
            if i < min_sample_leaf or (total_len - i) < min_sample_leaf:
                continue

            left_len = i
            right_len = total_len - i

            # Instant Gini calculation from dictionary counts
            left_gini = 1.0 - sum((c / left_len) ** 2 for c in left_counts.values())
            right_gini = 1.0 - sum((c / right_len) ** 2 for c in right_counts.values() if c > 0)

            total_gini = (left_len / total_len) * left_gini + (right_len / total_len) * right_gini
            diff_gini = original_gini - total_gini

            if diff_gini > max_reduction:
                max_reduction = diff_gini
                best_split = i

        if max_reduction > 0 and best_split is not None:
            return best_split, max_reduction
        return None
    
    def full_split(self, features, depvector):
        best_split_features = []
        best_split_depvector = []
        best_feature = None
        best_value = None
        highest_reduction = 0.0

        # Combine features and target into one temporary frame
        df = features.copy()
        df["target"] = depvector

        for x in features.columns:
            sorted_df = df.sort_values(by=x)
            sorted_target = sorted_df["target"].tolist()

            split_info = self.split(sorted_target)

            if split_info is None:
                continue

            split_idx, reduction = split_info

            if reduction > highest_reduction:
                highest_reduction = reduction

                # Split features (drop temporary target column)
                left_X = sorted_df.iloc[:split_idx].drop(columns=["target"])
                right_X = sorted_df.iloc[split_idx:].drop(columns=["target"])

                # Split dependent vector (target labels)
                left_y = sorted_df["target"].iloc[:split_idx]
                right_y = sorted_df["target"].iloc[split_idx:]

                best_split_features = [left_X, right_X]
                best_split_depvector = [left_y, right_y]
                best_feature = x

                val_left = sorted_df[x].iloc[split_idx - 1]
                val_right = sorted_df[x].iloc[split_idx]
                best_value = (val_left + val_right) / 2

        return best_split_features, best_split_depvector, best_feature, best_value

    def build_tree(self, features, depvector, current_depth=0):
        # --- Stopping Conditions ---
        flat_y = depvector.flatten().tolist() if hasattr(depvector, 'flatten') else list(depvector)

        if current_depth >= self.max_depth or len(set(flat_y)) == 1 or len(features) == 0:
            most_common_action = max(set(flat_y), key=flat_y.count)
            return Node(value=most_common_action)

        # --- Find the Best Split ---
        split_info = self.full_split(features, depvector)
        best_split_features, best_split_depvector, best_feature, best_value = split_info

        # Fallback if no valid split reduces Gini
        if best_feature is None:
            most_common_action = max(set(flat_y), key=flat_y.count)
            return Node(value=most_common_action)

        # --- Recursive Step ---
        left_X, right_X = best_split_features
        left_y, right_y = best_split_depvector

        left_child = self.build_tree(left_X, left_y, current_depth + 1)
        right_child = self.build_tree(right_X, right_y, current_depth + 1)

        return Node(
            feature=best_feature,
            threshold=best_value,
            left=left_child,
            right=right_child,
        )

    def train(self, features, depvector):
        # Ensure features is a Pandas DataFrame
        if not isinstance(features, pd.DataFrame):
            features = pd.DataFrame(features)

        # Ensure depvector is 1-dimensional
        if hasattr(depvector, 'values'):
            depvector = depvector.values.ravel()
        elif isinstance(depvector, np.ndarray):
            depvector = depvector.ravel()
            
        self.root = self.build_tree(features, depvector, current_depth=0)

    def predict(self, sample):
        node = self.root

        while node.value is None:
            if sample[node.feature] <= node.threshold:
                node = node.left
            else:
                node = node.right

        return node.value

    def save_tree(self):
        with open(self.tree_path, "wb") as f:
            pickle.dump(self.root, f)

    def load_tree(self):
        with open(self.tree_path, "rb") as f:
            self.root = pickle.load(f)