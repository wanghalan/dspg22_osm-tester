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

    assert args.output.endswith('.csv') or args.output.endswith('.xlsx'), 'The file output must be a csv (.csv) or an excel (.xlsx) file'

    df = pd.read_csv(args.input)
    oracle = "https://router.project-osrm.org/route/v1/driving/{0};{1}?annotations=distance"
    # oracle = "https://router.project-osrm.org/table/v1/car/{0};{1}"

    # convert the strinng in the coor column into objects using the function eval
    df['coor'] = df['coor'].map(eval)
    logging.debug(df['coor'])

    # remove the paran around the object and convert it back to a string (in lon lat, instead of lat lon format!)
    df['coor'] = df['coor'].apply(lambda x: '%s,%s' % (x[1], x[0]))

    # Get pairs for the given number limited by the total number of coordinates
    pairs = [random_pairs(df['coor'])
             for i in range(args.number)]

    print(pairs)
    # input()
    print(df)
    # For each pair, save the results
    responses = []
    start = []
    end = []
    queries = []
    for coor in tqdm(pairs):
        logging.debug(coor)
        query = oracle.format(coor[0], coor[1])
        logging.debug(query)
        queries.append(query)
        start.append(coor[0])
        end.append(coor[1])
        r = requests.get(query)
        responses.append(str(r.text))
        logging.debug(responses)

    # Append these results to the csv and save it to the output
    pair_df = pd.DataFrame()
    pair_df['start'] = start
    pair_df['end'] = end
    pair_df['response'] = responses
    pair_df['query'] = queries

    # Append the city names to the start and end csvs
    pair_df['start_name'] = pair_df['start'].apply(
        lambda x: df[df['coor'] == x]['name'].values[0])
    pair_df['end_name'] = pair_df['end'].apply(
        lambda x: df[df['coor'] == x]['name'].values[0])

    # Reordering the data frame
    pair_df = pair_df[['start_name', 'start',
                       'end_name', 'end', 'query', 'response']]

    if args.output.endswith('.csv'):
        pair_df.to_csv(args.output, index=False)
    elif args.output.endswith('.xlsx'):
        pair_df.to_excel(args.output, engine='xlsxwriter', index=False)
    logging.debug(pair_df)
