#!/usr/bin/env python

import os
from cloudify import ctx
from cloudify.state import ctx_parameters as inputs

try:
    import mysql.connector as mariadb
except ImportError:
    import pip
    pip.main(['install', 'mysql-connector-python-rf'])
    import mysql.connector as mariadb


if __name__ == '__main__':

    db_password = inputs.get('db_password', str())
    mysql_commands = inputs.get('mysql_commands', [])

    db = mariadb.connect(user='root', passwd=db_password, db='mysql')
    cur = db.cursor()

    for mysql_command in mysql_commands:
        ctx.logger.debug('COMMAND: {0}'.format(mysql_command))
        cur.execute(mysql_command)

    db.close()
