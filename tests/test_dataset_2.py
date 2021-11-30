from tests.abstract.t_roughset import AbstractClasses


class TestRoughSet(AbstractClasses.TRoughSet):
    """
        Run tests for dataset: 2

    """

    def setUp(self):
        super().setUpDataSet(2)
        pass

    def tearDown(self) -> None:
        # TODO: Destroy shared data
        pass

    # def test_get_Xy_with_indiscrenibility_relations_index(self):
    #     super().test_get_Xy_with_indiscrenibility_relations_index()
