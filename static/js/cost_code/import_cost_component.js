let cost_id = $('#cost_code_id').val();

$(document).ready(function(){
    $('.check_type').each(function(){
        if($(this).children().length == 0){
           $(this).text('-')
        }
    })


    $('#costcodetype_list').DataTable({
        serverSide: true,
        ajax: {
            url: "/cost_code/getcomponent",                    
            type: 'GET',
            data: function (d) {
                d.costcode_master_id = costcode_master_id;
            }
        },
    
        columns: [
            { data: 's_no' },
            { data: 'name' },
        ],
        language: {
            emptyTable: "---"
        }
      });


})
// $(document).ready(function(){
//     alert(csrf_token)
//     console.log({'csrf_token':csrf_token})
// })
var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val()
$('#id_create_cost_tbl >tbody > tr').not(':first').each(function(index,tr){
    let prev_val = parseInt($(tr).prev('tr').find('.comp_code_cls').val());
    let get_seq = parseInt($(tr).find('.comp_code_cls').attr('data_id')); 
    let get_len =parseInt($(tr).find('.comp_code_cls').attr('maxlength'));
    let add_vals= prev_val + get_seq +1;
    console.log({'prev_val':prev_val,'get_seq':get_seq,'get_len':get_len,'add_vals':add_vals})
    if (add_vals.toString().length <= get_len){
        let con_val = pad(add_vals,get_len)
        $(tr).find('.comp_code_cls').val(isNaN(con_val) ? "" : con_val);
        $(tr).find('.hidden_component_val').val(isNaN(con_val) ? "" : con_val);
    }
})

function pad(str, max) {
    str = str.toString();
    return str.length < max ? pad("0" + str, max) : str;
  }

  $(document).on('click','.minus-cls',function(){
    let this_row=$(this)
    let get_val=parseInt($(this).attr('data_id'))+1;
    let max_data=parseInt($(this).attr('max_data'));
    let data= $(this).closest('tr')
    $(this).closest('tr').find('.comp_cls').next('.span_cls').remove();
    let duplicate_count = 0;
    let new_val =$(this).closest('tr').find('.comp_cls').val()
    let get_same_row=$(this).closest('tr')
    let last_tr
    let get_name=$(this).closest('tr').find('.comp_cls').attr('name')
    $('input[name='+get_name+']').not(get_same_row.find('input[name='+get_name+']')).each(function(index,data){
        console.log($(this))
        let val= $(data).val();
        if (val != ''){
            if (val == new_val){
                last_tr=$(data)
                duplicate_count ++;
            }
        }
    })
    if(duplicate_count == 1){
        last_tr.removeClass('add-error-cls')
    }
    $(this).closest('tr').remove()
    data.nextAll('tr').not('.check_count').each(function(index, tr) {
        let tr_val=parseInt($(tr).find('.comp_code_cls').val())
        let cal_val = tr_val - get_val
        let convert_val=pad(cal_val.toString(),max_data)
        if(convert_val != 'NaN'){
        $(tr).find('.comp_code_cls').val(convert_val)
        }
        else{
            $(tr).find('.comp_code_cls').val('')
        }
     
    });
    let i=1;
    $('#id_create_cost_tbl >tbody > tr').each(function(index,tr){
        $(tr).find('td:first').text(i);
        i ++;
    })
})




$('.submit_cls').click(function(e){
    e.preventDefault()
    let count= 0;
    $('input[type="text"]').each(function(index,data){
        let val= $(data).val()
        if (val == ''){
            $(data).addClass('add-error-cls')
            count ++;
        }
    });
    $('.comp_code_cls').each(function(){
        let max_length=$(this).closest('tr').find('.comp_code_cls').attr('maxlength')
        if (max_length != $(this).val().length){
            $(this).addClass('add-error-cls')
            count ++;
        }
    })
    let check = $(".common_cls").hasClass("add-error-cls")
    if (check == false){
        $('#loader').removeClass('hidden')
        $('#cost_type_form')[0].submit();
        $(this).attr('disabled',true)

    }
})

$(document).on('keyup','.add-error-cls',function(){
    $(this).removeClass('add-error-cls')
})

