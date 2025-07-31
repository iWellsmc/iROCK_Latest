var get_list= [];
$(document).ready(function(){
   
    $(".main_cls option").each(function(key,value) {

    get_list.push({'id':$(this).val(),'name':$(this).text()}); 
    // or $(this).val()
});
})


$(document).on('focus','.taxtypecls',function(){
    previous_val=$(this).val()
    a=$(this).closest('tr').find('.taxtypecls').val()
    b=$(this).closest('tr').prev().find('.taxtypecls').length
    if (b==0){    
        $(this).closest('tr').find('.del_button').attr("disabled", true);
    }
    else{
        
        num=$(this).closest('tr').prev().find('.taxtypecls').val()
        num2=$(this).closest('tr').find('.taxtypecls').val()
        var newArray = get_list.filter(function(item)
        {
        return item.id > num;
        });
        if(parseInt(num) <7){
            var get_element=$(this)
            var option='<option value="">--Select--</option>'
            $(newArray).each(function (key,val) {
                option += '<option value="'+val.id+'">'+val.name+'</option>'
            })
            get_element.html(option);
            $(this).find(`option[value=${previous_val}]`).prop('selected', true)
        }  
    }

    
})


$(document).ready(function(){
    $('#tax_table_id').find('tbody tr:first').find('.del_button').hide()
})


$(document).on('change','.selec_cls',function(){
    a=$(this).closest('tr').find('.selec_cls').val()
    b=$(this).closest('tr').prev().find('.selec_cls').length
    console.log({'len':b})
    if (b==0){    
    $(this).closest('tr').find('.del_button').attr("disabled", true);
    var val=$('#tax_table_id tr:last').find('.selec_cls :selected').val();    
    $(this).closest('tr').nextAll('tr').remove();
    }
    else{
        num=$(this).closest('tr').prev().find('.selec_cls').val()
        num2=$(this).closest('tr').find('.selec_cls').val()
        arr=[]
        
        for(i=parseInt(num)+1;i<=7;i++){
            arr.push(i)
        }
        arr_get_value=arr[0]
        
        if(parseInt(num2)==arr_get_value){
            console.log('success')
        }
        else{
            Swal.fire('Order Mismatch')            
            $(this).closest('tr').find('.selec_cls').prop('selectedIndex',0);
        
        }
    }    
})


$(document).on('change','.newcls',function(){
    html=`<tr class="row mb-3"> <td class="wid-tx wid-tl col-10"><select class="form-control taxtypecls newcls" name="module_id"></select></td> <td class="same-line-tx col-2 add-process-btn-con"><button id="add" class="btn btn-clr add-btn add pha-sebtn" type="button" value="Add" onclick="add_click()"> <i class="fa fa-plus"></i> </button> <button id="delete" class="btn btn-clr delete delete-btn" type="button" value="delete"> <i class="fa fa-minus"></i> </button></td></tr>`
        val=$('#tax_table_id tr:last').prev().find('.taxtypecls :selected').val();
        val_1=$('#tax_table_id tr:last').find('.taxtypecls :selected').val();
        console.log({'val is tr':val})
        arr=[]
        
        for(i=parseInt(val)+1;i<=7;i++){
            arr.push(i)
        }
        arr_get_value=arr[0]
        
        if(parseInt(val_1)==arr_get_value){
            console.log('success')
        }
        else{
            Swal.fire('Order Mismatch')            
            $(this).closest('tr').find('.taxtypecls').prop('selectedIndex',0);
        
        }

})

$(document).on('change','.taxtypecls ',function(){
    var val=$('#tax_table_id tr:last').find('.taxtypecls :selected').val();
    console.log({'val':val})
    if (parseInt(val) == 7){
        $(this).closest('tr').nextAll('tr').remove();
    }
  
})

function add_click(){
    $(document).on('focus','.wid-tl',function(){
    })
}


var ids=1
$(document).on('click','#add',function(){

    var val=$('#tax_table_id tr:last').find('.taxtypecls :selected').val();
    // console.log({'value':val})

    var newArray = get_list.filter(function(item)
    {
    return item.id > val;
    });
    var html =`<tr class="row mb-3"> <td class="wid-tx wid-tl col-10"><select class="form-control form-select taxtypecls newcls" name="module_id"></select></td> <td class="same-line-tx col-2 add-process-btn-con"><button id="add" class="btn btn-clr add-btn add pha-sebtn" type="button" value="Add" onclick="add_click()"> <i class="fa fa-plus"></i> </button> <button id="delete" class="btn btn-clr delete delete-btn" type="button" value="delete"> <i class="fa fa-minus"></i> </button></td></tr>`
    if(parseInt(val) <7){
        $(this).closest('table').append(html)
        var get_element=$('#tax_table_id tr:last').find('.taxtypecls')
        var option='<option value="">--Select--</option>'
        $(newArray).each(function (key,val) {
            option += '<option value="'+val.id+'">'+val.name+'</option>'
        })
        console.log('option',option)
        get_element.append(option);
        
    }  
    else{
        
    }
    ids ++;

})


$(document).on('click','#delete',function(){
    // var table_len=$('#tax_table_id tbody tr').length
    // if (table_len > 1){
    //     $(this).closest('tr').remove()
    // }
    var_name=$(this).closest('tr').find('.taxtypecls').val()
    var_name1=parseInt(var_name)
    if( var_name1<=7){
        $(this).closest('tr').nextAll('tr').remove()
        $(this).closest('tr').remove()
    }
    if(var_name==''){
        $(this).closest('tr').remove()
    }

})

$(document).ready(function(){

    $('#addtaxformid').validate(); 
    $("[name=taxtype]").rules("add", {
        required: true,
        });  
         
    })
    $("[name=taxname]").each(function(){
        $(this).rules("add", {
            required: true,
        });
    })



    $(document).on('keyup','.taxnamecls',function(){
        //$(".taxnamecls").focusout(function(){
        var csrf_token = $('.csrf_token').val()
        let process_id=$('#process_id').attr('data-id')
        var val=$(this).val().toLowerCase()
        $(this).closest('td').find('span').remove();
        var currentelement=$(this)
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken":csrf_token},
            url: "/invoiceguard/validateprocess/",
            data: {'process_name':$.trim(val),'process_id':process_id
        },
            success: function(data){
                if (data.status == true){ 
                    // currentelement.attr('data-error',0); 
                    currentelement.closest('div').find('span').remove();
                    currentelement.after('<span class="waring-err">Process Already Exists</span>')
                }
                else{
                        currentelement.closest('div').find('span').remove();
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
                            currentelement.closest('div').find('span').remove();
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
        var count_process=0
        var tax_type2=$('.taxtypecls')
        console.log('taxtype_2',tax_type2)
        tax_type2.each(function(){
            value_counter=$(this).val()
            if(value_counter==''){
                $(this).addClass('con_error')
                count_process++
            }
        })
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
        if (count == 0 && count_process==0){
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