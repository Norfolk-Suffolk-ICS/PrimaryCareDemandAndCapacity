from typing import Optional, Dict, Any, Callable
from pydantic import Field, BaseModel

from sklearn.pipeline import Pipeline, FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures, StandardScaler
from sklearn.linear_model import Ridge, LinearRegression
from sklearn import metrics
import scipy.stats as stats

import constants as const

from sklearn import set_config

set_config(transform_output="pandas")


DEFAULT_POLY_DEGREE = 2
DEFAULT_PCA_COMPONENTS = 2


LINEAR_REGRESSION_GRID_SEARCH = {
    "linear_regression__fit_intercept": [True, False],
    "linear_regression__positive": [True, False],
}
POLYNOMIAL_GRID_SEARCH = {
    "polynomial__degree": [2, 3, 4],
    "polynomial__interaction_only": [True, False],
    "polynomial__include_bias": [True, False],
}

PCA_GRID_SEARCH = {
    "preprocess__scale_pca__pca__n_components": [2, 3, 4],
    "preprocess__scale_pca__pca__svd_solver": ["auto", "full", "arpack", "randomized"],
    "preprocess__scale_pca__pca__whiten": [True, False],
    "preprocess__scale_pca__pca__copy": [True, False],
    "preprocess__scale_pca__pca__iterated_power": [None, "auto", "arpack", "randomized"],
    "preprocess__scale_pca__pca__tol": [None, 0.0, 0.1, 0.01],
}

RIDGE_REGRESSION_GRID_SEARCH = {
    "ridge__alpha": stats.uniform(loc=0, scale=1),
    "ridge__fit_intercept": [True, False],
    "ridge__positive": [True, False],
    "ridge__positive": [True, False],
    "ridge__solver": ["auto", "svd", "cholesky", "lsqr", "sparse_cg", "sag", "saga"],
}


REGRESSION_METRICS = [
    metrics.max_error,
    metrics.mean_absolute_error,
    metrics.mean_squared_error,
    metrics.median_absolute_error,
    metrics.r2_score,
]


class ModelConfig(BaseModel):
    name: str
    estimator: Pipeline
    grid_search_params: Dict[str, Any]
    train_metrics: Dict[str, float | int] = Field(default_factory=dict)
    test_metrics: Dict[str, float | int] = Field(default_factory=dict)
    best_params_by_metric: Dict[str, dict] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True


# create all the model configs
MODEL_CONFIGS = [
    ModelConfig(
        name="basic",
        estimator=Pipeline(
            [
                (
                    "preprocess",
                    ColumnTransformer(
                        [("onehot", OneHotEncoder(sparse_output=False), ["month"])],
                        remainder="passthrough",
                    ),
                ),
                ("linear_regression", LinearRegression()),
            ]
        ),
        grid_search_params={**LINEAR_REGRESSION_GRID_SEARCH},
    ),
    ModelConfig(
        name="poly_linear",
        estimator=Pipeline(
            [
                (
                    "preprocess",
                    ColumnTransformer(
                        [("onehot", OneHotEncoder(sparse_output=False), ["month"])],
                        remainder="passthrough",
                    ),
                ),
                ("polynomial", PolynomialFeatures(degree=DEFAULT_POLY_DEGREE)),
                ("linear_regression", LinearRegression()),
            ]
        ),
        grid_search_params={
    **POLYNOMIAL_GRID_SEARCH,
    **LINEAR_REGRESSION_GRID_SEARCH,
},
    ),
    ModelConfig(
        name="poly_ridge",
        estimator=Pipeline(
            [
                (
                    "preprocess",
                    ColumnTransformer(
                        [("onehot", OneHotEncoder(sparse_output=False), ["month"])],
                        remainder="passthrough",
                    ),
                ),
                ("polynomial", PolynomialFeatures(degree=DEFAULT_POLY_DEGREE)),
                ("ridge", Ridge()),
            ]
        ),
        grid_search_params={
    **POLYNOMIAL_GRID_SEARCH,
    **RIDGE_REGRESSION_GRID_SEARCH,
},
    ),
    ModelConfig(
        name="pca_linear",
        estimator=Pipeline(
            steps=[
                (
                    "preprocess",
                    ColumnTransformer(
                        transformers=[
                            ("onehot", OneHotEncoder(sparse_output=False), ["month"]),
                            (
                                "scale_pca",
                                Pipeline(
                                    [
                                        ("scale", StandardScaler()),
                                        ("pca", PCA(n_components=2)),
                                    ]
                                ),
                                const.GP_LIST_AGE_LABELS,
                            ),
                        ],
                        remainder="passthrough",
                    ),
                ),
                ("linear_regression", LinearRegression()),
            ]
        ),
        grid_search_params={**PCA_GRID_SEARCH, **LINEAR_REGRESSION_GRID_SEARCH},
    ),
    ModelConfig(
        name="pca_ridge",
        estimator=Pipeline(
            steps=[
                (
                    "preprocess",
                    ColumnTransformer(
                        transformers=[
                            ("onehot", OneHotEncoder(sparse_output=False), ["month"]),
                            (
                                "scale_pca",
                                Pipeline(
                                    [
                                        ("scale", StandardScaler()),
                                        ("pca", PCA(n_components=2)),
                                    ]
                                ),
                                const.GP_LIST_AGE_LABELS,
                            ),
                        ],
                        remainder="passthrough",
                    ),
                ),
                ("ridge", Ridge()),
            ]
        ),
        grid_search_params={**PCA_GRID_SEARCH, **RIDGE_REGRESSION_GRID_SEARCH},
    ),
]


