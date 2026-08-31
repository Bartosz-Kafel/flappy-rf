from ml import DecisionTree

class RandomForest():
    def __init__(self, max_depth, n_estimators=50):
        self.datasets = []
        self.n_estimators = n_estimators
        self.dt = DecisionTree(max_depth)

        pass

    def bootstrap_sampling(self, dataset):
        for i in range(self.n_estimators):
            bootstrapped_ds = dataset.sample(frac=1, replace=True)
            self.datasets.append(bootstrapped_ds)

    def train(self, dataset):
        self.bootstrap_sampling(dataset)
        for i in range(self.n_estimators):
            cart = DecisionTree(self.max_depth)
            cart.train(self.datasets[i])



            pass


