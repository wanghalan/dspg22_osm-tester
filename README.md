# dspg22_osm-tester
If you are trying to merge [Open Street Map (OSM)](https://www.openstreetmap.org/#map=5/38.007/-95.844) data, how do you know that the merged files are working successfully?

System Overview
---
![System Overview](https://raw.githubusercontent.com/yaoeh/dspg22_osm-tester/main/documentation/system-overview.png)


Quickstart
---
To start, we use the [overpass api](https://wiki.openstreetmap.org/wiki/Overpass_API) to download coordinates of specific cities to look at. For example, to get the coordinates for Virginia and West Virginia

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
Which should return something like. Note that the lat lon format is flipped to lon lat, which is what the OSRM server takes as an input
```python
     start_name                   start      end_name                     end                                              query                                           response
0    Petersburg   -77.4019268,37.227928       Hampton  -76.3452057,37.0300969  https://router.project-osrm.org/route/v1/drivi...  {"code":"Ok","routes":[{"geometry":"ebfbFdqlwM...
1       Hampton  -76.3452057,37.0300969  Harrisonburg  -78.8688833,38.4493315  https://router.project-osrm.org/route/v1/drivi...  {"code":"Ok","routes":[{"geometry":"{m_aFvd~pM...
2      Richmond    -77.43428,37.5385087      Poquoson  -76.3965772,37.1219885  https://router.project-osrm.org/route/v1/drivi...  {"code":"Ok","routes":[{"geometry":"{sbdF~}rwM...
3       Roanoke   -79.9414313,37.270973  Newport News    -76.42977,36.9775016  https://router.project-osrm.org/route/v1/drivi...  {"code":"Ok","routes":[{"geometry":"yonbF|p|fN...
4  Newport News    -76.42977,36.9775016    Portsmouth  -76.3532998,36.8444196  https://router.project-osrm.org/route/v1/drivi...  {"code":"Ok","routes":[{"geometry":"mdu`F~tnqM...
5     Arlington  -77.0841585,38.8903961    Portsmouth  -76.3532998,36.8444196  https://router.project-osrm.org/route/v1/drivi...  {"code":"Ok","routes":[{"geometry":"ixjlF`onuM...
6    Winchester  -78.1652404,39.1852184    Chesapeake  -76.2466798,36.7183708  https://router.project-osrm.org/route/v1/drivi...  {"code":"Ok","routes":[{"geometry":"ukdnFpxa|M...
7       Hampton  -76.3452057,37.0300969      Poquoson  -76.3965772,37.1219885  https://router.project-osrm.org/route/v1/drivi...  {"code":"Ok","routes":[{"geometry":"{m_aFvd~pM...
8    Portsmouth  -76.3532998,36.8444196       Suffolk  -76.5835703,36.7282096  https://router.project-osrm.org/route/v1/drivi...  {"code":"Ok","routes":[{"geometry":"sc{_Ffz_qM...
9       Fairfax  -77.3063733,38.8462236         Galax  -80.9239671,36.6612387  https://router.project-osrm.org/route/v1/drivi...  {"code":"Ok","routes":[{"geometry":"{cblFz{yvM...
```

Finally, to run the tests to check against the server responses
```python
python osm-test.py -i 10_vw_responses.csv -d 127.0.0.1:80

# If you haven't started your docker isntance, run something like this first: 
# docker run -t -i -p 80:5000 -v "${PWD}:/data" osrm/osrm-backend osrm-routed --algorithm mld /data/<filename>.osrm, where 8000 would be the local port, and 5000 the docker port
```

Which should return something like this
```python
[True]	(0.00)	(docker: 331120.8,server: 331120.8)	-76.3452057,37.0300969 to -78.8688833,38.4493315
[False]	(0.10)	(docker: 114815.1,server: 114815)	-77.43428,37.5385087 to -76.3965772,37.1219885
[True]	(0.00)	(docker: 426893,server: 426893)	-79.9414313,37.270973 to -76.42977,36.9775016
[True]	(0.00)	(docker: 22749.6,server: 22749.6)	-76.42977,36.9775016 to -76.3532998,36.8444196
[False]	(130.20)	(docker: 310488.8,server: 310358.6)	-77.0841585,38.8903961 to -76.3532998,36.8444196
[False]	(0.10)	(docker: 374642.9,server: 374643)	-78.1652404,39.1852184 to -76.2466798,36.7183708
[True]	(0.00)	(docker: 16002.7,server: 16002.7)	-76.3452057,37.0300969 to -76.3965772,37.1219885
[True]	(0.00)	(docker: 28624.7,server: 28624.7)	-76.3532998,36.8444196 to -76.5835703,36.7282096
[True]	(0.00)	(docker: 495691.9,server: 495691.9)	-77.3063733,38.8462236 to -80.9239671,36.6612387

Total matches: 7/10 (0.70)
Overall MAD: 13.04
```

Misc
---
How to merge osm files [gist](https://gist.github.com/yaoeh/859cefaea7b61046d084ead1b3d104a1)

Acknowledgement
---
This project was built as part of the 2022 [Data Science for the Public Good (DSPG) internship program](https://biocomplexity.virginia.edu/data-science-public-good-internship-program)
