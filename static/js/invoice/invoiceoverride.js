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
    // if (check_value){
        // let get_list=list;
        // let myArray='';
        // $('.user_cls').each(function (index,val){
        //     let selected_value=$(val).find(':selected').val()
        //     console.log('selected_value',selected_value)
        //     myArray = get_list.filter(function( obj ) {
        //         return obj.val !== selected_value;
        //     });
        //     get_list = myArray
        // })
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
})

$('#save_id').click(function(e){
    e.preventDefault()
    get_count=check_error()
    if (get_count == 0)[
        $('#assign_user_id')[0].submit()
    ]
})

function check_error(){
    let count=0;
    $('.user_cls').each(function(index,value){
        current_value=$(value).find(':selected').val() || '';
        if (current_value == ''){
            $(value).addClass('con_error');
            count += 1;
        }
    })
    return count
}
