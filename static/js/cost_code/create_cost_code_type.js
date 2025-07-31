let cost_id = $('#cost_code_id').val();
// var startlen = $('.comp_code_cls').val().length
// $(document).on('click','.add-cls',function(){
//     let find_empty=0
//     trindex = $(this).closest('tr').next('tr').index()
//     $('.comp_code_cls').each(function(){
//         let current_value=$.trim($(this).val())
//         if(current_value == ''){
//             find_empty+++
//             $(this).addClass('con_error')
//         }
//     })
//     if(find_empty == 0){
//     if (trindex != -1){
//         let tr_clone=$(this).closest('tr').clone();
//         tr_clone.find('.comp_code_cls').val('');
//         tr_clone.find('.comp_cls').val('');
//         $(this).closest('tr').after(tr_clone)
//         let check_el=$(this).closest('tr').find('.minus-cls').length;
//         let get_sequence=$(this).closest('tr').find('.comp_code_cls').attr('data_id');
//         let get_max_length = $(this).closest('tr').find('.comp_code_cls').attr('maxlength');
//         if (check_el == 0){
//             tr_clone.find('td:last').append('<button id="delete" data_id="'+get_sequence+'" class="btn btn-clr minus-cls waves-effect waves-float waves-light" type="button" max_data="'+get_max_length+'"><i class="fa fa-minus"></i></button>');
//         }
//     }
//     else{
//     let get_sequence=$(this).closest('tr').find('.comp_code_cls').attr('data_id');
//     let get_max_length = $(this).closest('tr').find('.comp_code_cls').attr('maxlength');

//     // let get_val=$('#id_create_cost_tbl >tbody > tr:last').find('.comp_code_cls').val();
//     let get_val = getMaxVal();
//     let tr_clone=$(this).closest('tr').clone();
//     tr_clone.find('.comp_cls').val('');
//     let add_val=parseInt(get_sequence)+1+parseInt(get_val);
//     let convert_val=pad(add_val.toString(),get_max_length)
//     if(range == 0){
//         tr_clone.find('.comp_code_cls').val(convert_val);
//     }
//     else{
//          tr_clone.find('.comp_code_cls').val('');
//     }
//    let check_el=$(this).closest('tr').find('.minus-cls').length;
//     if (check_el == 0){
//         tr_clone.find('td:last').append('<button id="delete" data_id="'+get_sequence+'" class="btn btn-clr minus-cls waves-effect waves-float waves-light" type="button" max_data="'+get_max_length+'"><i class="fa fa-minus"></i></button>');
//     }
//     let new_val=$(this).closest('tr').find('.comp_code_cls').val()
//     if (new_val == ''){
//         tr_clone.find('.comp_code_cls').val('')
//     }
//     $(this).closest('tbody').append(tr_clone);
//     var final_val=$('#id_create_cost_type >tbody> tr:last > td ').find('.comp_code_cls').val()
//     if(final_val.length != get_max_length){
//         $('#id_create_cost_type >tbody> tr:last > td ').find('.comp_code_cls').val('')
//     }
// }
//     }
// })

$(document).on('click','.add-cls',function(){
    let tr_clone=$(this).closest('tr').clone();
    tr_clone.find('.comp_cls').val('');
    $(this).closest('tr').after(tr_clone)

})

function getMaxVal(){
    var maxVal = 0;
    $("#id_create_cost_type >tbody > tr").each(function(index,tr) {
    var cellValue = parseFloat($(tr).find(".comp_code_cls").val());
    if (!isNaN(cellValue) && cellValue > maxVal) {
        maxVal = cellValue;
    }
    });
    return maxVal
}

