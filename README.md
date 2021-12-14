# Tracking communities accross time:

It tracks  network communities across consecutive time frames. In particular
it detects the evolutionary phenomenon a community can sustain from one time frame
to another:
- continuing
- shrinking
- growing
- split
- merge
- dissolving
- No_event (when none of the above events holds)
The code is based on the implementation of [1]



## File Structure & running

- It contains 6 .py (thon) files
config.py , event.py , hypergraph.py, inclusion.py , preprocessing.py , tracker.py
- To run from terminal: $ python3 Tracker.py input_example/community_edges.json
(python tracker.py <inputfile>.json)
- output: a file named 'results.csv', the format is:
```window ID, community ID, window ID, community ID, event```
- In config.py there are 2 parameters Alpha,Beta. These are the thresholds for the event
identification. Should be between [0.1,1]

## Input data format

The file given as input to the GED algorithm must adhere to the following JSON template:

```sh
{
    "windows":
     [      //array of windows (i.e. timeframes)
        {
            "communities":
             [     //array of communities in each window
                [     //array of edges in each community
                    [   //array containing two node ids between which an edge exists (this is an edge of the community)
                     ]
                ]
            ]
        }
    ]
}
```
We assume that the data set has been split into time frames and that communities have
been discovered in each time frame.

An example input file is provided in the "input/example" directory to test GED, consisting of 20 windows.
input/example/community_edges.json

```sh
                                             <-------  community ---------->   <-------  community ---------->
time-step:1 --> {"windows":[{"communities":[ [[id1,id2],[id2,id3],[id3,id1]], [[id4,id5],[id5,id6],[id6,id7]] ]
time-step:2 --> {"windows":[{"communities":[ [[id8,id9],[id9,id10],[id10,id1]], [[id11, id12],[id12,id13],[id13,id11]] ]
```


## Output-data-format

- The output file generated by GED has the following format:
<window id for current timestep>,<community id for current timestep>,<window id for next timestep>,<community id for next timestep>,<event>
- E.g. ```0,40,1,42,continuing``` means that community 40 in window 0 has evolved (corresponds) to community 42 in the next window (window 1) and the associated event with this evolution is continue.
- Windows are numbered consecutively starting from 0. The same holds for the communities in each window.


## References
[1]: Piotr Brodka,  Stanislaw Saganowski,  and Przemyslaw Kazienko  (2011), *Tracking group evolution in social networks*, International Conference on Social Informatics, 316--319, Springer



## Licence
community-tracking - NCSR Demokritos module Copyright 2016 Michail Apostolou

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at: https://www.apache.org/licenses/LICENSE-2.0

