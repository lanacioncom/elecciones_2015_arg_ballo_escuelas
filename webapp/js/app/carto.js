define(['app/context','app/config', 'app/templates'], function (ctxt, config, templates) {

    // Cartodb templates
    var perc_ccss_tpl = _.template(templates.perc_cartocss);
    var diff_ccss_tpl = _.template(templates.diff_cartocss);
    var hex_perc_ccss_tpl = _.template(templates.hex_perc_cartocss);
    var hex_diff_ccss_tpl = _.template(templates.hex_diff_cartocss);
    var winner_sql_tpl = _.template(templates.cdb_winner_sql);
    var party_sql_tpl = _.template(templates.cdb_party_sql);
    var party_sql_poll_winner_tpl = _.template(templates.cdb_party_poll_winner_sql);
    var hex_sql_tpl = _.template(templates.cdb_hex_query_sql);
    var hex_winner_sql_tpl = _.template(templates.cdb_hex_query_winner_sql);
    var hex_sub_party_sql_tpl = _.template(templates.cdb_hex_sub_party_sql);
    var hex_sub_party_sql_poll_winner_tpl = _.template(templates.cdb_hex_sub_party_poll_winner_sql);
    var hex_sub_winner_sql_tpl = _.template(templates.cdb_hex_sub_winner_sql);
    var hex_test_sql_tpl = _.template(templates.cdb_hex_test_sql);


    function update_layer() {
        var query, cartocss;
        var i_hex = "agg_cnt, agg_perc, agg_list, agg_votes, agg_votes_prev";
        var i_nohex = "id_agrupado, id_partido, nombre, positivos,"+
                      "votos, votos_paso, adif, diferencia, perc";
        
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
                    cartocss = perc_ccss_tpl({data: config.diccionario_datos, 
                                         zooms: config.zoom_perc_multipliers});
                    // GET THE WINNER FOR EACH POLLING STATION
                    query = winner_sql_tpl({orden: 'perc'});
                } else {
                    // GET PARTY DATA
                    cartocss = perc_ccss_tpl({data: config.diccionario_datos, 
                                         zooms: config.zoom_perc_multipliers});
                    // GET THE PARTY FOR EACH POLLING STATION
                    query = party_sql_tpl({id_partido: pid, orden: 'perc'});
                }
                break;
            case "fuerza":
                cartocss = hex_perc_ccss_tpl({data: config.diccionario_datos});
                if (pid == "0000") {
                    // AGGREGATE CALCULATING WINNERS OVER EACH HEXAGON
                    subquery = hex_sub_winner_sql_tpl();
                    query = hex_winner_sql_tpl({multiplier: ctxt.hex_size, 
                                                zoom: ctxt.zoom,
                                                subquery: subquery});
                    query = hex_winner_sql_tpl({zoom: ctxt.zoom});
                    interactivity = 'agg_votes, agg_perc';
                }
                else {
                    //subquery = hex_sub_party_sql_tpl({id_partido: pid});
                    //query = hex_sql_tpl({multiplier: ctxt.hex_size,
                    //                           zoom: ctxt.zoom,
                    //                           subquery: subquery});
                    query = hex_sql_tpl({zoom: ctxt.zoom, id_partido: pid});
                    interactivity = 'agg_votes, agg_perc, agg_diff';   
                }
                break;
            case "difpaso":
                // ALWAYS WITH A SELECTED PARTY, DEFAULT OVERALL WINNER
                var color = config.diccionario_datos[pid].color_partido;
                // SHOW THE HEXAGON AGGREGATION
                cartocss = hex_diff_ccss_tpl({data: config.diccionario_datos});
                    
                // subquery = hex_sub_party_sql_tpl({id_partido: pid});
                // query = hex_sql_tpl({multiplier: ctxt.hex_size,
                //                      zoom: ctxt.zoom,
                //                      subquery: subquery});
                query = hex_sql_tpl({zoom: ctxt.zoom, id_partido: pid});
                interactivity = 'agg_votes, agg_perc, agg_diff';   
                query
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

        var sql = "SELECT crowdsource_geo(";
        sql += id_agrupado+",";
        sql += true+",'";
        sql += comentario+"') as cartodb_id;";
        $.ajax({
            type: 'POST',
            url: 'https://lndata.cartodb.com/api/v2/sql',
            crossDomain: true,
            data: {"q":sql},
            dataType: 'json',
            success: function(responseData, textStatus, jqXHR) {
                //console.log(responseData.rows[0].cartodb_id);
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