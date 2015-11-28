define(['app/context'], function(ctxt){


    function set(){
        location.hash = min2share();
    }


    /** Validate permalink status */
    function validate(){
        if ((ctxt.selected_tab == 'difpaso' ||
            ctxt.selected_tab == 'difpv') &&
            ctxt.selected_party == "0000") {
            ctxt.selected_party = "0135";
            set();
        }
    }

    /** Minimize the url to share in social networks */
    var ctxtDict = {
        toShort: {
            selected_party: "sp",
            selected_tab: "st",
            selected_polling: "se",
            selected_hex: "sh",
            w: "w",
            sw: "sw",
            zoom: "z",
            lat: "lt",
            lng: "lg"
        },
        toLong: {
            sp : 'selected_party',
            st : 'selected_tab',
            se : 'selected_polling',
            sh : 'selected_hex',
            w : 'w',
            sw : 'sw',
            z : 'zoom',
            lt : 'lat',
            lg : 'lng'
        }
    };

    /** Get url data and store it in the app context */
    function get(u){
    /*jshint evil:true */
        var re = /^([1-9]\d*\.?\d+|true|false|null|0\.\d+)$/;
        
        // If a URL is passed use that, use the location hash otherwise
        u = u ? u : location.hash.replace("#", "");
        if(u){
            u = u.split(/\&/);
            u.forEach(function(c, i){
                c = c.split("=");
                
                var key_long = ctxtDict.toLong[c[0]];
                
                if(c[1]){
                    if (re.test(c[1])) {
                        ctxt[key_long] = eval(c[1]);
                    }
                    else {
                        ctxt[key_long] = c[1];
                    }
                }
                else {
                    ctxt[key_long] = null;
                }
            });
        }
    }

    /** minimizes the context data to set the permalink of the app */
    function min2share(){
        var ctxtMin = {};
        
        for (var k in  ctxt){
            var key_short = ctxtDict.toShort[k];
            ctxtMin[key_short] = ctxt[k];
            if(!key_short){
                console.log("Esta key del contexto no esta definida"+
                            " en el diccionario: %s", k);
            }
        }

        return $.param(ctxtMin);
    }

    return {
        get: get,
        set: set,
        validate: validate,
        min2share: min2share

    };
});