def baseline_scorer(y_true, y_pred):
    """
    Calculate the scores for a baseline model.

    Parameters:
    - y_true: The true values of the target variable.
    - y_pred: The predicted values of the target variable.

    Returns:
    - metrics_dict: A dictionary containing the scores for each metric in the REGRESSION_METRICS list.
    """
    metrics_dict = {}
    for metric in REGRESSION_METRICS:
        score = metric(y_true, y_pred)
        metrics_dict[metric.__name__] = score
    return metrics_dict


# Custom transformer to allow parameter selection for different PCA methods
class CustomPCA(BaseEstimator, TransformerMixin):
    def __init__(self, method='PCA', n_components=2, kernel='linear'):
        self.method = method
        self.n_components = n_components
        self.kernel = kernel
        self.pca_ = None

    def fit(self, X, y=None):
        if self.method == 'PCA':
            self.pca_ = PCA(n_components=self.n_components)
        elif self.method == 'KernelPCA':
            self.pca_ = KernelPCA(n_components=self.n_components, kernel=self.kernel)
        elif self.method == 'SparsePCA':
            self.pca_ = SparsePCA(n_components=self.n_components)
        self.pca_.fit(X)
        return self

    def transform(self, X):
        return self.pca_.transform(X)

    def get_params(self, deep=True):
        return {'method': self.method, 'n_components': self.n_components, 'kernel': self.kernel}

    def set_params(self, **params):
        for param, value in params.items():
            setattr(self, param, value)
        return self

def find_best_pca_for_forecasting(df, age_columns, target_column, n_components_range=[2, 5, 10], kernel_options=['linear', 'poly', 'rbf']):
    # Prepare the features and target variable
    X = df[age_columns]
    y = df[target_column]
    
    # Define the parameter grid
    param_grid = [
        { 'pca__method': ['PCA'], 'pca__n_components': n_components_range },
        { 'pca__method': ['KernelPCA'], 'pca__n_components': n_components_range, 'pca__kernel': kernel_options },
        { 'pca__method': ['SparsePCA'], 'pca__n_components': n_components_range },
    ]

    # Create a pipeline
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('pca', CustomPCA()),  # Custom PCA wrapper
        ('regressor', LinearRegression())
    ])

    # Perform grid search
    grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='r2')
    grid_search.fit(X, y)
    
    # Get the best estimator
    best_pipeline = grid_search.best_estimator_
    
    # Split the data into training and test sets for evaluation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Fit the best pipeline on the training data
    best_pipeline.fit(X_train, y_train)
    
    # Predict on the test set
    y_pred = best_pipeline.predict(X_test)
    
    # Evaluate the performance
    r2 = r2_score(y_test, y_pred)
    
    print(f'Best PCA Method: {grid_search.best_params_["pca__method"]}')
    print(f'Best PCA n_components: {grid_search.best_params_["pca__n_components"]}')
    if 'pca__kernel' in grid_search.best_params_:
        print(f'Best Kernel: {grid_search.best_params_["pca__kernel"]}')
    print(f'R² Score: {r2}')
    
    return best_pipeline

# best_pca = find_best_pca_for_forecasting(complete_dataset_df, PCA_COLS, TARGET__COL, n_components_range=[2,3,4,5,6])

# Plot
# fig, ax = plt.subplots(figsize=(10, 7.5), subplot_kw={'projection': '3d'})
# x_trans = best_pca.named_steps['pca'].transform(X_train_age_groups)
# ax.scatter(X_train[:, 0], X_train[:, 1], X_train[:, 2], c=y_train)
# plt.show()