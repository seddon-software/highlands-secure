/* 
############################################################
#
#    Highlands Client
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################
*/

// global variables: do not change
var cookies;
var results;
var questions;
var options;
var chartData;

//number of rows and columns in grid (not used in latest version)
var android = navigator.appVersion.indexOf("Android") !== -1;
if(android) {
    var ROWS = 11;
    var COLS = 11;
} else {
    var ROWS = 21;
    var COLS = 21;
}

function div(item, id, css) {
	let html = $(`<div>${item}</div>`);
	if(id) html.attr("id", id);
	if(css) html.css(css);
	return html;
}

function span(item, id, css) {
	let html = $(`<span>${item}</span>`);
	if(id) html.attr("id", id);
	if(css) html.css(css);
	return html;
}

function setStyles() {
	function addClassRuleToStylesheet(rule) {
		sheet.insertRule(rule, sheet.cssRules.length);		
	}
	let noOfStylesheets = window.document.styleSheets.length;
    let sheet = window.document.styleSheets[noOfStylesheets-1];

    addClassRuleToStylesheet(`
	    .ui-widget-content.ui-helper-clearfix {
	    	margin-top: 0;
		}`);

    addClassRuleToStylesheet(`
    	.ui-widget-header .ui-state-active { 
    		border-color: ${ACTIVE_TAB_BUTTON_BORDER_COLOR};
    		background-color: ${ACTIVE_TAB_BUTTON_BORDER_COLOR}; 
	    }`);
    		
    addClassRuleToStylesheet(`
		.ui-widget-header  {
			border: 0;
			background: ${TAB_HEADING_BACKGROUND_COLOR};
		}`);
    addClassRuleToStylesheet(`
	    .ui-dialog-buttonpane {
	    	margin-top: 0;
	    }`);
    addClassRuleToStylesheet(`
		.button {
		    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);
			background-color: red;
	    }`);

    addClassRuleToStylesheet(`
	    .internal {
	        height: 100%;
	        width: 100%;
	        font-size: 150%;    
	        line-height: 100%;
	        border-width: 1px;
	        border-style: solid;
	        border-color: white;
	        filter: drop-shadow(1px 1px 5px #808080);
	        overscroll-behavior: contain;
	    }`);
    addClassRuleToStylesheet(`
	    .square {
	        float: left;
	        margin: 0;
	        padding: 0;
	    }`);
    addClassRuleToStylesheet(`
	    .ui-overlay-a, .ui-page-theme-a, .ui-page-theme-a .ui-panel-wrapper {
	    	text-shadow: 0 0 0 #f3f3f3
	    }`);

    $(".tabs-button").css({
    	"border":"red",
    	"color":TAB_BUTTON_COLOR,
    	"background-color":TAB_BUTTON_BACKGROUND_COLOR
    });

	$("#errorMessage").css({
		"font-size": "x-large",
		"color": ERROR_MESSAGE_COLOR
	});

	$("div#canvas").css({
		"background-color": ASSESSMENT_BACKGROUND_COLOR
	});

	$("div#tabs").css({
		"background-color": BACKGROUND_COLOR
	});

	$("div#headings").css({
		"display": "flex",
		"width": "100%",
		"flex-direction": "row",
		"justify-content": "center",
		"align-items": "center",
		"align-content": "space-between",
		"background-color": TITLE_BAR_COLOR
	});

	$(".tab-title, #charts-title, #piecharts-title").css({
	    "text-align": "center",
	    "font-size": "xx-large",
	    "margin-bottom": "4vh",
	    "color": CHARTS_TITLE_COLOR
	});
	
	$("#overview-tab, #responses-tab, #growth-tab, .ui-page").css({
	    "background-color": CHART_BACKGROUND_COLOR
	});
	
	$("#tabs, #responses-tab, #piechart > div").css({
	    "background-color": CHART_BORDER_COLOR
	});

	$("#heading-frame").css({
		"display": "flex",
		"flex-direction": "column",
//		"width": "100%",
		"text-align": "center",
//		"border-top": BANNER_TITLE_COLOR,
//		"border-bottom": BANNER_TITLE_COLOR,
//	    "border-width": "5px",
//	    "border-top-style": "solid",
//	    "border-bottom-style": "solid",
		"padding-left": "15vw",
	    "font-size": "xx-large",
		"color": BANNER_TITLE_COLOR
	});
}

