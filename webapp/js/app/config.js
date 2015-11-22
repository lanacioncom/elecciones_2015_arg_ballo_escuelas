define(['cartodbjs'], function(dummy) {

    var cdn_proxy = "http://olcreativa.lanacion.com.ar/dev/get_url/img.php?img=";
    var mapboxUrl = cdn_proxy+'https://{s}.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={token}';
    //var mapboxUrl = 'https://{s}.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={token}';

    return {
        zoom_perc_multipliers: {
            4:  2,
            5:  3,
            6:  6,
            7:  4,
            8:  4,
            9:  6,
            10: 8,
            11: 14,
            12: 15,
            13: 21,
            14: 22,
            15: 25,
            16: 30,
            17: 30,
            18: 40
        },
        carto_user: 'lndata',
        carto_layers:[], 
        arg_center: [-40.647, -62.139],
        izoom: 4,
        izoom_mob: 4,
        sql: null,
        screen_width: null,
        diccionario_datos: null,
        current_latlng: null,
        prev_zoom_level: null,
        hex_zoom_threshold: 14,
        cities: {
            'arg': {
                center: L.latLng(-40.647, -62.139),
                zoom: 4
            },
            'conurbano': {
                center: L.latLng(-34.64902575352698, -58.54751586914063),
                zoom: 10
            },
            'caba': {
                center: L.latLng(-34.606932330061724, -58.44829559326172),
                zoom: 12
            },
            'cordoba': {
                center: L.latLng(-31.40844712033033, -64.21096801757812),
                zoom: 12
            },
            'rosario': {
                center: L.latLng(-32.947318116407644, -60.68332672119141),
                zoom: 12
            },
            'laplata': {
                center: L.latLng(-34.9140886169061, -57.96455383300781),
                zoom: 12
            }
        },
        //url_telegramas: 'http://www.resultados.gob.ar/nacionaltelegr/01/001/0001/010010001_0030.htm',
        base_layer: L.tileLayer(mapboxUrl, {
            id: 'lanacionmapas.363845a0',  
            attribution: "OpenStreetMaps", 
            token: 'pk.eyJ1IjoibGFuYWNpb25tYXBhcyIsImEiOiJjaWdhNm5zYjIwNHZ4dHRtMXRzOHU0cWU3In0.K8BvqeEt2V2xrXL5Tk7snQ'}),
        initial_data: {
            'results': [
                {"id_partido":"0131","votos_paso":8493753,"votos":9144031,"diferencia":650240, 'pct': 36.91},
                {"id_partido":"0135","votos_paso":6665120,"votos":8474836,"diferencia":1809697, 'pct': 34.21}],
            'polling_totals': {
                nombre: "Resultado Total",
                electores: 32632646,
                votantes:  24413915,
                positivos: 24772286,
                participacion: 74.81
            }
        },
        // Sharing default
        url_parent: 'http://www.lanacion.com.ar'
    };
});