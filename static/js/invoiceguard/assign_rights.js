
$(".chk-all-box").change(function() {
    // Get the "checked" state of the "select all" checkbox
    let isChecked = $(this).prop("checked");
        // Find all checkboxes in the same table row as the "select all" checkbox and set their "checked" property to match
    $(this).hasClass('selec_invrec_app') == true ? $(this).closest("tr").find("input[type='checkbox']").not('.pro_app_cls').prop("checked", isChecked) : $(this).closest("tr").find("input[type='checkbox']").prop("checked", isChecked);
});
$(document).ready(function(){
    $('.usercls >tbody > tr').each(function() {
    let full_len= $(this).find(".chk-all-box").hasClass('selec_invrec_app') == true ? $(this).find('.sub-cls').not('.pro_app_cls').length :$(this).find('.sub-cls').length;
    console.log('full_len',full_len)
    let get_checked_data=$(this).find(".chk-all-box").hasClass('selec_invrec_app') == true ? $(this).find('.sub-cls:checked').not('.pro_app_cls').length : $(this).find('.sub-cls:checked').length;
    console.log('get_checked_data',get_checked_data)
    if (full_len==get_checked_data){
        $(this).find(".chk-all-box").hasClass('selec_invrec_app') == true ? $(this).find('.selec_invrec_app').prop('checked',true) :$(this).find('.selec_field').prop('checked',true)
    }
    else{
        $(this).find(".chk-all-box").hasClass('selec_invrec_app') == true ? $(this).find('.selec_invrec_app').prop('checked',false) :$(this).find('.selec_field').prop('checked',false)
    }
    });
});

$(".sub-cls").click(function(){
    a=$(this).closest('tr').find('.selec_field').attr('id')
    full_len=$(this).closest('tr').find('.sub-cls').length;
    var check_true=0;
    $(this).closest('tr').find('.sub-cls').each(function() {
    if($(this).prop('checked')) {
        check_true+=1;
    }
    });
    if (full_len==check_true){
        $(`#${a}`).prop('checked',true)
    }
    else{
        $(`#${a}`).prop('checked',false)
    }
})

$(document).on('click','.pro_app_cls',function(){
    $(this).closest('tr').find(".pro_app_cls").prop('checked',false);
    $(this).prop('checked',true);
})

$(document).on('change','.sub-cls',function(){
    $('.usercls >tbody > tr').each(function() {
        let full_len= $(this).find(".chk-all-box").hasClass('selec_invrec_app') == true ? $(this).find('.sub-cls').not('.pro_app_cls').length :$(this).find('.sub-cls').length;
        console.log('full_len',full_len)
        let get_checked_data=$(this).find(".chk-all-box").hasClass('selec_invrec_app') == true ? $(this).find('.sub-cls:checked').not('.pro_app_cls').length : $(this).find('.sub-cls:checked').length;
        console.log('get_checked_data',get_checked_data)
        if (full_len==get_checked_data){
            $(this).find(".chk-all-box").hasClass('selec_invrec_app') == true ? $(this).find('.selec_invrec_app').prop('checked',true) :$(this).find('.selec_field').prop('checked',true)
        }
        else{
            $(this).find(".chk-all-box").hasClass('selec_invrec_app') == true ? $(this).find('.selec_invrec_app').prop('checked',false) :$(this).find('.selec_field').prop('checked',false)
        }
        });
})

// var allChecked = true;
// $(".sub-cls").click(function() {
//     $('.sub-cls').each(function() {
//     if(!$(this).prop('checked')) {
//         allChecked = false;
//         return false; // exit the loop early
//     }
//     });
//     console.log(allChecked)
//     if(allChecked) {
        
//         $('.selec_field').prop('checked',true)
//     } 
//     else {
//         $('.selec_field').prop('checked',false)
//     }
// })
// $('.sub-cls').each(function() {
//     if(!$(this).prop('checked')) {
//         allChecked = false;
//         return false; // exit the loop early
//     }
//     });
// if(allChecked) {
//     $('.selec_field').prop('checked',true)
// } else {
//     $('.selec_field').prop('checked',false)
// }
//   $(".sub-cls").change(function() {
//     if ($(this).prop('checked',false)){
//         $('.selec_field').prop('checked',false)
//     }

//     var check_all=$('.sub-cls').prop('checked');
//     console.log({'check_all':check_all})
//     $('.selec_field').prop('checked',check_all)
    
//   })


// $("input[type='checkbox']").change(function(){
//     if ($(this).attr('checked',false)){
//         a=$(".chk-all-box").attr('checked',false)
//         console.log(a)
//     }
    //  var valcheck=$(this).removeProp('checked');
    //  a=$(this).closest('tr').find(".chk-all-box").prop('checked',valcheck)
    //  alert(a)
