#!/usr/bin/bash python3
# -*- coding: utf-8 -*-

import csv
import json
import pandas as pd
import os

def json_to_csv():
    save_dir = './csv/dataset.csv'
    entries = os.listdir('./json')

    for file in entries:
        with open( './json/' + file ) as data_file:
            data = json.load(data_file)
        try:
            df = pd.json_normalize(data)
            df.to_csv(save_dir, mode='a')
        except Exception as ex:
            print('FAILED TO OPEN FILE', ex)

if __name__ == '__main__':
    json_to_csv()
