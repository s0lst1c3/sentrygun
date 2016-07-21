protocol = 'http'

$(document).ready(function() {

	// setup page -------------------------------------------------------------
	init_selectable();

	get_all_alerts();

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

	//socket.on('connect', on_connect);

	socket.on('dismiss alerts', on_alert_dismiss);
	
	socket.on('add alert', on_alert_add);

	// dom events -------------------------------------------------------------

	$('.nav-button').click(request_disconnect);

	$('.dismiss-button').click(dismiss_alerts);
	
	$(document).on('submit', 'form', on_form_submit);
});
