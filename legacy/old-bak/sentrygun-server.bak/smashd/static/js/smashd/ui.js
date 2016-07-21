function init_selectable() {

	$('.sel-table>tbody').bind('mousedown', function(e) {

		e.metaKey = true;
	}).selectable({
		filter: 'tr',
		cancel: 'a'
	});

}
