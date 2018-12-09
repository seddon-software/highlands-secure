/* 
############################################################
#
#    Highlands Client
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################
*/

var chartGroups;

function displayCharts() {
	let a1 = getAjaxData2(`/emails-and-clients?uuid=${document.uuid}`);
	let a2 = getAjaxData2(`/chart-data?uuid=${document.uuid}`);
	$.when(a1, a2).done(function(emailsAndClientsResponse, chartDataResponse) {
		let emails = emailsAndClientsResponse[0][0];
		let clients = emailsAndClientsResponse[0][1];
		let categories = chartDataResponse[0]['categories'];
		let toolTips = chartDataResponse[0]['toolTips'];
		let chartData = chartDataResponse[0]['data'];
		chartGroups = chartDataResponse[0]['groups'];
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
	if(data === undefined) return
	// x-axis: <Aspect>, <values array>
	// y-axis: <categories>
	// axes are swapped
	let key = selection[0];
	let group = selection[1];
	let columns = data[key][key];
	
	// filter categories and tooltips ...
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
	
	// aspects are already sorted alphabetically
	
	let o = {};  // used to generate chart
	o["bindto"] = '#chart';
	o["axis"] = { rotated:true, x:{ type:'category', tick: { width:3000, multiline: false }, categories:categories}};
    o["bar"]  = { width:{ ratio: 0.5}}; // this makes bar width 50% of length between ticks
	o["data"] = { columns: data[key][key], groups: chartGroups, type: 'bar', labels: true };
	o["size"] = { height: height },
    o["padding"] = { left: $(window).width()/6 },
    o["tooltip"] = { contents: 
    	function (d) {
        	let index = d[0].x;
        	let title = toolTips[index];
            let text = `<table class="${this.CLASS.tooltip}"><tr><th colspan="2">${title}</th></tr>`;

	        for (let i = 0; i < d.length; i++) {
	        	// some aspects may not haveimportant questions
		        let aspect = data[key][key][i][0];
	            if(!aspect.includes("*")) {	// not an important aspect
	            	let value = d[i].value;
	            	let importantValue = 0;
	            	try {
	            		let nextAspect = data[key][key][i+1][0];
	            		if(nextAspect.includes("*")) {
	            		    importantValue = d[i+1].value;
	            		}
	            	} catch(e) {
	            		// no next aspect, so ignore error
	            	}
	            	let valueText = `total = ${value + importantValue}: important = ${importantValue}, other = ${value}`;
		            text += `<tr>
		                         <td>${d[i].name}</td>
		                         <td>${valueText}</td>
		                     </tr>`;
	            }
	        }
	        text += "</table>";
	        return text;
	    }	
	}
	c3.generate(o);
}


