/* 
############################################################
#
#    Highlands Client
#
#    © Highlands Negotiations, 2018, v1.0
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

function displayPieCharts() {
	positionCopyright();
	pieChartData = undefined;
	pieChartQuestionsAndOptions = undefined;
	getAjaxData('/piechart-data', getPieChartData);
	getAjaxData('/piechart-questions-options', getPieChartQuestionsAndOptions);
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
	let menu = buildMenu2(pieChartData, "pie-filter", clients, emails);
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
