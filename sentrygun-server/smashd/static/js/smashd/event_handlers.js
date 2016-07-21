current_alerts = {

	storage : {},
	add : function(new_alert) {

		alert_id = new_alert['id'];

		console.log(alert_id);

		if (!(alert_id  in this.storage) || this.storage[alert_id] === 0) {

			this.storage[alert_id] = 0;
			this.create_collapsible(new_alert);
		}
		this.storage[alert_id]++;
		console.log(this.storage[alert_id]);
		this.add_to_collapsible(new_alert);

		//alert_location = new_alert['location'];
		//if (!(alert_location in this.storage) || this.storage[alert_location] === 0) {

		//	this.storage[alert_location] = 0;
		//	this.create_collapsible(alert_location);
		//}
		//this.storage[alert_location]++;
		//console.log(this.storage[alert_location]);
		//this.add_to_collapsible(new_alert);
		//this.notify();
	},
	remove : function(a) {

		this.remove_from_collapsible(a);
		//this.storage[alert_location]--;
		//console.log(this.storage[alert_location]);
		//if (this.storage[alert_location] === 0) {

		this.destroy_collapsible(a['id']);
		//}
	},
	create_collapsible : function(a) {

		console.log('swag');

		alert_id = a['id'];
		ssid = a['essid'];
		bssid = a['bssid'];
		channel = a['channel'];
		intent = a['intent'];

		$('#set').append('<div data-role="collapsible" class="'+alert_id+'"><h3>'+ssid+' '+bssid+' '+channel+' '+intent+'</h3><p></p></div>').collapsibleset('refresh');
	
		$('.'+alert_id+' p').append('<div class="tablewrap"></div>');
		$('.'+alert_id+' .tablewrap').append('<div class="overflower"></div>');
		$('.'+alert_id+' .overflower').append('<form data-ajax="false" class="'+alert_id+'form"></form>');
		$('.'+alert_id+' form').append('<span class="tablespan"></span>');
		//$('.'+alert_location+' .tablespan').append('<table data-role="table" class="ui-responsive table-stroke"></table>');
		$('.'+alert_id+' .tablespan').append('<table data-role="table" class="sel-table ui-responsive table-shadow"></table>');
		$('.'+alert_id+' .tablespan table').append('<thead></thead>');
		$('.'+alert_id+' .tablespan table').append('<tbody id="'+alert_id+'"></tbody>');
		$('.'+alert_id+' thead').append('<th>Device</th>');
		$('.'+alert_id+' thead').append('<th>Distance</th>');
		$('.'+alert_id+' thead').append('<th>TX</th>');

		$('.'+alert_id+' form').append('<fieldset data-role="controlgroup" data-type="horizontal" ></fieldset>');

		$('.'+alert_id+' fieldset').append('<input type="radio" name="radio-choice-2" id="radio-choice-21" value="choice-1" checked="checked" />');
		$('.'+alert_id+' fieldset').append('<label for="radio-choice-21">Locate</label>');
		$('.'+alert_id+' fieldset').append('<input type="radio" name="radio-choice-2" id="radio-choice-22" value="choice-2" />');
		$('.'+alert_id+' fieldset').append('<label for="radio-choice-22">Deauth</label>');
		$('.'+alert_id+' fieldset').append('<input type="radio" name="radio-choice-2" id="radio-choice-23" value="choice-3" />');
		$('.'+alert_id+' fieldset').append('<label for="radio-choice-23">Napalm</label>');
		$('.'+alert_id+' fieldset').append('<input type="radio" name="radio-choice-2" id="radio-choice-24" value="choice-4" />');
		$('.'+alert_id+' fieldset').append('<label for="radio-choice-24">Dismiss</label>');
		$('.'+alert_id+' fieldset').append('<input style="margin-left: 1em" type="submit" value="Submit"/>');
		$('.'+alert_id+' form').trigger('create');
		$('.'+alert_id+' form table').trigger('create');
		/*
		$('#set').append('<div data-role="collapsible" class="'+alert_location+'"><h3>'+alert_location+'</h3><p></p></div>').collapsibleset('refresh');
	
		$('.'+alert_location+' p').append('<div class="tablewrap"></div>');
		$('.'+alert_location+' .tablewrap').append('<div class="overflower"></div>');
		$('.'+alert_location+' .overflower').append('<form data-ajax="false" class="'+alert_location+'form"></form>');
		$('.'+alert_location+' form').append('<span class="tablespan"></span>');
		//$('.'+alert_location+' .tablespan').append('<table data-role="table" class="ui-responsive table-stroke"></table>');
		$('.'+alert_location+' .tablespan').append('<table data-role="table" class="sel-table ui-responsive table-shadow"></table>');
		$('.'+alert_location+' .tablespan table').append('<thead></thead>');
		$('.'+alert_location+' .tablespan table').append('<tbody id="'+alert_location+'"></tbody>');
		$('.'+alert_location+' thead').append('<th>Type</th>');
		$('.'+alert_location+' thead').append('<th>BSSID</th>');
		$('.'+alert_location+' thead').append('<th>Channel</th>');
		$('.'+alert_location+' thead').append('<th>ESSID</th>');
		$('.'+alert_location+' thead').append('<th>Details</th>');
		$('.'+alert_location+' thead').append('<th>Timestamp</th>');
		$('.'+alert_location+' thead').append('<th>tx</th>');
		$('.'+alert_location+' form').append('<fieldset data-role="controlgroup" data-type="horizontal" ></fieldset>');

		$('.'+alert_location+' fieldset').append('<input type="radio" name="radio-choice-2" id="radio-choice-21" value="choice-1" checked="checked" />');
		$('.'+alert_location+' fieldset').append('<label for="radio-choice-21">Locate</label>');
		$('.'+alert_location+' fieldset').append('<input type="radio" name="radio-choice-2" id="radio-choice-22" value="choice-2" />');
		$('.'+alert_location+' fieldset').append('<label for="radio-choice-22">Deauth</label>');
		$('.'+alert_location+' fieldset').append('<input type="radio" name="radio-choice-2" id="radio-choice-23" value="choice-3" />');
		$('.'+alert_location+' fieldset').append('<label for="radio-choice-23">Napalm</label>');
		$('.'+alert_location+' fieldset').append('<input type="radio" name="radio-choice-2" id="radio-choice-24" value="choice-4" />');
		$('.'+alert_location+' fieldset').append('<label for="radio-choice-24">Dismiss</label>');
		$('.'+alert_location+' fieldset').append('<input style="margin-left: 1em" type="submit" value="Submit"/>');
		$('.'+alert_location+' form').trigger('create');
		$('.'+alert_location+' form table').trigger('create');

	*/
	},
	destroy_collapsible : function(alert_id) {

		$('.'+alert_id).remove();
	},
	add_to_collapsible : function(a) {

		console.log('woah');
		alert_id = a['id'];
		$('#'+alert_id).empty();
		//console.log(a['locations']);

		var sortable = [];
		for (var device in a['locations']) {

			sortable.push([device, a['locations'][device]]);
		}
		sortable.sort(

			function(a, b) { 

				return b[1] - a[1];
			}
		)
		for (var i = 0, len = sortable.length; i < len; i++) {
		
			var next_row = sortable[i];
			console.log('next row: '+next_row);
			console.log(i);
			console.log(len);
			$('#'+alert_id).append('<tr class="tr'+i+'">');
			$('#'+alert_id+' .tr'+i).append('<td class="device-id">'+next_row[0]+'</td>');
			$('#'+alert_id+' .tr'+i).append('<td class="distance">'+(1.0/Math.sqrt(next_row[1]))+'</td>');
			$('#'+alert_id+' .tr'+i).append('<td class="tx">'+next_row[1]+'</td>');
			
		}

		console.log(sortable);
		/*

		console.log('test');
		alert_location = a['location'];
id='+alert

		console.log(a['id']);
	
		// need to make this table not suck lol
		$('.'+alert_location+' tbody').append('<tr id="'+a['id']+'">');
		$('#'+a['id']).append('<td class="intent">'+a['intent']+'</td>');
		$('#'+a['id']).append('<td class="bssid">'+a['bssid']+'</td>');
		$('#'+a['id']).append('<td class="channel">'+a['channel']+'</td>');
		$('#'+a['id']).append('<td class="essid">'+a['essid']+'</td>');
		$('#'+a['id']).append('<td class="smdescription">'+this.intent2description(a['intent'])+'</td>');
		$('#'+a['id']).append('<td class="timestamp">'+new Date(parseInt(a['timestamp']))+'</td>');
		$('#'+a['id']).append('<td class="tx">'+a['tx']+'</td>');

		init_selectable();
		//$('table').table('refresh');
		*/


	},
	remove_from_collapsible : function(a) {

		var id = a['id'];

		$('#'+id).remove();
	},
	intent2description : function(intent) {

		return 'description goes here';
	},
	notify : function() {
		return;
	}
}
// EVENTS

