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
                if (ctxt.selected_tab.startsWith("dif")) {
                    if (ctxt.selected_party == d.id_partido) {
                        return false;
                    } else {
                        ctxt.selected_party = d.id_partido;
                        // Analytics
                        ga.fire_analytics_event("partido",ctxt.selected_party);
                    }
                } 
                else {
                    // Always clean filters
                    $(".btn_filt.sub").addClass("off");
                    $(".btn_filt").removeClass("active");
                    
                    if (ctxt.selected_party != d.id_partido){
                        ctxt.selected_party = d.id_partido;
                        // Analytics
                        ga.fire_analytics_event("partido",ctxt.selected_party);
                        // Hide references
                        $(".refes").hide();
                        $(".filtros").fadeIn(100);
                    } 
                    else {
                        // Reset filters
                        ctxt.w = null;
                        ctxt.sw = null;
                        ctxt.selected_party = "0000";
                        // Show references
                        $(".filtros").fadeOut(100);
                        $(".refes").show();
                    }
                }
                
                // Set permalink
                permalink.set();
                _self.update_filter();
                // We moved this to the cartodb loaded event
                //_self.update_ref();
                _self.fold();
                _self.map.closePopup();
                // Get new query, cartocss and interactivity
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
        // Updated selected party based on context
        _self.update_filter();
        // Updated selected party based on context
        _self.update_ref();
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

    Overlay.prototype.update_ref = function() {
        switch (ctxt.selected_tab) {
            case 'difpaso':
            case 'difpv':
                d3.select("#hexdif_1").style("fill", helpers.get_party_color());
                break;
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

    return Overlay;
});