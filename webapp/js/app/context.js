/** Stores the status of the app
    Used as permalink and sharing purposes */
define({
/*************************** APP STATUS *****************************/
    // Used to set the political party
    selected_party: "0000",
    // Used to set the tab of the visualization
    selected_tab: "escuela",
    // Used to store the selected polling station
    selected_polling: null,
    // Used to store the selected hexagon
    selected_hex: null,
    // Used to filter polling stations by result once a party is selected
    w: null,
    // Used to filter polling stations by change once a party is selected
    sw: null,
/*************************** MAP STATUS *****************************/
    // Map zoom
    zoom: 4,
    // Map latitude
    lat: -40.647,
    // Map longitude
    lng: -62.139
});