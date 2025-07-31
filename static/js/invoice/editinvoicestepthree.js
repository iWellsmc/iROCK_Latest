
jQuery.noConflict();
$(window).keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });
 

function save_func(){
    $('.workvalcls').removeClass('add-error-cls')
    var count=0
    var workvalue=$('.workvalcls').val()
    if ($('#id_checklist tbody tr').eq(1).find('.checkfile').is(':checked')){
        if ($('.supportingfile').val() == ""){
            $('.workvalcls').addClass('add-error-cls')
            count ++;
        }
        else{
            $('.workvalcls').removeClass('add-error-cls')
        }
        //else if(workvalue != totalinvoicevalue){
        //    $('.workvalcls').addClass('add-error-cls')
        //    count ++;
        //}
    }
    $('.invoicefile').each(function(){
        if ($(this).val() == ""){
            $(this).addClass('add-error-cls')
            count ++;
        }
        else{
            $(this).removeClass('add-error-cls')
        }
    })
    $('.inv-main-file').each(function(){
        console.log("hah");
        var val=$(this).val()
        if (val == ""){
            var value=$(this).closest('div').next('div').find('input[type=hidden]').val()
            if (value == ''){
                $(this).addClass('add-error-cls')
                count ++;
            }

        }
        else{
            $(this).removeClass('add-error-cls')
        }
    })

    return count
}

$(document).on('click','#draftsub',function(e){
    $("<input>").attr({name: "submit_type",id: "hiddenId",type: "hidden",value: 0}).appendTo("form");
})


$(document).on('click','#id_file_save',function(e){
    e.preventDefault()
    $('.workvalcls').removeClass('add-error-cls')
    var sum = 0;
    $('.workvalcls').each(function(){
        var value = $(this).val().replace(/,/g , '');
        // add only if the value is number
        if(!isNaN(value) && value.length != 0) {
            sum += parseFloat(value);
        }
    });
    /*if ($('.wrk-main').is(':checked')){
    if (Number(sum) != Number(totalinvoicevalue.replace(/,/g , ''))){
        swal.fire('WCC Value should match with total value of invoice Submitted')
        //$(this).addClass('add-error-cls')
        //$(this).val('')
        return false
        // $('.dis-cls').attr('disabled',true) 
    }
    else{
        //return true
        //$(this).removeClass('add-error-cls')
        // $('.dis-cls').removeAttr('disabled')
    }
}*/
    var error_value=save_func()
    if (error_value == 0){
        $("<input>").attr({name: "submit_type",id: "hiddenId",type: "hidden",value: 1}).appendTo("form");
        $('#invfileadd')[0].submit()
    }
    // alert(count)
})

$(document).on('click','#final_Save_id',function(e){
    e.preventDefault()
    var error_value=save_func()
    var sum = 0;
   $('.workvalcls').each(function(){
       var value = $(this).val().replace(/,/g , '');
       // add only if the value is number
       if(!isNaN(value) && value.length != 0) {
           sum += parseInt(value);
       }
   });
   console.log(sum,23456)
   /*if ($('.wrk-main').is(':checked')){
    if (Number(sum) != Number(totalinvoicevalue.replace(/,/g , ''))){
        swal.fire('WCC Value should match with total value of invoice Submitted')
        //$(this).addClass('add-error-cls')
        //$(this).val('')
        return false
        // $('.dis-cls').attr('disabled',true) 
    }
    else{
        //return true
        //$(this).removeClass('add-error-cls')
        // $('.dis-cls').removeAttr('disabled')
    }}*/
    // alert(error_value)
    if (error_value == 0){
        Swal.fire({
                text: 'Do You Want to Submit Invoice?',
                showDenyButton: true,
                // showCancelButton: true,
                // textColor:'#77d61f',
                confirmButtonColor: '#77d61f',
                denyButtonColor:'#AF2B50',
                confirmButtonText: 'Yes',
                denyButtonText: 'No',
                customClass: {
                actions: 'my-actions',
                //   cancelButton: 'order-1 right-gap',
                confirmButton: 'order-2',
                denyButton: 'order-3',
                }
            }).then((result) => {
                if (result.isConfirmed) {
                    $("<input>").attr({name: "submit_type",id: "hiddenId",type: "hidden",value: 3}).appendTo("form");
                    $('#invfileadd')[0].submit()
                    // window.location.href = '../invoicelist';
                    return true;
                }
        })
    }
})


  $(document).on('change','.inv-main-file',function(){
    var count=0

    var workvalue=$('.workvalcls').val()
    // alert(workvalue)
    var wccfile=$(this).closest('tr').next('tr').find('.checkfile').is(':checked')
    // $('.inv-main-file').each(function(){
    //     var val=$(this).val()
    //     if (val == ""){
    //         $(this).addClass('add-error-cls')
    //         count ++;
    //     }
    //     else{
    //         $(this).removeClass('add-error-cls')
    //     }
    // })
    if (wccfile == true){
        if (workvalue == ""){
            $('.workvalcls').addClass('add-error-cls')
            count ++;
        }
    }

    console.log(count,'count')
    if (count > 0){
        $('.dis-cls').attr('disabled',false) 
    }
    // else{
    //     // $('.dis-cls').removeAttr('disabled')
        
        
    // }
})



