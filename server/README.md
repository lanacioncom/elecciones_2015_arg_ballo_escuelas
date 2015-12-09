Server usage
============

## Introduction

We use gulp to launch our development web server using live reloading of assets.

We also use gulp tasks in order to optimize, minimify, uglify and build our app.

We have used the [_gulp-requirejs_](https://www.npmjs.com/package/gulp-requirejs) node package to integrate the requirejs optimization in our gulp deployment process.

## Requirements
* Have [_nodejs_](https://nodejs.org/) && [_bower_](http://bower.io/) installed

## Local webserver process

1. Go to the server folder

        $ cd server

2. Install dependencies

        $ npm install && bower install

3. Run the local server

        $ gulp

4. Open a browser on **http://localhost:8080** and play around. The server is using livereload so that any changes on the js, css or html files will be automatically refreshed.


## Build process
1. Go to the server folder

        $ cd server

2. Install dependencies (_if you didn't already_)

        $ npm install && bower install

3. Run the build process

        $ gulp build

4. Test results serving from the build folder

        $ gulp server_prod

5. Open a browser on **http://localhost:9000** and check that everything looks fine

## Implementation notes

* We are using a timestamp to version both css and javascript minified files

* This project uses require.js to help modularize our javascript files, the build process includes a call to _ropmitize_ the optimizer that require.js provides to prepare a project for production environments
