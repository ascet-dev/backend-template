from adc_aiopg.repository import PostgresAccessLayer

import models as m


class DAO(PostgresAccessLayer, metadata=m.base.meta):
    pass
