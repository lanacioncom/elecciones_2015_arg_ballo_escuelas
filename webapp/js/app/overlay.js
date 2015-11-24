/** overlay app */
define(['app/context', 'app/config', 'app/permalink',
        'app/analytics', 'app/carto',
        'app/templates', 'app/helpers', 'app/view_helpers'], 
        function(ctxt, config, permalink, ga, cdb, 
                 templates, helpers, view_helpers){
    var Overlay = function(map){
    "use strict";
        var _self = this;
        _self.map = map;
        _self.anchoWrapper = $(window).width();
        _self.ayuda.init();
        _self.create();
    };

    var resta;
    Overlay.prototype.create = function(){
        /** update overlay */
        var _self = this;

        var ul = d3.select('ul#overlay_li_content');
        var overlay_tpl = _.template(templates.overlay_html);
        
        // Initial results
        results = config.initial_data.results;
        polling_totals = config.initial_data.polling_totals;

        var max = results[0].porc;

        var li = ul.selectAll("li.candidato")
            .data(results, function(d){ return d.id_partido;});

        li.enter().append("li")
            .attr("class", "candidato")
            .attr('id', function(d){
                return "li_"+d.id_partido;
            })
            .html(function(d){
                return overlay_tpl({
                        d: d,
                        vh: view_helpers,
                        dict_datos: config.diccionario_datos,
                        max: max
                });
            })
            .on("click", function(d){
                // Has to have one party selected
                if (ctxt.selected_tab.startsWith("dif")) {
                    if (ctxt.selected_party == d.id_partido) {
                        return false;
                    } else {
                        ctxt.selected_party = d.id_partido;
                        // Analytics
                        ga.fire_analytics_event("partido",ctxt.selected_party);
                    }
                } 
                else if (ctxt.selected_tab == "fuerza"){
                    if (ctxt.selected_party != d.id_partido){
                        ctxt.selected_party = d.id_partido;
                    } 
                    else {
                        ctxt.selected_party = "0000";
                    }
                } 
                else {
                    config.show_party_help = false;
                    $("div.ayuFilt1").fadeOut();
                    if (ctxt.selected_party != d.id_partido){
                        ctxt.selected_party = d.id_partido;
                        // Analytics
                        ga.fire_analytics_event("partido",ctxt.selected_party);
                        // Hide references
                        $(".refes").fadeOut(100);
                        $(".filtros").fadeIn(100);
                    } 
                    else {
                        // Reset filters
                        ctxt.w = null;
                        ctxt.sw = null;
                        ctxt.selected_party = "0000";
                        // Show references
                        $(".filtros").fadeOut(100);
                        $(".refes").fadeIn(100);
                    }
                }
                
                // Set permalink
                permalink.set();
                _self.update_filter();
                _self.map.closePopup();
                // Get new map data
                cdb.update_layer();
            });

        // Set height
        var li_height;
        if(_self.anchoWrapper < 450){
            li_height=72;
        }else{
            li_height=78;
        }

        li.style("top", function( d, i){
            return li_height * i + "px";
        });

        
        if(_self.anchoWrapper < 450){
            resta = 55;
        }else{
            resta = 95;
        }
        
        // Once the hidden overlay is filled show only in folded mode
        var $overlay = $('#overlay');
        var por_hidden = $overlay.width() - resta;
        $overlay.animate({right:-por_hidden},'fast');
        // Updated selected party status based on context
        _self.update_filter();
    };



    Overlay.prototype.fold = function() {
        var $overlay = $('#overlay');
        d3.selectAll("li.candidato").classed('active', false);
        var por_hidden = $overlay.width() - resta;
        $overlay.animate({right:-por_hidden},'fast');
        this.update();
        $overlay.removeClass("activo");
        $(".formu").removeClass("on");
    };

    Overlay.prototype.unfold = function (){
        var $overlay = $('#overlay');
        $overlay.animate({right:'0%'}, 'fast', function(){
            //helpers.animate_barras();
        }); 
        $overlay.addClass("activo");
    };

    Overlay.prototype.update = function(results, polling_totals){
        /** update overlay */
        var _self = this;

        var ul = d3.select('ul#overlay_li_content');
        // Initial configuration
        if (!results) {
            results = config.initial_data.results;
            polling_totals = config.initial_data.polling_totals;
        }
        var max = results[0].votos;

        // Update results
        var li = ul.selectAll("li.candidato")
            .data(results, function(d){ return d.id_partido;});

        // Update visual status
        var w_content = $(".cont_barra").width() * 0.75;

        li.each(function(d, i){
            var el = d3.select(this);
            el.select(".porc").html(view_helpers.get_formatted_num(d.porc*100,1) + "%");
            el.select(".votos").html(view_helpers.get_formatted_num(d.votos,0) + " votos");
            // update width bars TODO
        });

        var li_height = null;
        if(_self.anchoWrapper < 450){
            li_height=72;
        }else{
            li_height=78;
        }
        
        li.transition().duration(600)
            .style("top", function( d, i){
                return li_height * i + "px";
            })
            .each('end', function(d){
                var el = d3.select(this);
                // update width bars
                var bar_w = (+d.votos / +max)*w_content;
                el.select(".barra").transition().duration(500).style("width", bar_w+"px");
                el.select(".porc").html(view_helpers.get_formatted_num(d.porc*100,1) + "%");
                el.select(".votos").html(view_helpers.get_formatted_num(d.votos,0) + " votos");

            });
        // update selected party visually
        _self.update_filter();
    };

    Overlay.prototype.update_filter = function() {
        var pid = ctxt.selected_party;
        var ul = d3.select('ul#overlay_li_content');
        ul.selectAll("li.candidato").classed('active', false);
        if (ctxt.selected_party != "0000") {
            ul.classed('filter', true);
            ul.select("#li_"+pid).classed('active', true);
        }else {
            ul.classed('filter', false);
        }
    };


    Overlay.prototype.update_overlay_height = function( li_size ){
        var height_header_overlay = $("#contet_header_overlay").height();
        var wrapper = $("div#wrapper_ul_overlay"),
        h = $("#mapa_cont").height() - heigth_header_overlay;
        wrapper.height(h);
    };

    //* Update references and data filters if needed */
    Overlay.prototype.update_ref = function() {
        var _self = this;
        if (ctxt.selected_tab.startsWith("dif")) {
            d3.select("#hexdif_1").style("fill", helpers.get_party_color());
            $(".refes").show();
            $(".filtros").hide();
        }
        else if (ctxt.selected_tab == 'fuerza') {
            var data = helpers.get_party_colors();
            d3.select(".porcentajes").selectAll("polygon")
              .data(data)
              .style("fill", function(d) {return d;});
            $(".refes").show();
            $(".filtros").hide();
        } 
        else {
            // If we have a party selected toggle filters or references
            if (ctxt.selected_party == '0000') {
                $(".refes").show();
                $(".filtros").hide();
            } else {
                $(".refes").hide();
                update_data_filters();
                $(".filtros").show();
            }
        }
    };


    Overlay.prototype.ayuda = {
        'init': function(){ 
            var help = this; 
            $(".ayuda_overlay").on("click", function(){
                help.remove(); 
                return false;
            }); 
        },
        'update_position': function(){
            var $help = $(".ayuda_overlay");
            if($help.length){
                var $ul = $("ul#overlay_ul");
                var pos = $ul.offset();
                
                var left = $help.width() + -8,
                    top = ($('li:first-child', $ul).height() / 2 ) - 25;
                
                var window_width = $(window).width();
                
                if (window_width <= 768){
                    this.remove();
                    
                } else if (window_width <= 850) { 
                    top -= 60;
                    left += 20;
                } else if (window_width <= 1103){
                    left += 20;
                }
                
                $help.css('top', pos.top + top);
                $help.css('left', -left);
                
            }
        },
        'hide': function (){
            var $help = $(".ayuda_overlay");
            $help.fadeOut();
        },
        'show': function() {
            var $help = $(".ayuda_overlay");
            $help.fadeIn();

        },
        'remove': function(){
            var $help = $(".ayuda_overlay");
            $help.remove();
        }
    };

    /************** EVENTOS HTML **************************/
    $(".ayuFilt").click(function() {
        $(this).fadeOut(100);
    });

    /** filters when a candidate is selected */
    $("div.btn_filt").click(function(){
        $el = this;
        //Get rid of hint
        $(".ayuFilt").fadeOut(); 

        switch($el.dataset.key) {
            case 'w':
                ctxt.sw = null;
                if (!$el.classList.contains("active")) {
                    ctxt.w = "1";
                } else {
                    ctxt.w = null;
                }
                break;
            case 'wall':
                // Ignore if elements is selected
                if (!($el.classList.contains("off"))) return false;
                ctxt.w = "1";
                ctxt.sw = null;
                break;
            case 'wnew':
                // Ignore if elements is selected
                if (!($el.classList.contains("off"))) return false;
                ctxt.w = "1";
                ctxt.sw = "1";
                break;
            case 'wold':
                // Ignore if elements is selected
                if (!($el.classList.contains("off"))) return false;
                ctxt.w = "1";
                ctxt.sw = "0";
                break;
            case 'l':
                ctxt.sw = null;
                if (!$el.classList.contains("active")) {
                    ctxt.w = "0";
                } else {
                    ctxt.w = null;
                }
                break;
            case 'lall':
                // Ignore if elements is selected
                if (!($el.classList.contains("off"))) return false;
                ctxt.w = "0";
                ctxt.sw = null;
                break;
            case 'lnew':
                // Ignore if elements is selected
                if (!($el.classList.contains("off"))) return false;
                ctxt.w = "0";
                ctxt.sw = "1";
                break;
            case 'lold':
                // Ignore if elements is selected
                if (!($el.classList.contains("off"))) return false;
                ctxt.w = "0";
                ctxt.sw = "0";
                break;
        }
        ctxt.selected_polling = null;
        ctxt.selected_hex = null;
        permalink.set();
        update_data_filters();
        // Get new map data
        cdb.update_layer();

        return false;
    });

    function update_data_filters() {
        var key, sub_key;
        if (helpers.is_empty(ctxt.w)) {
            // Reset data filters
            $(".btn_filt[data-key='w']").removeClass("active");
            $(".btn_filt[data-key='l']").removeClass("active");
            //Clear all subfilters
            $(".btn_filt.sub").addClass("off");
        }
        else {
            // First clear all subfilters
            $(".btn_filt.sub").addClass("off");
            // Activate the corresponding data filter && sub_filter
            key = (+ctxt.w) ? 'w' : 'l';
            nokey = (+ctxt.w) ? 'l' : 'w';
            if (helpers.is_empty(ctxt.sw)) {
                sub_key = key+'all';
            } else {
                sub_key = (+ctxt.sw) ? key+'new' : key+'old';
            }
            update_key_filter(key);
            update_sub_key_filter(sub_key);
        }

        //** Updates the class of the filter to activate it*/
        function update_key_filter(key) {
            var nokey = (key == "w") ? 'l': 'w';
            $(".btn_filt[data-key='"+key+"']").addClass("active");
            $(".btn_filt[data-key='"+nokey+"']").removeClass("active");
        }

        //** Updates the class of the subfilters to activate it*/
        function update_sub_key_filter(sub_key) {
            $(".btn_filt.sub[data-key='"+sub_key+"']").removeClass("off");
        }
    }

    return Overlay;
});