/* on_alert_add()
 *
 */
function on_alert_add(e) {

	current_alerts.add(e);
}

/* on_alert_dismiss()
 *
 */
function on_alert_dismiss(e) {

	console.log(e);
	for (var i = 0; i < e.length; i++) {
		current_alerts.remove(e[i]);
	}
}

/* on_connect()
 *
 */
function on_connect(e, socket) {

	socket.emit('connected');
}

/* on_form_submit()
 *
 */
function on_form_submit(e) {

	e.preventDefault();

	var checked = $(this).find('input[type=radio]:checked')[0];
	switch (checked.value) {

		case 'choice-1':
			console.log('Locate');
			break;
		case 'choice-2':
			console.log('Deauth');
			deauth_targets(this);
			break;
		case 'choice-3':
			console.log('Napalm');
			napalm_targets(this);
			break;
		case 'choice-4':
			console.log('Dismiss');
			dismiss_alerts(this);
			break;
		default:
			console.log('Invalid choice');
	}
}

// ACTIONS

function get_all_alerts() {

	$.getJSON( "/webcli/connect", function( alerts ) {
		console.log('test');

		for (var i = 0; i < alerts.length; i++) {

			current_alerts.add(alerts[i]);
		}

	});
}

/* dismiss_alerts()
 *
 */
