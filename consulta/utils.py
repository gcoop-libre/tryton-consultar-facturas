#!/usr/bin/env python3
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import os

def get_app_base_path():
    return os.path.dirname(os.path.realpath(__file__))

def get_instance_folder_path():
    return os.path.join(get_app_base_path(), 'instance')
