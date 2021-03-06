define(['app/context', 'app/config'],

function(ctxt, config) {

    function is_empty(str) {
        return (!str || 0 === str.length);
    }
    
    return {
        animate_barras: function() {
            var w_content = $(".cont_barra").width();
            $("#overlay .cont_barra .barra").each(function(i, el){
                var $el = $(this);
                var w = parseFloat($el.data("width"));
                w =  w_content*w/100 + "px";
                $el.animate({width: w});
            });
        },
        zero_pad: function(num, size) {
            var s = "00000" + num;
            return s.substr(s.length-size);
        },
        get_party_colors: function() {
            var pid = ctxt.selected_party;
            var rango = config.diccionario_datos[pid].rango.slice(0);
            return rango.reverse();
        },
        get_party_color: function() {
            return config.diccionario_datos[ctxt.selected_party].color_partido;
        },
        is_empty: is_empty,
        selected_feature: function() {
            if ((!is_empty(ctxt.selected_hex)) ||
                (!is_empty(ctxt.selected_polling))) {
                return true;
            }
            return false;
        },
        sim_click: function(selector) {
            // Simulate a click on an existing element
            // If there are many pick the first one.
            var a_selector = $(selector);
            if (a_selector.length) {
                a_selector[0].click();
            }
        },
        show_party_help: function() {
            if (ctxt.selected_tab == "escuela" && 
                ctxt.selected_party == "0000" &&
                config.show_party_help) {
                return true;
            }
            return false;
        },
        data_filtered: function() {
            if ((!is_empty(ctxt.w))|| 
                (!is_empty(ctxt.sw))) {
                return true;
            }
            return false;
        }
    };
});