$(document).on('click','.checkfile',function(){
    var val=$(this).val()
    var wcc_id=$(this).attr('wcc_id') || ''
    if ( wcc_id == ''){
        if ($(this).is(':checked')){
            if (val == "2"){
                var html='<table class="work_comp_table"><tbody> <tr><td><input type="hidden" name="workcompletionid" value="" class="work_hdid"><input type="text" name="workcomplete" class="workvalcls work_cls" value=""></td> <td class="che-smline"><button id="add_file" class="btn btn-clr add-btn workcomp" type="button" value="add"><i class="fa fa-add"></i></button> <button id="remove_file" class="btn btn-clr add-btn" type="button"  value="minus"><i class="fa fa-minus"></i></button></td> </tr></tbody></table>'
                $('.icon_cls').after(html)
                
            }
            var html ='<table class="che-table"><tbody><tr><td><input type="file" accept="image/png, image/jpeg, application/pdf" name="file'+val+'" class="form-control filecls inp-voice3 filesize"><span class="maxmp">(Max: 25MB)</span><br><span class="file-error-message"></span></td><td class="in-btn-wid che-smline"><button id="add_file" class="btn btn-clr add-btn" type="button" dataid="'+val+'" value="add"><i class="fa fa-add"></i></button> <button id="remove_file" class="btn btn-clr add-btn" type="button" dataid="'+val+'" value="minus"><i class="fa fa-minus"></i></button></td></tr></tbody></table>';
            $(this).closest('tr').find('.addfilecls').html(html)
        }
        else{
            $(this).prop('checked',false)
            if ($('.wrk-main').is(':checked')){
            }
            else{
                $(".work_comp_table").remove()
            }
            $(this).closest('tr').find('.inv-file-cls').html('')
            $(this).closest('tr').find('.addfilecls').html('')
        }
    }
    else{
        $(this).prop('checked',true)
    }
})

$(document).on('change', '.filecls', function() {
    console.log("File input changed");
    var fileSize = this.files[0].size; // Size in bytes
    console.log("File size:", fileSize);
    var maxSize = 25 * 1024 * 1024; // 25MB in bytes
    console.log("Max size:", maxSize);
    var errorMessageElement = $(this).closest('tr').find('.file-error-message');
    
    if (fileSize > maxSize) {
        errorMessageElement.text('*File size exceeds 25MB limit. Please choose a smaller file.');
        errorMessageElement.css('color', 'red');
        $(this).val(''); // Clear the file input
    } else {
        errorMessageElement.text('');
    }
});


$(document).on('click','#add_file',function(){
    var html = $(this).closest('tr');
    console.log('html', html)
    var empty_file = html.clone();
    empty_file.find(':file').val('');
    empty_file.find('.file-error-message').text(''); // Clear error message
    html.after(empty_file);
    //$(this).closest('table').append(html)
    $('.work_comp_table').find('tr:last td:eq(0) .work_hdid').val('')
    $('.work_comp_table').find('tr:last td:eq(0) .workvalcls').val('')
    $('.work_comp_table').find('tr:last td:eq(0) .workvalcls').removeAttr('readonly')
    $('.work_comp_table').find('tr:last td:eq(0) .filecls').val('')
})

$(document).on('click','#remove_file',function(){
    var table_len=$(this).closest('table').find('tr').length;
    console.log(table_len)
    if (table_len >1){
        $(this).closest('tr').remove()
    }

})

// $(document).on('change','.workvalcls',function(){
//     var val=$(this).val()
//     var removecomma=totalinvoicevalue.replace(/,/g , '')
//     if (removecomma !=val){
//         swal.fire('Value Mismatch')
//         $(this).addClass('add-error-cls')
//     }
//     else{
//         $(this).removeClass('add-error-cls')
//     }
// })
function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
/*$(document).on('click','#draftsub',function(e){
    e.preventDefault()
    var error_value=save_func()
    alert(error_value)
    if (error_value == 0){
        return true
    }
})*/

