/* 
############################################################
#
#    Highlands Client
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################
*/

//var tableData;


function displayTableData() {
	let a1 = getAjaxData2(`/emails-and-clients?uuid=${document.uuid}`);
	let a2 = getAjaxData2(`/table-data?uuid=${document.uuid}`);
	$.when(a1, a2).done(function(emailsAndClients, tableData) {
		drawTableCharts(emailsAndClients[0], tableData[0]);
	});
}

function drawTableCharts(emailsAndClients, tableData) {
	let emails = emailsAndClients[0];
	let clients = emailsAndClients[1];
	let id = "table-filter";
	buildMenu("#table-filter-drop-down", id, clients, emails);
	let title = div(`${TABLE_CHARTS_TAB_TEXT}`, "", { color:`${TABLE_CHARTS_TITLE_COLOR}`});
	$("#table-title").html(title);
	if (emails.length === 0) return;

	function attachPieChart(key, filter) {
		o = {
			    data: {
			        columns: [],
			        type : 'pie'
			    },
			    "tooltip": {"contents":"this_will_be_replaced"}
			};
			let n = tableData[key]['tabs'].length;
			for(let i = 0; i < n; i++) {
				o['bindto'] = `#table-chart-${key}-${i}`;
				o['data']['columns'] = tableData[key]['data'][filter][i];
		 	    o["tooltip"]["contents"] = function(d, defaultTitleFormat, defaultValueFormat, color) {
		 	    	var sum = 0;
					d.forEach(function (e) {
						sum += e.value;
					});
					defaultTitleFormat = function() {
						return `Frequency = ${sum}`;
					};
					return c3.chart.internal.fn.getTooltipContent.apply(this, arguments);
				};
				$(`#table-tab-title-${key}-${i}`).text(`${tableData[key]['tabs'][i]}`);
				$(`#table-tab-title-${key}-${i}`).css({ "color":`${TABLE_CHARTS_TABS_COLOR}`, "background-color":`${TABLE_CHARTS_TABS_BACKGROUND_COLOR}`});
				c3.generate(o);
			}
	}
	
	function drawAllTableCharts(tableData, clientOrEmail) {
	 	$("#tablecharts").empty();
		for(let key in tableData) {
			let question = div(`<p>${key}.${tableData[key]['question']}<br/>`, "", {"color":`${TABLE_CHARTS_QUESTIONS_COLOR}`});
			$("#tablecharts").append(question)
			createTabs(tableData, "#tablecharts", key);
			attachPieChart(key, clientOrEmail);
		}
	}
	// initial draw
	drawAllTableCharts(tableData, 'all');

	$("#table-filter").on("change", function(e) { 
		if(e.val === "-") {
			drawAllTableCharts(tableData, 'all');
		} else {
			let parts = e.val.split(',');
			let group = parts[0];
			let clientOrEmail = parts[1];
			drawAllTableCharts(tableData, clientOrEmail);
		}
	});

}

function createTabs(tableData, selector, n) {
	let tabs = div("", `table-tabs-${n}`);
	$(selector).append(tabs);
	let tabObject = {};
	$(function() {$(`#table-tabs-${n}`).tabs(tabObject);});

	// lists first
	let ulist = $("<ul></ul>");
	$(ulist).attr("id", `table-ulist-${n}`);
	$(`#table-tabs-${n}`).append(ulist);
	
	for(let i = 0; i < tableData[n]['tabs'].length; i++) {
		let list = $(`<li onmousemove='setTimeout(positionCopyright, 100)'></li>`);
		let anchor = $(`<a href="#tab-${n}-${i}" id="table-tab-title-${n}-${i}"></a>`);
		anchor.addClass("table-tab-titles");
		$(ulist).append(list);
		$(list).append(anchor);
	}
    $(".table-tab-titles").css({
    	"font-size":TABLE_TAB_TITLES_FONT_SIZE
    });


	// then add divs
	for(let i = 0; i < tableData[n]['tabs'].length; i++) {
		let outer = div("", `tab-${n}-${i}`);
		outer.addClass(`table-tab-${n}-class`);
		let inner = div("", `table-chart-${n}-${i}`);
		if(i === 0) {
			$(`#table-ulist-${n}`).after(outer);
		} else {
			$(`.table-tab-${n}-class`).last().after(outer);
		}
		$(outer).append(inner);
	}	
}