function questionAnswered(selector, n) {
    $(selector).css("background-color", QUESTION_ANSWERED_COLOR);
    $(`#title-${n}`).css("color", "black");
	$(`#asterisk-${n}`).text("");
	$("#errorMessage").html("");
}

function questionAnswerInvalid(selector, n) {
    $(selector).css("background-color", QUESTION_ANSWER_INVALID_COLOR);	
}

function removeCookiesOnStartup() {
	var cookies = $.cookie();
	for(let cookie in cookies) {
	   $.removeCookie(cookie);
	}
}

function useCookiesToSetFields(selector, textbox, n, questionType) {
    let cookieValue = $.cookie(`cookie${n}`);
    if(cookieValue) {
    	let cookieContents = JSON.parse($.cookie(`cookie${n}`));
    	$(textbox).val(cookieContents.name);
    	questionAnswered(selector, n);
		results[n] = keyValuePair(questionType, { "question":n, "name":cookieContents.name });
    }
}

function keyValuePair(key, value) {
	let o = {}
	o[`${key}`] = value;
	return o;
}

function displayQuestion(questionNumber, questionText, i, questionType) {
	let selector = `#border${i}`;
	let period = ". ";
	let asterisk = `<span id="asterisk-${i}" style="color:red;font-size:x-large"></span>`;
	
	if(questionNumber === "") { 
		questionNumber = "";	// titles don't have question numbers
		period = "";			// don't put a period in front of title
	}
	let title = div(`<br/><b>${asterisk}${questionNumber}${period}${questionText}</b>`, `title-${i}`);
	title.addClass("titles");
	$(selector).append(title);
	if(questionType === "title") {
		let css = {"background-color":QUESTION_HEADER_COLOR,
				   "font-size":"xx-large",
				   "text-align":"center",
				   "margin-top":QUESTION_MARGIN_TOP};
		$(title).css(css);		
	}
}

function displayCheckboxes(options, marks, n, questionType, questionNumber) {
	let selector = `#border${n}`;
	for(var i = 0; i < options.length; i++) {
    	let checkbox = span(`<input type="checkbox" name="checkbox${n}" id="check-${questionNumber}-${i}" value="${i}"`);
	    $(selector).append("<span>");
	    $(selector).append(checkbox);
	    $(selector).append(options[i]);
	    $(selector).append("</span></br>");
	}
	
	// change the color when checkbox selected
	$(`input[type=checkbox][name=checkbox${n}]`).change(function(event) {
	    let checkedValues = "";
	    let checkedMarks = "";
	    $(`input[name="checkbox${n}"]:checked`).each(function() {
	    	checkedValues += this.value + " ";
	    	checkedMarks += marks[this.value] + " ";
	    });
	    if(checkedValues === "") {		// user has unchecked everything
	    	questionAnswerInvalid(selector, n);
	    	cancelResult(n);
	    } else {
			questionAnswered(selector, n);
	    	let section = questions[n][1];
	    	let optionCount = options.length;
			results[n] = keyValuePair(questionType, {
					"question"    : questionNumber, 
					"section"     : section, 
					"selection"   : checkedValues, 
					"marks"       : checkedMarks, 
					"optionCount" : optionCount});	    	
	    		}
	});
}

function displayRadioButtons(options, marks, n, questionType, questionNumber) {
	let selector = `#border${n}`;
	for(var i = 0; i < options.length; i++) {
		let radioButton = $(`<input type="radio" name="radioButton${n}" id="radio-${questionNumber}-${i}" value=` + `${i}` + ' />');
	    $(selector).append("<span>");
	    $(selector).append(radioButton.clone());
	    $(selector).append(options[i]);
	    $(selector).append("</span></br>");
	}

	// change the color when radio button selected
	$(`input[type=radio][name=radioButton${n}]`).change(function(event) {
    	questionAnswered(selector, n);
    	let section = questions[n][1];
    	let optionCount = options.length;
    	let value = $(`input[name=radioButton${n}]:checked`).val();
		results[n] = keyValuePair(questionType, {
			"question"    : questionNumber, 
			"section"     : section, 
			"selection"   : value, 
			"marks"       : marks[value], 
			"optionCount" : optionCount
		});
	});
}

