# -*- coding: utf-8 -*-
from django.db import models


class BigAutoField(models.AutoField):
    def db_type(self, connection):
        if connection.vendor == 'mysql':
            return "bigint AUTO_INCREMENT"
        elif connection.vendor == 'oracle':
            return "NUMBER(19)"
        elif connection.vendor == 'postgresql':
            return "bigserial"
        elif connection.vendor == 'sqlite':
            return "integer"
        else:
            raise NotImplementedError('The %s vendor does not supported.' % connection.vendor)
        return super(BigAutoField, self).db_type(connection)