/** global configs */
var cfg = {
        cwd:'../webapp/',
        opt_path: '../webapp/opt',
        dest:'../build/',
        commit: Math.floor(Date.now() / 1000),
        prod_url: 'http://especiales.lanacion.com.ar/multimedia/proyectos/15/elecciones/elecciones_2015_arg_pv_escuelas/index.html',
        log: function(msg) {console.log(msg);}
    };

var js_min = 'all.v'+cfg.commit+'.min.js';
var libs_min = 'vendor.v'+cfg.commit+'.min.js';
var css_min = 'all.v'+cfg.commit+'.min.css';
var lib_jquery_min = 'jquery.min.js';
var lib_autocomplete_min = 'jquery-ui.min.js';

module.exports.cfg = cfg;
module.exports.js_min = js_min;
module.exports.libs_min = libs_min;
module.exports.css_min = css_min;
module.exports.lib_jquery_min = lib_jquery_min;
module.exports.lib_autocomplete_min = lib_autocomplete_min;