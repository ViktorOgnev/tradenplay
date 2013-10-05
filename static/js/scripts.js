////////////////////////////////////////////////////////////////////////////////
// Success functions for different successful ajax events //////////////////////
////////////////////////////////////////////////////////////////////////////////

function productReviewSuccess(json_response) {
	$("#review_errors").empty();
	// evaluate the "success" parameter
	console.log("productReviewSuccess have been called");
	if (json_response.success == "True") {
		// disable the submit button to prevent duplicates
		$("#submit_review").attr('disabled', 'disabled');
		// if this is first review, get rid of "no reviews" text
		$("#no_reviews").empty();
		// add the new review to the reviews section
		$("#reviews").prepend(json_response.html).slideDown();
		// get the newly added review and style it with color
		new_review = $("#reviews").children(":first");
		new_review.addClass('new_review');
		// hide the review form
		$("#review_form").slideToggle();
	} else {
		//add the error text to the review_errors div
		$("#review_errors").append(json_response.html);
	}
}

function tagSuccess(json_response) {
	console.log("tagSuccess have been called");
	if (json_response.success == "True") {
		$("#add_tag").attr('disabled', 'disabled');
		$("#tags").empty();
		$("#tags").prepend(json_response.html).slideDown();
	}
}

function loginFormSuccess(json_response) {
	console.log("loginFormSuccess have been called");
	console.log(json_response.html);
	if (json_response.success == "True") {

		// Get rid of the existing auth links
		//$("#auth_box").empty();
		$("#authbox_login_container>popover-content").empty();
		// renew the contents of tagbox
		//$("#auth_box").prepend(json_response.html).slideDown();
		$("#authbox_login_container>popover-content").prepend(json_response.html).slideDown();

	} else {
		//add the error text to the errors div
		//$("#auth_box").append(json_response.html);
		$("#authbox_login_container>popover-content").append(json_response.html);
	}
}

function logoutLinkSuccess(json_response) {
	console.log("logoutLinkSuccess have been called");
	if (json_response.success == "True") {

		// Get rid of the existing auth links
		$("#auth_box").empty();
		// renew the contents of tagbox
		$("#auth_box").prepend(json_response.html).slideDown();

	} else {
		//add the error text to the review_errors div
		$("#auth_box").append(json_response.html);
	}
}

function loginLinkSuccess(json_response) {
	console.log("loginLinkSuccess have been called");
	console.log(json_response.html);
	if (json_response.success == "True") {

		// Get rid of the existing auth links
		$("#auth_box").empty();
		// renew the contents of tagbox
		$("#auth_box").prepend(json_response.html).slideDown();

	} else {
		//add the error text to the errors div
		$("#auth_box").append(json_response.html);
	}
}
////////////////////////////////////////////////////////////////////////////////
// Ajax event handlers                                    //////////////////////
////////////////////////////////////////////////////////////////////////////////

function ajaxSubmit(event, successFunction) {
	
	console.log("ajaxSubmit have been called");
	event.preventDefault();
	var form = $(event.target);
	$.ajax({
		url : form.attr('action'),
		type : form.attr('method'),
		data : form.serialize(),
		dataType : 'json',
		success : successFunction,
		error : function (xhr, textStatus, errorThrown) {
			//log ajax errors
			console.log("There was an error processing ajax request: \n" +
				"\t -the text status is: ' " + textStatus + "'\n" +
				"\t -the error thrown is:' " + String(errorThrown) + "'" +
				"\t -the data sent  is: ' " + this.data + "'" +
				"\t -the method is: ' " + this.type + "'");
		}
	});
}








// ajax-process autorisation liks such as login, logout and sign-in
function processAuthLink(event, successFunction) {
	console.log("processAuthLink have been called");
	event.preventDefault();
	var ancor = $(event.target);
	$.ajax({
		url : ancor.attr('href'),
		//type: 'GET',
		// data: ancor.serialize(),
		dataType : 'json',
		success : successFunction,
		error : function (xhr, textStatus, errorThrown) {
			//log ajax errors

			console.log("There was an error processing ajax request: \n" +
				"\t -the text status is: ' " + textStatus + "'\n" +
				"\t -the error thrown is:' " + String(errorThrown) + "'" +
				"\t -the data sent  is: ' " + this.data + "'");
			//console.log(xhr);
			//console.log(thrownError);

		}
	});
};

function slideToggleReviewForm() {
	$("#review_form").slideToggle();
	$("#add_review").slideToggle();
}

function statusBox() {
	$('<div id="loading">Loading...</div>')
	.prependTo("#main")
	.ajaxStart(function () {
		$(this).show();
	})
	.ajaxStop(function () {
		$(this).hide();
	})
}

function prepareDocument() {
	//prepare the search box
	$("#id_q").click(function (event) {
		$(event.target).attr("value", "");
	});
	$("form#search").submit(function () {
		text = $("#id_q").val();
		if (text == "" || text == "Search" || text.length < 2) {
			/* alert("Enter a search term."); */
			return false;
		}
	});
	// Prepare product review form
	$("form#review").submit(function (evnt) {
		ajaxSubmit(evnt, productReviewSuccess);
	});

	$("#cancel_review").click(slideToggleReviewForm);
	// Tagging functionality
	$("form#tag").submit(function (event) {
		ajaxSubmit(event, tagSuccess);
	});
	$("#id_tag").click(function (event) {
		$(event.target).attr("value", "");
	});
	// Authorisation functionality
	$("#logout").click(function (event) {
		processAuthLink(event, logoutLinkSuccess);
	});

	$('#login').popover({
		content : function () {
			return $('#popover_content_wrapper').html();
		},
		html : true,
		placement : 'bottom'
	});
	
    
});

	//$("#login").click(function(event){offer_login(event);});
	$("popover-content>#login_form").submit(function (event) {
		ajaxSubmit(event, loginFormSuccess);
	});

	statusBox();
}

$(document).ready(prepareDocument());
