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
		let categories = chartDataResponse[0]['categories'];
		let toolTips = chartDataResponse[0]['toolTips'];
		let chartData = chartDataResponse[0]['data'];
		console.log(clients);
		console.log(toolTips);
		console.log(chartData);
		drawChart(emails, clients, chartData, categories, toolTips);
	});
}

function drawChart(emails, clients, chartData, categories, toolTips) {
	buildMenu("#filter-drop-down", "filter", clients, emails);
	generateChart(categories, toolTips, chartData, ["all", "-"]);

	$("#filter").on("change", function(e) { 
		function getSelection() {
			if(e.val === "-") {
				return ['all', '-'];
			} else {
				let parts = e.val.split(',');
				let group = parts[0];
				let text = parts[1];
				return [text, group];
			}
		}
		generateChart(categories, toolTips, chartData, getSelection());
	});
}


function generateChart(categories, toolTips, data, selection) {
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
	let key = selection[0];
	let group = selection[1];
	let columns = data[key][key];
	
	// now filter categories and tooltips
	// group will be 'client' or 'email' 
	// swap tooltips and categories if group is email
	if(key != 'all') {
		filteredCategories = [];
		filteredToolTips = []
		for(let i = 0; i < categories.length; i++) {
			if(group === 'client') {
				if(categories[i] === key) {
					filteredCategories.push(categories[i]);
					filteredToolTips.push(toolTips[i]);
				}
			} else { // 'email' 
				if(toolTips[i] === key) {
					filteredCategories.push(toolTips[i]);
					filteredToolTips.push(categories[i]);
				}				
			}
		}
		categories = filteredCategories;
		toolTips = filteredToolTips;
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
			title: function(i) { return toolTips[i]; }
//			value: function(value, ratio, id) { return value; }
		}
	}
	c3.generate(o);
}
