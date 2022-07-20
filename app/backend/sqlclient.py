from api.settings import RDS_USER, RDS_DATABASE, RDS_PASSWORD, RDS_URL, RDS_PORT
from sqlalchemy import create_engine, insert, MetaData, Table, Column, Integer, String
from sqlalchemy_utils import database_exists, create_database


class RDSClient:
    def __init__(self):
        self.flatten = lambda lis: [x for l in lis for x in l]
        self.engine = create_engine(f"mysql+mysqlconnector://"
                            f"{RDS_USER}:{RDS_PASSWORD}"
                            f"@{RDS_URL}:{RDS_PORT}/{RDS_DATABASE}")

        self.tables = {}


    def create_db(self):
        if not database_exists(self.engine.url):
            print(f"Created database {RDS_DATABASE}.")
            create_database(self.engine.url)


    def create_table_generic(self, table_name: str, header: list):

        if not self.engine.has_table(self.engine, table_name):
            meta = MetaData(self.engine)

            if header[-1] == 'cause':
                header.pop()
                columns = [Column(col, Integer) for col in header] + [Column('cause', String(64))]
                print (columns)
                table = Table(table_name, meta, *columns)
            else:
                columns = [Column(col, Integer) for col in header]
                table = Table(table_name, meta, *columns)

            self.tables[table_name] = table

            meta.create_all(self.engine)
            print(f"Created table {table_name}.")


    def insert_dict(self, table_name: str, data_dict: dict):
        ins = self.tables[table_name].insert().values(data_dict)

        with self.engine.connect() as conn:
            result = conn.execute(ins)


