# filepath: /mypublicip/mypublicip/mypublicip/mypublicip.py
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
########################################################################################################################
# This file is a part of Jeyriku.net.
#
# Created: 01.08.2025 16:50:27
# Author: Jeremie Rouzet
#
# Last Modified: 01.08.2025 17:29:52
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Jeyriku.net
########################################################################################################################

"""
Module to retrieve the public IP address of the current connection.
"""

import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

def get_public_ip():
    """
    Retrieves the public IP address using curl and returns it as a string.
    Returns None if retrieval fails.
    """
    try:
        result = subprocess.run(['curl', '-s', 'ifconfig.me'], capture_output=True, text=True, check=True)
        public_ip = result.stdout.strip()
        logger.info("The Public IP attached to this connection was retrieved successfully: %s", public_ip)
        return public_ip
    except subprocess.CalledProcessError as e:
        logger.error("An error occurred while trying to retrieve the public IP: %s", e)
        return None

def main():
    logger.info("This script will attempt to retrieve the public IP attached to this connection.")
    print()
    ip = get_public_ip()
    if ip:
        print("Public IP:", ip)
    else:
        print("Could not retrieve public IP.")

if __name__ == "__main__":
    main()