$(document).on('click','.minus-cls',function(){
    let get_val=parseInt($(this).attr('data_id'))+1;
    let bef_tr=parseFloat($(this).closest('tr').prev('tr').find('.comp_code_cls').val())
    let after_tr=parseFloat($(this).closest('tr').next('tr').find('.comp_code_cls').val())
    let current_val=parseFloat($(this).closest('tr').find('.comp_code_cls').val())
    console.log({'bef_tr':bef_tr,'after_tr':after_tr,'current_val':current_val})
    let check_bef=current_val -get_val
    let check_after=current_val +get_val
    console.log({'check_bef':check_bef,'bef_tr':bef_tr})
    if(bef_tr == check_bef && check_after ==after_tr){
    let max_data=parseInt($(this).attr('max_data'));
    let data= $(this).closest('tr')
    let data_row= $(this).closest('tr').find('.add-error-cls')
    console.log('data_row',data_row)
    let count_value=0
    $('.add-error-cls').not(data_row).each(function(){
        count_value++
    })
    if (count_value == 0){
        $('.final-cls').attr('disabled',false) 
    }
    data.nextAll('tr').each(function(index, tr) {
        let tr_val=parseInt($(tr).find('.comp_code_cls').val())
        let cal_val = tr_val-get_val
        let convert_val=pad(cal_val.toString(),max_data)
        console.log({'cal_val':cal_val,'tr_val':tr_val,'convert_val':convert_val,'get_val':get_val,'max_data':max_data})
        // if (convert_val != 'NaN'){
            $(tr).find('.comp_code_cls').val(convert_val)
        // }
        
    });
}
    $(this).closest('tr').remove();
})

function pad (str, max) {
    str = str.toString();
    return str.length < max ? pad("0" + str, max) : str;
  }

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
    let check = $(".common_cls").hasClass("add-error-cls")
    console.log('check',check)
    if (check == false){
        $('#loader').removeClass('hidden')
        $('#cost_type_form')[0].submit();
        
    }
    $('.final-cls').attr('disabled','disabled') 
})

$(document).on('keyup','.add-error-cls',function(){
    $(this).removeClass('add-error-cls')
})


$(document).on('keyup','.comp_cls',function(){
    if(!$(this).val()){
        $(this).css("border", "1px solid red");
    }else{
        $(this).css("border", "");
    }
})

$(document).on('keyup','.common_cls',function(){
    $(this).removeClass('con_error')
    $(this).next('.invoicenumspn').html("")
    var submitclass =  $('.final-cls')
    var spanremove = $(this).closest('tr')
    console.log("submitclass",submitclass)
    $(this).closest('tr').find('.span_cls').remove();
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val()
    let duplicate_count = 0;
    let get_val = $(this).val()
    let get_name=$(this).attr('name')
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
   
    $.ajax({
        type: "POST",
        url: '/cost_code/checkcostcodetype',
        data: { 'cost_code_type': get_val,'field':get_name,'csrfmiddlewaretoken':csrftoken ,'cost_id':cost_id,'costypeid':costypeid},
        success: function (data) {
            console.log(data.status)
            if (data.status == false){
                console.log('1')
                that.addClass('add-error-cls')
                // that.next('.invoicenumspn').html("<p class='ptag'>Data  already exist</p>")
                // $('<span class="span_cls">Data already exist</span>').insertAfter(spanremove)
                submitclass.attr('disabled','disabled')
            }
            else{
                console.log('2')
                // that.removeClass('add-error-cls')
                that.next('.invoicenumspn').html("")
                submitclass.attr('disabled',false)
            }
        }
    })
})
 
$('#cost_type_form').submit(function(e) {
    e.preventDefault(); 
    let validation=false
    let componentname=[]
    let allcostcode=[]

    $('#id_create_cost_type').find('tr').each((rowindex, row) => {
        $(row).find('.comp_cls').each((index, component) => {
            // console.log($(component).val())
            if(!$(component).val()){            
                validation=true
                $(component).css("border", "1px solid red");
            }else{
                componentname.push($(component).val())
                $(component).css("border", "");
      
            }
        })
        $(row).find('.comp_code_cls').each((index, costcode) => {
            // console.log($(component).val())
            if(!$(costcode).val()){            
                validation=true
                $(costcode).css("border", "1px solid red");
            }else{
                allcostcode.push($(costcode).val())
                $(costcode).css("border", "");
      
            }
        })
    })

    checkduplicate_componentname=checkduplicatevalue(componentname)
    checkduplicate_allcostcode=checkduplicatevalue(allcostcode)
    let err_len=$('.add-error-cls').length
    console.log(checkduplicate_componentname)
    console.log(checkduplicate_allcostcode) 
    if(checkduplicate_componentname == false && validation==false && checkduplicate_allcostcode == false && err_len==0){
        this.submit();
    }else{
        return false
    }
})