function cancelResult(n) {
	results[n] = undefined;
}

function displayEmail(text, n, questionType, autoFill, questionNumber) {
	let selector = `#border${n}`;
	if(text.trim() !== "blank" && text.trim() !== "autofill") $(selector).append(div(text));
	let textbox = div(`<input type="text" name="text${n}" id="text-${questionNumber}"`);
    $(selector).append(textbox);
    textbox.css({"width":"100%", "transform":`translateX(${PERCENTAGE_SHIFT_TEXTBOX_RIGHT}%)`});
    // not using autofill here: email should be filled in from document.email property
    //    if(autoFill) useCookiesToSetFields(selector, `#text-${questionNumber}`, n, questionType);
    $(`#text-${questionNumber}`).val(document.email);
	let answer = {"question":questionNumber, "name":document.email}
	results[n] = keyValuePair(questionType, answer);
	questionAnswered(selector, n);

	// make this field read only (but not for automatic tests)
	if(!document.auto)
		$(`#text-${questionNumber}`).prop("readonly", true);
    
    // this field is automatically fiiled in and is read only.  Therefore the change function is longer called.
    // change the color when text changed
    $(`#text-${questionNumber}`).change(function(event) {
    	function isEmail(email) {
    		let regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    		return regex.test(email);
    	}
    	let value = $(this).val();
    	if(isEmail(value.trim())) {
    		let answer = {"question":questionNumber, "name":value}
    		questionAnswered(selector, n);
    		results[n] = keyValuePair(questionType, answer);
		    if(autoFill) $.cookie(`cookie${n}`, JSON.stringify(answer));
    	} else {
    		questionAnswerInvalid(selector, n);
    		cancelResult(n);
    	}
	});	
}

function displayClient(text, n, questionType, autoFill, questionNumber) {
	// no autofill for client
	let selector = `#border${n}`;
	if(text.trim() !== "blank" && text.trim() !== "autofill") $(selector).append(div(text));
	let textbox = div(`<input type="text" name="text${n}" id="text-${questionNumber}"`);
    $(selector).append(textbox);
    textbox.css({"width":"100%", "transform":`translateX(${PERCENTAGE_SHIFT_TEXTBOX_RIGHT}%)`});
    if(autoFill) useCookiesToSetFields(selector, `#text-${questionNumber}`, n, questionType);

    // change the color when text changed
    $(`#text-${questionNumber}`).change(function(event) {
    	let value = $(this).val();
    	if(value.trim() === "") { // user has erased input
    		questionAnswerInvalid(selector, n);
    		cancelResult(n);
    	} else {
    		questionAnswered(selector, n);
    		results[n] = keyValuePair(questionType, {"question":questionNumber, "name":value});
    	    if(autoFill) $.cookie(`cookie${n}`, value);    			
    	}
	});	
}

function displayTextArea(text, n, questionType, autoFill, questionNumber) {
	let selector = `#border${n}`;
	if(text.trim() !== "blank" && text.trim() !== "autofill") $(selector).append(div(text));
	let textbox = div(`<textarea rows="${TEXTAREA_ROWS}" cols="${TEXTAREA_COLS}" style="min-width:${TEXTAREA_MIN_WIDTH};max-width:${TEXTAREA_MAX_WIDTH}" name="text${n}" id="text-${questionNumber}"`);
    $(selector).append(textbox);
    textbox.css({"padding":TEXTAREA_PADDING});
    // "transform":`translateX(${PERCENTAGE_SHIFT_TEXTBOX_RIGHT}%)`
    if(autoFill) useCookiesToSetFields(selector, `#text-${questionNumber}`, n, questionType);

    // change the color when text changed
    $(`#text-${questionNumber}`).change(function(event) {
    	let value = $(this).val();
    	if(value.trim() !== "") {
    		let answer = {"question":questionNumber, "name":value};
	    	questionAnswered(selector, n);
			results[n] = keyValuePair(questionType, answer);
		    if(autoFill) $.cookie(`cookie${n}`, JSON.stringify(answer));
    	} else {
    		cancelResult(n);
    		questionAnswerInvalid(selector, n);
    	}
	});
}

