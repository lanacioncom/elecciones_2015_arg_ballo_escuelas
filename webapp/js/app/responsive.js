define(['app/context', 'app/config'], function(ctxt, config) {

    function is_small_screen() {
        return config.screen_width <= 768 ? true : false;
    }

    return {
        set_media_zoom: function() {
            config.screen_width = $("body").width();
            ctxt.zoom = is_small_screen() ? 9 : 10;
        },
        init: function() {
            if (is_small_screen()) {
                config.show_draw_help = false;    
            }
        },
        is_small_screen: is_small_screen
    };
});