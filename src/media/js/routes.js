(function() {

var dependencies;
/* dtrace */

// Please leave quotes around keys! They're needed for Space Heater.
var routes = [
    {'pattern': '^/$', 'view_name': 'apiplayground'}
];

dependencies = routes.map(function(i) {return 'views/' + i.view_name;});
/* /dtrace */
window.routes = routes;

define(
    'routes',
    // Dynamically import all the view modules from the routes
    dependencies,
    function() {
        for (var i = 0; i < routes.length; i++) {
            var route = routes[i];
            var view = require('views/' + route.view_name);
            route.view = view;
        }
        return routes;
    }
);

})();
