# dspg22_osm-tester
If you are trying to merge [Open Street Map (OSM)](https://www.openstreetmap.org/#map=5/38.007/-95.844) data, how do you know that the merged files are working successfully? Don't worry, this repository might save you some work

Usage
---
```python
usage: osm-coor-get.py [-h] -a AREAS [AREAS ...] -o OUTPUT

Get city coordinates to test som merge files

options:
  -h, --help            show this help message and exit
  -a AREAS [AREAS ...], --areas AREAS [AREAS ...]
                        Areas to extract cities from
  -o OUTPUT, --output OUTPUT
```
```python
usage: osm-tester.py [-h] -i INPUT -n NUMBER -o OUTPUT [-v | --verbose | --no-verbose] [--override | --no-override]

Given input of city coordinates, append a distance column

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        a csv extracted by osm-coor-get script that contains the city coordinates
  -n NUMBER, --number NUMBER
                        number of pairs to calculate distance on
  -o OUTPUT, --output OUTPUT
  -v, --verbose, --no-verbose
  --override, --no-override
  ```

Quickstart
---
To use, use the [overpass api](https://wiki.openstreetmap.org/wiki/Overpass_API) to download coordinates of specific areas to look at. For example, in our case, we look towards Virginia and West Virginia

```python
python osm-coor-get.py -a Virginia "West Virginia" -o vw.csv
```
This returns something like the following into ```vw.csv```
```python
               name                       coor           area
0      Harrisonburg  (38.4493315, -78.8688833)       Virginia
1           Bristol  (36.5959685, -82.1885009)       Virginia
2             Galax  (36.6612387, -80.9239671)       Virginia
3          Staunton   (38.1495947, -79.072557)       Virginia
4           Hampton  (37.0300969, -76.3452057)       Virginia
5           Fairfax  (38.8462236, -77.3063733)       Virginia
6           Roanoke   (37.270973, -79.9414313)       Virginia
7           Suffolk  (36.7282096, -76.5835703)       Virginia
8        Portsmouth  (36.8444196, -76.3532998)       Virginia
9        Petersburg   (37.227928, -77.4019268)       Virginia
10       Chesapeake  (36.7183708, -76.2466798)       Virginia
11        Lynchburg  (37.4137536, -79.1422464)       Virginia
12  Charlottesville   (38.029306, -78.4766781)       Virginia
13        Arlington  (38.8903961, -77.0841585)       Virginia
14     Newport News    (36.9775016, -76.42977)       Virginia
15       Winchester  (39.1852184, -78.1652404)       Virginia
16         Poquoson  (37.1219885, -76.3965772)       Virginia
17   Virginia Beach  (36.8529841, -75.9774183)       Virginia
18       Alexandria  (38.8051095, -77.0470229)       Virginia
19         Richmond    (37.5385087, -77.43428)       Virginia
20          Norfolk  (36.8968052, -76.2602336)       Virginia
21          Beckley  (37.7781702, -81.1881557)  West Virginia
22         Wheeling  (40.0639616, -80.7209149)  West Virginia
23          Weirton  (40.4189566, -80.5895167)  West Virginia
24       Charleston  (38.3505995, -81.6332812)  West Virginia
25       Huntington   (38.4192496, -82.445154)  West Virginia
26      Martinsburg  (39.4562528, -77.9639604)  West Virginia
27       Morgantown  (39.6296809, -79.9559437)  West Virginia
28      Parkersburg  (39.2699565, -81.5506916)  West Virginia
```

Now, use the osm-tester.py to generate pairs of coordinates that return a csv with responses from the osrm official website. For example, we can take the generated ```vw.csv``` and get a response csv with 10 results using
```python
python osm-tester.py -i vw.csv -n 10 -o 10_vw_responses.csv
```
Which should return something like
```python
                    start                     end                                           response
0   38.1495947,-79.072557  39.2699565,-81.5506916  {"code":"Ok","routes":[{"geometry":"hcyoEi}qvC...
1   38.1495947,-79.072557  38.8903961,-77.0841585  {"code":"Ok","routes":[{"geometry":"|dedLgyqpF...
2   38.029306,-78.4766781   38.1495947,-79.072557  {"code":"Ok","routes":[{"geometry":"|dedLgyqpF...
3    37.5385087,-77.43428   38.4192496,-82.445154  {"code":"Ok","routes":[{"geometry":"hcyoEi}qvC...
4  39.2699565,-81.5506916  36.7183708,-76.2466798  {"code":"Ok","routes":[{"geometry":"|hrsEqfayB...
5  36.8529841,-75.9774183  37.4137536,-79.1422464  {"code":"Ok","routes":[{"geometry":"|dedLgyqpF...
6  36.6612387,-80.9239671  37.4137536,-79.1422464  {"code":"Ok","routes":[{"geometry":"|hrsEqfayB...
7  36.5959685,-82.1885009  36.8529841,-75.9774183  {"code":"Ok","routes":[{"geometry":"|hrsEqfayB...
8   37.227928,-77.4019268    36.9775016,-76.42977  {"code":"Ok","routes":[{"geometry":"|dedLgyqpF...
9  37.7781702,-81.1881557  38.3505995,-81.6332812  {"code":"Ok","routes":[{"geometry":"bqc~L_lxzK...
```

As for how to merge the osm files, well... I've put together a [gist](https://gist.github.com/yaoeh/859cefaea7b61046d084ead1b3d104a1)! glhf

Credit
---
This project was built as part of the 2022 [Data Science for the Public Good (DSPG) internship program](https://biocomplexity.virginia.edu/data-science-public-good-internship-program)