function checkduplicatevalue(array) {
    var valueSet = new Set();
    for (var i = 0; i < array.length; i++) {
      var value = array[i];
      if (valueSet.has(value)) {
        return true; 
      }
      valueSet.add(value);
    }
    return false; 
}

// $(document).on('blur','.comp_code_cls',function(){
   
//    if (($(this).val().length) < startlen){
   
//       $(this).addClass('add-error-cls')
//       $('.final-cls').attr('disabled','disabled')
//     }
//     else{
       
//         $('.final-cls').attr('disabled',false) 
//     }
//     if($(this).val().length != total_digit ){
//         $(this).addClass('add-error-cls')
//     }
//     console.log('total_digit',total_digit)
// })

$(document).on('change','.comp_code_cls',function(){
    console.log('val',$(this).val())
    console.log('no',startwith.length)
    if(parseInt($(this).val()) < parseInt(startwith)  ){
        console.log('small')
        $(this).addClass('add-error-cls')
        $('.final-cls').attr('disabled','disabled')
        $(this).closest('tr').find('#add').attr('disabled','disabled')
        // console.log('path',$(this).closest('tr').find('#add'))
    }
    else{
       $('.final-cls').attr('disabled',false)
       $(this).closest('tr').find('#add').attr('disabled',false) 
    }
    if($(this).val().length <(startwith.length)){
        $(this).addClass('add-error-cls')
        $('.final-cls').attr('disabled','disabled')
        $(this).closest('tr').find('#add').attr('disabled','disabled')
    }
    else{
        $('.final-cls').attr('disabled',false)
        $(this).closest('tr').find('#add').attr('disabled',false) 
     }
})
   
console.log('class',$('.comp_cls').val())  
$(document).on('click','.final-cls',function(){
   if($('.comp_cls').val() == ''){
       $(this).attr('disabled','disabled')
       $('.comp_cls').addClass('add-error-cls')
    }
})

$(document).on('keyup','.comp_cls',function(){
    var $th = $(this);
    $th.val($th.val().replace(/(\s{2,})/g, ' '));
    $th.val($th.val().replace(/^\s*/, ''));
    console.log($th.val().length)
});

$(document).on('change','.comp_cls',function(){
    var value=$(this).val()
    var new_val=$.trim(value)
    $(this).val(new_val)
    $(this).next('.invoicenumspn').html("")
    var submitclass =  $('.final-cls')
    var spanremove = $(this).closest('tr')
    console.log("submitclass",submitclass)
    $(this).closest('tr').find('.span_cls').remove();
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val()
    let duplicate_count = 0;
    let get_val = $(this).val()
    let get_name=$(this).attr('name')
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
})




$(document).on('keyup','.comp_cls',function(){
    const prev_val=$(this).closest('td').find('.hidden_type').val()
    count_num=0
    $('.comp_cls').not($(this)).each(function(){
        if(prev_val == $(this).val()){
            count_num++
        }
    })
    
    if(count_num == 1 ){
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

$(document).on('change','.rangecls',function(){
    currentval = $(this).val()
    curentcomponent = $(this)
    savebtn = $('.final-cls')

    $.ajax({
    type:"POST",
    headers: { "X-CSRFToken": csrftoken},
    url:'/cost_code/validatecostcoderange/',
    data:{'pk':id},
            success: function(data){
               if(parseInt(data.fromrange) > parseInt(currentval)){
                    Swal.fire("Current Value Must Be Greater Than ",data.fromrange)
                    curentcomponent.val(' ')
                    savebtn.attr('disabled',true)
               }
               if(data.torange != 0){
               if(parseInt(data.torange) < parseInt(currentval)){
                Swal.fire("Current Value Must Be Less Than ",data.torange)
                curentcomponent.val(' ')
                savebtn.attr('disabled',true)
           }
        }
         }
   })
})