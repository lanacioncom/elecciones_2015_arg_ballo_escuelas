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
        arg_center: [-40.647, 62.139],
        izoom: 4,
        izoom_mob: 4,
        sql: null,
        screen_width: null,
        diccionario_datos: null,
        current_latlng: null,
        prev_zoom_level: null,
        hex_zoom_threshold: 12,
        cities: {
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
                {"id_partido":"0135","votos_paso":6665120,"votos":8474836,"diferencia":1809697, 'pct': 34.21},
                {"id_partido":"0138","votos_paso":4564127,"votos":5299455,"diferencia":735319, 'pct': 21.39},
                {"id_partido":"0137","votos_paso":733593,"votos":810939,"diferencia":77344, 'pct': 3.27},
                {"id_partido":"0132","votos_paso":778885,"votos":627328,"diferencia":-151558, 'pct': 2.53},
                {"id_partido":"0133","votos_paso":466695,"votos":415697,"diferencia":-50998, 'pct': 1.68}],
            'polling_totals': {
                nombre: "Resultado Total",
                electores: 32632646,
                votantes:  24413915,
                positivos: 24772286,
                participacion: 74.81
            }
        }
    };
});