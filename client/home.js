/* 
############################################################
#
#    Highlands Client
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################
*/


function displayCompletedAssessments() {
	$("#completed-assessments").empty();
	$("#home-title").html(HOME_TAB_TITLE);
	let title = div(`${COMPLETED_ASSESSMENTS_TAB_TEXT}`, "", { color:`${COMPLETED_ASSESSMENTS_TITLE_COLOR}`});
	$("#completed-assessments-title").html(title);
	let a = getAjaxData3(`/completed-assessments?email=${document.email}&uuid=${document.uuid}`);
	$.when(a).done(function(data) {
		var jsonObject = $.parseJSON(data);
		doAssessmentTable(jsonObject);
	});
}

function doAssessmentTable(data) {
	$("#completed-assessments").empty();
	d3.select("#completed-assessments")
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
	      	.html(function(d) { return unescape(d); });
   	    });
	$(".pdfView").click(function() {
		$("#display-pdf").dialog();
		$("#display-pdf").dialog("option", "width", window.innerWidth);
		$("#display-pdf").dialog("option", "height", window.innerHeight);

		$("#display-pdf").html(
			`<embed src="/download-pdf?pdf=${this.id}" type="application/pdf" 
			        width="100%" height="100%">&nbsp;> 
			 </embed>`);
	});
}
