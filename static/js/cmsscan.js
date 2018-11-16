function init_scan(){
	$.post( "/scan", $("#scan_form").serialize(), function( data ) {
	  if (data.error){
	  	 $.growl({ title: "Error", message: data.error, style: 'error', location:'br'});
	  } else {
	  	 var msg = data.url + '<br>(' + data.cms + ') - ' + data.message
	  	 $.growl({ title: "Success", message: msg, style: 'notice', location:'br'});
	  }

	});
	return false;
}


function delete_result(id, elm) {
	$.confirm({
    title: 'Are you sure?',
    content: 'Delete the scan results permenently',
    type: 'red',
    typeAnimated: true,
    buttons: {
        tryAgain: {
            text: 'Delete',
            btnClass: 'btn-red',
            action: function(){
            	$.post( "/delete", { id: id}, function( data ) {
				  if (data.status === "ok"){
				  	 $.growl({ title: "Success", message: 'Scan Deleted!', style: 'notice', location:'br'});
				  	setTimeout(function(){
					   window.location.reload();
					}, 1000);
				  } else {
				  	 $.growl({ title: "Error", message: 'Failed to Delete Scan!', style: 'error', location:'br'});  	 
				  }

				});
            }
        },
        close: function () {
        }
    }
});
}