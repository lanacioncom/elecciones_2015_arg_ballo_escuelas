/** global configs */
var cfg = {
        cwd:'../webapp/',
        opt_path: '../webapp/opt',
        dest:'../build/',
        commit: Math.floor(Date.now() / 1000),
        prod_url: 'http://especiales.lanacion.com.ar/multimedia/proyectos/15/elecciones/elecciones_2015_arg_ballo_escuelas/index.html',
        log: function(msg) {console.log(msg);}
    };

var js_min = 'all.v'+cfg.commit+'.min.js';
var libs_min = 'vendor.v'+cfg.commit+'.min.js';
var lib_cartodb_min = 'cartodb.js';
var css_min = 'all.v'+cfg.commit+'.min.css';

module.exports.cfg = cfg;
module.exports.js_min = js_min;
module.exports.libs_min = libs_min;
module.exports.lib_cartodb_min = lib_cartodb_min;
module.exports.css_min = css_min;