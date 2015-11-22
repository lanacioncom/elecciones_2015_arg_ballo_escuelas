define(['app/context'], function(context){

    function set(){
        var ctxt = JSON.stringify(context);
        ctxt = ctxt.replace(/\"|\{|\}/g, '')
                   .replace(/,/g, "&")
                   .replace(/:/g, "=");
        location.hash = ctxt;
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
                    context[c[0]] = eval(c[1]);
                }
                else {
                    context[c[0]] = c[1];
                }
            });
        }
    }

    /** Validate permalink status */
    function validate(){
        if ((context.selected_tab == 'difpaso' ||
            context.selected_tab == 'difpv') &&
            context.selected_party == "0000") {
            context.selected_party = "0131";
            set();
        }
    }

    return {
        get: get,
        set: set,
        validate: validate
    };
});