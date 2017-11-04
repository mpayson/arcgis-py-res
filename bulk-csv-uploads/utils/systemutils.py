"""utils for interacting with file systems"""
import os

def get_subdirectories():
    """gets a list of subdirectories from calling file"""
    return next(os.walk('.'))[1]

def get_csvs(dir_path):
    """get all the csvs at a given file path"""
    return [file for file in os.listdir(dir_path) if file.endswith('.csv')]
