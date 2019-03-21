"""Module dedicated to extraction of Landmarking Metafeatures.

Notes:
    For more information about the metafeatures implemented here,
    check out `Rivolli et al.`_.

References:
    .. _Rivolli et al.:
        "Towards Reproducible Empirical Research in Meta-Learning,"
        Rivolli et al. URL: https://arxiv.org/abs/1808.10406
"""

import typing as t
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import numpy as np


class MFELandmarking:
    """Keep methods for metafeatures of ``Landmarking`` group.

    The convention adopted for metafeature extraction related methods is to
    always start with ``ft_`` prefix to allow automatic method detection. This
    prefix is predefined within ``_internal`` module.

    All method signature follows the conventions and restrictions listed below:
        1. For independent attribute data, ``X`` means ``every type of attribu-
            te``, ``N`` means ``Numeric attributes only`` and ``C`` stands for
            ``Categorical attributes only``.

        2. Only ``X``, ``y``, ``N``, ``C``, ``splits``, ``folds``, ``score``
        and ``random_state`` are allowed to be required method arguments. All
        other arguments must be strictly optional (i.e., has a predefined de-
        fault value).

        3. The initial assumption is that the user can change any optional ar-
            gument, without any previous verification of argument value or its
            type, via **kwargs argument of ``extract`` method of MFE class.

        4. The return value of all feature extraction methods should be a sin-
            gle value or a generic Sequence (preferably a :obj:`np.ndarray`)
            type with numeric values.

    There is another type of method adopted for automatic detection. It is ad-
    opted the prefix ``precompute_`` for automatic detection of these methods.
    These methods run while fitting some data into an MFE model automatically,
    and their objective is to precompute some common value shared between more
    than one feature extraction method. This strategy is a trade-off between
    more system memory consumption and speeds up of feature extraction. Their
    return value must always be a dictionary whose keys are possible extra ar-
    guments for both feature extraction methods and other precomputation me-
    thods. Note that there is a share of precomputed values between all valid
    feature-extraction modules (e.g., ``class_freqs`` computed in module ``sta-
    tistical`` can freely be used for any precomputation or feature extraction
    method of module ``landmarking``).
    """

    @classmethod
    def precompute_landmarking_class(cls, X: np.ndarray, y: np.ndarray,
                                     folds: int, random_state: t.Optional[int],
                                     **kwargs) -> t.Dict[str, t.Any]:
        """Precompute distinct classes and its frequencies from ``y``.

        Args:
            X (:obj:`np.ndarray`, optional): attributes from fitted data.
            y (:obj:`np.ndarray`, optional): target attribute from fitted data.
            folds (int): number of folds to k-fold cross validation.
            random_state (int, optional): If int, random_state is the seed used
            by the random number generator; If RandomState instance, random_st-
            ate is the random number generator; If None, the random number gen-
            erator is the RandomState instance used by np.random.

            **kwargs: additional arguments. May have previously precomputed be-
                fore this method from other precomputed methods, so they can
                help speed up this precomputation.

        Return:
            dict: with following precomputed items:
                - ``skf`` (:obj:`StratifiedKFold`): Stratified K-Folds cross-
                validator. Provides train/test indices to split data in
                train/test sets.
        """

        prepcomp_vals = {}

        if X is not None and y is not None\
           and not {"skf"}.issubset(kwargs):
            skf = StratifiedKFold(n_splits=folds, random_state=random_state)
            prepcomp_vals["skf"] = skf

        return prepcomp_vals

    @classmethod
    def importance(cls, X: np.ndarray, y: np.ndarray,
                   random_state: t.Optional[int]) -> np.ndarray:
        clf = DecisionTreeClassifier(random_state=random_state).fit(X, y)
        return np.argsort(clf.feature_importances_)

    @classmethod
    def ft_best_node(cls, X: np.ndarray, y: np.ndarray, skf: StratifiedKFold,
                     score: t.Callable[[np.ndarray, np.ndarray], np.ndarray],
                     random_state: t.Optional[int]) -> np.ndarray:
        """Construct a single decision tree node model induced by the most
        informative attribute to establish the linear separability.

        Args:
            X (:obj:`np.ndarray`, optional): attributes from fitted data.

            y (:obj:`np.ndarray`, optional): target attribute from fitted data.

            skf (:obj:`StratifiedKFold`): stratified K-Folds cross-validator.
                Provides train/test indices to split data in train/test sets.

            score (callable): function to compute score of the K-fold evalua-
                tions. Possible functions are described in `scoring.py` module.

            random_state (int, optional): If int, random_state is the seed used
                by the random number generator; If RandomState instance, ran-
                dom_state is the random number generator; If None, the random
                number generator is the RandomState instance used by np.random.

            **kwargs: additional arguments. May have previously precomputed be-
                fore this method from other precomputed methods, so they can
                help speed up this precomputation.

        Return:
            np.ndarray: The performance of each fold.
        """
        result = []
        for train_index, test_index in skf.split(X, y):
            model = DecisionTreeClassifier(max_depth=1,
                                           random_state=random_state)
            X_train = X[train_index, :]
            X_test = X[test_index, :]
            y_train, y_test = y[train_index], y[test_index]

            model.fit(X_train, y_train)
            pred = model.predict(X_test)
            result.append(score(y_test, pred))

        return np.array(result)

    @classmethod
    def ft_random_node(cls, X: np.ndarray, y: np.ndarray, skf: StratifiedKFold,
                       score: t.Callable[[np.ndarray, np.ndarray], np.ndarray],
                       random_state: t.Optional[int]) -> np.ndarray:
        """Construct a single decision tree node model induced by a random
        attribute.

        Args:
            X (:obj:`np.ndarray`, optional): attributes from fitted data.

            y (:obj:`np.ndarray`, optional): target attribute from fitted data.

            skf (:obj:`StratifiedKFold`): stratified K-Folds cross-validator.
                Provides train/test indices to split data in train/test sets.

            score (callable): function to compute score of the K-fold evalua-
                tions. Possible functions are described in `scoring.py` module.

            random_state (int, optional): If int, random_state is the seed used
                by the random number generator; If RandomState instance, ran-
                dom_state is the random number generator; If None, the random
                number generator is the RandomState instance used by np.random.

            **kwargs: additional arguments. May have previously precomputed be-
                fore this method from other precomputed methods, so they can
                help speed up this precomputation.

        Return:
            np.ndarray: The performance of each fold.
        """
        result = []
        for train_index, test_index in skf.split(X, y):
            attr = np.random.randint(0, X.shape[1], size=(1,))
            model = DecisionTreeClassifier(max_depth=1,
                                           random_state=random_state)
            X_train = X[train_index, :][:, attr]
            X_test = X[test_index, :][:, attr]
            y_train, y_test = y[train_index], y[test_index]

            model.fit(X_train, y_train)
            pred = model.predict(X_test)
            result.append(score(y_test, pred))

        return np.array(result)

    @classmethod
    def ft_worst_node(cls, X: np.ndarray, y: np.ndarray, skf: StratifiedKFold,
                      score: t.Callable[[np.ndarray, np.ndarray], np.ndarray],
                      random_state: t.Optional[int]) -> np.ndarray:
        """Construct a single decision tree node model induced by the worst
        informative attribute.

        Args:
            X (:obj:`np.ndarray`, optional): attributes from fitted data.

            y (:obj:`np.ndarray`, optional): target attribute from fitted data.

            skf (:obj:`StratifiedKFold`): stratified K-Folds cross-validator.
                Provides train/test indices to split data in train/test sets.

            score (callable): function to compute score of the K-fold evalua-
                tions. Possible functions are described in `scoring.py` module.

            random_state (int, optional): If int, random_state is the seed used
                by the random number generator; If RandomState instance, ran-
                dom_state is the random number generator; If None, the random
                number generator is the RandomState instance used by np.random.

            **kwargs: additional arguments. May have previously precomputed be-
                fore this method from other precomputed methods, so they can
                help speed up this precomputation.

        Return:
            np.ndarray: The performance of each fold.
        """
        result = []
        for train_index, test_index in skf.split(X, y):
            importance = MFELandmarking.importance(X[train_index],
                                                   y[train_index],
                                                   random_state)
            model = DecisionTreeClassifier(max_depth=1,
                                           random_state=random_state)
            X_train = X[train_index, :][:, [importance[0]]]
            X_test = X[test_index, :][:, [importance[0]]]
            y_train, y_test = y[train_index], y[test_index]

            model.fit(X_train, y_train)
            pred = model.predict(X_test)
            result.append(score(y_test, pred))

        return np.array(result)

    @classmethod
    def ft_linear_discr(cls, X: np.ndarray, y: np.ndarray,
                        skf: StratifiedKFold,
                        score: t.Callable[[np.ndarray, np.ndarray], np.ndarray]
                        ) -> np.ndarray:
        """Apply the Linear Discriminant classifier to construct a linear split
        (non parallel axis) in the data to establish the linear separability.

        Args:
            X (:obj:`np.ndarray`, optional): attributes from fitted data.

            y (:obj:`np.ndarray`, optional): target attribute from fitted data.

            skf (:obj:`StratifiedKFold`): stratified K-Folds cross-validator.
                Provides train/test indices to split data in train/test sets.

            score (callable): function to compute score of the K-fold evalua-
                tions. Possible functions are described in `scoring.py` module.

            **kwargs: additional arguments. May have previously precomputed be-
                fore this method from other precomputed methods, so they can
                help speed up this precomputation.

        Return:
            np.ndarray: The performance of each fold.
        """

        result = []
        for train_index, test_index in skf.split(X, y):
            model = LinearDiscriminantAnalysis()
            X_train = X[train_index, :]
            X_test = X[test_index, :]
            y_train, y_test = y[train_index], y[test_index]

            model.fit(X_train, y_train)
            pred = model.predict(X_test)
            result.append(score(y_test, pred))

        return np.array(result)

    @classmethod
    def ft_naive_bayes(cls, X: np.ndarray, y: np.ndarray, skf: StratifiedKFold,
                       score: t.Callable[[np.ndarray, np.ndarray], np.ndarray],
                       ) -> np.ndarray:
        """Evaluate the performance of the Naive Bayes classifier. It assumes
        that the attributes are independent and each example belongs to a cer-
        tain class based on the Bayes probability.

        Args:
            X (:obj:`np.ndarray`, optional): attributes from fitted data.

            y (:obj:`np.ndarray`, optional): target attribute from fitted data.

            skf (:obj:`StratifiedKFold`): stratified K-Folds cross-validator.
                Provides train/test indices to split data in train/test sets.

            score (callable): function to compute score of the K-fold evalua-
                tions. Possible functions are described in `scoring.py` module.

            **kwargs: additional arguments. May have previously precomputed be-
                fore this method from other precomputed methods, so they can
                help speed up this precomputation.

        Return:
            np.ndarray: The performance of each fold.
        """

        result = []
        for train_index, test_index in skf.split(X, y):
            model = GaussianNB()
            X_train = X[train_index, :]
            X_test = X[test_index, :]
            y_train, y_test = y[train_index], y[test_index]

            model.fit(X_train, y_train)
            pred = model.predict(X_test)
            result.append(score(y_test, pred))

        return np.array(result)

    @classmethod
    def ft_one_nn(cls, X: np.ndarray, y: np.ndarray, skf: StratifiedKFold,
                  score: t.Callable[[np.ndarray, np.ndarray], np.ndarray],
                  ) -> np.ndarray:
        """Evaluate the performance of the 1-nearest neighbor classifier. It
        uses the euclidean distance of the nearest neighbor to determine how
        noisy is the data.

        Args:
            X (:obj:`np.ndarray`, optional): attributes from fitted data.

            y (:obj:`np.ndarray`, optional): target attribute from fitted data.

            skf (:obj:`StratifiedKFold`): stratified K-Folds cross-validator.
                Provides train/test indices to split data in train/test sets.

            score (callable): function to compute score of the K-fold evalua-
                tions. Possible functions are described in `scoring.py` module.

            **kwargs: additional arguments. May have previously precomputed be-
                fore this method from other precomputed methods, so they can
                help speed up this precomputation.

        Return:
            np.ndarray: The performance of each fold.
        """

        result = []
        for train_index, test_index in skf.split(X, y):
            model = KNeighborsClassifier(n_neighbors=1)
            X_train = X[train_index, :]
            X_test = X[test_index, :]
            y_train, y_test = y[train_index], y[test_index]

            model.fit(X_train, y_train)
            pred = model.predict(X_test)
            result.append(score(y_test, pred))

        return np.array(result)

    @classmethod
    def ft_elite_nn(cls, X: np.ndarray, y: np.ndarray, skf: StratifiedKFold,
                    score: t.Callable[[np.ndarray, np.ndarray], np.ndarray],
                    random_state: t.Optional[int]) -> np.ndarray:
        """Elite nearest neighbor uses the most informative attribute in the
        dataset to induce the 1-nearest neighbor. With the subset of informati-
        ve attributes is expected that the models should be noise tolerant.

        Args:
            X (:obj:`np.ndarray`, optional): attributes from fitted data.

            y (:obj:`np.ndarray`, optional): target attribute from fitted data.

            skf (:obj:`StratifiedKFold`): stratified K-Folds cross-validator.
                Provides train/test indices to split data in train/test sets.

            score (callable): function to compute score of the K-fold evalua-
                tions. Possible functions are described in `scoring.py` module.

            random_state (int, optional): If int, random_state is the seed used
                by the random number generator; If RandomState instance, ran-
                dom_state is the random number generator; If None, the random
                number generator is the RandomState instance used by np.random.

            **kwargs: additional arguments. May have previously precomputed be-
                fore this method from other precomputed methods, so they can
                help speed up this precomputation.

        Return:
            np.ndarray: The performance of each fold.
        """
        result = []
        for train_index, test_index in skf.split(X, y):
            importance = MFELandmarking.importance(X[train_index],
                                                   y[train_index],
                                                   random_state)
            model = KNeighborsClassifier(n_neighbors=1)
            X_train = X[train_index, :][:, [importance[-1]]]
            X_test = X[test_index, :][:, [importance[-1]]]
            y_train, y_test = y[train_index], y[test_index]

            model.fit(X_train, y_train)
            pred = model.predict(X_test)
            result.append(score(y_test, pred))

        return np.array(result)