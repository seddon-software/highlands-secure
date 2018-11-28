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
	let title = div(`${EXCEL_TAB_TEXT}`, "", { color:`${EXCEL_TITLE_COLOR}`});
	$("#excel-title").html(title);

	let a = getAjaxData2(`/excel-data?uuid=${document.uuid}`);
	$.when(a).done(function(excelData) {
		var jsonObject = $.parseJSON(excelData);
		displaySpreadsheet(jsonObject);
	});
}

function displaySpreadsheet(data) {
	$("#excelcharts").empty();
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
            		    .style("color", EXCEL_HEADINGS_COLOR)
            			.style("background-color", EXCEL_HEADINGS_BACKGROUND_COLOR)
            			.style("text-align", "center");
            	} else if(row % 2 === 0) { 
            		d3.select(this)
            		    .style("color", EXCEL_EVEN_ROWS_COLOR)
            		    .style("background-color", EXCEL_EVEN_ROWS_BACKGROUND_COLOR);
            	} else {
            		d3.select(this)
        		    .style("color", EXCEL_ODD_ROWS_COLOR)
        		    .style("background-color", EXCEL_ODD_ROWS_BACKGROUND_COLOR);            		
            	}
        		d3.select(this).style("border-style", "outset");
			})	        
	      	.text(function(d) { return unescape(d); });
   	    });
}


