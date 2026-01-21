#!/usr/bin/env python3

from multiprocessing import Pool
import subprocess
import os

src = "/data/prod/"
dest = "/data/prod_backup/"
def backup(folder):
    subprocess.call(["rsync", "-arq", os.path.join(src, folder), os.path.join(dest,folder)])

if __name__ == "__main__":
    subdir = [
        fold
        for fold in os.listdir(src)
        if os.path.isdir(os.path.join(src, fold))
    ]  
    with Pool(os.cpu_count()) as p:
        p.map(backup, subdir)
        