function displayText(text, n, questionType, autoFill, questionNumber) {
	let selector = `#border${n}`;
	if(text.trim() !== "blank" && text.trim() !== "autofill") $(selector).append(div(text));
	let textbox = div(`<input type="text" name="text${n}" id="text-${questionNumber}"`);
    $(selector).append(textbox);
    textbox.css({"width":"100%", "transform":`translateX(${PERCENTAGE_SHIFT_TEXTBOX_RIGHT}%)`});
    if(autoFill) useCookiesToSetFields(selector, `#text-${questionNumber}`, n, questionType);

    // change the color when text changed
    $(`#text-${questionNumber}`).change(function(event) {
    	let value = $(this).val();
    	if(value.trim() !== "") {
    		let answer = {"question":`${questionNumber}`, "name":value}
	    	questionAnswered(selector, n);
			results[n] = keyValuePair(questionType, answer);
		    if(autoFill) $.cookie(`cookie${n}`, JSON.stringify(answer));
    	} else {
    		cancelResult(n);
    		questionAnswerInvalid(selector, n);
    	}
	});
}

function displayTitle(text, n, questionNumber) {
	let selector = `#border${n}`;
 	let css = {"background-color":QUESTION_HEADER_COLOR, 
			   "font-size":"large"};
 	let html = div(text, `title${n}`, css);
    $(selector).append(html);
    results[n] = {"title":{"question":questionNumber}};
}

function drawTable(selector, options, n, questionType, questionNumber) {
	let rows = options.length;
	let cols = options[0].length;
	
	let rowText = [];
	let columnText = [];
	for(let r = 1; r < rows; r++) {
	    rowText.push(options[r][0]);	
	}
	for(let c = 1; c < cols; c++) {
	    columnText.push(options[0][c]);	
	}
	
	function getTemplateSpacing(hw) {
		let n, space;
		let extraSpaces = TABLE_COLUMN_SPACING;
		if(hw === 'h') {
			n = rowText.length + 1;
			space = TABLE_SPACING_BETWEEN_ROWS;
		}
		if(hw === 'w') {
			n = columnText.length + 1;
			space = 90/(n+extraSpaces);
		}
		let spacing = "";
		for(let i = 0; i < n; i++) {
			// make the first width (1+extraSpaces) times as big as others
			if(hw === 'w' && i === 0) 
				spacing += `${(1+extraSpaces)*space}v${hw} `;
			else
				spacing += `${space}v${hw} `;	
		}
		return spacing;
	}
	let container = div("", `table${n}`, {"display":"grid"});
	$(selector).append(container);
	$(container).css({"grid-template-rows":`${getTemplateSpacing('h')}`, "grid-template-columns":`${getTemplateSpacing('w')}`}); 
	
	for(let row = 0; row < rowText.length+1; row++) {
		for(let col = 0; col < columnText.length+1; col++) {
			let html;
			if(row == 0 && col == 0) {
				html = div("&nbsp;");
			} else if(row == 0 && col >= 1) {
				html = div(`${columnText[col-1]}`, `radio-${questionNumber}-${row}-${col}`);
				html.css({"text-align": "center", "transform":"translateX(-50%)"});
			} else if (row >= 1 && col == 0) {
				html = div(`${rowText[row-1]}`, `radio-${questionNumber}-${row}-${col}`);			
				html.css({"text-align":"left", "margin-left":"5px", "margin-right":"5px", "transform":"translateX(0%)"});
			} else {
			    let css = "display: block; margin-right: auto; margin-left: auto;";
			    let name;
			    if(questionType === "table")
			    	name = `radio-${n}-${row}`
			    else
			    	name = `radio-${n}`
				html = div(`<div style="${css}""><input style="${css}" type="radio" name="${name}" id="radio-${questionNumber}-${row}-${col}" value="${row}:${col}"></div>`);
				$(container).append(html);
				html.css({"transform":`translateX(-50%)`});
			}
			if(row == 0 || col == 0) $(container).append(html);
		}
	}
	return rows - 1;	// used to size array of results
}

