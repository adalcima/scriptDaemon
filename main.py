#!/usr/bin/python3

import time
import gc
from uuid import UUID

import sys
sys.path.append('/usr/local/bin/')
from config.my_server import DatabaseConfig, UuidConfig


while True:
    # Set environment
    my_db_access = DatabaseConfig()
    uuid_config = UuidConfig()

    gc.collect()
    wait = int(uuid_config.waiting_time)
    try:
        print("Starting uuidd")
        accessdb = {"user": my_db_access.user, "password": my_db_access.passwd, "dbname": my_db_access.name}

        # Check for new requirements. If there are any requirementes, call
        # uuidManager function for building every uuid script one by one.
        script = UUID(uuid_config.path, accessdb)
        new_requests = script.req()
        if new_requests:
            print("New request")
            for request in new_requests:
                # 1: Create new uuid script
                # 5: Create empty script
                status_script = request[7]
                if status_script == 1:
                    script.uuidManager(request)
                elif status_script == 5:
                    script.createEmpty(request)
        else:
            print("There are not requests")
        print(script.exit())
        time.sleep(wait)
    except:
        time.sleep(wait)
