/* 
############################################################
#
#    Highlands Client
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################
*/

function buildMenu(selector, id, clients, emails) {
	let menu = `
		<div><label>Filter:</label>
		<select id=${id}>
		<optgroup label="filter">
		<option value="-">none</option>
		</optgroup>
		<optgroup label="by&nbsp;client">`;
	clients.forEach(function(client) {
		menu += `<option value="client,${client.trim()}">${cleanupSelectText(client)}</option>`;
		});
	menu += `
		</optgroup>
		<optgroup label="by&nbsp;email">`;
	emails.forEach(function(email) {
		menu += `<option value="email,${email.trim()}">${email.trim()}</option>`;
	});
	menu += `</optgroup></select></div>`;
	let html = $(`${menu}`);
	html.css({'width':'auto'});
	$(selector).html(html);
	$(`#${id}`).select2({theme: "classic", dropdownAutoWidth : 'true', width: 'auto'});
	return menu;
}

function buildMenu2(data, id, clients, emails) {
	function getClients() {
		let clients = [];
		Object.keys(data).forEach(function(key) {
			if(key.indexOf('@') === -1 && key !== 'all') clients.push(key);
		});
		return clients;
	}
	function getEmails() {
		let emails = [];
		Object.keys(data).forEach(function(key) {
			if(key.indexOf('@') !== -1) emails.push(key);
		});
		return emails;
	}
	if(clients === undefined) clients = getClients();
	if(emails  === undefined) emails = getEmails();
	let menu = `
		<div><label>Filter:</label>
		<select id=${id}>
		<optgroup label="filter">
		<option value="-">none</option>
		</optgroup>
		<optgroup label="by&nbsp;client">`;
	clients.forEach(function(client) {
		menu += `<option value="client,${client.trim()}">${cleanupSelectText(client)}</option>`;
		});
	menu += `
		</optgroup>
		<optgroup label="by&nbsp;email">`;
	emails.forEach(function(email) {
		menu += `<option value="email,${email.trim()}">${email.trim()}</option>`;
	});
	menu += `</optgroup></select></div>`;
	return menu;
}

function buildMenu3(selector, id, topics) {
	let menu = `
		<div><label>Filter:</label>
		<select id=${id}>
		<optgroup label="by&nbsp;log file">`;
	topics.forEach(function(topic) {
		menu += `<option value="topic,${topic.trim()}">${cleanupSelectText(topic)}</option>`;
		});
	menu += `</optgroup></select></div>`;
	let html = $(`${menu}`);
	html.css({'width':'auto'});
	$(selector).html(html);
	$(`#${id}`).select2({theme: "classic", dropdownAutoWidth : 'true', width: 'auto'});
	return menu;
}

function cleanupSelectText(text) {
	text = text.trim();
	return text.replace(/ /g,"&nbsp;");
}


