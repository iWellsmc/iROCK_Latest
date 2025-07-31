$(document).on('keyup','.new_level_cls',function(){
    levelid = $(this).attr('data_id')
    currentposition=$(this)
    savebtb=$('.final-cls')
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token},
      url: "/cost_code/validatecclevel/",
      data: {'currentval':$.trim($(this).val()),'levelid':levelid},
      success: function(data){
        currentposition.next('.waring-err').remove()
        if (data.status == true){ 
            currentposition.addClass('con_error')
            currentposition.after('<span class="waring-err">Component Name Already Exists</span>')
            savebtb.attr('disabled',true)
        }
        else{
            currentposition.removeClass('con_error')
            savebtb.attr('disabled',false)
        }
       }
    });
   })

   $(document).on('click','.final-cls',function(){
    $('.final-cls').attr('disabled',false)
   })