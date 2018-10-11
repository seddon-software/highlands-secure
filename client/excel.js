/* 
############################################################
#
#    Highlands Client
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################
*/


function displayExcelData() {
	let a = getAjaxData2(`/excel-data?${document.uuid}`);
	$.when(a).done(function(excelData) {
		var jsonObj = $.parseJSON(excelData);
		var uri_dec = decodeURIComponent(jsonObj);
		displaySpreadsheet(jsonObj);
	});
}

function displaySpreadsheet(data) {
	d3.select("#excelcharts")
        .selectAll("tr")
	    .data(data)
   	    .enter()
   	    .append("tr")
   	    .each(function(d, row) {
   	    	d3.select(this).selectAll("td")
	  	    .data(d)
	     	.enter()
	        .append("td")
			.each(function(d, col) {
				if(row === 0) { 
            		d3.select(this)
            		    .style("color", "red")
            			.style("background-color", "blue")
            			.style("text-align", "center");
            	} else if(row % 2 === 0) { 
            		d3.select(this)
            		    .style("color", "black")
            		    .style("background-color", "cornsilk");
            	} else {
            		d3.select(this)
        		    .style("color", "black")
        		    .style("background-color", "wheat");            		
            	}
        		d3.select(this).style("border-style", "outset");
			})	        
	      	.text(function(d) { return unescape(d); });
   	    });
}


