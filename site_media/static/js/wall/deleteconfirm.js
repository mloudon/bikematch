function addDelegates()
{
	$('div.delete-confirm').delegate('a.delete-confirm-option', 'click', function() {
		
		confirmdiv = $(this).parents('div.delete-confirm');
		deletediv = $(this).closest('div.deleteable');
		
		linktext = $(this).text();
		
		if (linktext == 'no') {
			
			confirmdiv.hide();
			return false;
		}
		
		submit_url = $(this).attr('href');
		
		
		$.post(submit_url,{}, function(data)
		{
			if (data.success) {
					deletediv.remove();
					
			} else {
			    
			}					
	
		}, 'json');
		return false;
	});
}

$(document).ready(function() {

	$('a.delete-confirm-required').each( function(index) {
		submit_url = $(this).attr('href');
		confirm_html = '<div class="delete-confirm">'
    		+ '<p> are you sure? <a href="'+ submit_url +'" class="delete-confirm-option">yes</a> /'
    		+ ' <a href="" class="delete-confirm-option">no</a></div>'
		$(this).after(confirm_html);
		
		$(this).click(function() {
       		parentdiv = $(this).parent('div');
			$('div.delete-confirm',parentdiv).show();
			return false;
    	});
    	
    	return false;
	});
	
	addDelegates();
	$('div.delete-confirm').hide();
});
