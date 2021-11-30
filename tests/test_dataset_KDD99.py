import os
import pandas as pd
from pandas import Int64Index

from tests.abstract.t_roughset import AbstractClasses


class TestRoughSet(AbstractClasses.TBase):
    """
        Run tests for dataset: KDD99


    """

    def setUp(self):
        self.enabled = True  # Dataset contains > 4 mln records
        self.test_dataset_num = "KDD99"

        self.KDD99_FILE_PATH = os.environ.get(
            "ROUGHSETS_KDD99_TEST_DATA_FOLDER",
            "http://kdd.ics.uci.edu/databases/kddcup99/corrected.gz")

        # Don't use setUpDataSet() from Parent class
        # super().setUpDataSet()
        self.setUpDataSet()

    def setUpDataSet(self):
        if not self.enabled:
            return "Test not enabled, so skip loading data"

        # import roughsets_pandas as rst
        from roughsets_base.roughset_dt import RoughSetDT

        columns = ["duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", "land", "wrong_fragment",
                   "urgent", "hot", "num_failed_logins", "logged_in", "num_compromised", "root_shell", "su_attempted",
                   "num_root", "num_file_creations", "num_shells", "num_access_files", "num_outbound_cmds",
                   "is_hot_login", "is_guest_login", "count", "srv_count", "serror_rate", "srv_serror_rate",
                   "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate", "srv_diff_host_rate",
                   "dst_host_count", "dst_host_srv_count", "dst_host_same_srv_rate", "dst_host_diff_srv_rate",
                   "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate", "dst_host_serror_rate",
                   "dst_host_srv_serror_rate", "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "target"]

        df = pd.read_csv(self.KDD99_FILE_PATH, header=None)

        # %timeit -r1 -n1 df = pd.read_csv(self.KDD99_FILE_PATH, header=None)
        # 54.3 s ± 0 ns per loop (mean ± std. dev. of 1 run, 1 loop each)

        self.X = df.iloc[:, 0:41]
        self.y = df.iloc[:, 41]

        self.rough_set: RoughSetDT = RoughSetDT(self.X, self.y)

    def tearDown(self) -> None:
        # TODO: Destroy shared data
        pass

    def test_kdd_A(self):
        if not self.enabled:
            return "Test not enabled"

        filename = self.get_test_dataset_path("kdd_positive_region_A.zip")
        true_positive_region_of_X = pd.read_csv(filename, compression='zip', header=0, squeeze=True)
        true_positive_region_of_X: Int64Index = Int64Index(true_positive_region_of_X)

        filename = self.get_test_dataset_path("kdd_boundary_region_A.csv")
        true_boundary_region_of_X = pd.read_csv(filename, header=0, squeeze=True)
        true_boundary_region_of_X = Int64Index(true_boundary_region_of_X)

        filename = self.get_test_dataset_path("kdd_negative_region_A.csv")
        true_negative_region_of_X = pd.read_csv(filename, header=0, squeeze=True)
        true_negative_region_of_X = Int64Index(true_negative_region_of_X)

        self.rough_set.get_indiscernibility_relations()

        positive_region_of_X, boundary_region_of_X, upper_approximation_of_X, negative_region_of_X = \
            self.rough_set.get_approximation_indices()

        # %timeit -r1 -n1 positive_region_of_X, boundary_region_of_X, upper_approximation_of_X, negative_region_of_X = RST.get_approximation_indices()
        # 1min 3s ± 0 ns per loop (mean ± std. dev. of 1 run, 1 loop each)

        self.assert_check_eqality_of_2_dataframe_indices(positive_region_of_X, true_positive_region_of_X)
        self.assert_check_eqality_of_2_dataframe_indices(boundary_region_of_X, true_boundary_region_of_X)
        self.assert_check_eqality_of_2_dataframe_indices(negative_region_of_X, true_negative_region_of_X)

    def test_kdd_B(self):
        if not self.enabled:
            return "Test not enabled"

        # subset = ["duration", "protocol_type"]
        subset = [0, 1]

        filename = self.get_test_dataset_path("kdd_positive_region_B.zip")
        true_positive_region_of_X = pd.read_csv(filename, compression='zip', header=0, squeeze=True)
        true_positive_region_of_X: Int64Index = Int64Index(true_positive_region_of_X)

        filename = self.get_test_dataset_path("kdd_boundary_region_B.zip")
        true_boundary_region_of_X = pd.read_csv(filename, header=0, squeeze=True)
        true_boundary_region_of_X = Int64Index(true_boundary_region_of_X)

        filename = self.get_test_dataset_path("kdd_negative_region_B.csv")
        true_negative_region_of_X = pd.read_csv(filename, header=0, squeeze=True)
        true_negative_region_of_X = Int64Index(true_negative_region_of_X)

        # self.rough_set.get_indiscernibility_relations(
        #     subset=subset
        # )

        # X_IND, y_IND, IND_OF_X_EXT = self.rough_set.get_Xy_with_indiscernibility_relations_index(subset=subset)

        positive_region_of_X, boundary_region_of_X, upper_approximation_of_X, negative_region_of_X = \
            self.rough_set.get_approximation_indices(subset=subset)

        self.assert_check_eqality_of_2_dataframe_indices(positive_region_of_X, true_positive_region_of_X)
        self.assert_check_eqality_of_2_dataframe_indices(boundary_region_of_X, true_boundary_region_of_X)
        self.assert_check_eqality_of_2_dataframe_indices(negative_region_of_X, true_negative_region_of_X)
