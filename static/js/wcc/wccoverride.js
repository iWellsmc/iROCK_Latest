var option_dict={}
var list=[]
$("#users_id option").each(function(){
    var this_option_value=$(this).val();
    var this_text=$(this).text()
    option_dict={"name":this_text,"val":this_option_value}

    list.push(option_dict)
});

$(document).on('click','#add-row',function(){
    let check_value=$(this).closest('tr').find('.user_cls').find(':selected').val() || '';
        let html='<tr><td>';
        html +='<select name="users" class="user_cls form-control"><option value="">--Select--</option>'
        $(list).each(function(ind,value){
            html +='<option value="'+value.val+'">'+value.name+'</option>'
        })
        html +='</select>'
        html +='<td><button id="add-row" class="btn-clr add-row btn add-btn waves-effect waves-float waves-light" type="button" value="add"><i class="fa fa-plus"></i></button><button id="delete-row" class="btn-clr delete-row btn add-btn waves-effect waves-float waves-light" type="button" value="delete"><i class="fa fa-minus"></i></button></td></tr>';
        if (check_value){
            $('#user_table tbody').append(html);
        }
    // }
})

$(document).on('click','#delete-row',function(){
    let tbl_len=$('#user_table tbody tr').length
    if (tbl_len > 1){
        $(this).closest('tr').remove();
    }
    overall_error_check()
})

$('#save_id').click(function(e){
    e.preventDefault()
    overall_error_check()
    get_count=$('.con_error').length
    console.log(get_count)
    if (get_count == 0)[
        $('#assign_user_id')[0].submit()
    ]
})



$(document).on('change','.user_cls',function(){
    overall_error_check()
})

// function check_empty_error(){
//     $('.user_cls').each(function(index,value){
//         current_value=$(value).find(':selected').val() || '';
//         if (current_value == ''){
//             $(value).addClass('con_error');
//         }
//     })
// }

function overall_error_check(){
    $('.user_cls').each(function(index,value){
        let count=0;
        current_value=$(value).find(':selected').val() || '';
        if (current_value){
            $(value).removeClass('con_error');
            $('.user_cls').each(function(index1,value1){
                inner_current_value=$(value1).find(':selected').val() || '';
                if (current_value == inner_current_value){
                    count += 1;
                }
            })
            
        }
        else{
            $(value).addClass('con_error');
        }
        if (current_value){
            if (count > 1){
                $(value).addClass('con_error');
            }
            else{
                $(value).removeClass('con_error');
            }
        }
    })
}