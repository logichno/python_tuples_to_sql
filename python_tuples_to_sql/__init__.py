__version__ = '0.0.1'

from collections import namedtuple

Acc = namedtuple('Acc', 't max has_nulls')


class NamedTuplesToSql:
    accs = None
    rows_count = 0

    def feed(self, ntuple):
        if self.accs is None:
            self.accs = dict(
                [(k, Acc(t=None, max=None, has_nulls=False)) for (k, v) in
                 ntuple._asdict().items()])
        self._accumulate_row(ntuple)
        self.rows_count += 1

    def sql_create_table(self, table_name: str):
        lines = [make_sql_create_table_line(field, acc) for (field, acc) in
                 self.accs.items()]
        before = f'CREATE TABLE {table_name} (\n'
        after = '\n);'
        return before + ',\n'.join(lines) + after

    @staticmethod
    def _accumulate(value, acc: Acc):
        if value is None:
            return acc._replace(has_nulls=True)
        t = type(value)
        if acc.t is None and value is None:
            return acc
        elif acc.t is not None and value is not None and acc.t != t:
            raise ValueError(f'value: {value}, acc: {acc}')
        maximum = acc.max
        has_nulls = acc.has_nulls
        if value is None:
            has_nulls = True
        else:
            if isinstance(value, bool):
                pass
            elif isinstance(value, int):
                maximum = max(value, maximum or value)
            elif isinstance(value, str):
                maximum = max(len(value), maximum or len(value))

        return Acc(t, maximum, has_nulls)

    def _accumulate_row(self, ntuple):
        for (k, v) in ntuple._asdict().items():
            self.accs[k] = self._accumulate(v, self.accs[k])


def make_sql_create_table_line_types_only(acc):
    t = '???'
    if type_eq(acc.t, bool):
        t = 'boolean'
    elif type_eq(acc.t, int):
        if acc.max is None:
            pass
        elif acc.max < 32767:
            t = 'smallint'
        elif acc.max < 2147483647:
            t = 'integer'
        else:
            t = 'bigint'
    elif type_eq(acc.t, dict):
        t = 'jsonb'
    elif type_eq(acc.t, str):
        t = f'varchar ({acc.max})'
    nn = '' if acc.has_nulls else ' not null'
    return f'{t}{nn}'


def make_sql_create_table_line(field, acc):
    return f'{field} {make_sql_create_table_line_types_only(acc)}'


def type_eq(t, expected):
    return t is not None and t == expected
