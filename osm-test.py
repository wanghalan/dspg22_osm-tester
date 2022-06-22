import requests
import json
import pandas as pd
from tqdm import tqdm
import argparse
import random
import os
import logging
import numpy as np
from sklearn.metrics import mean_squared_error


def random_pairs(obj_list):
    return [obj_list[i] for i in random.sample(range(len(obj_list)), 2)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Given a ground truth csv generating by osm-ground and a docker server ip address, print out the number of matches')
    parser.add_argument(
        '-i', '--input', help='a csv extracted by osm-ground script that contains the ground truth from the server', type=str, required=True)
    parser.add_argument(
        '-d', '--docker', help='the docker ip address and port from which to call the pull. For example, 127.0.0.1:80', type=str, required=True)
    parser.add_argument('-v', '--verbose',
                        action=argparse.BooleanOptionalAction)

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(
            format='%(levelname)s:%(message)s', level=logging.DEBUG)

    assert os.path.isfile(args.input)
    df = pd.read_csv(args.input)
    logging.debug(df)

    local_server_query = "http://%s/route/v1/driving/{0};{1}?annotations=distance" % args.docker
    matches = 0

    server_dists = []
    local_dists = []
    for index, row in df.iterrows():
        query = local_server_query.format(
            row['start'], row['end'])
        logging.debug('Query: %s' % query)
        response = requests.get(query).text
        response = eval(response)

        distance = response['routes'][0]['distance']
        osrm_server_dist = eval(row['response'])['routes'][0]['distance']
        match = (distance == osrm_server_dist)

        if match:
            matches += 1
        logging.debug('\tResponse from docker: %s' % distance)
        logging.debug('\tResponse from osrm server: %s' % osrm_server_dist)
        logging.debug('-' * 80)
        print('[%s]\t(%.2f)\t(docker: %s,server: %s)\t%s to %s' % (match, mean_squared_error([osrm_server_dist], [distance]), distance, osrm_server_dist, row['start'], row['end']
                                                                   ))
        logging.debug('=' * 80)
        local_dists.append(distance)
        server_dists.append(osrm_server_dist)
    print()
    print('Total matches: %s/%s (%.2f)' %
          (matches, len(df), matches / len(df)))
    print('Overall RMSE: %.2f' % mean_squared_error(
        server_dists, local_dists))
