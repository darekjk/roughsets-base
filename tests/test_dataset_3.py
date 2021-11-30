from tests.abstract.t_roughset import AbstractClasses


class TestRoughSet(AbstractClasses.TRoughSet):
    """
        Run tests for dataset: 3

    """

    def setUp(self):
        super().setUpDataSet(3)

    def tearDown(self) -> None:
        # TODO: Destroy shared data
        pass
