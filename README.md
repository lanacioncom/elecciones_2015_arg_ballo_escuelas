2015 Argentina Ballotage Elections by polling station
=====================================================

## Introduction

This project was built to visualize the results of the past 2015 ballotage presidential elections of Argentina in terms of which party has won in each polling station, what percentage did each party get and how it compares with the results from the same polling station in the previous elections (primary elections and first round).


## Backend

For the backend we had two sources of information:

1. The official applications for windows provided by the government for each election
    * Primary elections
    * First round
    * Ballotage

2. The geolocated polling stations provided by the national electoral board.

We have processed the data out of those sources and generated PostGIS tables to upload to La Nación cartoDB account.

During our first attempt of rendering an hexagon grid on the fly for Argentina first round elections _cartoDB_ staff had warned us of the performance related problems with the rendering on their side: our hexagon size was small and that was too demanding for high zoom levels. 

We did not want to increase the hexagon size since we thought it would deteriorate the UX experience, so after discussing with cartoDB engineers we came up with a solution to pregenerate the hexagons (our data was not going to change) and load them in a new cartoDB table so that the calculation process was much simpler.

More info && usage [here](backend/README.md)


## Frontend

### Design process

For the frontend we gave [D3js](http://d3js.org/) a try as an overlay on top of leaflet, but due to the number of locations in our dataset (over 13.000) the rendering process was too demanding to meet our performance criteria. 

So we decided that we would rely on cartoDB to serve the processed tiles directly from the server, That limits our capacity of customization of the markers a bit, but it was the only way to get a _good performance_ out of our app.

### Custom reader analysis

We also wanted to engage the reader into finding the region they related more with to check the elections results or make custom analysis. We were playing with the idea of letting the reader paint over the map to select the polling stations they wanted to get the results from. Sometimes administrative levels are just too rigid and do not capture the living parts of a city.

Having previous results from past elections gave us the opportunity to make a visual comparison on the results for each party at a detailed level. While designing the app we wanted to be able to have a quick overview of the differences and went with a bicolor approach to show the differences at one glance.

More info && usage [here](webapp/README.md)


## Server
We are using _npm_, _bower_ and _gulp_ to automate the development and building process.

The building process takes care of minimizing, uglifying and versioning the static files so that it plays nice with the newsroom http cache configuration.

More info && usage [here](server/README.md)


## Deploy (_Specific to La Nación architecture_)
We are using fabric to automate the deployment process.

Once we have optimized, minimized, uglified and versioned our frontend app, we will deploy to our servers using a fabric task that connects to the server filesystem using the SMB protocol. 

More info && usage [here](deploy/README.md)


## Technologies && Libraries

* Backend:
    [fabric](http://www.fabfile.org/), [mdbtools](https://github.com/brianb/mdbtools), [dataset](https://dataset.readthedocs.org/en/latest/) and [cartodb](https://cartodb.com/)
* Frontend:
    [d3js](http://d3js.org/), [leaflet](http://leafletjs.com/), [leaflet-draw-plugin](https://github.com/Leaflet/Leaflet.draw), [cartodbjs](http://docs.cartodb.com/cartodb-platform/cartodb-js.html), [underscore](http://underscorejs.org/) and [requirejs](http://requirejs.org/) 


## Credits

* [Marta Alonso](https://twitter.com/malonfe)
* [Cristian Bertelegni](https://twitter.com/cbertelegni)
* [Juan Elosua](https://twitter.com/jjelosua)
* [Gastón de la llana](https://twitter.com/gasgas83)
* [Pablo Loscri](https://twitter.com/ploscri)


## Acknowledgments

We would like to thank the creators and maintainers of the libraries used for this project. We stand in the shoulders of giants.