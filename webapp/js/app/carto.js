define(['app/context','app/config', 'app/templates'], function (ctxt, config, templates) {

    // Cartodb templates
    var perc_ccss_tpl = _.template(templates.perc_cartocss);
    var diff_ccss_tpl = _.template(templates.diff_cartocss);
    var hex_perc_ccss_tpl = _.template(templates.hex_perc_cartocss);
    var hex_diff_ccss_tpl = _.template(templates.hex_diff_cartocss);
    var winner_sql_tpl = _.template(templates.cdb_winner_sql);
    var party_sql_tpl = _.template(templates.cdb_party_sql);
    var hex_party_sql_tpl = _.template(templates.cdb_hex_party_sql);
    var hex_winner_sql_tpl = _.template(templates.cdb_hex_winner_sql);
    var hex_test_sql_tpl = _.template(templates.cdb_hex_test_sql);
    var crowdsource_sql_tpl = _.template(templates.cdb_crowdsource_sql);


    function update_layer() {
        var query, cartocss;
        var i_hex = "id_hexagono, num_loc, id_partido, ganador, swing,"+
                    "votos, votos_pv, votos_paso,"+
                    "porc, porc_pv, porc_paso,"+
                    "diff_pv, diff_paso";
        var i_nohex = "id_agrupado, nombre, direccion, id_partido, ganador, swing,"+
                      "votos, votos_pv, votos_paso,"+
                      "porc, porc_pv, porc_paso,"+
                      "diff_pv, diff_paso, adiff_pv";
        
        var pid = ctxt.selected_party;
        var interactivity = i_hex;
        if (ctxt.selected_tab == "escuela") {
            interactivity = i_nohex;
        }

        // TEST QUERIES
        // var test_sql = hex_test_sql_tpl({multiplier: 40, 
        //                                  zoom: ctxt.zoom});
        // config.sql.execute(test_sql)
        // .done(function(data){
        //     console.log(data);
        // });

        switch (ctxt.selected_tab) {
            case "escuela":
                if (pid == "0000") {
                    // GET WINNER DATA
                    cartocss = perc_ccss_tpl({'data': config.diccionario_datos, 
                                         'zooms': config.zoom_perc_multipliers});
                    // GET THE WINNER FOR EACH POLLING STATION
                    query = winner_sql_tpl({orden: 'votos'});
                } else {
                    // GET PARTY DATA
                    cartocss = perc_ccss_tpl({'data': config.diccionario_datos, 
                                         'zooms': config.zoom_perc_multipliers
                                         });
                    // GET THE PARTY FOR EACH POLLING STATION
                    query = party_sql_tpl({'id_partido': pid, 
                                           'orden': 'votos',
                                           'fwinner': ctxt.w,
                                           'fswing': ctxt.sw});
                }
                break;
            case "fuerza":
                cartocss = hex_perc_ccss_tpl({data: config.diccionario_datos});
                if (pid == "0000") {
                    query = hex_winner_sql_tpl({zoom: ctxt.zoom});
                }
                else {
                    query = hex_party_sql_tpl({'zoom': ctxt.zoom,
                                               'id_partido': pid,
                                               'fwinner': ctxt.w,
                                               'fswing': ctxt.sw});
                }
                break;
            case "difpaso":
            case "difpv":
                // ALWAYS WITH A SELECTED PARTY, DEFAULT OVERALL WINNER
                var color = config.diccionario_datos[pid].color_partido;
                // SHOW THE HEXAGON AGGREGATION
                cartocss = hex_diff_ccss_tpl({'data': config.diccionario_datos,
                                              'tab': ctxt.selected_tab});

                query = hex_party_sql_tpl({'zoom': ctxt.zoom,
                                           'id_partido': pid,
                                           'fwinner': null,
                                           'fswing': null});
                break;
        }

        // Apply new query and style
        config.carto_layers[0].set({
            sql: query,
            cartocss: cartocss,
            interactivity: interactivity,
        });
        // Show loader
        $(".loader").show();
    }

    /** persist readers feedback on polling station geolocation*/
    function send_crowdsource(id_agrupado, comentario) {
        var sql = crowdsource_sql_tpl({'id': id_agrupado,
                                       'comment': comentario});
        $.ajax({
            type: 'POST',
            url: 'https://lndata.cartodb.com/api/v2/sql',
            crossDomain: true,
            data: {"q":sql},
            dataType: 'json',
            success: function(responseData, textStatus, jqXHR) {
            },
            error: function (responseData, textStatus, errorThrown) {
                console.log("Problem saving the data" + textStatus);
            }
        });
    }

    return {
        update_layer: update_layer,
        send_crowdsource: send_crowdsource,
    };
});