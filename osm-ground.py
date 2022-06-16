import requests
import json
import pandas as pd
from tqdm import tqdm
import argparse
import random
import os
import logging


def random_pairs(obj_list):
    return [obj_list[i] for i in random.sample(range(len(obj_list)), 2)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Given input of city coordinates, create a random number of pairs and query the server to generate the ground truth')
    parser.add_argument(
        '-i', '--input', help='a csv extracted by osm-coor-get script that contains the city coordinates', type=str, required=True)
    parser.add_argument('-n', '--number', type=int,
                        help='number of pairs to calculate distance on', required=True)
    parser.add_argument('-o', '--output', type=str, required=True)
    parser.add_argument('-v', '--verbose',
                        action=argparse.BooleanOptionalAction)
    parser.add_argument('--override',
                        action=argparse.BooleanOptionalAction)

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(
            format='%(levelname)s:%(message)s', level=logging.DEBUG)

    assert os.path.isfile(args.input)
    if not args.override:
        assert not os.path.isfile(args.output)

    df = pd.read_csv(args.input)
    oracle = "https://router.project-osrm.org/route/v1/driving/{0};{1}?annotations=distance"

    # convert the strinng in the coor column into objects using the function eval
    df['coor'] = df['coor'].map(eval)
    logging.debug(df['coor'])

    # remove the paran around the object and convert it back to a string
    df['coor'] = df['coor'].apply(lambda x: '%s,%s' % (x[0], x[1]))

    # Get pairs for the given number limited by the total number of coordinates
    pairs = [random_pairs(df['coor'])
             for i in range(args.number)]

    print(df)
    # For each pair, save the results
    responses = []
    start = []
    end = []
    for coor in tqdm(pairs):
        logging.debug(coor)
        query = oracle.format(coor[0], coor[1])
        logging.debug(query)
        r = requests.get(query)
        start.append(coor[0])
        end.append(coor[1])
        responses.append(r.text)
        logging.debug(responses)

    # Append these results to the csv and save it to the output
    pair_df = pd.DataFrame()
    pair_df['start'] = start
    pair_df['end'] = end
    pair_df['response'] = responses
    pair_df.to_csv(args.output, index=False)
    logging.debug(pair_df)