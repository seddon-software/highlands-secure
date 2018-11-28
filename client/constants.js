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
var android = navigator.appVersion.indexOf("Android") !== -1;


// colors
var ACTIVE_TAB_BUTTON_BORDER_COLOR = "black";
var ASSESSMENT_BACKGROUND_COLOR = "thistle";
var BACKGROUND_COLOR = "white";
var BANNER_TITLE_COLOR = "goldenrod";
var CHARTS_TITLE_COLOR = "darkmagenta";
var CHART_BACKGROUND_COLOR = "Gainsboro";
var CHART_BORDER_COLOR = "Gainsboro";
var CHECKBOX_QUESTIONS_COLOR = "blue";
var CHECKBOX_TITLE_COLOR = "darkmagenta";
var COMPLETED_ASSESSMENTS_TITLE_COLOR = "darkmagenta";
var COPYRIGHT_BACKGROUND_COLOR = "rgba(0, 0, 0, 0.1)"; 
var COPYRIGHT_TEXT_COLOR = "rgba(0, 0, 0, 0.6)";
var DIALOG_BACKGROUND_COLOR = 'rgb(255, 150, 200)'; 
var ERROR_MESSAGE_COLOR = "red";
var EXCEL_EVEN_ROWS_BACKGROUND_COLOR = "cornsilk";
var EXCEL_EVEN_ROWS_COLOR = "black";
var EXCEL_HEADINGS_BACKGROUND_COLOR = "darkgoldenrod";
var EXCEL_HEADINGS_COLOR = "white";
var EXCEL_ODD_ROWS_BACKGROUND_COLOR = "wheat";
var EXCEL_ODD_ROWS_COLOR = "black";
var EXCEL_TITLE_COLOR = "darkmagenta";
var GROWTH_HEADING_COLOR = "darkmagenta";
var GROWTH_QUESTIONS_COLOR = "blue";
var GROWTH_TITLES_COLOR = "darkmagenta";
var LOG_TITLE_COLOR = "darkmagenta";
var OVERVIEW_STATUS = "blue";
var PIECHART_TITLES_COLOR = "blue";
var PIECHART_BACKGROUND_COLOR = "Gainsboro";
var PIECHART_BORDER_COLOR = "Gainsboro";
var QUESTION_ANSWER_INVALID_COLOR = "Thistle";
var QUESTION_ANSWERED_COLOR = 'cornflowerblue';
var QUESTION_BODY_COLOR = "DarkSeaGreen";
var QUESTION_HEADER_COLOR = "azure";
var REGISTERED_USERS_TITLE_COLOR = "darkmagenta";
var SYSLOG_TITLE_COLOR = "darkmagenta";
var TAB_BUTTON_COLOR = "black";
var TAB_BUTTON_BACKGROUND_COLOR = "cornflowerblue";
var TAB_HEADING_BACKGROUND_COLOR = "lightgray";
var TABLE_CHARTS_QUESTIONS_COLOR = "blue";
var TABLE_CHARTS_TABS_COLOR = "blue";
var TABLE_CHARTS_TABS_BACKGROUND_COLOR = "antiquewhite";
var TABLE_CHARTS_TITLE_COLOR = "darkmagenta";
var TITLE_BAR_COLOR = "azure";

// fonts
var GRID_CHILDREN_FONT_SIZE = "16px";
var TABLE_TAB_TITLES_FONT_SIZE = "medium"; // xx-small, x-small, small, medium, large, x-large, xx-large

// layout
var BANNER_WIDTH = "60%";
var COPYRIGHT_WIDTH = "50vw";
var MARGIN_LEFT = "5%";
var MARGIN_RIGHT = "5%";
var PERCENTAGE_SHIFT_TEXTBOX_RIGHT = 20;
var QUESTION_MARGIN_TOP = "10vh";
var TEXTAREA_ROWS = 5;
var TEXTAREA_COLS = 80;
var TEXTAREA_MIN_WIDTH = "95%";
var TEXTAREA_MAX_WIDTH = "95%";
var TEXTAREA_PADDING = "5%";
var TABLE_COLUMN_SPACING = 1.0;
var TABLE_SPACING_BETWEEN_ROWS = 5;

// Tab Titles
var ASSESSMENT_TAB_TITLE = "Assessment";
var COMPLETED_ASSESSMENTS_TAB_TEXT = "Completed Assessments";
var HOME_TAB_TITLE = "Coaching"
var OVERVIEW_TAB_TITLE = "Overview";
var RESPONSES_TAB_TITLE = "Responses";
var SCATTER_TAB_TITLE = "Growth";
var CHECKBOXES_TAB_TITLE = "Checkboxes";
var TABLE_CHARTS_TAB_TITLE = "Table Charts";


// Tab Text
var CHECKBOXES_TAB_TEXT = "Checkboxes:";
var EXCEL_TAB_TEXT = "Database Record Dump";
var LOG_TAB_TEXT = "Highlands Assessment Log";
var OVERVIEW_TAB_TEXT = "Forensics:";
var RESPONSES_TAB_TEXT = "Frequency of Answer:";
var REGISTERED_USERS_TAB_TEXT = "Registered Users:";
var SCATTER_TAB_TEXT = "Growth:";
var SYSLOG_TAB_TEXT = "System Logs";
var TABLE_CHARTS_TAB_TEXT = "Table Charts:";

//miscellaneous
var BANNER_TEXT = "Highlands Negotiations LLC";
var COPYRIGHT_MESSAGE = "\u00A9 Highlands Negotiations, 2018-19, v1.1";
var SCATTER_X_TITLE = 'Market Growth';
var SCATTER_Y_TITLE = 'Client Revenue Growth';
var TERMS_AND_CONDITIONS = "http://www.highlandsnegotiations.com/";
var WHERE_TO_GO_ON_EXIT = "http://www.highlandsnegotiations.com/";

// login text
var cookiesText = 
	"This website uses cookies to ensure you get the best experience on our website.<br/>" +
	"We use cookies to save you repeating responses in the assessment you are about to complete.<br/>" +
	"Please click to agree to the use of these cookies";
var cookiesWarning = "please accept cookies before proceeding<br/>";
var doChangePasswordMessage = "change password<br/>"; 
var doLoginErrorMessage = "invalid login attempt(wrong password, invalid email), try again"; 
var doLoginMessage = "login to assessmydeal<br/>";
var doRegisterMessage = "Please enter a password for your account and the code sent to you by email"; 
var greeting = "Assess My Deal: <em>what do you want to do?</em>";
var loginMessage = 
	"<br/><br/><br/>Before you can login you must register.  We will send you a code via email for you to use during " +
    "the registration. " + 
    "<br/>You can change passwords with the facility provided, but if you forget your password " +
    "you will need to re-register." +
    "<br/>Please note that you must use a business email.  We will not accept personal domains such as " + 
    "<em>'hotmail.com'</em> or <em>'google.com'</em>." +
    "<p>Be aware that we collect certain data through the assessment that may be considered personally identifiable, " + 
    `such as your IP address.  For full terms and conditions please click <a href="${TERMS_AND_CONDITIONS}">here</a>.`;
