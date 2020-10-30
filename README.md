## Install

```pip install git+https://github.com/logichno/python_tuples_to_sql.git#egg=python_tuples_to_sql```

## Usage

```
from collections import namedtuple
from python_tuples_to_sql import NamedTuplesToSql

T = namedtuple('T', 'id column1 column2 column3 column4')
agg = NamedTuplesToSql()
agg.feed(T(42,         1,    'test1', True,  {'dict_field': 42}))
agg.feed(T(2147483647, 2,    'test2', False, {'dict_field': 13}))
agg.feed(T(1,          None, 'test3', False, None))
print(agg.sql_create_table('tablename'))

------------------------
CREATE TABLE tablename (
id bigint not null,
column1 smallint,
column2 varchar (5) not null,
column3 boolean not null,
column4 jsonb
);
```
