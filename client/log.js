/* 
############################################################
#
#    Highlands Client
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################
*/


function displayLog() {
	let title = div(`${LOG_TAB_TEXT}`, "", { color:`${LOG_TITLE_COLOR}`});
	$("#log-title").html(title);

	let a = getAjaxData3(`/log?uuid=${document.uuid}`);
	$.when(a).done(function(logFile) {
		var lines = logFile.split("\n");
		var result = "<br/>";

		for(let i = 0; i < lines.length; i++)
		    result = lines[i] + "<br/>" + result;
		$("#theLog").html(result);		
	});
}

function displaySystemLogs() {
	function printFile(text) {
		var lines = text.split("\n");
		var result = "<br/>";

		for(let i = 0; i < lines.length; i++)
		    result = lines[i] + "<br/>" + result;
		$("#theSyslog").html(result);
	}

	$("#theSyslog").empty();
	let a = getAjaxData3(`/system-logs?uuid=${document.uuid}`);
	$.when(a).done(function(data) {
		var jsonObject = $.parseJSON(data);
		let id = "syslog-filter";
		let options = Object.keys(jsonObject);
		buildMenu3("#syslog-filter-drop-down", id, options);
		let title = div(`${SYSLOG_TAB_TEXT}`, "", { color:`${SYSLOG_TITLE_COLOR}`});
		$("#syslog-title").html(title);
		printFile(jsonObject[options[0]]);
		$("#syslog-filter").on("change", function(e) { 
			let parts = e.val.split(',');
			let group = parts[0];
			let text = parts[1];
			printFile(jsonObject[text]);
		});
	});
}