$(document).on('click','.work',function(e){
    // jquery each function to get all the values of the input fields
    var sum = 0;
    $('.workvalcls').each(function(){
        var value = $(this).val().replace(/,/g , '');
        // add only if the value is number
        if(!isNaN(value) && value.length != 0) {
            sum += parseFloat(value);
        }
    });
    var val=$(this).val()
    var count=0 
    var remove_comma_current_val=val.replace(/,/g , '')
    var add_comma=numberWithCommas(remove_comma_current_val)
    $(this).val(add_comma)
    // alert(add_comma)
    // var removecomma=totalinvoicevalue.replace(/,/g , '')
    if (val == ""){
        count ++;
    }
    //$('.inv-main-file').each(function(){
    //        var val=$(this).val()
    //        if (val == ""){
    //            $(this).addClass('add-error-cls')
    //            count ++;
    //        }
    //        else{
    //            $(this).removeClass('add-error-cls')
    //        }
    //    })
    // alert(count)
    if (count > 0){
        // swal.fire('Invoice File Missing or Wcc Value Missing')
        // $('.dis-cls').attr('disabled',true) 
    }
    else{
        // $('.dis-cls').removeAttr('disabled')
        
    }
    console.log(sum,123456)
/*    if ($('.wrk-main').is(':checked')){
    if (Number(sum) != Number(totalinvoicevalue.replace(/,/g , ''))){
        swal.fire('WCC Value should match with total value of invoice Submitted')
        //$(this).addClass('add-error-cls')
        //$(this).val('')
        return false
        // $('.dis-cls').attr('disabled',true) 
    }
    else{
        return true
        //$(this).removeClass('add-error-cls')
        // $('.dis-cls').removeAttr('disabled')
    }}*/
})

$(document).on('change','.invfil',function(){
    if ($(this).val() != ""){
        $(this).closest('div').next('div').remove()
    }
})

$(document).on('click','.remove-file',function(){
    $(this).closest('div').remove()
})



//     e.preventDefault()
//     var count=0
//     var checkwork=$('.workvalcls').closest('tr').find('.checkfile').is(":checked")
//     if (checkwork == true){
//         if ($('.workvalcls').val() != totalinvoicevalue){
//             count ++;
//         }
//     }
//     if (count == 0 ){
//     Swal.fire({
//             text: 'Are you sure you wish to submit?',
//             showDenyButton: true,
//             // showCancelButton: true,
//             // textColor:'#77d61f',
//             confirmButtonColor: '#77d61f',
//             denyButtonColor:'#AF2B50',
//             confirmButtonText: 'Yes',
//             denyButtonText: 'No',
//             customClass: {
//               actions: 'my-actions',
//             //   cancelButton: 'order-1 right-gap',
//               confirmButton: 'order-2',
//               denyButton: 'order-3',
//             }
//           }).then((result) => {
//             if (result.isConfirmed) {
//                 $("<input>").attr({name: "submit_type",id: "hiddenId",type: "hidden",value: 0}).appendTo("form");
//                 $('#invfileadd')[0].submit()
//                 return true;
//             //   var current_url=$(location).attr("href")
//             //   var replace_url=current_url.replace("createmaster/",'createblock/'+project_id+'')
//             //   window.location.href = replace_url;
//                 // $(".step-1").hide();
//                 // $(".step-2").show();
//             //   Swal.fire('Saved!', '', 'success')
//             } else if (result.isDenied) {
                
//             //   var current_url=$(location).attr("href")
//             //   var replace_url=current_url.replace("createmaster/","listmaster/")
//             //   window.location.href = replace_url;
//               // Swal.fire('Changes are not saved', '', 'info')
//             }
//           })
//         }
// })

    // $(document).on('click','.final-cls',function(){
    //     var filecount=$('.color-fil').children().length
    $(document).on('change','.work_cls',function(){
        $(this).next('span').remove();
        var val=$(this).val()
        // if (val!='No Max Limit')
        // {
        $(this).val(val.replace(/([-€~!@#$%^&*()_+=`{}\[\]\|\\:;'<>A-Za-z])+/g, ''));
        // }
       
        // var number=$(this).val()
        // if ( number !=''){
        //     if (number==0){
        //         $(this).after('<span class="waring-err">Value cannot be Zero</span>')
        //     }
        //     else{
        //         $(this).next('span').remove();
        //     }
        // }
        // else{
        //     $(this).next('span').remove();
        // }
        $(".work_cls").each(function() {
            var num = $(this).val();
            var removecomma=num.replace(/,/g, '');
            var commaNum = numberWithCommas(decimal_value(removecomma));
            $(this).val(commaNum);
        });
        if($(this).val().indexOf('.')!=-1){         
            if($(this).val().split(".")[1].length > 2){                
                if( isNaN( parseFloat( this.value ) ) ) return;
                this.value = parseFloat(this.value).toFixed(2);
            }  
         }            
         return this; //for chaining
    });

    function decimal_value(val){
    if (val != ''){
        var con_val=val.toString()
        var remove_commas= con_val.replace(/,/g, "");
        console.log(remove_commas)
        if (remove_commas == Math.floor(remove_commas)){
            return remove_commas
        }
        else{
            return parseFloat(remove_commas).toFixed(2)
        }
    }
    else{
        return val
    }


}

function numberWithCommas(number) {

var parts = number.toString().split(".");

parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
console.log(parts)
return parts.join(".");
}

$(document).ready(function() {
    var submissionCount = 0;
    var maxSubmissions = 1; // Change this to the desired number of submissions
  
    $("form").submit(function(event) {
        submissionCount++;
        if (submissionCount >= maxSubmissions) {
            $(".generate_report_3").prop('disabled', true);
        }
    });
  });
