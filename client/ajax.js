/* 
############################################################
#
#    Highlands Client
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################
*/

/*
 * This function is a simple wrapper around the JQuery AJAX call
 */

function getAjaxData(url, fn) {
    $.ajax(
    {
        url: url,
        type: 'GET',
        contentType:'application/json',
        dataType:'json',
        success: function(data) {
        	fn(data);
        }
    });
}