function displayTable(entry, n, questionType, questionNumber) {
	let selector = `#border${n}`;
	let options = entry[1];
	let rows = drawTable(selector, options, n, questionType, questionNumber);	
	let values = Array(rows);
	
	$(`#table${n} input:radio`).on('change', function(event){
		function handleTable() {
			let pair = value.split(':').map(Number);
			let buttonRow = pair[0] - 1;	// row of radio buttons
			let button = pair[1];		// which button
			values[buttonRow] = button;
			
			if(!values.includes(undefined)) {
				questionAnswered(selector, n);
				let marks = [];
				for(let i = 0; i < values.length; i++) {
					let mark = options[i+1][values[i]];
					marks.push(mark);
				};
		    	let section = questions[n][1];
		    	let optionCount = options[0].length - 1;  // -1 for the sidebar text
				results[n] = keyValuePair(questionType, {
					"question"   : questionNumber, 
					"section"    : section, 
					"selection"  : values, 
					"marks"      : marks, 
					"optionCount": optionCount
		});
			}
		}
		function handleTable2() {
			function getLabels() {
				let xLabels = [];
				let yLabels = options[0].slice();
				yLabels.splice(0, 1);
				for(let i = 1; i < options.length; i++) {
					xLabels.push(options[i][0])
				}
				return [xLabels, yLabels]
			}
			let pair = value.split(':').map(Number);
			let buttonRow = pair[0];
			let buttonCol = pair[1];
			let mark = options[buttonRow][buttonCol];

			questionAnswered(selector, n);
	    	let section = questions[n][1];
	    	let cols = options[0].length - 1;
	    	let rows = options.length - 1;
	    	let optionCount = `${rows}:${cols}`;
			results[n] = keyValuePair(questionType, {
				"question"   : questionNumber, 
				"section"    : section, 
				"selection"  : value, 
				"marks"      : mark, 
				"xTitle"     : 'Market Growth',
				"yTitle"     : 'Client Revenue Growth',
				"xLabels"    : getLabels()[0],
				"yLabels"	 : getLabels()[1],
				"optionCount": optionCount});
			}
		let name = event.currentTarget.name;
		let value = event.currentTarget.value;
		if(questionType === "table") handleTable();
		if(questionType === "table2") handleTable2();
	});
}
 
function displayQuestionsAndOptions() {
 	function zip(a, b) {
		var result = [];
		for(var i = 0; i < a.length; i++){
			result.push([a[i], b[i]]);
		}
		return result;
	}
	
	results = new Array(questions.length);
 	let entries = zip(questions, options);
    for(var i = 0; i < entries.length; i++) {
    	let entry = entries[i];
		let questionNumber = entry[0][0];
		let questionSection = entry[0][1];
		let questionText = entry[0][2];
		let questionType = entry[0][3]; 
		let autoFill = entry[0][4];
		let options;
		let marks;
		let html = $(`<div id='border${i}'/>`);
		$("#questions").append(html);
		html.css({"margin-left":MARGIN_LEFT, "margin-right":MARGIN_RIGHT, "background-color":QUESTION_BODY_COLOR});

		displayQuestion(questionNumber, questionText, i, questionType);
		if(questionType === "radio") {
			options = entry[1][0];
			marks = entry[1][1];
			displayRadioButtons(options, marks, i, questionType, questionNumber);
		}
		if(questionType === "checkbox") {
			options = entry[1][0];
			marks = entry[1][1];
			displayCheckboxes(options, marks, i, questionType, questionNumber);
		}
		if(questionType === "text") {
			text = entry[1][0];
			displayText(text[0], i, questionType, autoFill, questionNumber);
		}
		if(questionType === "textarea") {
			text = entry[1][0];
			displayTextArea(text[0], i, questionType, autoFill, questionNumber);
		}
		if(questionType === "email") {
			text = entry[1][0];
			displayEmail(text[0], i, questionType, autoFill, questionNumber);
		}
		if(questionType === "client") {
			text = entry[1][0];
			displayClient(text[0], i, questionType, autoFill, questionNumber);
		}
		if(questionType === "title") {
			text = entry[1][0];
			displayTitle(text[0], i, questionType, questionNumber);
		}
		if(questionType === "graph") {
 			options = entry[1];
			displayGraph(options, i, questionType, questionNumber);
		}
		if(questionType === "table") {
			displayTable(entry, i, questionType, questionNumber);
		}
		if(questionType === "table2") {
			displayTable(entry, i, questionType, questionNumber);
		}
    }
}

