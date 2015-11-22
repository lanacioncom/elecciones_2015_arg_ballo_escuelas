define(['app/context'], function(ctxt) {

    function fire_analytics_event(action, data){
        _gaq.push(['_trackEvent','elecciones_2015_arg_ballo_escuelas',
                   action, data]);
    }

    return {
        'fire_analytics_event': fire_analytics_event
    };
});