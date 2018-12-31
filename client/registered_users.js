/* 
############################################################
#
#    Highlands Client
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################
*/


function displayRegisteredUsers() {
	$("#registerUsersInfo").empty();
	let title = div(`${REGISTERED_USERS_TAB_TEXT}`, "", { color:`${REGISTERED_USERS_TITLE_COLOR}`});
	$("#registerUsers-title").html(title);
	let a = getAjaxData3(`/registered-users?uuid=${document.uuid}`);
	$.when(a).done(function(data) {
		var jsonObject = $.parseJSON(data);
		doTable(jsonObject);
	});
}

function doTable(data) {
	$("#registerUsersInfo").empty();
	d3.select("#registerUsersInfo")
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
