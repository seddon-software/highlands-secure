/* 
############################################################
#
#    Highlands Client
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################
*/


// !!!! important
// xSort is undocumented, c3.js reorders json data without this attribute and this in turn messes up the data index
// https://stackoverflow.com/questions/48465126/c3-charts-dynamic-bubble-size-in-scatter-plot-wrong-index
// https://github.com/c3js/c3/issues/547#issuecomment-56292971

var scatterFrequencies;

function displayScatterChart() {
	let a1 = getAjaxData2(`/emails-and-clients?uuid=${document.uuid}`);
	let a2 = getAjaxData2(`/scatter-data?uuid=${document.uuid}`);
	$.when(a1, a2).done(function(emailsAndClients, scatterData) {
		scatterChartCallback(emailsAndClients[0], scatterData[0]);
	});
}

function scatterChartCallback(emailsAndClients, scatterData) {
	let emails = emailsAndClients[0];
	let clients = emailsAndClients[1];
	let id = "scatter-filter";
	buildMenu("#scatter-filter-drop-down", id, clients, emails);
	let heading = div(`${SCATTER_TAB_TEXT}`, "", {'color':`${GROWTH_TITLES_COLOR}`});
	$("#scattercharts-title").html(heading);
	if (emails.length === 0) return;

	let questionNumber = scatterData['question'][0];
	let questionText = scatterData['question'][1];
	let title = div(`<br/>${questionNumber}. ${questionText}`, "", { color:GROWTH_QUESTIONS_COLOR});
	$("#scatter-filter-drop-down").append(title);

	// initial draw
	scatterFrequencies = scatterData.frequencies['all'];
	drawAllScatterCharts(scatterData);	
	
	$("#scatter-filter").on("change", function(e) { 
		if(e.val === "-") {
			scatterFrequencies = scatterData.frequencies['all'];
		} else {
			let parts = e.val.split(',');
			let group = parts[0];
			let text = parts[1];
			scatterFrequencies = scatterData.frequencies[text];
		}
		function clearAllScatterCharts() {
	 	    $("#scatterchart").empty();
		}
		clearAllScatterCharts();
		drawAllScatterCharts(scatterData);
	});
}

function drawAllScatterCharts(scatterData) {
	function isInteger(n) {
		let base = Math.floor(n);
		let diff = Math.abs(base - n);
		return diff < 0.0001;
	}
	
	function getScatterCount() {
		let total = 0;
		let data = scatterData.frequencies['all'];
		for(let i = 0; i < data.length; i++) {
			for(let k = 0; k < data[0].length; k++)
				total += data[i][k];  
		}
		return total;
	}

	let frequencies = scatterFrequencies;
	let rows = frequencies.length;
	let cols = frequencies[0].length;
	let columnData = [["x"],[" "]];
	for(let i = 0; i < rows; i++) {
		for(let k = 0; k < cols; k++) {
			columnData[0].push(i);
			columnData[1].push(k);
		}
	}
	let o = {'bindto':"#scattercharts", 'legend':{hide:true} };
	o['data'] = {
			xSort:false, 
			xs:{' ': 'x'}, 
			type:'scatter',
			columns:columnData,
			color: function(color,d){
				if(d === " ") return;
				let count = getScatterCount();
				let x = d.x;
				let y = d.value;
				let frequency = frequencies[x][y];
				color = "black";
				if(frequency > count/5) color = "red";
				if(frequency > count/2.5) color = "blue";
				return color;
			}};
	o['point'] = {
	        r: function(d) {
				let count = getScatterCount();
	        	let xy = d['index'];
	        	let x = Math.floor(xy / rows);
	        	let y = xy % rows;
	        	let factor = 100;
	            return frequencies[x][y]*factor / count;
	        }
	    };

	o['axis'] = {
	        x: {
	        	min: -0.4,
	        	max:  4.4,
	            label: {
	            	position: 'outer-center',
	            	text: SCATTER_X_TITLE
	            },
	            tick: {
	            	count: 5,
	            	format: function(x) { 
            			return scatterData.xLabels[x];
	            	},
	                fit: false
	            }
	        },
	        y: {
	            label: {
	            	position: 'outer-middle',
	            	text: SCATTER_Y_TITLE
	            },
				tick: {
					format: function(y) { 
	            		if(isInteger(y))
	            			return scatterData.yLabels[y];
	            		else
	            			return '';
	            	}
	        	}
	        }
	    };
	o['tooltip'] = {
        format: {
            title: function (d) {
            	return 'Frequency'; 
            },
            value: function (value, ratio, id, index) {
	        	let x = Math.floor(index / rows);
            	let y = index % rows;
            	return `${frequencies[x][y]}`;
            }
        }
    };
	c3.generate(o);
}
