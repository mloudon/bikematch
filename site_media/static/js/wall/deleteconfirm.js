function addDelegates()
{
	$('div.delete-confirm').delegate('a.delete-confirm-option', 'click', function(event) {
		event.preventDefault();
		confirmdiv = $(this).parents('div.delete-confirm');
		deletediv = $(this).closest('div.deleteable');
		
		linktext = $(this).text();
		if (linktext == 'no') {
			confirmdiv.hide();
		}
		else {
			submit_url = $(this).attr('href');
				$.post(submit_url,{}, function(data)
				{
					if (data.success) {
							deletediv.remove();
							
					} else {
					  //add something here  
					}					
			
				}, 'json');
		}
	});
}

$(document).ready(function() {

	$('a.delete-confirm-required').each( function(index) {

		submit_url = $(this).attr('href');
		confirm_html = '<div class="delete-confirm">'
    		+ '<p> are you sure? <a href="'+ submit_url +'" class="delete-confirm-option">yes</a> /'
    		+ ' <a href="" class="delete-confirm-option">no</a></div>'
		$(this).after(confirm_html);
		
		$(this).click(function(event) {
       		event.preventDefault();
       		parentdiv = $(this).parent('div');
			$('div.delete-confirm',parentdiv).show();
    	});
    	
	});
	
	addDelegates();
	$('div.delete-confirm').hide();
});
