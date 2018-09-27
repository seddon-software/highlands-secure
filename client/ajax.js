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

function getAjaxData2(url, fn) {
    let a = $.ajax(
    {
        url: url,
        type: 'GET',
        contentType:'application/json',
        dataType:'json'
    });
    return a;
}

function getAjaxData3(url, fn) {
    let a = $.ajax(
    {
        url: url,
        type: 'GET',
        contentType:'application/text',
        dataType:'text'
    });
    return a;
}

