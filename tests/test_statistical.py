"""Test module for General class metafeatures."""
import pytest

from pymfe.mfe import MFE
from tests.utils import load_xy
import numpy as np

GNAME = "statistical"


class TestStatistical():
    """TestClass dedicated to test Statistical metafeatures."""

    @pytest.mark.parametrize(
        "dt_id, ft_name, exp_value, precompute",
        [
            ###################
            # Mixed data
            ###################
            (0, "can_cor", [4.967439e-01, np.nan], True),
            (0, "gravity", 1.675634e+05, True),
            (0, "cor", [1.441612e-01, 1.677086e-01], True),
            (0, "cov", [7.066178e+08, 5.239762e+09], True),
            (0, "nr_disc", 1, True),
            (0, "eigenvalues", [3.690903e+12, 1.224126e+13], True),
            (0, "g_mean", [np.nan, np.nan], True),
            (0, "h_mean", [5.998783e+04, 1.989364e+05], True),
            (0, "iq_range", [1.920484e+05, 6.339866e+05], True),
            (0, "kurtosis", [7.790129e-01, 1.927274e+00], True),
            (0, "mad", [1.256607e+05, 4.159848e+05], True),
            (0, "max", [2.069934e+06, 6.837930e+06], True),
            (0, "mean", [4.029463e+05, 1.333427e+06], True),
            (0, "median", [1.470961e+05, 4.873190e+05], True),
            (0, "min", [1.478355e+04, 4.903048e+04], True),
            (0, "nr_cor_attr", [1.818182e-02], True),
            (0, "nr_norm", 0, True),
            (0, "nr_outliers", 11, True),
            (0, "range", [2.055151e+06, 6.788900e+06], True),
            (0, "sd", [5.807830e+05, 1.920665e+06], True),
            (0, "sd_ratio", np.nan, True),
            (0, "skewness", [1.563538e+00, 3.244487e-01], True),
            (0, "sparsity", [9.183673e-02, 1.060439e-01], True),
            (0, "t_mean", [1.609781e+05, 5.329507e+05], True),
            (0, "var", [3.690903e+12, 1.224125e+13], True),
            # (0, "w_lambda", 8.276401e-01, True),
            (0, "can_cor", [4.967439e-01, np.nan], False),
            (0, "gravity", 1.675634e+05, False),
            (0, "cor", [1.441612e-01, 1.677086e-01], False),
            (0, "cov", [7.066178e+08, 5.239762e+09], False),
            (0, "nr_disc", 1, False),
            (0, "eigenvalues", [3.690903e+12, 1.224126e+13], False),
            (0, "g_mean", [np.nan, np.nan], False),
            (0, "h_mean", [5.998783e+04, 1.989364e+05], False),
            (0, "iq_range", [1.920484e+05, 6.339866e+05], False),
            (0, "kurtosis", [7.790129e-01, 1.927274e+00], False),
            (0, "mad", [1.256607e+05, 4.159848e+05], False),
            (0, "max", [2.069934e+06, 6.837930e+06], False),
            (0, "mean", [4.029463e+05, 1.333427e+06], False),
            (0, "median", [1.470961e+05, 4.873190e+05], False),
            (0, "min", [1.478355e+04, 4.903048e+04], False),
            (0, "nr_cor_attr", [1.818182e-02], False),
            (0, "nr_norm", 0, False),
            (0, "nr_outliers", 11, False),
            (0, "range", [2.055151e+06, 6.788900e+06], False),
            (0, "sd", [5.807830e+05, 1.920665e+06], False),
            (0, "sd_ratio", np.nan, False),
            (0, "skewness", [1.563538e+00, 3.244487e-01], False),
            (0, "sparsity", [9.183673e-02, 1.060439e-01], False),
            (0, "t_mean", [1.609781e+05, 5.329507e+05], False),
            (0, "var", [3.690903e+12, 1.224125e+13], False),
            # (0, "w_lambda", 8.276401e-01, False),
            ###################
            # Categorical data
            ###################
            # (1, "can_cor", [0.79982271, np.nan], True),
            (1, "gravity", 0.76488534, True),
            # (1, "cor", [np.nan, np.nan], True),
            (1, "cov", [0.01065760, 0.01849074], True),
            # (1, "nr_disc", 1, True),
            (1, "eigenvalues", [0.12702470, 0.15885051], True),
            # (1, "g_mean", [0, 0], True),
            (1, "h_mean", [0, 0], True),
            (1, "iq_range", [0.33333333, 0.47756693], True),
            # (1, "kurtosis", [np.nan, np.nan], True),
            (1, "mad", [0, 0], True),
            # (1, "max", [0.97435897, 0.16012815], True),
            # (1, "mean", [0.70575399, 0.28775599], True),
            # (1, "median", [0.79487179, 0.40907387], True),
            (1, "min", [0, 0], True),
            # (1, "nr_cor_attr", np.nan, True),
            (1, "nr_norm", 0, True),
            (1, "nr_outliers", 25, True),
            # (1, "range", [0.97435897, 0.16012815], True),
            (1, "sd", [0.32349560, 0.15153916], True),
            # (1, "sd_ratio", np.nan, True),
            # (1, "skewness", [np.nan, np.nan], True),
            (1, "sparsity", [0.49521243, 0.02778647], True),
            # (1, "t_mean", [0.74908425, 0.35654219], True),
            (1, "var", [0.12702470, 0.08652912], True),
            # (1, "w_lambda", np.nan, True),
            # (1, "can_cor", [0.79982271, np.nan], False),
            (1, "gravity", 0.76488534, False),
            # (1, "cor", [np.nan, np.nan], False),
            (1, "cov", [0.01065760, 0.01849074], False),
            # (1, "nr_disc", 1, False),
            (1, "eigenvalues", [0.12702470, 0.15885051], False),
            # (1, "g_mean", [0, 0], False),
            (1, "h_mean", [0, 0], False),
            (1, "iq_range", [0.33333333, 0.47756693], False),
            # (1, "kurtosis", [np.nan, np.nan], False),
            (1, "mad", [0, 0], False),
            # (1, "max", [0.97435897, 0.16012815], False),
            # (1, "mean", [0.70575399, 0.28775599], False),
            # (1, "median", [0.79487179, 0.40907387], False),
            (1, "min", [0, 0], False),
            # (1, "nr_cor_attr", np.nan, False),
            (1, "nr_norm", 0, False),
            (1, "nr_outliers", 25, False),
            # (1, "range", [0.97435897, 0.16012815], False),
            (1, "sd", [0.32349560, 0.15153916], False),
            # (1, "sd_ratio", np.nan, False),
            # (1, "skewness", [np.nan, np.nan], False),
            (1, "sparsity", [0.49521243, 0.02778647], False),
            # (1, "t_mean", [0.74908425, 0.35654219], False),
            (1, "var", [0.12702470, 0.08652912], False),
            # (1, "w_lambda", np.nan, False),
            ###################
            # Numerical data
            ###################
            (2, "can_cor", [0.72548576, 0.36680730], True),
            (2, "gravity", 3.20517457, True),
            (2, "cor", [0.58981572, 0.34191469], True),
            (2, "cov", [0.59432267, 0.56030719], True),
            (2, "nr_disc", 2, True),
            (2, "eigenvalues", [1.14232282, 2.05710822], True),
            (2, "g_mean", [3.22172156, 2.02456808], True),
            (2, "h_mean", [2.97629003, 2.14893747], True),
            (2, "iq_range", [1.70000000, 1.27540843], True),
            (2, "kurtosis", [-0.79537400, 0.75835782], True),
            (2, "mad", [1.07488500, 0.60678020], True),
            (2, "max", [5.42500000, 2.44318781], True),
            (2, "mean", [3.46366667, 1.91901800], True),
            (2, "median", [3.61250000, 1.91936404], True),
            (2, "min", [1.85000000, 1.80831413], True),
            (2, "nr_cor_attr", 0.5, True),
            (2, "nr_norm", 1, True),
            (2, "nr_outliers", 1, True),
            (2, "range", [3.57500000, 1.65000000], True),
            (2, "sd", [0.94731040, 0.57146108], True),
            (2, "sd_ratio", 1.27345134, True),
            (2, "skewness", [0.06603418, 0.29886394], True),
            (2, "sparsity", [0.02871478, 0.01103236], True),
            (2, "t_mean", [3.46972222, 1.90505400], True),
            (2, "var", [1.14232282, 1.33129110], True),
            (2, "w_lambda", 0.02352545, True),
            (2, "can_cor", [0.72548576, 0.36680730], False),
            (2, "gravity", 3.20517457, False),
            (2, "cor", [0.58981572, 0.34191469], False),
            (2, "cov", [0.59432267, 0.56030719], False),
            (2, "nr_disc", 2, False),
            (2, "eigenvalues", [1.14232282, 2.05710822], False),
            (2, "g_mean", [3.22172156, 2.02456808], False),
            (2, "h_mean", [2.97629003, 2.14893747], False),
            (2, "iq_range", [1.70000000, 1.27540843], False),
            (2, "kurtosis", [-0.79537400, 0.75835782], False),
            (2, "mad", [1.07488500, 0.60678020], False),
            (2, "max", [5.42500000, 2.44318781], False),
            (2, "mean", [3.46366667, 1.91901800], False),
            (2, "median", [3.61250000, 1.91936404], False),
            (2, "min", [1.85000000, 1.80831413], False),
            (2, "nr_cor_attr", 0.5, False),
            (2, "nr_norm", 1, False),
            (2, "nr_outliers", 1, False),
            (2, "range", [3.57500000, 1.65000000], False),
            (2, "sd", [0.94731040, 0.57146108], False),
            (2, "sd_ratio", 1.27345134, False),
            (2, "skewness", [0.06603418, 0.29886394], False),
            (2, "sparsity", [0.02871478, 0.01103236], False),
            (2, "t_mean", [3.46972222, 1.90505400], False),
            (2, "var", [1.14232282, 1.33129110], False),
            (2, "w_lambda", 0.02352545, False),
        ])
    def test_ft_methods_general(self, dt_id, ft_name, exp_value, precompute):
        """Function to test each meta-feature belongs to statistical group.
        """
        precomp_group = "statistical" if precompute else None
        X, y = load_xy(dt_id)
        mfe = MFE(
            groups=["statistical"], features=[ft_name]).fit(
                X.values, y.values, precomp_groups=precomp_group)
        value = mfe.extract()[1]

        if exp_value is np.nan:
            assert value[0] is exp_value

        else:
            assert np.allclose(value, exp_value, atol=0.001,
                               rtol=0.05, equal_nan=True)

    @pytest.mark.parametrize(
        "dt_id, exp_value, precompute, test, failure",
        [
            (0, 0, False, "shapiro-wilk", "soft"),
            (1, 0, False, "shapiro-wilk", "soft"),
            (2, 1, False, "shapiro-wilk", "soft"),
            (0, 0, True, "shapiro-wilk", "soft"),
            (1, 0, True, "shapiro-wilk", "soft"),
            (2, 1, True, "shapiro-wilk", "soft"),
            (0, 0, False, "dagostino-pearson", "soft"),
            (1, 0, False, "dagostino-pearson", "soft"),
            (2, 2, False, "dagostino-pearson", "soft"),
            (0, 0, True, "dagostino-pearson", "soft"),
            (1, 0, True, "dagostino-pearson", "soft"),
            (2, 2, True, "dagostino-pearson", "soft"),
            (0, 0, False, "anderson-darling", "soft"),
            (1, 0, False, "anderson-darling", "soft"),
            (2, 2, False, "anderson-darling", "soft"),
            (0, 0, True, "anderson-darling", "soft"),
            (1, 0, True, "anderson-darling", "soft"),
            (2, 2, True, "anderson-darling", "soft"),
            (0, 0, False, "all", "soft"),
            (1, 0, False, "all", "soft"),
            (2, 2, False, "all", "soft"),
            (0, 0, True, "all", "soft"),
            (1, 0, True, "all", "soft"),
            (2, 2, True, "all", "soft"),
            (0, 0, False, "all", "hard"),
            (1, 0, False, "all", "hard"),
            (2, 1, False, "all", "hard"),
            (0, 0, True, "all", "hard"),
            (1, 0, True, "all", "hard"),
            (2, 1, True, "all", "hard"),
        ])
    def test_normality_tests(self,
                             dt_id,
                             exp_value,
                             precompute,
                             test,
                             failure):
        """Test normality tests included in ``nr_norm`` statistical method.
        """
        precomp_group = "statistical" if precompute else None
        X, y = load_xy(dt_id)
        mfe = MFE(
            groups=["statistical"], features="nr_norm").fit(
                X.values, y.values, precomp_groups=precomp_group)
        value = mfe.extract(nr_norm={"failure": failure, "method": test})[1]

        if exp_value is np.nan:
            assert value[0] is exp_value

        else:
            assert np.allclose(value, exp_value, atol=0.001,
                               rtol=0.05, equal_nan=True)

    @pytest.mark.parametrize(
        "test, failure",
        [
            ("invalid", "soft"),
            ("anderson-darling", "invalid"),
            ("invalid", "invalid"),
            (None, "soft"),
            ("all", None),
        ])
    def test_error_normality_tests(self, test, failure):
        with pytest.warns(RuntimeWarning):
            X, y = load_xy(0)
            mfe = MFE(groups=["statistical"], features="nr_norm")
            mfe.fit(X.values, y.values, precomp_groups=None)
            mfe.extract(nr_norm={"failure": failure, "method": test})
