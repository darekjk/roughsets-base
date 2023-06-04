import os
import pathlib
import unittest
from hypothesis import example, given, strategies as st

import pytest
from pandas.core.indexes.frozen import FrozenList

from roughsets_base.roughset_dt import RoughSetDT
import pandas as pd
from pandas import DataFrame, Series
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.testing.assert_frame_equal.html
from pandas.testing import assert_frame_equal, assert_series_equal, assert_index_equal, assert_extension_array_equal


class AbstractClasses:
    """
    Abstract classes for tests

    """

    class TBase(unittest.TestCase):
        def get_test_dataset_path(self, filename):
            path = pathlib.Path(__file__).parent.absolute()
            df = os.path.join(path, "../datasets", str(self.test_dataset_num), filename)
            return df

        def get_test_dataframe(self, filename):
            filepath = self.get_test_dataset_path(filename)
            df: DataFrame = pd.read_csv(filepath, sep=",")

            return df

        def get_test_data_series(self, filename):
            filepath = self.get_test_dataset_path(filename)
            data: Series = pd.read_csv(filepath).squeeze()

            return data

        def read_test_X_y_dataset(self):
            self.X: DataFrame = self.get_test_dataframe("X.csv")
            self.y: Series = self.get_test_data_series("y.csv")

        def read_approximations_test_indices(self):
            subsets: list = []

            dfa_indices: DataFrame = self.get_test_dataframe("approx_indices.csv")
            dfa_subsets: DataFrame = self.get_test_dataframe("approx_subsets.csv")

            subsets_id = dfa_subsets["subset_id"]

            def get_region_indices(df: DataFrame, region: int):
                str_indices = df.iloc[region, 2]
                if pd.isna(str_indices):
                    return pd.Index([], dtype='int64')

                indices_list = str_indices.split(" ")
                indices_list = [int(x) for x in indices_list]
                result = pd.Index(indices_list, dtype='int64')

                return result

            def get_subset_column_names(df: DataFrame, subset_id: int):
                str_column_names = df.iloc[subset_id, 1]
                if pd.isna(str_column_names):
                    return None

                result = str_column_names.split(" ")

                return result

            def get_subset_concepts(df: DataFrame, subset_id: int):
                str_concepts = df.iloc[subset_id, 2]
                if pd.isna(str_concepts):
                    return None

                result = str_concepts.split(" ")

                return result

            for subset_id in subsets_id:
                dfa = dfa_indices[dfa_indices["subset_id"] == subset_id].reset_index(drop=True)

                positive = get_region_indices(dfa, 0)
                boundary = get_region_indices(dfa, 1)
                upper_approx = get_region_indices(dfa, 2)
                negative = get_region_indices(dfa, 3)

                subset_column_names = get_subset_column_names(dfa_subsets, subset_id)
                subset_concepts = get_subset_concepts(dfa_subsets, subset_id)

                subset = {
                    "subset_id": subset_id,
                    "subset_column_names": subset_column_names,
                    'subset_concepts': subset_concepts,

                    "positive": positive,
                    "boundary": boundary,
                    "upper_approximation": upper_approx,
                    "negative": negative
                }

                subsets.append(subset)

            return subsets

        def setUpDataSet(self, test_dataset_num):
            self.test_dataset_num = test_dataset_num
            self.read_test_X_y_dataset()

            self.rough_set: RoughSetDT = RoughSetDT(
                X=self.X, y=self.y,
                ind_index_name="IND"
            )

        def assert_check_eqality_of_2_dataframes(self, X1: DataFrame, X2: DataFrame):

            diff = False
            try:
                if not X1.empty and X2.empty:
                    assert X1.shape == X2.shape
                    diff = assert_frame_equal(X1, X2)
            except Exception as err:
                diff = True

            assert diff in [None, False], "Data frames are not equal."

        def assert_check_eqality_of_2_data_series(self, x1: Series, x2: Series):

            try:
                diff = False
                if not x1.empty and x2.empty:
                    diff = assert_series_equal(x1, x2)
            except Exception as err:
                diff = True

            assert diff in [None, False], "Data series are not equal."

        def assert_check_eqality_of_2_dataframe_indices(
                self,
                index1, index2,
                check_names=False, check_order=False
        ):
            try:
                diff = False

                if not (index1.empty and index2.empty):
                    assert_index_equal(
                        index1, index2,
                        check_names=check_names, check_order=check_order
                    )

            except Exception as err:
                diff = True

            assert diff in [None, False], "Indices are not equal."

    class TRoughSet(TBase):
        """Generic Test"""

        def tearDown(self) -> None:
            raise Exception("Inherit Test and add SetUp method")

        def test_X_has_not_index_column(self):
            """"""
            assert "index" not in self.X.columns

        def test_get_indiscernibility_relation(self):
            ind_of_x = self.rough_set.get_indiscernibility_relations(
                subset=None,
                return_indiscernibility_index=False
            )
            true_ind_of_x = self.get_test_dataframe("IND_OF_X.csv")

            self.assert_check_eqality_of_2_dataframes(ind_of_x, true_ind_of_x)

        def test_get_Xy_with_indiscrenibility_relations_index(self):
            x_ind, y_ind, ind_of_x_ext = self.rough_set.get_Xy_with_indiscernibility_relations_index(
                subset=None
            )
            true_x_ind = self.get_test_dataframe("X_IND.csv")
            true_y_ind = self.get_test_dataframe("y_IND.csv")
            true_ind_of_x_ext = self.get_test_dataframe("IND_OF_X_EXT.csv")

            self.assert_check_eqality_of_2_dataframes(x_ind, true_x_ind)
            self.assert_check_eqality_of_2_dataframes(y_ind, true_y_ind)
            self.assert_check_eqality_of_2_dataframes(ind_of_x_ext, true_ind_of_x_ext)

        def test_get_approximation_indices(self):
            subsets = self.read_approximations_test_indices()

            for subset in subsets:
                subset_id = subset["subset_id"]
                subset_column_names = subset["subset_column_names"]
                subset_concepts = subset["subset_concepts"]

                true_positive_region_of_X = subset["positive"]
                true_boundary_region_of_X = subset["boundary"]
                true_upper_approximation_of_X = subset["upper_approximation"]
                true_negative_region_of_X = subset["negative"]

                positive_region_of_X, boundary_region_of_X, upper_approximation_of_X, negative_region_of_X = \
                    self.rough_set.get_approximation_indices(
                        subset=subset_column_names,  # if None  get all
                        concepts=subset_concepts  # if None  get all
                    )

                self.assert_check_eqality_of_2_dataframe_indices(positive_region_of_X, true_positive_region_of_X)
                self.assert_check_eqality_of_2_dataframe_indices(boundary_region_of_X, true_boundary_region_of_X)
                self.assert_check_eqality_of_2_dataframe_indices(upper_approximation_of_X,
                                                                 true_upper_approximation_of_X)
                self.assert_check_eqality_of_2_dataframe_indices(negative_region_of_X, true_negative_region_of_X)

        def test_get_approximation(self):
            subsets = self.read_approximations_test_indices()

            for subset in subsets:
                subset_id = subset["subset_id"]
                subset_column_names = subset["subset_column_names"]
                subset_concepts = subset["subset_concepts"]

                true_positive_region_of_X = subset["positive"]
                true_boundary_region_of_X = subset["boundary"]
                true_upper_approximation_of_X = subset["upper_approximation"]
                true_negative_region_of_X = subset["negative"]

                positive_region_of_X, boundary_region_of_X, upper_approximation_of_X, negative_region_of_X = \
                    self.rough_set.get_approximation_indices(
                        subset=subset_column_names,  # if None  get all
                        concepts=subset_concepts  # if None  get all
                    )

                positive = self.rough_set.get_approximation_objects(positive_region_of_X)
                boundary = self.rough_set.get_approximation_objects(boundary_region_of_X)
                upper_approximation = self.rough_set.get_approximation_objects(upper_approximation_of_X)
                negative = self.rough_set.get_approximation_objects(negative_region_of_X)

                true_positive = self.rough_set.get_approximation_objects(true_positive_region_of_X)
                true_boundary = self.rough_set.get_approximation_objects(true_boundary_region_of_X)
                true_upper_approximation = self.rough_set.get_approximation_objects(true_upper_approximation_of_X)
                true_negative = self.rough_set.get_approximation_objects(true_negative_region_of_X)

                X, y = positive
                true_X, true_y = true_positive
                self.assert_check_eqality_of_2_dataframes(X, true_X)
                self.assert_check_eqality_of_2_data_series(y, true_y)

                X, y = boundary
                true_X, true_y = true_boundary
                self.assert_check_eqality_of_2_dataframes(X, true_X)
                self.assert_check_eqality_of_2_data_series(y, true_y)

                X, y = upper_approximation
                true_X, true_y = true_upper_approximation
                self.assert_check_eqality_of_2_dataframes(X, true_X)
                self.assert_check_eqality_of_2_data_series(y, true_y)

                X, y = negative
                true_X, true_y = true_negative
                self.assert_check_eqality_of_2_dataframes(X, true_X)
                self.assert_check_eqality_of_2_data_series(y, true_y)
