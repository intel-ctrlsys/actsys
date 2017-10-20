# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#

"""Sample of a GUI page generator to demonstrate the ease of adding a GUI."""
import cherrypy
class GuiWrapper(object):

    @cherrypy.expose
    def index(self):
        return """
        <html>
        <head>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
        <script type = "text/javascript" language = "javascript">

        $(document).ready(function(){
            $("#api_route").keypress(function(e) {
                if(e.keyCode==13) onButton();
            });
        });

        function onButton(){
            var url = window.location.protocol+"//"+window.location.hostname;
            var port = window.location.port;
            if (port != "") {
                url += ":"+port
            }
            var path = $("#api_route").val();
            url += "/api/" + path.split("/").slice(2).join('/');
            $.getJSON(url, function(data){
                var json_string = JSON.stringify(data, null, 4);
                $("#url").text(url);
                $("#response").text( json_string );
            });
        };
        </script>
        </head>
        <body>
        <form>
        API Route: <input type="text" id=api_route value="" placeholder="Enter API Route Here"><br>
        <button type="button" id="go_button" onclick=onButton()>GO!!</button>
        <div id="url">
        </div>
        <pre id="response">
        </pre>
        </body>
        </html>
        """
