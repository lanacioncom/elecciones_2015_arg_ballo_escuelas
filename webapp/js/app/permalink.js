define(['app/context'], function(ctxt){

    function set(share){
        var context;
        if (share) {
            var ctxtbis = ctxt.clone();
            c = min2share(ctxtbis);
            context = c.replace(/\"|\{|\}/g, '')
                       .replace(/,/g, "&")
                       .replace(/:/g, "=");
        } else {
            var c = JSON.stringify(ctxt);
            context = c.replace(/\"|\{|\}/g, '')
                       .replace(/,/g, "&")
                       .replace(/:/g, "=");
        }
        location.hash = context;
    }

    function get(u){
        /*jshint evil:true */
        u = u ? u : location.hash.replace("#", "");
        if(u){
            u = u.split(/\&/);
            u.forEach(function(c, i){
                c = c.split("=");
                var re = /^([1-9]\d*\.?\d+|true|false|null|0\.\d+)$/;
                if (re.test(c[1])) {
                    ctxt[c[0]] = eval(c[1]);
                }
                else {
                    ctxt[c[0]] = c[1];
                }
            });
        }
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
    function min2share(){
        
    }

    return {
        get: get,
        set: set,
        validate: validate,
        min2share: min2share

    };
});