import copy
import logging

import pandas as pd
from pandas import DataFrame, Series


class RoughSetSI:
    """Class RoughSet to model an Information System SI = (X, A).

    DT = f(X, A, y),

    where:
    X - objects of universe,
    A - attributes describing objects of X,

    """

    def __init__(self, X: DataFrame, ind_index_name="IND_INDEX"):
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

        self.ind_rel_column_index_name = "index"

        # cache variables
        self.__indiscrenibility_relation: DataFrame = None  # distinct rows of X with ID of IND
        self.__R: DataFrame = None  # R -> X; A row of R has ID from __ind_rel which connect row from X to IND

        self.logger_name = __name__
        self.logger = logging.getLogger(self.logger_name)

        if not isinstance(X, DataFrame):
            raise Exception("X must be a type of Pandas DataFrame. See more: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html")

        self.X = X

        if self.ind_rel_column_index_name in self.X.columns:
            raise ValueError(f"You can not use {self.ind_rel_column_index_name} as a column name.")

        self.ind_index_name = ind_index_name  # nazwa kolumny pomocniczej dla relacji nieodróżnialności

    def get_deepcopy(self):
        """Get deepcopy of the object

        reference: https://docs.python.org/3/library/copy.html
        """
        return copy.deepcopy(self)

    def get_X(self) -> DataFrame:
        """
        Get X and y as one DataFrame
        """
        return self.X

    @property
    def __column_names_X(self) -> list:
        return self.X.columns.values.tolist()

    def __get_empty_X(self, columns=None) -> DataFrame:
        """Get empty X"""
        if columns is None:
            columns = self.__column_names_X
        return DataFrame(columns=columns)

    @property
    def __rows_count(self):
        """Get rows count of X"""

        return len(self.X.index)

    @property
    def is_empty(self):
        """
        Check if y is empty (so X also must be empty)

        """
        result = True if self.__rows_count == 0 else False
        return result

    def get_indiscernibility_relations(self, subset=None, return_indiscernibility_index: bool = True):
        """
        Compute indiscernibility relations for X DataFrame

        According to RoughSet Theory, it is a set of data supposed to be similar with respect to this relation.


        Parameters
        ----------
        subset: column label or sequence of labels, optional
            Only consider certain columns for identifying duplicates,
            by default use all of the columns.

        return_indiscernibility_index: bool, default: True
            Whether to return additional column with index of indiscernibility relations

        Returns
        -------
        DataFrame or None
            DataFrame with indiscernibility relations or None.

        """

        if subset in [None, []] or (len(subset) == len(self.X.columns) and subset == self.X.columns):
            subset = None
            df = self.X
        else:
            df = self.X[subset]

        IND_OF_X = df.drop_duplicates().reset_index(drop=True).reset_index()
        IND_OF_X.rename(columns={self.ind_rel_column_index_name: self.ind_index_name}, inplace=True)

        if not return_indiscernibility_index:
            ind = IND_OF_X[IND_OF_X.columns.drop(self.ind_index_name)]
        else:
            ind = IND_OF_X

        return ind

    def get_X_with_indiscernibility_relations_index(self, subset=None):

        if subset in [None, []] or (len(subset) == len(self.X.columns) and subset == self.X.columns):
            subset = None

        IND_OF_X = self.get_indiscernibility_relations(subset=subset)

        # Add column <self.ind_rel_column_index_name> with an original row number in X
        _on_columns = subset if subset is not None else self.X.columns.values.tolist()
        X_IND = self.X.reset_index(
            drop=False
        ).merge(
            IND_OF_X, how="inner", on=_on_columns
        ).sort_values(
            by=self.ind_rel_column_index_name
        )

        # Set original row number using data from column <self.ind_rel_column_index_name>
        X_IND = X_IND.set_index(self.ind_rel_column_index_name)
        X_IND.index.name = None

        return X_IND, IND_OF_X
