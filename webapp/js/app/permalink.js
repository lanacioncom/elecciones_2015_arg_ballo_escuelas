define(['app/context'], function(ctxt){


    function set(share){
        var context;
        min2share();
        if (share) {
            var ctxtbis = ctxt.clone();
            c = min2share();
            context = c.replace(/\"|\{|\}/g, '')
                       .replace(/,/g, "&")
                       .replace(/:/g, "=");
        } else {
            var c = JSON.stringify(ctxt);
            context = c.replace(/\"|\{|\}/g, '')
                       .replace(/,/g, "&")
                       .replace(/:/g, "=");
        }

        location.hash = $.param(min2share());
    }


    /** Validate permalink status */
    function validate(){
        if ((ctxt.selected_tab == 'difpaso' ||
            ctxt.selected_tab == 'difpv') &&
            ctxt.selected_party == "0000") {
            ctxt.selected_party = "0131";
            set();
        }
    }

    /** Minimize the url to share in social networks */
    var ctxtDict = {
        toShort: {
            selected_party: "sp",
            selected_tab: "st",
            selected_polling: "sp",
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
            sp : 'selected_polling',
            sh : 'selected_hex',
            w : 'w',
            sw : 'sw',
            z : 'zoom',
            lt : 'lat',
            lg : 'lng'
        }
    };

    function get(u){
        /*jshint evil:true */
        u = u ? u : location.hash.replace("#", "");
        if(u){
            u = u.split(/\&/);
            u.forEach(function(c, i){
                c = c.split("=");
                var re = /^([1-9]\d*\.?\d+|true|false|null|0\.\d+)$/;
                var key = ctxtDict.toLong[c[0]];
                if (re.test(c[1])) {
                    ctxt[key] = eval(c[1]);
                }
                else {
                    ctxt[key] = c[1];
                }
            });
        }
    }

    function min2share(){
        var ctxtMin = {};
        
        for (var k in  ctxt){
            var key = ctxtDict.toShort[k];
            ctxtMin[key] = ctxt[k];
            if(!ctxtDict.toShort[k]){
                console.log("Esta key del contexto no esta definida en el diccionario: %s", k);
            }
        }

        return ctxtMin;
    }

    return {
        get: get,
        set: set,
        validate: validate,
        min2share: min2share

    };
});