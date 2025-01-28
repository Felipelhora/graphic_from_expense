from decouple import config

DB_CONFIG = {
                'db_username': config('db_username'),
                'db_password': config('db_password'),
                'db_host': config('db_host'),
                'db_port': config('db_port'),
                'db_name': config('db_name'),
            }


