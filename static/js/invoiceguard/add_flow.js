
var get_list= [];
$(document).ready(function(){
   $(".main_cls option").each(function(key,value) {
    get_list.push({'id':$(this).val(),'name':$(this).text()}); 
    });
})


var ids=1
var new_list=[]
$(document).on('click','#add',function(){
    var html =`<tr> <td class="wid-tx"><select class="form-control form-select newcls taxtypecls" name="process" ></select></td> <td class="same-line-tx"><button id="add" class="btn btn-clr add-btn pha-sebtn" type="button" value="Add"> <i class="fa fa-plus"></i> </button> <button id="delete" class="btn btn-clr delete-btn" type="button" value="delete"> <i class="fa fa-minus"></i> </button></td></tr>`
    
    $(this).closest('table').append(html)
    ids ++;
    var val=$('#tax_table_id tr:last').prev().find('.taxtypecls :selected').val();
    var val2=$('#tax_table_id tr:last').prevAll().find('.taxtypecls :selected').val();
    new_list.push(val)
    var newArray = get_list.filter(function(item) {
    return !new_list.includes(item.id);
    });

    
        console.log({"new array":newArray})
        if(parseInt(val)){
            var get_element=$('#tax_table_id tr:last').find('.taxtypecls')
            console.log({'get element':get_element})
            var option='<option value="">--Select--</option>'
            $(newArray).each(function (key,val) {
                option += '<option value="'+val.id+'">'+val.name+'</option>'
            })
            console.log('option',option)
            get_element.append(option);
        }
        
})



$(document).on('click','#delete',function(){
    var table_len=$('#tax_table_id tbody tr').length
    if (table_len > 1){
        $(this).closest('tr').remove()
    }
    var val=$('#tax_table_id tr:last').prev().find('.taxtypecls :selected').val();
    new_list.pop(val)

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


new_list2 = [];

$(document).on('change', '.taxtypecls', function() {
    a=$(this).closest('tr').find('.taxtypecls').val()
    $(this).closest('tr').find('.del_button').attr("disabled", true);
    var val=$('#tax_table_id tr:last').find('.taxtypecls :selected').val();    
    var new_val=$(this).closest('tr').nextAll('tr').find('.taxtypecls')
    console.log({'new val':new_val})
    new_val.each(function(){
        new_list.pop($(this).val())
    })
    console.log({'new val':new_val})
    $(this).closest('tr').nextAll('tr').remove();
});


    $(document).on('keyup','.taxnamecls',function(){
        //$(".taxnamecls").focusout(function(){
        var val=$(this).val().toLowerCase()
        $(this).closest('td').find('span').remove();
        var currentelement=$(this)
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": csrf_token},
            url: "/invoiceguard/validatflow",
            data: {'flow_name':$.trim(val)},
            success: function(data){
                if (data.status == true){ 
                    // currentelement.attr('data-error',0); 
                    currentelement.closest('div').find('span').remove();
                    currentelement.after('<span class="waring-err">Flow name Already Exists</span>')
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
                            currentelement.after('<span class="waring-err">Flow name Already Exists</span>')
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
        var tax_type2=$('.taxtypecls')
        console.log('taxtype',tax_type2)
    
        var count_flow=0
        tax_type2.each(function(){
            value_counter=$(this).val()
            if (value_counter==''){
                $(this).addClass('con_error')
                count_flow++
            }
        })
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
            if (span_len.length > 0){
                count ++;
            }
            
        });
        if (count == 0 && count_flow==0){
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



