Frontend usage
==============

## Requirements
* Have [_nodejs_](https://nodejs.org/) && [_bower_](http://bower.io/) installed

## Process
1. Go to the server folder

        $ cd server

2. Install dependencies

        $ npm install && bower install

3. Run the local server

        $ gulp

4. Open a browser on **http://localhost:8000** and play around. The server is using livereload so that any changes on the js or html files will be automatically published to the server.

## Implementation notes

### Leaflet draw plugin

* We wanted to let the reader *select one and only one* draw shape The original [_leaflet draw plugin_](https://github.com/Leaflet/Leaflet.draw) we have found the following [issue](https://github.com/Leaflet/Leaflet.draw/issues/315) with the idea to switch the drawing controls so that the user can only generate one shape at a time. We have found that in the switching process a reference was lost while firing disable events and gave a javascript error since the error was due to the removed control we have tweaked it so that it checks if the reference is still there and ignores it otherwise.

    ```js
    //On the L.EditToolbar _save method
    _save: function () {
        this._activeMode.handler.save();
        // Not sure why we need this hack but we do need it
        // Probably due to the switching process of drawcontrols in 
        // draw:deleted 
        if (this._activeMode) {
            this._activeMode.handler.disable();
        }
    },
    ```

* Allowing only one drawing at a time restricts the functionality of the draw plugin. Since our interaction is much simpler we wanted to provide an easier way to delete drawings so that it involved only one user interaction instead of the original 3 interactions in the plugin code. All our changes are marked with **MAF Change** for example:

    ```js
    _removeLayer: function (e) {
        var layer = e.layer || e.target || e;
        this._deletableLayers.removeLayer(layer);
        //MAF Change: Dust bin deletes drawings. We don't need to store deleted layers for recovering. We simulate the save button.
        // this._deletedLayers.addLayer(layer);
        layer.fire('deleted');
        this.save();
    },
    ```