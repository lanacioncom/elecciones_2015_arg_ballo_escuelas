define(['app/context', 'app/config'], function(ctxt, config) {

    function is_small_screen() {
        return config.screen_width < 700 ? true : false;
    }

    return {
        set_media_zoom: function() {
            config.screen_width = $("body").width();
            ctxt.zoom = is_small_screen() ? 9 : 10;
        },
        // close_slide: function() {
        //     $('#results').animate({right:'0%'},'fast', function(){
        //         // $('#results').html('');
        //         if (config.screen_width > 550) {
        //             $('.leaflet-popup-pane *').hide();
        //         }
        //     });
        // },
        is_small_screen: is_small_screen
    };
});