function dismiss_alerts(form) {
	

	console.log($(form));
	var tbody = $(form).find('tbody');
	console.log(tbody);
	var alert_location = tbody.attr('id');
	console.log('send this: '+alert_location);
	
	alerts = [];
	alerts.push({ 'id' : alert_location });
	//console.log(alert_location);
	//rows = tbody.find('tr');
	//for (var i = 0; i < rows.length; i++) {
	//	console.log($(rows[i]).hasClass('ui-selected'));
	//	if ($(rows[i]).hasClass('ui-selected')) {

	//		alerts.push({
	//			'id' : rows[i].id,
	//			'location' : alert_location
	//		});
	//	}
	//}
	$.ajax({
    	type: 'POST',
    	url: 'alert/dismiss',
		data: JSON.stringify(alerts),
    	success: function(data) { console.log(data); },
    	contentType: "application/json",
    	dataType: 'json'
	});
}


/* request_disconnect()
 *
 */
function request_disconnect(socket) {

	socket.emit('disconnect request');
}

function napalm_targets(form) {


	console.log($(form));
	var tbody = $(form).find('tbody');
	var alert_location = tbody.attr('id');
	var alerts = [ { 'id' : alert_location } ];
	console.log('alert is: '+alerts);
	$.ajax({
    	type: 'POST',
    	url: '/napalm',
		data: JSON.stringify(alerts),
    	success: function(data) { console.log(data); },
    	contentType: "application/json",
    	dataType: 'json'
	});

}

function deauth_targets(form) {


	console.log($(form));
	var tbody = $(form).find('tbody');
	var alert_location = tbody.attr('id');
	var alerts = [ { 'id' : alert_location } ];
	console.log('alert is: '+alerts);
	$.ajax({
    	type: 'POST',
    	url: '/deauth',
		data: JSON.stringify(alerts),
    	success: function(data) { console.log(data); },
    	contentType: "application/json",
    	dataType: 'json'
	});

}
