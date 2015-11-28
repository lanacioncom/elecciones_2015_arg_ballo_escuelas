define([], function() {

    // Make use of our own internal CDN to store basemap tile images
    var cdn_proxy = "http://olcreativa.lanacion.com.ar/dev/get_url/img.php?img=";
    var mapboxUrl = cdn_proxy+"https://{s}.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={token}";
    // Uncomment to remove CDN proxying
    //var mapboxUrl = "https://{s}.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={token}";

    return {
/********************** RESPONSIVE SETTINGS ********************************/
        screen_width: null,
/**************************CARTODB SETTINGS ********************************/
        carto_user: "lndata",
        // Used to store the cartodb layers
        carto_layers:[],
        // To access cartoDB SQL API
        sql: null,
/***************************** MAP SETTINGS ********************************/
        arg_center: [-38.15, -65.916],
        min_zoom: 4,
        max_zoom: 18,
        /* Base layer for the map created with mapBox Studio to tweak details
           like street labels depending on zoom levels */
        base_layer: L.tileLayer(mapboxUrl, {
            id: "lanacionmapas.363845a0", 
            token: "pk.eyJ1IjoibGFuYWNpb25tYXBhcyIsImEiOiJjaWdhNm5zYjIwNHZ4dHRtMXRzOHU0cWU3In0.K8BvqeEt2V2xrXL5Tk7snQ"}),
/***************************** APP SETTINGS ********************************/
        // Used to size the polling station results based on zoom value
        zoom_perc_multipliers: {
            4:  2,
            5:  3,
            6:  3,
            7:  3,
            8:  3,
            9:  4,
            10: 6,
            11: 9,
            12: 12,
            13: 21,
            14: 22,
            15: 25,
            16: 30,
            17: 30,
            18: 40
        },
        // Used to store the parties data dictionary after async loading
        diccionario_datos: null,
        // Used to detect if the user is zooming in or out
        prev_zoom_level: null,
        // Used to set max zoom while in hexagon visualizations
        hex_zoom_threshold: 14,
        // Shortcut buttons target map position
        cities: {
            "arg": {
                center: L.latLng(-40.64, -62.13),
                zoom: 4
            },
            "conurbano": {
                center: L.latLng(-34.64, -58.54),
                zoom: 10
            },
            "caba": {
                center: L.latLng(-34.60, -58.44),
                zoom: 12
            },
            "cordoba": {
                center: L.latLng(-31.40, -64.21),
                zoom: 12
            },
            "rosario": {
                center: L.latLng(-32.94, -60.68),
                zoom: 12
            },
            "laplata": {
                center: L.latLng(-34.91, -57.96),
                zoom: 12
            }
        },
        /* National results for 1ra. vuelta used to reorder the parties on the
           overlay when folded away */
        initial_data: {
            "results": [
                {"id_partido":"0135", "votos_paso":6665120, "votos_pv":8474836, 
                 "votos":12903301, "diff_paso":1809697, "diff_pv":4428465, 
                 "porc": 0.514, "porc_pv": 34.21},
                {"id_partido":"0131", "votos_paso":8493753, "votos_pv":9144031,
                 "votos":12198441, "diff_paso":650240, "diff_pv":3054410,
                 "porc": 0.486, "porc_pv": 36.91}],
            "polling_totals": {
                nombre: "Resultado Total",
                electores: 32064684,
                votantes:  25738560,
                positivos: 25101742,
                participacion: 0.809
            }
        },
        // Sharing default URL
        parent_url: 'http://www.lanacion.com.ar',
        // Store user helper texts visibility
        show_draw_help: true,
        show_party_help: true,
        show_data_help: true,
        // Used to reuse the map popup instead of closing and opening new ones
        popup: null
    };
});