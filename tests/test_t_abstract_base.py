import pandas as pd
from tests.abstract.t_roughset import AbstractClasses

class TestRoughSet(AbstractClasses.TBase):
    """
    Test basic methods of abstract classes

    """

    def setUp(self):
        pass

    def test_assert_check_eqality_of_2_dataframe_indices(self):
        index1_1 = pd.Index([0, 1, 2], dtype='int64')
        index1_2 = pd.Index([0, 2, 1], dtype='int64')
        
        index2_1 = pd.Index([0, 2, 1], name="index2", dtype='int64')
        index2_2 = pd.Index([0, 2, 1], name="index3", dtype='int64')

        # Check default values works
        # 1. An order of index should not matters
        self.assert_check_eqality_of_2_dataframe_indices(
            index1_1, index1_2
        )
        # 2. Names of index should not matter
        self.assert_check_eqality_of_2_dataframe_indices(
            index2_1, index2_2
        )
