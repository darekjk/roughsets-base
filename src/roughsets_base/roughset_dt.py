import copy
import logging

import pandas as pd
from pandas import DataFrame, Series, Int64Index

from roughsets_base.roughset_si import RoughSetSI


class RoughSetDT(RoughSetSI):
    """Class RoughSet to model a decision table (DT).

    DT = f(X, A, y),

    where:
    X - objects of universe,
    A - attributes describing objects of X,
    y - a decision attribute related to X.

    """

    def __init__(self, X: DataFrame, y: Series = None, ind_index_name="IND_INDEX"):
        """Initialize object of class RoughSet

        Parameters
        ----------

        X: DataFrame
            Objects of universe of type: pandas DataFrame
        y: Series
            Decision set related to X or None if used simple SI
        ind_index_name: string, default 'IND_INDEX'
            Name of a special column to store index of discernibilty relation,
            computed by the function: get_indiscernibility_relations function.

        Note: X and y are computed as data structures with nominal values.

        References
        ----------
        pandas array: https://pandas.pydata.org/docs/reference/arrays.html
        """

        super().__init__(X, ind_index_name)

        self.default_class_attr = "target"

        if isinstance(y, list):
            y = pd.Series(y, name=self.default_class_attr)

        self.__assert_X_y(X, y)
        self.y = y

        if self.ind_rel_column_index_name in self.X.columns:
            raise ValueError(f"You can not use {self.ind_rel_column_index_name} as a column name.")

        self.ind_index_name = ind_index_name  # nazwa kolumny pomocniczej dla relacji nieodróżnialności

    def __assert_X_y(self, X, y):
        if not isinstance(y, Series):
            raise Exception("y must be a type of list or Pandas Series. See more: https://pandas.pydata.org/docs/reference/api/pandas.Series.html")

        if not isinstance(X, DataFrame):
            raise Exception("X must be a type of Pandas DataFrame. See more: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html")

        if not len(X.index) == len(y.index):
            raise Exception("Number of objects in X does not match number of decisions in y.")

    def concat_X_and_y(self, X, y) -> DataFrame:
        """Add y series as a column to X DataFrame"""
        Xy = pd.concat([X, y], axis=1)
        return Xy

    def get_Xy(self) -> DataFrame:
        """
        Get X and y as one DataFrame
        """
        return self.concat_X_and_y(self.X, self.y)

    @property
    def __column_name_y(self) -> str:
        return self.y.name

    def __get_empty_X(self, columns=None) -> DataFrame:
        """Get empty X"""
        if columns is None:
            columns = self.__column_names_X
        return DataFrame(columns=columns)

    def __get_empty_y(self) -> Series:
        """Get empty y"""

        column = self.__column_name_y
        return Series(data=[], name=column)

    def get_all_concepts(self):
        return self.y.drop_duplicates().reset_index(drop=True)

    def get_Xy_with_indiscernibility_relations_index(self, subset=None):

        X_IND, IND_OF_X = self.get_X_with_indiscernibility_relations_index(subset)

        # Add column with an IDrelation: X_IND -> y
        y_IND = pd.DataFrame(self.y.copy())
        y_IND[self.ind_index_name] = X_IND[self.ind_index_name]

        # Zliczenie ilości klas dla każdej relacji nieodróżnialności
        # i dodanie do IND_OF_X
        # Count classes for each indiscernibility_relation
        y_class_count = y_IND.drop_duplicates().groupby(
            [self.ind_index_name]
        )[self.y.name].count().reset_index(
            name="count"
        )["count"]

        # Add number of classes to each indiscernibility_relation
        IND_OF_X["y_class_count"] = y_class_count

        return X_IND, y_IND, IND_OF_X

    def get_approximation_indices(self, concepts=None, subset=None):
        """
        Get Pandas DataFrame indices which describe approximations boundaries.

        Parameters
        ----------

        concepts: list of decisions for which approximations boundaries must be evaluated.
            If None, computation will be done for all decisions.

        subset: column label or sequence of labels, optional
            Only consider certain columns for identifying duplicates,
            by default use all of the columns.

        Returns
        -------
        Tuple: positive_region_of_X, boundary_region_of_X, upper_approximation_of_X, negative_region_of_X


        """

        if concepts is None or concepts == [] or concepts == pd.Series.empty:
            concepts = self.get_all_concepts()

        if not isinstance(concepts, Series):
            concepts = pd.Series(concepts)

        # IND_OF_X_EXT - indiscernibilty relations (extended with columns: y_class_count and <self.ind_index_name>)
        X_IND, y_IND, IND_OF_X_EXT = self.get_Xy_with_indiscernibility_relations_index(
            subset=subset
        )

        # Get indexes of indiscernibilty relations, related to concepts
        IND_concept = y_IND[
            y_IND[self.y.name].isin(concepts)
        ][self.ind_index_name].drop_duplicates()

        # Get indexes of IND_OF_X_EXT which belong to concept
        IND_OF_X_by_concept = IND_OF_X_EXT[IND_OF_X_EXT[self.ind_index_name].isin(IND_concept)]

        # Get a lower approximation (if only one concept) or sum of lower approximations (if more than one concept)
        # (DataFrame's indexes of dataset X)
        ind_index_of_lower_approximation: Series = IND_OF_X_by_concept[
            IND_OF_X_by_concept["y_class_count"] == 1
        ][self.ind_index_name]
        lower_approximation_of_X: Int64Index = X_IND[
            X_IND[self.ind_index_name].isin(ind_index_of_lower_approximation)
        ].index

        # Get a boundary region (DataFrame's indexes of dataset X)
        ind_index_of_boundary_region: Series = IND_OF_X_by_concept[
            IND_OF_X_by_concept["y_class_count"] > 1
        ][self.ind_index_name]
        boundary_region_of_X: Int64Index = X_IND[
            X_IND[self.ind_index_name].isin(ind_index_of_boundary_region)
        ].index

        # Get a upper approximation (if only one concept) or sum of upper approximations (if more than one concept)
        # (DataFrame's indexes of dataset X)
        upper_approximation_of_X: Int64Index = lower_approximation_of_X.append(boundary_region_of_X).sort_values()

        # Get a negative region (DataFrame's indexes of dataset X)
        negative_region_of_X = self.X.index.delete(upper_approximation_of_X).sort_values()

        # Get a negative region (DataFrame's indexes of dataset X) (method 2)
        # IND_OF_X_negative_by_concept = IND_OF_X_EXT[
        #     ~IND_OF_X_EXT[self.ind_index_name].isin(IND_concept)
        # ]
        # ind_index_of_negative_region: Series = IND_OF_X_negative_by_concept[self.ind_index_name]
        # negative_region_of_X: Int64Index = X_IND[
        #     X_IND[self.ind_index_name].isin(ind_index_of_negative_region)
        # ].index

        return lower_approximation_of_X, boundary_region_of_X, upper_approximation_of_X, negative_region_of_X

    def get_approximation_objects(self, approximation_indices: Int64Index) -> (DataFrame, Series):
        """
        Get subset (defined by approximation_indices) of X and y objects
        """
        selection = self.y.index.isin(approximation_indices)
        return self.X[selection], self.y[selection]
