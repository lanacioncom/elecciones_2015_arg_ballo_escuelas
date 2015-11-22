define(['app/context', 'app/config', 'app/analytics'], function(ctxt, config, ga) {

    function activate_share (url_parent){
        var txt_share = "Mirá los resultados de mi búsqueda en el mapa de elecciones de @LANACION";
        // var _self = this; 
        /** share */
        $("#compartir").click(function(){
            $("#share").fadeIn(100);
            ga.fire_analytics_event('click','btn_compartir'); 
        });

        $("#facebook").click(function(){
            myPopup('https://www.facebook.com/sharer/sharer.php?u=' + get_url_to_share());
            ga.fire_analytics_event('click','facebook');
        });

        $("#twit").click(function(){
            myPopup('http://twitter.com/share?text='+txt_share+'&url='+ get_url_to_share() +'&hashtags=elecciones2015');
            ga.fire_analytics_event('click','twitter');
        });

        $("#google").click(function(){
            myPopup('https://plus.google.com/share?url=' + get_url_to_share());
            ga.fire_analytics_event('click','google+');
        });

        $("#mail").click(function(){
            $(this).attr("href" , "mailto:?subject=Resultados por escuela ballottage 2015 La Nación&body="+txt_share+" --> " + get_url_to_share());
            ga.fire_analytics_event('click','mail');
        });

        function myPopup(url) {
            var alto = $(window).height();
            window.open( url, "Compartir", "status = yes, height = 360, width = 500, resizable = yes, left = 450, top =" +(alto/2) );
            return false;
        }

        function get_url_to_share(){
            // TODO
            console.log(config.url_parent);
            // parent url - REPLACE WITH THE URL FOR PYM
            url_parent = url_parent ? url_parent : location.href.split("#")[0];
            var url = url_parent.split("?")[0]; 
            // var h = location.hash.replace('#', '');
            var h = helpers.permalink.get_short_hash();
            // console.log(encodeURI(url +"?l="+ h));
            var s = (url ? url : document.URL) +"?" +h;
            return encodeURIComponent(s);
        }
    }

    return {
        'activate_share': activate_share
    };
});