function positionCopyright() {
    $("#copyright").html(COPYRIGHT_MESSAGE);
    $("#copyright").css("color", COPYRIGHT_TEXT_COLOR)
    			   .css("background-color", COPYRIGHT_BACKGROUND_COLOR)
                   .css("bottom", "0px")
                   .css("position", "fixed");
}
    
function getQuestions() {
    $.ajax(
    {
        url: '/questions',
        type: 'GET',
        contentType:'application/json',
        dataType:'json',
        success: function(data) {
        	questions = data;
        }	
    });
}

function getOptions() {
    $.ajax(
    {
        url: '/options',
        type: 'GET',
        contentType:'application/json',
        dataType:'json',
        success: function(data) {
        	options = data;
        	displayQuestionsAndOptions();
        }	
    });
}

function addClickHandlers() {
	function allQuestionsAnswered() {
		let all = true;
		for(let i = 0; i < results.length; i++) {
			if(results[i] === undefined) {
				all = false; break;
			}
		}
		return all;
	}

	function continueOrExit() {
		function clearPage() {
		    $("#questions").empty();
			getQuestions();
			getOptions();
			positionCopyright();
		}
		$("#modal_dialog").dialog({
		    resizable: false,
		    height:"auto",
		    title: "Highlands Assessment",
		    modal: true,
		    buttons: {
		    	"No": {
		    		id: "continue-no", 
		    		text: "No", 
		    		click: function() {
		    			$(this).dialog("close");
		    			setInterval(function() {location.assign(`${WHERE_TO_GO_ON_EXIT}`)}, 500);
		    		}
		    	},
		    	"Yes": {
		    		id: "continue-yes", 
		    		text: "Yes", 
		    		click: function() {
		    			$(this).dialog("close");
		    			clearPage();
		    		}
		    	}
		    }
		});
			
		$("#modal_dialog").html("Do you want to complete another client profile?")
		                  .css({"font-size":"large", "background-color":DIALOG_BACKGROUND_COLOR});
	}

	function highlightMissingAnswers() {
		for(let n = 0; n < results.length; n++) {
			console.log(n, results[n]);
			if(!results[n]) {
				$(`#asterisk-${n}`).text("* ");
			}
		}
	}
	
	$("#showResults").mousedown(function(e) {
		setTimeout(function() {
			if(allQuestionsAnswered()) {
				$("#errorMessage").html("Results Submitted");
				let resultsAsText = JSON.stringify(results);
   	        	console.log(results);
				$.ajax(
			   	    {
			   	        url: '/results',
			   	        type: 'POST',
			   	        contentType:'application/json',
			   	        dataType:'text',
			   	        data: resultsAsText,
			   	        success: function(data) {
			   	        	console.log("results sent OK");
			   	        	continueOrExit();
			   	    }	
			   	});
			} else {
				$("#errorMessage").html("Some questions still need valid answers");
				$("#errorMessage").css({"margin-left":`${MARGIN_LEFT}`});
   	        	setTimeout(function() {highlightMissingAnswers()}, 50);
			}
		}, 250);
    });    
}
