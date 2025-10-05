

        $(document).ready(function() {

            var socket = io();
            var graphData = {xvals: graphs[0].x, yvals: [graphs[0].y, graphs[1].y, graphs[2].y]};
            var count_hour = 0;
            

            socket.on('connect', function() {
                socket.emit('my_event', {data: 'I\'m connected!'});
                socket.emit('my_event', graphs[2].y);
                
            });

            socket.on('setInitial',  function(data) {
                console.log(data)
              
            });

            socket.on('updateValue',  function(data) {
                socket.emit('my_event', data);

                graphData.yvals[2].push(data/1000);
                

                
                if (graphData.yvals[2].length > 24) {
                      graphData.yvals[2].shift();
                      graphData.yvals[0].push(data);
                      graphData.yvals[0].shift();
                      graphData.yvals[1].push(350-data);
                      graphData.yvals[1].shift();
                      }

                Plotly.update('chart', { x: graphData.xvals, y: graphData.yvals });
              
            });


         });
