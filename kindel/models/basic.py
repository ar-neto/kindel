"""Abstract classes iherited by all the other models in this repository"""

from abc import abstractmethod, ABC
from collections import namedtuple

from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor

from kindel.utils.data import featurize

Dataset = namedtuple("Dataset", ["train", "valid", "test"])
Example = namedtuple("Example", ["x", "y"])


class Model(ABC):
    """Model definition abstract class. Contains the blueprint of all the methods
    that need to be defined by a model"""

    def __init__(self, **hyperparameters):
        self.model = self._create_model(**hyperparameters)

    @abstractmethod
    def prepare_dataset(self, df_train, df_valid, df_test): ...

    @abstractmethod
    def train(self): ...

    @abstractmethod
    def predict(self, x): ...

    @abstractmethod
    def featurize(self, df): ...

    @abstractmethod
    def _create_model(self, hyperparameters): ...


class ScikitLearnModel(Model):
    """Model class template to aid the definition of sci-kit learn models"""

    def prepare_dataset(self, df_train, df_valid, df_test):
        X_train, y_train = self.featurize(df_train)
        X_valid, y_valid = self.featurize(df_valid)
        X_test, y_test = self.featurize(df_test)
        self.data = Dataset(
            train=Example(x=X_train, y=y_train),
            valid=Example(x=X_valid, y=y_valid),
            test=Example(x=X_test, y=y_test),
        )
        return self.data

    def train(self):
        self.model.fit(self.data.train.x, self.data.train.y)

    def predict(self, x):
        preds = self.model.predict(x.cpu())
        return preds

    def featurize(self, df):
        return featurize(df, smiles_col="smiles", label_col="y")


class RandomForest(ScikitLearnModel):
    """sci-kit learn Random Forest implementation"""

    def _create_model(self, **hyperparameters):
        return RandomForestRegressor(**hyperparameters, n_jobs=-1)


class XGBoost(ScikitLearnModel):
    """sci-kit learn Gradient boosting regression implementation"""

    def _create_model(self, **hyperparameters):
        return XGBRegressor(**hyperparameters)


class KNeareastNeighbors(ScikitLearnModel):
    """sci-kit k-nearest neighborW implementation"""

    def _create_model(self, **hyperparameters):
        return KNeighborsRegressor(**hyperparameters)
