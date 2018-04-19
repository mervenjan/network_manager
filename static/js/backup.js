$(function () {
        $('#backup_all').click(function () {
            var socket = new WebSocket("ws://" + window.location.host + "/backup_network_config/");
            socket.onopen = function () {
                console.log('WebSocket open');//成功连接上Websocket
                socket.send($('#tftp_host').val());//发送数据到服务端
            };
            socket.onmessage = function (e) {
                console.log('message: ' + e.data);//打印服务端返回的数据
                $('#messagecontainer').prepend('<p><pre>' + e.data + '</pre></p>');
            };
        });
    });