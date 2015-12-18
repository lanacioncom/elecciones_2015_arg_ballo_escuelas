requirejs.config({
    baseUrl: "js",
    paths: {
        "draw": "../libs/leaflet.draw",
        "templates": "../templates", 
        "text": "../libs/requirejs-text/text",
        "d3": "../libs/d3/d3.min",
        "jquery": "../libs/jquery/dist/jquery.min",
        "jquery-ui": "../libs/jquery-ui/jquery-ui.min"
    },
    shim: {
        "jquery-ui": ["jquery"]
    }
});

requirejs(["app/context", "app/config", "app/templates", "app/carto",
           "app/responsive", "app/overlay", "app/helpers", "app/view_helpers",
           "app/draw", "app/permalink", "app/analytics", "app/share",
           "d3", "jquery-ui"],
function(ctxt, config, templates, cdb, responsive, Overlay, 
         helpers, view_helpers, 
         draw, permalink, ga, share, d3, dummy) {
    $(function() {
    "use strict";
        var _self = this;
        var map;

        //Instantiate pymjs
        _self.pymChild = new pym.Child();
        
        // STATIC TEMPLATES
        d3.select("#help_draw").html(templates.ayuda_draw_html);
        
        // Tooltip template 
        var popup_tpl = _.template(templates.popup_html);
        // Percentages tooltip template 
        var popup_perc_tpl = _.template(templates.popup_perc_html);
        // Differences tooltip template
        var popup_diff_tpl = _.template(templates.popup_diff_html);
        // Telegram template
        var telegram_tpl = _.template(templates.telegramas_html);
        // Telegram template
        var dc_embed_tpl = _.template(templates.telegrama_embed_html);


        // First get permalink status and set context accordingly
        // If we are inside the CMS and 

        permalink.get();
        permalink.validate();

        //Limit bounds of map to Argentina + offset
        var southWest = L.latLng(-83.5399697192, -110.92578125),
            northEast = L.latLng(-7.5367643221, -14.23828125),
            bounds = L.latLngBounds(southWest, northEast);

        // Initialize map
        map = L.map("map_container", {
            center: [ctxt.lat, ctxt.lng],
            zoom: ctxt.zoom,
            minZoom: 4,
            maxZoom: 18,
            attributionControl: false,
            maxBounds: bounds,
            closePopupOnClick: false
        });

        // Init SQL API
        config.sql = new cartodb.SQL({
            user: config.carto_user
        });
        // Add base layer
        map.addLayer(config.base_layer);
        

        //JET: Load sections 
        $.get("data/dict_partidos.json", function(data){
            config.diccionario_datos = data;
            init();
        });

        /** After data is loaded launch app */
        function init() {
            config.screen_width = $(window).width();
            responsive.init();
            init_nav();
            // initialize overlay
            _self.overlay = new Overlay(map);
            // Add cartodb_layer that being asynchronous
            // launches update after loading
            add_cartodb_layer();

            // Show helper texts and draw functionality
            if (config.show_draw_help) {
                $("#help_draw").fadeIn();
                map.addControl(draw.drawControlFull);
                //Draw layer
                map.addLayer(draw.drawnItems);

            }
            if (config.show_overlay_help) {
                $(".help_overlay_filter").fadeIn();
            }
        }

        // Set initial zoom level for responsiveness
        //media.set_media_zoom();
        
        function add_cartodb_layer() {
            // Add empty layer
            cartodb.createLayer(map, {
                user_name: config.carto_user,
                type: "cartodb",
                sublayers: [{}]
            })
            .addTo(map)
            .on("done", function(layer) {
                // Check if the layer has loaded
                layer.on("load", function() {
                    $(".loader").hide();
                    _self.overlay.update_ref();
                });
                var sublayer = layer.getSubLayer(0);
                config.carto_layers.push(layer.getSubLayer(0));
                layer.setInteraction(true);
                layer.on("featureClick", featureClick)
                     .on("featureOver", featureOver)
                     .on("featureOut", featureOut);

                update();
                // If we are using pym send the request for the parent_url
                // and send the height to adjust the iframe 
                _self.pymChild.sendMessage("pymEspecialesLoaded", "ready");
                _self.pymChild.sendHeight();

                $(window).resize(_.debounce(resizedw,500));

            })
            .on("error", function(err) {console.log(err);});
        }
        // Update window
        function resizedw() {
            var w = $(window).width();
            if(config.screen_width != w){
                config.screen_width = w;
                _self.pymChild.sendHeight();
            }
        }

        /** Event received from parent page using pym.js
            to send the parent url to the app */
        _self.pymChild.onMessage("setShareUrl", function(parent_url) {
            
            var utoken = parent_url.split("?");
            if (utoken.length > 1) {
                config.parent_url = parent_url;
                var query_string = utoken[1]; 
                // Analytics
                ga.fire_analytics_event("permalink", query_string);
                
                permalink.get(query_string);
                permalink.validate();

                init_nav();
                update();
                _self.overlay.update_filter();

                // Set map according to parentUrl
                move_to_position(L.latLng(ctxt.lat, ctxt.lng), ctxt.zoom, true);
            }
            share.activate_share(utoken[0]);
        });


        /** Determines if hex or polling station is selected
            gets the data for the overlay and once done calls
            featureClickDone with the data as if it had been
            clicked by the user
        */
        function update_selected_feature() {
            var poll = helpers.is_empty(ctxt.selected_polling) ? false : true;
            var fid = poll ? ctxt.selected_polling : ctxt.selected_hex;
            var query = poll ? "permalink_sql" : "permalink_hex_sql";
            config.sql.execute(templates[query],{"id": fid})
                .done(function(data) {
                    var position = JSON.parse(data.rows[0].geo).coordinates;
                    var latlng = L.latLng(position[1], position[0]);
                    if (poll) {
                        move_to_position(latlng);
                    } else {
                        var z = data.rows[0].zoom_level;
                        move_to_position(latlng, z, true);    
                    }
                    var d = data.rows[0];
                    featureClickDone(latlng, d, data);
                });
        }


        /** update vizualization based on the actual context */
        function update() {
            // Update the map data
            cdb.update_layer();

            if (helpers.selected_feature()) {
                update_selected_feature();
            }
        }

        function draw_deleted(e) {
            if (!draw.drawnItems.getLayers().length) {
                draw.drawControlEditOnly.removeFrom(map);
                draw.drawControlFull.addTo(map);
            }
            map.closePopup();
        }

        function draw_filter(e) {
            var draw_layer = null;
            var latlng = null;
            
            if (e.type === "draw:created") {
                draw_layer = e.layer;
                latlng = draw_layer.getBounds().getCenter(); 
                draw.drawnItems.addLayer(draw_layer);
                draw.drawControlFull.removeFrom(map);
                draw.drawControlEditOnly.addTo(map);
            }
            else {
                draw_layer = e.layers.getLayers()[0];
                latlng = draw_layer.getBounds().getCenter();
            }
            // Get the coordinates of the polygon we just drew
            var poly = draw_layer.getLatLngs();
            var sql_poly = [];
            for (var i in poly){
                sql_poly.push("CDB_LatLng("+poly[i].lat+","+poly[i].lng+")");
            }
            //SQL polygon must be a CLOSED loop
            sql_poly.push("CDB_LatLng("+poly[0].lat+","+poly[0].lng+")");
            //Center and zoom the map
            move_to_position(latlng);
            config.sql.execute(templates.draw_sql,{bounds: sql_poly.join()})
            .done(_.partial(featureClickDone, latlng, null))
            .error(function(errors) {
                console.log(errors);
            });
        }

        //** move to the selected position 
        //   and update context accordingly*/
        function move_to_position(latlng, zoom, z_changed) {
            if (z_changed) {
                ctxt.zoom = zoom;
            }
            ctxt.lat = +(latlng.lat).toFixed(2);
            ctxt.lng = +(latlng.lng).toFixed(2);
            permalink.set();
            if (z_changed) {
                map.setView(latlng, zoom);
            } else {
                map.panTo(latlng);
            }
        }

        function featureClick(event, loc, pos, data, layerNumber) {
            var fid;
            var latlng = L.latLng(loc[0], loc[1]); 
            move_to_position(latlng);

            if (ctxt.selected_tab != "escuela") {
                // Get hexagon data from DB
                ctxt.selected_hex = data.id_hexagono;
                permalink.set();

                //Analytics
                if (loc !== null) {
                    ga.fire_analytics_event("hexagono",ctxt.selected_hex);
                }

                fid = ctxt.selected_hex;
                config.sql.execute(templates.click_hex_sql,{"id": fid,
                                                            "orden": "votos"})
                    .done(_.partial(featureClickDone, loc, data))
                    .error(function(errors) {
                        console.log(errors);
                    });
            }
            else {
                ctxt.selected_polling = data.id_agrupado;
                permalink.set();

                //Analytics
                if (loc !== null) {
                    ga.fire_analytics_event("establecimiento",ctxt.selected_polling);
                }

                fid = data.id_agrupado;
                var query = templates.click_feature_sql;
                var params = {"id": fid, "orden": "votos"};
                config.sql.execute(query, params)
                      .done(_.partial(featureClickDone, loc, data))
                      .error(function(errors) {
                            console.log(errors);
                      });
            }
            return false;
        }

        //Called when the Cartodb SQL has finished
        //Origin featureClick or a draw selection
        function featureClickDone(latlng, establecimiento_data, votos_data) {

            // ONLY WHEN DRAWING
            if (!votos_data.total_rows) {
                var msg_header = "Error";
                var msg_body = "No se ha encontrado ninguna "+
                               "escuela con la selección actual";
                var content = popup_tpl({message_header: msg_header,
                                         message_body: msg_body});
                set_map_popup(latlng, content);
                return false;
            }

            // If it comes after a drawing
            if (!establecimiento_data) {
                establecimiento_data = {
                    "nombre": "Escuelas incluidas: "+votos_data.rows[0].num_loc
                };
                $("body").addClass("dibujo");
                //Overlay calculation
                var d = votos_data.rows;
                d.forEach(function(d) {
                    d.porc = (d.votos / d.positivos);
                });
            }
            else if (ctxt.selected_tab != "escuela") {
                // establecimiento_data is null
                var msg = "Escuelas incluidas: "+establecimiento_data.num_loc;
                establecimiento_data.nombre = msg;
                // For the crowdsourcing 
                $("body").addClass("dibujo");
            } else {
                $("body").removeClass("dibujo");
            }
            var tab = ctxt.selected_tab;
            var show_telegram = ctxt.selected_polling ? true: false;
            var ttip_data = {"poll": establecimiento_data,
                             "tab": tab,
                             "v": votos_data,
                             "dict_datos": config.diccionario_datos,
                             "vh": view_helpers,
                             "escuela": show_telegram};

            // If showing differences no overlay just popup
            if (ctxt.selected_tab == "difpaso" || 
                ctxt.selected_tab == "difpv") {
                // Remove unused party data
                ttip_data.v.rows = _.where(ttip_data.v.rows, 
                                           {id_partido: ctxt.selected_party});
                // Differences tooltip
                set_map_popup(latlng, popup_diff_tpl(ttip_data));
                return false;
            }
            // Feature tooltip
            set_map_popup(latlng, popup_perc_tpl(ttip_data));

            // Show the list of linked telegrams
            d3.select("div.telegramas").on("click", function(d) {
                if (ctxt.selected_polling) {
                    ga.fire_analytics_event("telegramas",ctxt.selected_polling);
                    var fid = ctxt.selected_polling;
                    config.sql.execute(templates.cdb_telegrams_sql,
                                       {"id": fid})
                    .done(function(data) {
                        var append_to = d3.select("#append");
                        var params = {"data": data.rows,
                                      "nombre": establecimiento_data.nombre,
                                      "vh": view_helpers,
                                      "preffix": ""};
                        append_to.html(telegram_tpl(params))
                                 .style("opacity", 0)
                                 .transition()
                                 .style("opacity", 1);
                        d3.select("#append div.cerrar").on("click", function(){
                            d3.select(".creVent")
                              .transition().style("opacity", 0)
                              .each("end", function(){append_to.html("");});
                        }, false);

                        //DocumentCloud embedded telegrams viewer
                        d3.selectAll(".dc_telegram").on("click", function(){
                            d3.select("div.creVent div.txts")
                                .classed("telegram_open", true);

                            // mark selected telegram
                            d3.selectAll("div.telegramas_wrapper .active")
                              .classed("active", false);
                            d3.select(this.parentNode).classed("active", true);
                            var $el = d3.select(this);

                            var id = $el.attr("id");
                            var append_to = d3.select("#dc_container");
                            var params = {"data": id,
                                          "vh": view_helpers};
                            append_to.html(dc_embed_tpl(params))
                                     .style({
                                        "width": "90%"
                                     });
                            }, false);

                    })
                    .error(function(errors) {
                        console.log(errors);
                    });
                }
            }, false);

            // Update overlay and open it up
            _self.overlay.update(votos_data.rows, establecimiento_data);
            _self.overlay.unfold();
        }

        function featureOver(e, latlng, pos, data, layerNumber) {
            $("#map_container").css("cursor", "pointer");
        }

        function featureOut(e) {
            $("#map_container").css("cursor", "auto");
        }


        /** Create or update a map popup depending 
        on context and current status */
        function set_map_popup(latlng, content) {
            if (!config.popup) {
                config.popup = L.popup();
            }
            if (config.popup._map) {
                config.popup.setLatLng(latlng).setContent(content).update();
            } else {
                config.popup.setLatLng(latlng).setContent(content).openOn(map);
            }
        }

        /** Initialize tab appearance based on context */
        function init_nav() {
            d3.select("body")
              .classed("escuela difpaso fuerza difpv", false);
            d3.selectAll(".btn").classed("on", false);
            var selector = ".btn#"+ctxt.selected_tab;
            $(selector).addClass("on");
            $("body").addClass(ctxt.selected_tab);
            if (ctxt.selected_tab != "escuela") {
                $("div.ayuFilt1").hide();
            }
            else {
                if (helpers.show_party_help()) {
                    $("div.ayuFilt1").fadeIn();
                }
                else {
                    $("div.ayuFilt1").hide();
                }
            }
        }

        /** Can be accessed on init or tab click */
        function update_nav() {
        /*jshint validthis: true */
            if (!this.classList.contains("on")) {
                d3.selectAll(".btn").classed("on", false);
                d3.selectAll(".btn").classed("visible", false);
                var $el = $(this); 
                $el.addClass("on");
                var btn_id = $el.attr("id").replace("#","");
                // Analytics
                ga.fire_analytics_event("click",btn_id);
                ctxt.selected_polling = null;
                ctxt.selected_hex = null;
                ctxt.w = null;
                ctxt.sw = null;
                ctxt.selected_tab = btn_id;
                // Control zoom issues with hexagons and helper text
                if (ctxt.selected_tab != "escuela") {
                    $("div.ayuFilt1").fadeOut();
                    if (ctxt.zoom > config.hex_zoom_threshold) {
                        map.setZoom(config.hex_zoom_threshold, 
                                    {"animate": false});
                    }
                    map.options.maxZoom = config.hex_zoom_threshold;
                    map.fire("zoomend", {forced: true});
                }
                else {
                    if (helpers.show_party_help()) {
                        $("div.ayuFilt1").fadeIn();
                    }
                    map.options.maxZoom = 18;
                    map.fire("zoomend", {forced: true});
                }
                d3.select("body")
                  .classed("escuela difpaso fuerza difpv", false);
                $("body").addClass(btn_id);
                switch (btn_id) {
                    case "escuela":
                        ctxt.selected_party = "0000";
                        break;
                    case "fuerza":
                        // defaults to winner party
                        ctxt.selected_party = "0000";
                        break;
                    case "difpaso":
                    case "difpv":
                        // defaults to winner party
                        if (ctxt.selected_party == "0000") {
                            ctxt.selected_party = "0135";
                        }
                        break;
                }
                permalink.set();
                // Always hide filters
                $(".btn_filt.sub").addClass("off");
                $(".btn_filt").removeClass("active");
                $(".refes").show();
                $(".filtros").hide();
                // Fire an update of the app
                _self.overlay.update_filter();
                map.closePopup();
                //_self.overlay.fold();
                cdb.update_layer();
                return false;
            }
        }

        //Remove drawing selection
        function remove_draw_layer(){
            var l = draw.drawnItems.getLayers();
            if (l.length){
                //only one layer allowed
                map.fire("draw:deletestart");
                draw.drawnItems.removeLayer(l[0]);
                map.fire("draw:deletestop");
                map.fire("draw:deleted");
            }
        }

/**************************** HTML EVENTS ***********************************/

        // filter buttons
        $(".short").click(function() {
            /*jshint validthis: true */
            map.closePopup();
            // To hide filters if we are on mobile
            var city = $(this).attr("id");
            // Google analytics
            ga.fire_analytics_event("shortcut", city);
            if (map.getZoom() >= config.cities[city].zoom) {
                move_to_position(config.cities[city].center,
                                 config.cities[city].zoom,
                                 true);
            } else {
                if (ctxt.selected_tab != "escuela") {
                    // TODO: Much better
                    ctxt.zoom = 14;
                    cdb.update_layer();
                }
                // wait to avoid bloated hex
                setTimeout(function(){ 
                    move_to_position(config.cities[city].center,
                                     config.cities[city].zoom,
                                     true);
                }, 500);
            }
            return false;
        });

        // Tab buttons
        $(".btn").click(update_nav);

        // Credits button
        $("#creditos").click(function() {
            var append_to = d3.select("#append");
            append_to.html(templates.creditos_html)
                     .style("opacity", 0)
                     .transition()
                     .style("opacity", 1);  
           
            $("#append").click(function() {
                d3.select(".creVent")
                  .transition().style("opacity", 0)
                  .each("end", function(){append_to.html("");});
                // Let the event bubble up to follow links
                //return false;
            });
            return false;
        });

        // Methodology button
        $("#metodo").click(function() {
            var append_to = d3.select("#append");
            append_to.html(templates.metodologia_html)
                     .style("opacity", 0)
                     .transition()
                     .style("opacity", 1);  
           
            $("#append").click(function() {
                d3.select(".creVent")
                  .transition().style("opacity", 0)
                  .each("end", function(){append_to.html("");});
                return false;
            });
            return false;
        });
        
        // Search button
        $(".lupa").click(function(){
            var $search = $("#searchbox");
            $("#buscar").toggleClass("activo");
            $search.toggleClass("invisible");
            if (!($search.hasClass("invisible"))) {
                $search.focus();
            }
            $search.val(null);
            return false;
        });

        // Crowdsource button
        $(".chequea").click(function(){
            $(".formu").toggleClass("on");
            return false;
        });

        // Mobile menu buttton
        $("#menu").click(function(){
            $("#escuela, #fuerza, #difpaso, #difpv").toggleClass("visible");
            return false;
        });

        /** crowdsource submit button */
        $("input#submit").click(function() {
            var comment = d3.select("textarea#msg").node();
            if (ctxt.selected_polling) {
                // Analytics
                ga.fire_analytics_event("crowdsource",ctxt.selected_polling);
                cdb.send_crowdsource(ctxt.selected_polling, comment.value);
            }
            comment.value = "";
            d3.select("div.formu").classed("on", false);
            return false;
        });

        // searchbox functionality
        $("#searchbox").autocomplete({
            minLength: 3,
            source: function( request, response ) {
                config.sql.execute(templates.search_sql,{q: request.term})
                .done(function(data) {
                    response(data.rows.map(function(r) {
                        return {
                            label: "("+r.localidad+") "+
                                   r.nombre+", "+r.direccion,
                            value: r.id_agrupado+" - ("+r.localidad+") "+
                                   r.nombre+", "+r.direccion
                        };
                    }));
                });
            },
            select: function( event, ui ) {
                ctxt.selected_polling = ui.item.value.split("-")[0].trim();
                ga.fire_analytics_event("search",ctxt.selected_polling);
                if (ctxt.selected_tab != "escuela") {
                    helpers.sim_click("div#escuela");
                }
                else {
                    ctxt.w = null;
                    ctxt.sw = null;
                    remove_draw_layer();
                    cdb.update_layer();
                }
                ctxt.selected_polling = ui.item.value.split("-")[0].trim();
                permalink.set();
                var id_agrupado = ctxt.selected_polling;
                config.sql.execute(templates.permalink_sql,
                                   {"id": id_agrupado})
                .done(function(data) {
                    var position = JSON.parse(data.rows[0].geo).coordinates;
                    var latlng = L.latLng(position[1], position[0]);
                    map.panTo(latlng);
                    var d = data.rows[0];
                    featureClickDone(latlng, d, data);
                });             
                $("#buscar").toggleClass("activo");
                $("#searchbox").toggleClass("invisible");
            }
        });

        // Draw helper text
        $("#help_draw").click(function() {
            config.show_draw_help = false;
            $("#help_draw").fadeOut();
            return false;
        });

        // party filters helper text
        $(".ayuFilt1").click(function() {
            config.show_party_help = false;
            $(this).fadeOut(100);
            return false;
        });

        // party winner filters helper text
        $(".ayuFilt").click(function() {
            config.show_data_help = false;
            $(this).fadeOut(100);
            return false;
        });

/**************************** MAP EVENTS ************************************/

        // Hide overlay if dragged position is out of bounds
        map.on("dragend", function(e) {
            if (config.popup !== null && 
                !map.getBounds().contains(config.popup.getLatLng())) {
                map.closePopup();
            }
            var cnt = map.getCenter();
            ctxt.lat = +(cnt.lat).toFixed(2);
            ctxt.lng = +(cnt.lng).toFixed(2);
            permalink.set();
        });

        map.on("zoomstart", function(e) {
            var prev_zoom_level = map.getZoom();
            config.prev_zoom_level = prev_zoom_level;
            if (ctxt.selected_hex) {
                map.closePopup();
            }
        });

        map.on("zoomend", function(e) {
            var current_zoom_level = map.getZoom();
            ctxt.zoom = current_zoom_level;
            // update layer only if needed
            if (ctxt.selected_tab != "escuela") {
                cdb.update_layer();
                if ((config.prev_zoom_level < current_zoom_level) && 
                    (current_zoom_level == config.hex_zoom_threshold)) {
                    // SHOW POPUP
                    var append_to = d3.select("#append");
                    append_to.html(templates.maxzoom_html).style("opacity", 0)
                             .transition().style("opacity", 1);  
                    d3.select("#append").on("click", function(){
                        d3.select(".creVent")
                          .transition().style("opacity", 0)
                          .each("end", function(){append_to.html("");});
                    }, false);

                    /** change view to polling stations for low zoom levels */
                    d3.select("div.cambianav").on("click", function(){ 
                        helpers.sim_click("div#escuela");
                    }, false);
                }
            }
            config.prev_zoom_level = current_zoom_level;
            permalink.set();
        });

        // Close popup and overlay
        map.on("popupclose", function(e) {
            remove_draw_layer();
            ctxt.selected_polling = null;
            ctxt.selected_hex = null;
            permalink.set();
            _self.overlay.fold();
        });

        /** DRAW LAYER EVENTS */
        map.on("draw:drawstart", function(e){
            // Remove helper text
            helpers.sim_click("div#help_draw");
            // Clear selected feature
            map.closePopup();
            draw.drawstart(e);
        });

        map.on("draw:drawstop", draw.drawstop);
        map.on("draw:deleted", draw_deleted);
        map.on("draw:created", draw_filter);
        map.on("draw:edited", draw_filter);
    });
});