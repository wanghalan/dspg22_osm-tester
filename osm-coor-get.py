import requests
import json
import pandas as pd
from tqdm import tqdm
import argparse
import random


def random_pairs(obj_list):
    return [obj_list[i] for i in random.sample(range(len(obj_list)), 2)]


def get_city_coors(area):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json];
    area[name="%s"];
    (node[place="city"](area););out;
    """ % area

    response = requests.get(
        overpass_url,
        params={'data': overpass_query}
    )

    coords = []
    names = []
    if response.status_code == 200:
        data = response.json()
        places = data.get('elements', [])
        for place in places:
            try:
                # print(place)
                coords.append((place['lat'], place['lon']))
                names.append(place['tags']['name'])
            # print("Got %s village coordinates!" % len(coords))
            # print(coords[0])
            except IndexError:
                print('Ran into index error')
    else:
        print("Error")
    return names, coords


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Get city coordinates to test som merge files')
    parser.add_argument('-a', '--areas', nargs='+',
                        help='Areas to extract cities from', required=True)
    parser.add_argument('-o', '--output', type=str, required=True)
    args = parser.parse_args()

    fdf = []
    for area in tqdm(args.areas):
        df = pd.DataFrame()
        names, coors = get_city_coors(area)
        assert len(names) == len(coors)
        df['name'] = names
        df['coor'] = coors
        df['area'] = area
        fdf.append(df)
    fdf = pd.concat(fdf, ignore_index=True)
    print(fdf)
    fdf.to_csv(args.output, index=False)