$(document).ready(function(){
    $('.comp_cls').each(function(){
        const get_val = $(this).val()
        const cost_id=$('#id_create_cost_tbl').attr('data-id')
        const that=$(this);
        $.ajax({
            type: "POST",
            url: '/cost_code/checkcostcomponent',
            data: { 'cost_code_type': get_val,'csrfmiddlewaretoken':csrftoken ,'cost_id':cost_id},
            success: function (data) {
                if (data.data != 0){
                    that.addClass('add-error-cls')
                    if (! that.closest('td').find('.span_cls').hasClass('span_cls')){
                        $('<span class="span_cls">Data Already Exist</span>').insertAfter(that)
                    } 
                }
                // else{
                //     // that.removeClass('add-error-cls')
                //     // that.next('.span_cls').remove();
                // }
            }
        })
    })

    $('.comp_code_cls').each(function(){
        const get_val = $(this).val()
        const get_name=$(this).attr('name')
        const cost_id=$('#id_create_cost_tbl').attr('data-id')
        const that=$(this);
        $.ajax({
            type: "POST",
            url: '/cost_code/checkcostcodenumber',
            data: { 'cost_code_type': get_val,'field':get_name,'csrfmiddlewaretoken':csrftoken ,'cost_id':cost_id},
            success: function (data) {
                if (data.data != 0){
                    that.addClass('add-error-cls')
                    if (! that.closest('td').find('.span_cls').hasClass('span_cls')){
                        $('<span class="span_cls">Data Already Exist</span>').insertAfter(that)
                    } 
                }
                // else{
                //     // that.removeClass('add-error-cls')
                //     // that.next('.span_cls').remove();
                // }
            }
        })
    })
})

$(document).ready(function(){
    $('.common_cls').each(function(){
        $(this).next('.span_cls').remove();
    let duplicate_count = 0;
    let get_val = $(this).val()
    let get_name=$(this).attr('name')
    let cost_id=$('#id_create_cost_tbl').attr('data-id')
    var that=$(this);
    $('input[name='+get_name+']').each(function(index,data){
        let val= $(data).val();
        if (val != ''){
            if (val == get_val){
                duplicate_count ++;
            }
        }
    })
    if (duplicate_count > 1){
        $(this).addClass('add-error-cls')
    }
    else{
        $(this).removeClass('add-error-cls')
    }
    })
})

$(document).on('keyup','.comp_cls',function(){
    $(this).next('.span_cls').remove();
    let duplicate_count = 0;
    let get_val = $(this).val()
    let get_name=$(this).attr('name')
    let cost_id=$('#id_create_cost_tbl').attr('data-id')
    var that=$(this);
    $('input[name='+get_name+']').each(function(index,data){
        let val= $(data).val();
        if (val != ''){
            if (val == get_val){
                duplicate_count ++;
            }
        }
    })
    // if (duplicate_count > 1){
    //     $(this).addClass('add-error-cls')
    //     $('<span class="span_cls">Data Already Exist</span>').insertAfter(that)
    // }
    // if (duplicate_count == 0){
    //     $(this).removeClass('add-error-cls')
    //     that.removeClass('span_cls')
    // }
    $.ajax({
        type: "POST",
        url: '/cost_code/checkcostcomponent',
        data: { 'cost_code_type': get_val,'field':get_name,'csrfmiddlewaretoken':csrftoken ,'cost_id':cost_id},
        success: function (data) {
            if (data.data != 0 || duplicate_count > 1){
                that.addClass('add-error-cls')
                if (! that.closest('td').find('.span_cls').hasClass('span_cls')){
                    $('<span class="span_cls">Data Already Exist</span>').insertAfter(that)
                } 
            }
            else{
                that.removeClass('add-error-cls')
                that.next('.span_cls').remove();
            }
        }
    })

})





$(document).on('keyup','.comp_code_cls',function(){
    $(this).next('.span_cls').remove();
    let duplicate_count = 0;
    let get_val = $(this).val()
    let get_name=$(this).attr('name')
    let cost_id=$('#id_create_cost_tbl').attr('data-id')
    var that=$(this);
    $('input[name='+get_name+']').each(function(index,data){
        let val= $(data).val();
        if (val != ''){
            if (val == get_val){
                duplicate_count ++;
            }
        }
    })
    // if (duplicate_count > 1){
    //     $(this).addClass('add-error-cls')
    //     $('<span class="span_cls">Data Already Exist</span>').insertAfter(that)
    // }
    // if (duplicate_count == 0){
    //     $(this).removeClass('add-error-cls')
    //     that.removeClass('span_cls')
    // }
    $.ajax({
        type: "POST",
        url: '/cost_code/checkcostcodenumber',
        data: { 'cost_code_type': get_val,'field':get_name,'csrfmiddlewaretoken':csrftoken ,'cost_id':cost_id},
        success: function (data) {
            if (data.data != 0 || duplicate_count > 1){
                that.addClass('add-error-cls')
                if (! that.closest('td').find('.span_cls').hasClass('span_cls')){
                    $('<span class="span_cls">Data Already Exist</span>').insertAfter(that)
                }      
            }
            else{
                that.removeClass('add-error-cls')
                that.next('.span_cls').remove();
            }
        }
    })

})

