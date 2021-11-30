from tests.abstract.t_roughset import AbstractClasses


class TestRoughSet(AbstractClasses.TRoughSet):
    """
        Run tests for dataset: 1

    """

    def setUp(self):
        super().setUpDataSet(1)
        pass

    def tearDown(self) -> None:
        # TODO: Destroy shared data
        pass
