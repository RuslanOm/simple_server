from sqlalchemy import (
    Table, Integer, VARCHAR, Text, MetaData, Column
)

meta = MetaData()

users = Table(
    'users', meta,
    Column('id', Integer, primary_key=True),
    Column('user_login', VARCHAR,),
    Column('pass', VARCHAR,),
    Column('comment', Text,)
)
