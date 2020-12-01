from optimus.engines.base.dataframe.extension import Ext as PandasExtension
from optimus.helpers.columns import parse_columns


class PandasDataFrame(PandasExtension):
    def __init__(self, data):
        super().__init__(self, data)

    @property
    def rows(self):
        from optimus.engines.pandas.rows import Rows
        return Rows(self)

    @property
    def cols(self):
        from optimus.engines.pandas.columns import Cols
        return Cols(self)

    @property
    def functions(self):
        from optimus.engines.pandas.functions import PandasFunctions
        return PandasFunctions(self)

    @property
    def constants(self):
        from optimus.engines.pandas.constants import constants
        return constants(self)

    def set_buffer(self, columns="*", n=None):
        return True

    def buffer_window(self, columns=None, lower_bound=None, upper_bound=None, n=None):

        if lower_bound is None:
            lower_bound = 0

        if lower_bound < 0:
            lower_bound = 0

        df_length = self.rows.count()

        if upper_bound is None:
            upper_bound = df_length

        input_columns = parse_columns(self, columns)

        if lower_bound == 0 and upper_bound == df_length:
            return self[input_columns]

        if upper_bound > df_length:
            upper_bound = df_length

        if lower_bound >= df_length:
            diff = upper_bound - lower_bound
            lower_bound = df_length - diff
            upper_bound = df_length

        return PandasDataFrame(self.data[input_columns][lower_bound: upper_bound])