// })




/*
$(document).on('click','.common-cls',function(){
    if ($(this).is(':checked')){
        $(this).closest('td').next('td').find('.common-cls').prop('checked',true)
    }
    else{
        if (!$(this).closest('td').next('td').next('td').find('.edit-main-cls').is(':checked')){
            $(this).closest('td').next('td').find('.common-cls').prop('checked',false)
        }

    }
})
projet view-cls*/
/*
$(document).on('click','.prev-view-cls',function(){
        if ($(this).closest('td').prev('td').find('.common-cls').is(':checked') || $(this).closest('td').next('td').find('.edit-main-cls').is(':checked')){
            $(this).prop('checked',true)
        }
})

$(document).on('click','.edit-main-cls',function(){
    if ($(this).is(':checked')){
        $(this).closest('td').prev('td').find('.common-cls').prop('checked',true)
    }
    else{
        if (!$(this).closest('td').prev('td').prev('td').find('.common-cls').is(':checked')){
        $(this).closest('td').prev('td').find('.common-cls').prop('checked',false)
        }
    } 
})


$('#usergen_id tbody tr').each(function () {

   var count=0 
   $(this).children('td:not(:nth-child(2))').each(function(){
        //console.log($(this).find('input:checkbox').val())
        if ($(this).find('input:checkbox').prop('checked')==false){
             
            count+=1

        }
    })
    console.log(count)
    if (count == 0){
        $(this).children('td:eq(0)').find('input:checkbox').prop('checked',true)
    }
});

$('table tbody tr').each(function(i) { 
    // Only check rows that contain a checkbox
    var $chkbox = $(this).find('input[type="checkbox"]');

})

$('input[name=check_all]').each(function () {
    dataid=$(this).attr('dataid')

    if ($(this).closest('tr').find('td:last-child input:checkbox').is(':checked',false) && $(this).closest('tr').find('td:nth-child(n) input:checkbox').is(':checked',false)){
       // console.log($(this).val())
        //$(this).prop('checked',true)
    }
    else{
        console.log('noi')
        $(this).prop('checked',true)
    });
*/
/*
$(document).on('click','input[name=check_all]',function(){

    dataid=$(this).attr('class');
     console.log(dataid)
    if ($(this).is(':checked')){
        
        $('.'+dataid+'').prop('checked',this.checked);
    }
    else{
        $('.'+dataid+'').prop('checked',false);
    }
})

$(document).on('click','.sub-cls',function(){
if ($('#styled-checkbox-pp-01').is(':checked',false) && $('#styled-checkbox-pp-02').is(':checked',false) && $('#styled-checkbox-pp-03').is(':checked',false) && $('#styled-checkbox-pp-04').is(':checked',false) && $('#styled-checkbox-pp-05').is(':checked',false) && $('#styled-checkbox-pp-06').is(':checked',false)){
    // alert('edfr')
    $(this).prop('checked',true)
}
else{
    $('#styled-checkbox-pp').prop('checked',false)
}
})


$(document).on('click','.sub-cls1',function(){
if($('#styled-checkbox-2').is(':checked',false) && $('#styled-checkbox-02').is(':checked',false) && $('#styled-checkbox-3').is(':checked',false) && $('#styled-checkbox-4').is(':checked',false)){
    $(this).prop('checked',true)
}
else{
    $('#styled-checkbox').prop('checked',false)
}
})



$(document).on('click','.sub-cls2',function(){
if($('#styled-checkbox-vm-01').is(':checked',false) && $('#styled-checkbox-vm-02').is(':checked',false) && $('#styled-checkbox-vm-03').is(':checked',false) && $('#styled-checkbox-vm-04').is(':checked',false)){
    $(this).prop('checked',true)
}
else{
    $('#styled-checkbox-vm').prop('checked',false)
}
})

$(document).on('click','.sub-cls3',function(){
if($('#styled-checkbox-cm-01').is(':checked',false) && $('#styled-checkbox-cm-02').is(':checked',false) && $('#styled-checkbox-cm-03').is(':checked',false) && $('#styled-checkbox-cm-04').is(':checked',false)){
    $(this).prop('checked',true)
}
else{
    $('#styled-checkbox-cm').prop('checked',false)
}
})

$(document).on('click','.sub-cls4',function(){
if($('#styled-checkbox-tm-01').is(':checked',false) && $('#styled-checkbox-tm-02').is(':checked',false) && $('#styled-checkbox-tm-03').is(':checked',false) && $('#styled-checkbox-tm-04').is(':checked',false)){
    $(this).prop('checked',true)
}
else{
    $('#styled-checkbox-tm').prop('checked',false)
}
})
*/
