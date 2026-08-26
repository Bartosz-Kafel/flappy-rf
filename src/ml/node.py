class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature      # Feature name/index to split on
        self.threshold = threshold  # Numeric cutoff value
        self.left = left            # Left child Node
        self.right = right          # Right child Node
        self.value = value          # Leaf prediction value (action 0 or 1)

    def is_leaf(self):
        return self.value is not None