$(document).on('click','.delete',function(){
    var get_id=$(this).attr('data_id')
    Swal.fire({
        title: 'Are you sure you want to delete ',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, I Confirm',
        cancelButtonText: 'No',
      }).then((result) => {
        if (result.isConfirmed) {
           $.ajax({
            type: "POST",
            url: '/cost_code/checkcostcodetype',
            data: {'csrfmiddlewaretoken':csrftoken ,'cost_id':get_id},
          success: function(data)
          {
            console.log(data)
            setTimeout(function(){  
            location.reload();  
            },1000);
          }
           });
          Swal.fire(vendor_name,'Deleted Successfully')
        }
    })
})

$(document).on('submit','#import_costcode_component',function(e) {
    e.preventDefault(); 
    var file = $('#import_file').prop('files')[0];
    if(file){
        this.submit()
    }else{
        $('#file-error').text("Please Choose File")
    }

})
$(document).on('change','#import_file',function(){
    var file = $(this).prop('files')[0];
    if(file){
        $('#file-error').text("")

    }
});

$(document).ready(function(){

})


 
// $('input').on('change', function () {

//     const queryString = window.location.search;
//     const parameters = new URLSearchParams(queryString);
//     const value = parameters.get('q');
//     if (value != null && $(this).val() == '') {
//         window.location.href = `scheme://gethost/cost_code/costcodetypelist/`
//     }
// });
$('input').on('change',function() {
    const queryString = window.location.search;
    const parameters = new URLSearchParams(queryString);
    const value = parameters.get('q');
      if(value!=null && $(this).val() == '') {
          window.location.href = `{{scheme}}://{{gethost}}/cost_code/costcodetypelist/`
      }
  });

$(document).on('input', "#myInput", function () {
    let query = $(this).val()
    let pageperdata = $('#datafilters').val()
    // alert(pageperdata)
    setTimeout(function () {
        searchComponent(query,1,pageperdata)
    }, 100);
});


$(document).on('click','.pg-circle',function(e){
    e.preventDefault();
    let query = $('#myInput').val();
    let page = $(this).attr('data-id')
    let pageperdata = $('#datafilters').val()
    searchComponent(query,page,pageperdata)
    // window.location.reload();
})

$(document).on('change','#datafilters',function(e){
    let query = $('#myInput').val();
    //let page = $(this).attr('data-id')
    let pageperdata = $(this).val()
    searchComponent(query,1,pageperdata)
});

function searchComponent(query,page,pageperdata) {
    pk = $('.listid').val()
    console.log(query,page,pageperdata)
    $.ajax({
        url: "/cost_code/costcodetypelist/" + pk,
        headers: { 'X-CSRFToken': csrf_token },
        data: {
            'q': query,
            'page':page,
            'pageperdata':pageperdata
        },
        type: 'POST',
        success: function (response) {
            console.log(1)
            if (response.status) {
                console.log('right')
                console.log(response)
                $('section').replaceWith(response.html)
                $('.check_type').each(function(){
                    if($(this).children().length == 0){
                       $(this).text('-')
                    }
                })
                let focusElement = $(document).find('#myInput')
                let elementLength = focusElement.val().length;
                focusElement[0].focus();
                focusElement[0].setSelectionRange(elementLength,elementLength);
                $('#datafilters').val($('.entries').val())
            } else {
                console.log('wrong')
            }
        },
        error: function () {
            console.log(2)
            // Error message
        }
    });
}

$(document).on('keyup','.comp_cls',function(){
    const prev_val=$(this).closest('td').find('.hidden_type').val()
    count=0
    $('.comp_cls').not($(this)).each(function(){
        if(prev_val == $(this).val()){
            count++
        }
    })
    
    if(count == 1 ){
        $('.comp_cls').not($(this)).each(function(){
            if(prev_val == $(this).val()){
                $(this).removeClass('add-error-cls')
            }
        })
    }
})

