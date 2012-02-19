function addDeleteConfirmHandler(deleteconfirmbutton)
{
		confirmdiv = deleteconfirmbutton.parents('div.delete-confirm');
		deletediv = deleteconfirmbutton.closest('div.deleteable');
		
		linktext = deleteconfirmbutton.text();
		if (linktext == 'no') {
			confirmdiv.hide();
		}
		else {
			submit_url = deleteconfirmbutton.attr('href');
				$.post(submit_url,{}, function(data)
				{
					if (data.success) {
							deletediv.remove();
							
					} else {
					  //add something here  
					}					
			
				}, 'json');
		}
}

function addDeleteConfirm(deletebutton)
{
	submit_url = deletebutton.attr('href');
	confirm_html = '<div class="delete-confirm">'
		+ '<p> are you sure? <a href="'+ submit_url +'" class="delete-confirm-option">yes</a> /'
		+ ' <a href="" class="delete-confirm-option">no</a></div>'
	deletebutton.after(confirm_html);
	
	deletebutton.click(function(event) {
		event.preventDefault();
		parentdiv = $(this).parent('div');
		deleteconfirmdiv = $('div.delete-confirm',parentdiv);
		deleteconfirmdiv.show();
	});
	
	deleteconfirmdiv = $('div.delete-confirm',deletebutton.parent('div'));
	deleteconfirmdiv.hide();
	
	$('a.delete-confirm-option',deleteconfirmdiv).on('click', function(event) {
		event.preventDefault();
		addDeleteConfirmHandler($(this));
	});
}

$(document).ready(function() {

	$('a.delete-confirm-required').each( function(index) {
		addDeleteConfirm($(this));
	});
	
});
