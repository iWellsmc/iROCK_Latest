

var ids=1
$(document).on('click','#add',function(){
    var html ='<tr> <td class="wid-tx"><input type="text" autocomplete="off" data-error="2" name="role_id" id="taxnameid'+ids+'" class="form-control taxnamecls bot-pha" placeholder="Role Name"></td> <td class="same-line-tx"><button id="add" class="btn btn-clr add-btn pha-sebtn ml-2" type="button" value="Add"> <i class="fa fa-plus"></i> </button> <button id="delete" class="btn btn-clr delete-btn" type="button" value="delete"> <i class="fa fa-minus"></i> </button></td></tr>'
    $(this).closest('table').append(html)
    ids ++;

})


$(document).on('click','#delete',function(){
    var table_len=$('#tax_table_id tbody tr').length
    if (table_len > 1){
        $(this).closest('tr').remove()
    }

})

$(document).ready(function(){

    $('#addtaxformid').validate(); 
    $("[name=taxtype]").rules("add", {
        required: true,
        });  
         
    $("[name=taxname]").each(function(){
        $(this).rules("add", {
            required: true,
        });
    })
})

    $(document).on('keyup','.taxnamecls',function(){
        //$(".taxnamecls").focusout(function(){
        var val=$(this).val().toLowerCase()
        $(this).closest('td').find('span').remove();
        var currentelement=$(this)
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken":  csrf_token },
            url: "/invoiceguard/validaterole/",
            data: {'role_name':$.trim(val)},
            success: function(data){
                if (data.status == true){ 
                    // currentelement.attr('data-error',0); 
                    currentelement.closest('td').find('span').remove();
                    currentelement.after('<span class="waring-err">Role Already Exists</span>')
                }
                else{
                        currentelement.closest('td').find('span').remove();
                        $('.final-cls').prop('disabled',false)
                        var z=0;
                        $("input").each(function(){
                            if (val !='' && y !=''){
                            var y=$(this).val().toLowerCase();
                            if($.trim(val)==$.trim(y)){
                                z=z+1;
                            }
                        }
                        });
                        
                        if(z > 1){
                            currentelement.closest('td').find('span').remove();
                            // currentelement.addClass("error")
                            // currentelement.attr('data-error',0); 
                            currentelement.after('<span class="waring-err">Role Already Exists</span>')
                        }
                        else{
                            currentelement.removeClass("error")
                            currentelement.attr('data-error',1); 

                        }
                    }
            }
        });
    })

    $(document).on('click','.save-cls',function(e){
        e.preventDefault();
        var tax_type=$('.taxtypecls').find(':selected').val()
        var count = 0
        if (tax_type == ''){
            $('.taxtypecls').addClass('con_error')
            count ++;
        }
        $('.taxnamecls').each(function(){
            var val=$(this).val()
            if (val == ''){
                count ++;
                $(this).addClass('con_error')
            }
            var span_len=$(this).next('span')
            console.log(span_len)
            if (span_len.length > 0){
                count ++;
            }
            
        });
        if (count == 0){
            $('#addtaxformid').submit()
            $(this).prop('disabled',true)
        }
        
    })

    $(document).on('keyup change','.con_error',function(){
        $(this).removeClass('con_error')
    })
    //$('.taxnamecls').keyup(function() {
        $(document).on('keyup','.taxnamecls',function(){
        var $th = $(this);
        $th.val($th.val().replace(/(\s{2,})/g, ' '));
        $th.val($th.val().replace(/^\s*/, ''));
        });