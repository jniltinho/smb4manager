


// Delete user
$("#users a.btn-danger").on("click",function(e){
      e.preventDefault();
      var username = $( this ).attr('data-user');
      var button   = $(this);
      bootbox.confirm("Do you want to delete?", function(result) {
               if (result) {
                  $(".loading").show();
                   button.addClass("disabled");
                   $.getJSON($SCRIPT_ROOT + '/users/del/' + username, { user: username }, function(responseText) {
                          $(".loading").hide();
                          bootbox.alert(responseText.message, function() { location.reload(); });
                 });
                }
               });
 });


// Edit User
 $("#users a.btn-info").on("click",function(e){
        e.preventDefault();
        var rid = $( this ).attr('data-rid');
        window.location = ('/users/edit/' + rid); 
 }); 



// bind form using ajaxForm 
// Form AddUser -> users_add
$('#users_add').ajaxForm({ 
        beforeSubmit:  showRequest,
        success:   showResponse,
        dataType:  'json', 
        clearForm: true,
        resetForm: true
}); 

function showRequest(formData, jqForm, options) { 
           $(".loading").show();
           $("#users_add :submit").prop("disabled", true);
           return true; 
}

function showResponse(responseText, statusText, xhr, $form) { 
         $(".loading").hide();
         bootbox.alert(responseText.message, function() {
              window.location="/users/";
         });
} 
