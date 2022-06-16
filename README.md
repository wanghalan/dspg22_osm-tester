# dspg22_osm-tester
If you are trying to merge [Open Street Map (OSM)](https://www.openstreetmap.org/#map=5/38.007/-95.844) data, how do you know that the merged files are working successfully?

Quickstart
---
To use, use the [overpass api](https://wiki.openstreetmap.org/wiki/Overpass_API) to download coordinates of specific cities to look at. For example, in our case, we look towards Virginia and West Virginia

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

Now, use the osm-tester.py to generate random pairs of coordinates that return a csv with responses from the [osrm server](https://router.project-osrm.org/). For example, we can take the generated ```vw.csv``` and get a response csv with 10 results using
```python
python osm-ground.py -i vw.csv -n 10 -o 10_vw_responses.csv
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

Finally, to run the tests to check against the server responses
```python
python osm-test.py -i 10_vw_responses.csv -d 127.0.0.1:80
```
Which should return something like
```python
[False]	(docker: 0,server: 585776.8) 38.1495947,-79.072557 to 39.2699565,-81.5506916
[True]	(docker: 0,server: 0) 38.1495947,-79.072557 to 38.8903961,-77.0841585
[True]	(docker: 0,server: 0) 38.029306,-78.4766781 to 38.1495947,-79.072557
[False]	(docker: 0,server: 585776.8) 37.5385087,-77.43428 to 38.4192496,-82.445154
[False]	(docker: 0,server: 585772.5) 39.2699565,-81.5506916 to 36.7183708,-76.2466798
[True]	(docker: 0,server: 0) 36.8529841,-75.9774183 to 37.4137536,-79.1422464
[True]	(docker: 0,server: 0) 36.6612387,-80.9239671 to 37.4137536,-79.1422464
[False]	(docker: 0,server: 585772.5) 36.5959685,-82.1885009 to 36.8529841,-75.9774183
[True]	(docker: 0,server: 0) 37.227928,-77.4019268 to 36.9775016,-76.42977
[True]	(docker: 0,server: 0) 37.7781702,-81.1881557 to 38.3505995,-81.6332812

Total matches: 6/10 (0.60)
```

Misc
---
How to merge osm files [gist](https://gist.github.com/yaoeh/859cefaea7b61046d084ead1b3d104a1)

Acknowledgement
---
This project was built as part of the 2022 [Data Science for the Public Good (DSPG) internship program](https://biocomplexity.virginia.edu/data-science-public-good-internship-program)
