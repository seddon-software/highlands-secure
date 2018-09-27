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
	let a = getAjaxData3("/log");
	$.when(a).done(function(logFile) {
		var lines = logFile.split("\n");
		var result = "";

		for(let i = 0; i < lines.length; i++)
		    result = lines[i] + "\n" + result;
		$("#theLog").text(result);		
	});
}
