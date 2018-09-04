/*
 * This file handles the display of checkbox data.
 * 
 * Entry point: function displayCheckboxData()
 * 
 * Checkbox data is requested from the server in displayCheckboxData() and received in the data parameter of setCheckboxData().
 * The checkbox data is then transfered to a global variable for later processing.  The client also needs email and client 
 * data for the filter on the checkbox page and this is requested from the server once the checkbox data is received using a
 * further AJAX call.
 * The email and client information is received in drawCheckboxCharts() as two arrays and unpacked into local variables: emails 
 * and clients.  The function then builds the filter using code from "utilities.js" and displays the checkbox data unfiltered.
 * If the user invokes the filter, then the callback code is called to implement the filter:
 *  	$("#checkbox-filter").on("change", function(e) { ...
 */

var checkboxData;

function displayCheckboxData() {
	getAjaxData("/checkbox-data", setCheckboxData);
}

function setCheckboxData(data) {
	checkboxData = data;
	getAjaxData("/emails-and-clients", drawCheckboxCharts);
}

function drawCheckboxCharts(data) {
	let emails = data[0];
	let clients = data[1];
	let id = "checkbox-filter";
	let menu = buildMenu(undefined, id, clients, emails);
	let html = $(`${menu}`);
	html.css({'width':'auto'});
	$("#checkbox-filter-drop-down").html(html);
	$("#checkbox-filter").select2({theme: "classic", dropdownAutoWidth : 'true', width: 'auto'});
	let title = div(`${CHECKBOXES_TAB_TEXT}`, "", { color:`${CHECKBOX_TITLE_COLOR}`});
	$("#checkbox-title").html(title);

	function drawAllCheckboxCharts(clientOrEmail) {
	 	$("#checkboxcharts").empty();
		for(let i = 0; i < checkboxData['record'].length; i++) {
			let number = checkboxData['record'][i]['Number'];
			let question = checkboxData['record'][i]['Question'];
			let title = div(`<br/>${number}. ${question}<p>`, "", { color:`${CHECKBOX_QUESTIONS_COLOR}`});
			$("#checkboxcharts").append(title);
			let html = div("", `checkbox-figure-${i}`);
			$("#checkboxcharts").append(html);
			
			drawCheckboxChart(`#checkbox-figure-${i}`, clientOrEmail, i);
		}
	}
	// initial draw
	drawAllCheckboxCharts('all');

	$("#checkbox-filter").on("change", function(e) { 
		if(e.val === "-") {
			drawAllCheckboxCharts('all');
		} else {
			let parts = e.val.split(',');
			let group = parts[0];
			let text = parts[1];
			drawAllCheckboxCharts(text);
		}
	});

}

function drawCheckboxChart(selector, clientOrEmail, i) {
	let o = {
		bindto: selector,
		padding: {
	        top:   10,
	    },
		axis: { rotated:false, x:{ type:'category', categories: ['frequencies (%)']}},
	    data: {
	        columns: [],
	        type: 'bar'
	    },
	    bar: {
	        width: {
	            ratio: 0.5
	        }
	    },
	    tooltip: {contents:"this_will_be_replaced"}
	};
	o['data']['columns'] = checkboxData['record'][i]['data'][clientOrEmail];
	o["tooltip"]["contents"] = function(d, defaultTitleFormat, defaultValueFormat, color) {
		let recordCount = checkboxData['recordCount'];
	    defaultTitleFormat = function() {
		    return `Frequency`;
	    };
	    defaultValueFormat = function(value) {
	    	return Math.round(value*recordCount/100);
	    }
	    return c3.chart.internal.fn.getTooltipContent.apply(this, arguments);
    }

	var chart = c3.generate(o);
}
