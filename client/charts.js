/* 
############################################################
#
#    Highlands Client
#
#    © Highlands Negotiations, June 2018, v0.5
#
############################################################
*/

var NUMBER = 0;
var SECTION = 1;
var QUESTION = 2;
var TYPE = 3;
var AUTOFILL = 4;
var OPTIONS = 5;
var VALUES = 6;

var pieChartData;
var filteredPieChartData;
var pieChartQuestionsAndOptions;
var clientsAndEmailsForCharts;

function displayPieCharts() {
	positionCopyright();
	pieChartData = undefined;
	pieChartQuestionsAndOptions = undefined;
	getAjaxData('/piechart-data2', getPieChartData);
	getAjaxData('/piechart-questions-options', getPieChartQuestionsAndOptions);
}

function displayCharts() {
	positionCopyright();
	getAjaxData("/emails-and-clients", getClientsAndEmailsForCharts);
}

function getClientsAndEmailsForCharts(data) {
	let emails = data[0];
	let clients = data[1];
	clientsAndEmailsForCharts = [emails, clients];
	getAjaxData('/chart-data', drawChart);
}

function getPieChartData(data) {
	pieChartData = data;
	if (pieChartData && pieChartQuestionsAndOptions) {
		drawPieChart(data);
	}
}

function getPieChartQuestionsAndOptions(data) {
	pieChartQuestionsAndOptions = data;
	if (pieChartData && pieChartQuestionsAndOptions) {
    	drawPieChart(data);
	}
}

function cleanupSelectText(text) {
	text = text.trim();
	return text.replace(/ /g,"&nbsp;");
}

