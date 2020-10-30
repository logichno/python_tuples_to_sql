import unittest
from python_tuples_to_sql import NamedTuplesToSql
from python_tuples_to_sql import make_sql_create_table_line_types_only
from collections import namedtuple


class TestPythonTuplesToSql(unittest.TestCase):

    def test_aggregations(self):
        T = namedtuple('T', 'i s b')
        agg = NamedTuplesToSql()
        agg.feed(T(42, 'test1', True))
        agg.feed(T(2, 'test2', False))
        agg.feed(T(None, None, None))

        self.assertEqual(agg.rows_count, 3)

        self.assertEqual(agg.accs['i'].max, 42)
        self.assertEqual(agg.accs['i'].t, int)

        self.assertEqual(agg.accs['s'].max, 5)
        self.assertEqual(agg.accs['s'].t, str)

        self.assertEqual(agg.accs['b'].max, None)
        self.assertEqual(agg.accs['b'].t, bool)

    def test_make_sql_create_table_line_int(self):
        T = namedtuple('T', 'i')
        agg = NamedTuplesToSql()

        agg.feed(T(42))
        sql_fragment = make_sql_create_table_line_types_only(agg.accs['i'])
        self.assertEqual(sql_fragment, 'smallint not null')

        agg.feed(T(None))
        sql_fragment = make_sql_create_table_line_types_only(agg.accs['i'])
        self.assertEqual(agg.rows_count, 2)
        self.assertEqual(sql_fragment, 'smallint')

        agg.feed(T(32767))
        sql_fragment = make_sql_create_table_line_types_only(agg.accs['i'])
        self.assertEqual(sql_fragment, 'integer')
        self.assertEqual(agg.accs['i'].max, 32767)

        agg.feed(T(2147483647))
        sql_fragment = make_sql_create_table_line_types_only(agg.accs['i'])
        self.assertEqual(sql_fragment, 'bigint')

    def test_make_sql_create_table_line_bool(self):
        T = namedtuple('T', 'b')
        agg = NamedTuplesToSql()

        agg.feed(T(False))
        sql_fragment = make_sql_create_table_line_types_only(agg.accs['b'])
        self.assertEqual(sql_fragment, 'boolean not null')

        agg.feed(T(None))
        sql_fragment = make_sql_create_table_line_types_only(agg.accs['b'])
        self.assertEqual(agg.rows_count, 2)
        self.assertEqual(sql_fragment, 'boolean')

    def test_make_sql_create_table_line_array(self):
        T = namedtuple('T', 'arr')
        agg = NamedTuplesToSql()
        agg.feed(T([{'a': 'b'}]))
        sql_fragment = make_sql_create_table_line_types_only(agg.accs['arr'])
        self.assertEqual(sql_fragment, 'jsonb not null')

        agg.feed(T(None))
        sql_fragment = make_sql_create_table_line_types_only(agg.accs['arr'])
        self.assertEqual(sql_fragment, 'jsonb')


if __name__ == '__main__':
    unittest.main()
