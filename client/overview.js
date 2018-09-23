/* 
############################################################
#
#    Highlands Client
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################
*/

//var clientsAndEmailsForCharts;

function displayCharts() {
	let a1 = getAjaxData2("/emails-and-clients");
	let a2 = getAjaxData2("/chart-data-7");
	$.when(a1, a2).done(function(emailsAndClientsResponse, chartDataResponse) {
		let emails = emailsAndClientsResponse[0][0];
		let clients = emailsAndClientsResponse[0][1];
		let categories = chartDataResponse[0]['categories']
		let chartData = chartDataResponse[0]['data']
		drawChart(emails, clients, chartData, categories);
	});
}

function drawChart(emails, clients, chartData, categories) {
	buildMenu("#filter-drop-down", "filter", clients, emails);
	$("#filter").on("change", function(e) { 
		function getSelection() {
			if(e.val === "-") {
				console.log("all");
			return 'all';
			} else {
				let parts = e.val.split(',');
				let group = parts[0];
				let text = parts[1];
				console.log(group, text);
				console.log("item");
				return text;
			}
		}
		let key = getSelection();
		if(key == 'all') {
			generateChart(categories, chartData, 'all');				
		} else {
			generateChart([key], chartData, getSelection());
		}
	});

	generateChart(categories, chartData, 'all');
}


function generateChart(categories, data, key) {
	function displayHeading() {
		let entries = categories.length;
		let heading = div(`<br/>Number of records = ${entries}<br/>`, "forensics-heading", {color:`${OVERVIEW_STATUS}`});
		if($("#forensics-heading").length) {
			$("#forensics-heading").html(heading)
		} else {
			$("#filter-drop-down").append(heading);
		}
	}
	
	// x-axis: <Aspect>, <values array>
	// y-axis: <categories>
	// axes are swapped
	let columns = data[key][key];
	if(key != 'all') {
		categories = [];
		for(let i = 1; i < columns[0].length; i++) {
			categories.push(key);
		}
	}
	displayHeading();
	let n = data[key][key][0].length - 0.5;
	let height = n * screen.height / 10;
	let o = {};  // used to generate chart
	o["bindto"] = '#chart';
	o["axis"] = { rotated:true, x:{ type:'category', categories:categories}};
    o["bar"]  = { width:{ ratio: 0.5}}; // this makes bar width 50% of length between ticks
	o["data"] = { columns: data[key][key], type: 'bar'};
	o["size"] = { height: height },
    o["padding"] = { left: $(window).width()/8 },
    o["tooltip"] = {
		format: {
//			title: function(i) { return filteredEmails[i]; },
//			value: function(value, ratio, id) { return value; }
		}
	}
	c3.generate(o);
}