function drawChart(data) {
	// data is presented as an array of objects
	// each entry has:
	//		key = "<aspect>,<client>-<email>,<guid>"
	//		value = <sum of marks>
	
	// work with copies of important arrays	
	var filteredClients;
	var filteredEmails;
	var filteredColumnData;

	let ASPECT = 0;
    let CLIENT = 1;
    
	function zip(a, b) {
		var result = [];
		for(var i = 0; i < a.length; i++){
			result.push([a[i], b[i]]);
		}
		return result;
	}
 	function splitKeys(keys) {
		var result = [];
		for(var i = 0; i < keys.length; i++){
			result.push([keys[i].split(',')]);
		}
		return result;
 		
 	} 	
	function determineClients() {
		// determine the categories shown on the y axis based on input "keys"
		// keys = "<aspect>,<client> <email>,<guid>"
		// remove aspect and then check for unique sets of "<client> <email>,<guid>" 
		// then remove the <guid> as its not shown on the chart
		let clients = [];
		keys.forEach(function(key) {
			// remove <aspect> and check for unique sets
			let client = key.replace(/^[^,]+,/,"");
			if($.inArray(client, clients) === -1) clients.push(client);
		});
		// now remove <guid> from end of strings
		for(let i = 0; i < clients.length; i++) {
			clients[i] = clients[i].replace(/,[^,]+$/,"");
		}
		// return categories used as y axis
		return clients;
	}
	function determineAspects() {
		function capitalize(string) {
		    return string.charAt(0).toUpperCase() + string.slice(1);
		}
		let aspects = [];
		keys.forEach(function(key) {
			let aspect = key.split(",")[ASPECT];
			aspect = capitalize(aspect);
			if($.inArray(aspect, aspects) === -1) aspects.push(aspect);
		});
		return aspects;
	}
	function splitValues() {
		let array = [];
		let spliceLength = values.length / aspects.length;
		while(values.length) array.push(values.splice(0, spliceLength));
		return array;
	}
	function addAspectNamesToStartOfColumn() {
		for(let i = 0; i < columnData.length; i++) {
			columnData[i].unshift(aspects[i]);
		}
	}
	
	function filter(filter, item) {
		// filter = "client" | "email"
		// item = "-" for no filter or the name to filter
		function takeCopiesOfImportantArrays() {
			filteredClients = clients.slice();
			filteredEmails = emails.slice();
			filteredColumnData = [];
			columnData.forEach(function(array) {	// need a deep copy
				filteredColumnData.push(array.slice())
			});
		}
		function removeItemsFromFilteredArrays(i) {
			filteredClients.splice(i, 1);
			filteredEmails.splice(i, 1);
			filteredColumnData.forEach(function(value) {
				value.splice(i+1, 1);  	// +1 to allow for aspect name at start of column
			});			
		}
		takeCopiesOfImportantArrays();
		if(item === "-") return;
		// must work backwards through array when splicing
		for(let i = clients.length - 1; i >= 0; i--) {
			let key;
			if(filter === "client") key = filteredClients[i].trim();
			if(filter === "email") key = filteredEmails[i].trim();
			
			if(key !== item.trim()) { // remove items from relevant arrays
				removeItemsFromFilteredArrays(i);
			}
		}
	}
	
	function generateChart() {
		function displayHeading() {
			let entries = filteredColumnData[0].length - 1;
			let heading = div(`<br/>Number of records = ${entries}<br/>`, "forensics-heading", {color:`${OVERVIEW_STATUS}`});
			if($("#forensics-heading").length) {
				$("#forensics-heading").html(heading)
			} else {
				$("#filter-drop-down").append(heading);
			}
		}
		displayHeading();
		
		// x-axis: <Aspect>, <values array>
		// y-axis: <client array>
		// axes are swapped
		let height = (filteredClients.length + 1) * screen.height / 10;
		let o = {};  // used to generate chart
		o["bindto"] = '#chart';
		o["axis"] = { rotated:true, x:{ type:'category', categories:filteredClients}};
	    o["bar"]  = { width:{ ratio: 0.5}}; // this makes bar width 50% of length between ticks
		o["data"] = { columns: filteredColumnData, type: 'bar'};
		o["size"] = { height: height },
	    o["padding"] = { left: $(window).width()/8 },
	    o["tooltip"] = {
			format: {
				title: function(i) { return filteredEmails[i]; },
				value: function(value, ratio, id) { return value; }
			}
		}
		c3.generate(o);
	}

	function addDropDown(selector) {
		function removeDuplicates(array) {
			let set = new Set(array);
			let it = set.values();
			return Array.from(it);
		}
		let uniqueClients = removeDuplicates(clients);
		let uniqueEmails = removeDuplicates(emails);		
		uniqueClients = clientsAndEmailsForCharts[1];
		uniqueEmails = clientsAndEmailsForCharts[0];

		let html = $(`${buildMenu(data, "filter", uniqueClients, uniqueEmails)}`);
		html.css({'width':'auto'});
		$(selector).prepend(html);

		$("#filter").select2({theme: "classic", dropdownAutoWidth : 'true', width: 'auto'});
    	$("#filter").on("change", function(e) { 
			if(e.val === "-")
				filter("client", "-");
			else {
				let parts = e.val.split(',');
				let group = parts[0];
				let text = parts[1];
				filter(group, text);
			}
			generateChart();
    	});
	}

	let keys = Object.keys(data);
	let values = Object.values(data);
	let clientsAndEmails = determineClients();
	let clients = [];
	let emails = [];
	for(let i = 0; i < clientsAndEmails.length; i++) {
		clients.push(clientsAndEmails[i].replace(/^(.*)<.*/,"$1"));
		emails.push(clientsAndEmails[i].replace(/^[^<]+[<](.*)>/,"$1"));
	}
	let aspects = determineAspects();
	columnData = splitValues();
	addAspectNamesToStartOfColumn();
	filter("client", "-");
	addDropDown("#filter-drop-down");
	generateChart();
}

function drawPieChart() {
	getAjaxData("/emails-and-clients", pieChartCallback);
}