$(document).on('change','.comp_cls',function(){
    $(this).closest('td').find('.hidden_type').val($(this).val())
})

$(document).on('click','#add-row',function(){
   
    clone_row=`<tr class='check_count'><td class="s_no"></td><td> <input type="hidden" name="hidden_type" class="hidden_type"><input type="text" name="component_name" class="form-control comp_cls common_cls" autocomplete="off"></td><td><input type="text" name="component_cost_code" class="form-control comp_code_cls common_cls" oninput="this.value = this.value.replace(/[^0-9]/g, '')" maxlength=${max_digit}></td><td class="text-center"><button id="add-row" class="btn btn-clr add-cls waves-effect waves-float waves-light" type="button" max_data=${max_digit}><i class="fa fa-plus"></i></button><button id="delete-row" class="btn btn-clr  waves-effect waves-float waves-light new_minus" type="button" data_id=${sequence_gap} max_data=${max_digit}><i class="fa fa-minus"></i></button></td></tr>`
    $tr_row=$(this).closest('tr')
    $tr_row.after(clone_row)
    console.log('clone_row',clone_row)
})

$(document).on('change','.comp_cls',function(){
    var current_val=$(this).val()
    var trimmedStr = current_val.trim();
    $(this).val(trimmedStr)
    let duplicate_count = 0;
    let get_val = $(this).val()
    let get_name=$(this).attr('name')
    let cost_id=$('#id_create_cost_tbl').attr('data-id')
    var that=$(this);
    $('input[name='+get_name+']').each(function(index,data){
        let val= $(data).val();
        if (val != ''){
            if (val == get_val){
                duplicate_count ++;
            }
        }
    })
    // if (duplicate_count > 1){
    //     $(this).addClass('add-error-cls')
    //     $('<span class="span_cls">Data Already Exist</span>').insertAfter(that)
    // }
    // if (duplicate_count == 0){
    //     $(this).removeClass('add-error-cls')
    //     that.removeClass('span_cls')
    // }
    $.ajax({
        type: "POST",
        url: '/cost_code/checkcostcomponent',
        data: { 'cost_code_type': get_val,'field':get_name,'csrfmiddlewaretoken':csrftoken ,'cost_id':cost_id},
        success: function (data) {
            if (data.data != 0 || duplicate_count > 1){
                that.addClass('add-error-cls')
                if (! that.closest('td').find('.span_cls').hasClass('span_cls')){
                    $('<span class="span_cls">Data Already Exist</span>').insertAfter(that)
                } 
            }
            else{
                that.removeClass('add-error-cls')
                that.next('.span_cls').remove();
            }
        }
    })
})


$(document).on('click','#add-row,#delete-row',function(){
    var s_no=1
    $('#id_create_cost_tbl tbody tr').each(function(){
      $(this).closest('tr').find('.s_no').text(s_no)
      s_no++
    })
})

$(document).on('change','.comp_code_cls',function(){
    $(this).closest('td').find('.hidden_component_val').val($(this).val())
    if($(this).val().length < startwith.length ){
        $(this).addClass('add-error-cls')
        $('.final-cls').attr('disabled','disabled')
        $(this).closest('tr').find('#add').attr('disabled','disabled')
    }
    else{
        $('.final-cls').attr('disabled',false)
        $(this).closest('tr').find('#add').attr('disabled',false) 
     }
})

$(document).on('keyup','.comp_code_cls',function(){
    const prev_val=$(this).closest('td').find('.hidden_component_val').val()
    count_num=0
    $('.comp_code_cls').not($(this)).each(function(){
        if(prev_val == $(this).val()){
            count_num++
        }
    })
    console.log('count_num',count_num)
    if(count_num == 1 ){
        $('.comp_code_cls').not($(this)).each(function(){
            if(prev_val == $(this).val()){
                $(this).removeClass('add-error-cls')
                $(this).next('.span_cls').remove();
            }
        })
    }
})

$(document).on('keyup','.comp_cls',function(){
    const prev_val=$(this).closest('td').find('.hidden_type').val()
    count=0
    $('.comp_cls').not($(this)).each(function(){
        if(prev_val == $(this).val()){
            count++
        }
    })
    
    if(count == 1 ){
        $('.comp_cls').not($(this)).each(function(){
            if(prev_val == $(this).val()){
                $(this).removeClass('add-error-cls')
                $(this).next('.span_cls').remove();
            }
        })
    }
})

$(document).on('click','.new_minus',function(){
   $(this).closest('tr').remove()
})

