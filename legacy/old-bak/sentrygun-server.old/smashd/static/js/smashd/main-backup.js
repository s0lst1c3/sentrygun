current_alerts = []
alert_even = false;
protocol = 'http'

alert_handler = function(message) {

	current_alerts.push(message['data']);

	var row_class = alert_even ? 'even-selectable' : 'odd-selectable';
	alert_even = !alert_even;
	
	var data = message['data'];
	var next_row = ['<tr class="',
						row_class,
						'"><td>',
						data['type'],
						'</td><td>',
						data['device'],
						'</td><td>',
						data['bssid'],
						'</td><td>',
						data['essid'],
						'</td><td>',
						data['channel'],
						'</td><td>',
						data['details'],
						'</td><td>',
						new Date(parseInt(data['timestamp']*1000)).toLocaleString(),
						'</td></tr>'].join('');

	// add button to dismiss
	$('#alertbody').append(next_row);
}

$(document).ready(function() {

	// setup page -------------------------------------------------------------
	$('.sel-table>tbody').bind('mousedown', function(e) {

		e.metaKey = true;
	}).selectable({
		filter: 'tr',
		cancel: 'a'
	});

	webcli_connect();

	// setup socketio ---------------------------------------------------------

	namespace = '/watchdog'

	sock_uri = [protocol,
		'://',
		document.domain,
		':',
		location.port,
		namespace].join('');
	
	var socket = io.connect(sock_uri);

	// socketio events --------------------------------------------------------

	socket.on('connect', function() {
		socket.emit('connected');
	});

	socket.on('dismiss alert', on_alert_dismiss);
	
	socket.on('add alert', on_alert_add);

	// dom events -------------------------------------------------------------

	$('.nav-button').click(function() {

		socket.emit('disconnect request');
		
	});

	$('.dismiss-button').click(dismiss_alert);
});