function pieChartCallback(data) {
	// uses globals: pieChartData, pieChartQuestionsAndOptions
	// the server sends data values of -1 when there is no data
	
	let emails = data[0];
	let clients = data[1];
	
    function truncate(s, length) {
	    if (s.length > length) {
	      s = s.substring(0, length - 3) + "...";
	    }
	    return s;
	}
    
	if($.isEmptyObject(pieChartData)) {
		$("#piecharts-message").text("no pie charts available");
		return;
	} else {
		$("#piecharts-message").text("");		
	}

	let maxLegendLength = 100;
	let menu = buildMenu(pieChartData, "pie-filter", clients, emails);
	let html = $(`${menu}<br/>`);
	html.css({'width':'auto'});
	$("#pie-filter-drop-down").html(html);
	$("#pie-filter").select2({theme: "classic", dropdownAutoWidth : 'true', width: 'auto'});
	$("#pie-filter").on("change", function(e) { 
		if(e.val === "-") {
			filteredPieChartData = pieChartData['all'];
		} else {
			let parts = e.val.split(',');
			let group = parts[0];
			let text = parts[1];
			filteredPieChartData = pieChartData[text];
		}
		clearAllPies();
		drawAllPies();
	});

	filteredPieChartData = pieChartData['all'];
	drawAllPies();
	
	function clearAllPies() {
 	    $("#piechart").empty;
	}
	
	function drawAllPies() {
		for(let i = 0; i < filteredPieChartData.length; i++) {
		    function appendTitle() {
		 	    title = `${number}. ${title}`;
		 	    title = div(title,"", {"width":"100%", "color":PIECHART_TITLES_COLOR, "background-color":PIECHART_BACKGROUND_COLOR})
		 	    $("#piechart").append(title);
		 	}
	
			let selector = `#chart${i}`;
			
	 	    let data = filteredPieChartData[i];
	 	    let number = pieChartQuestionsAndOptions[i][NUMBER];
	 	    let legend = pieChartQuestionsAndOptions[i][OPTIONS];
	 	    let title = pieChartQuestionsAndOptions[i][QUESTION];
	 	    
	 	    appendTitle();	// workaround for title broken in C3 library
	 	    let anchor = div("", `chart${i}`).css({"float":"left", "width":"100%", "background-color":PIECHART_BACKGROUND_COLOR});
	 	    $("#piechart").append(anchor);
	
	 		// make sure no more than n (=1) pie charts are drawn per line
	 	    let chartsPerLine = 1;
	 		let w1 = $(window).width()/filteredPieChartData.length;
	 		let w2 = $(window).width()/chartsPerLine;
	 		let width = Math.max(w1, w2);
	
	 	    pie = `["${truncate(legend[0],maxLegendLength)}", ${data[0]}]`;
	 	    for(let k = 1; k < data.length; k++) {
	 	    	if(data[k] !== -1) pie += `,\n["${truncate(legend[k], maxLegendLength)}", ${data[k]}]`;
	 	    }
	 	    // build object to generate piechart
	 	    o = `{
	 	    	"size": {"width":"${width}"},
	 	    	"padding": {"bottom":"40"},
	 	    	"legend": {"position":"right"},
	 	    	"bindto": "${selector}",
	 	    	"data": {
	 	    	    "columns": [${pie}],
			        "type" : "pie"
			    },
	 	    	"tooltip": {"contents":"this_will_be_replaced"}
	 	    	}`;
	 	    o = JSON.parse(o);
	 	    // JSON parsing converts the function to a string so change it to a function:
	 	    o["tooltip"]["contents"] = function(d, defaultTitleFormat, defaultValueFormat, color) {
	 		    						   var sum = 0;
	 		    						   d.forEach(function (e) {
	 		    							   sum += e.value;
	 		    						   });
	 		    						   defaultTitleFormat = function() {
	 		    							   return `Frequency = ${sum}`;
	 		    						   };
	 		    						   return c3.chart.internal.fn.getTooltipContent.apply(this, arguments);
	 								   }
	 		c3.generate(o);
		};
		let endOfPiecharts = div("", "", {"clear":"both"});
		$("#piechart").append(endOfPiecharts);
	}
}

