
$(window).keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });

function save_func(){
    var count=0
    var workvalue=$('.workvalcls').val()
    /*if ($('#id_checklist tbody tr').eq(1).find('.checkfile').is(':checked')){
        if (workvalue == ""){
            $('.workvalcls').addClass('add-error-cls')
            count ++;
        }
        else if(workvalue != totalinvoicevalue){
            $('.workvalcls').addClass('add-error-cls')
            count ++;
        }
    }*/
    $('.inv-main-file').each(function(){
        var val=$(this).val()
        if (val == ""){
            $(this).addClass('add-error-cls')
            count ++;
        }
        else{
            $(this).removeClass('add-error-cls')
        }
    })

    let supportingfile=$('.supportingfile').length;
    if (supportingfile == 0){
        $(".filecls").each(function(){
            var val=$(this).val()
            if (val == ''){
                $(this).addClass('con_error')
                count ++;
            }
            else{
                $(this).removeClass('add-error-cls')
            }
        })
    }
    return count;
}

$(document).on('click','#id_file_save',function(e){
    e.preventDefault()
    var sum = 0;
    $('.workval').each(function(){
        var value = $(this).val().replace(/,/g , '');
        // add only if the value is number
        if(!isNaN(value) && value.length != 0) {
            sum += parseInt(value);
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
     }}*/
    $('.workvalcls').removeClass('add-error-cls')
    var error_value=save_func()
    if (error_value == 0){
        $("<input>").attr({name: "submit_type",id: "hiddenId",type: "hidden",value: 1}).appendTo("form");
        $('#invfileadd')[0].submit()
    }
    // alert(count)
})

$(document).on('change','.inv-main-file',function(){
    var count=0
    var workvalue=$('.workvalcls').val()
    // alert(workvalue)
    var wccfile=$(this).closest('tr').next('tr').find('.checkfile').is(':checked')
    $('.inv-main-file').each(function(){
        var val=$(this).val()
        if (val == ""){
            $(this).addClass('add-error-cls')
            count ++;
        }
        else{
            $(this).removeClass('add-error-cls')
        }
    })
    if (wccfile == true){
        if (workvalue == ""){
            $('.workvalcls').addClass('add-error-cls')
            count ++;
        }
    }

    console.log(count)
    if (count == 0){
        $("<input>").attr({name: "submit_type",id: "hiddenId",type: "hidden",value: 0}).appendTo("form");
    
    }
})


$(document).on('click','.checkfile',function(){
    var val=$(this).val()
    var wcc_id=$(this).attr('wcc_id') || ''
    if ( wcc_id == ''){
        if ($(this).is(':checked')){
            if (val == "2"){
                $('.wcc-cls').removeAttr('style')
            }
            else{

            }
        
            var html ='<table class="che-table"><tbody><tr><td><input type="file" accept="image, .png, .jpeg, .pdf, .jpg" name="file'+val+'" class="form-control filecls inp-voice3 filesize"><span class="maxmp">(Max: 25MB)</span><br><span class="file-error-message"></span></td> <td class="in-btn-wid che-smline"><button id="add_file" class="btn btn-clr add-btn" type="button" dataid="'+val+'" value="add"><i class="fa fa-add"></i></button> <button id="remove_file" class="btn btn-clr add-btn" type="button" dataid="'+val+'" value="minus"><i class="fa fa-minus"></i></button></td> </tr></tbody></table>'
            $(this).closest('tr').find('.addfilecls').html(html)
        }
        else{
            console.log('a',$('.wrk-main').is(':checked'))
            if ($('.wrk-main').is(':checked')){
            }
            else{
                $('.wcc-cls').css('display','none')
            }
            $('.workvalcls').val('')
            $(this).closest('tr').find('.addfilecls').html('')
        }
    }
    else{
        $(this).prop('checked',true)
    }
})

$(document).on('click','#add_file',function(){
    var html=$(this).closest('tr').clone()
    $(this).closest('table').append(html)
    
    $(this).closest('table').find('tr:last td:eq(0) .workval').val('')
    $(this).closest('table').find('tr:last td:eq(0) .filecls').val(null)
})

$(document).on('click','#remove_file',function(){
    var table_len=$(this).closest('table').find('tr').length;
    console.log(table_len)
    if (table_len >1){
        $(this).closest('tr').remove()
    }

})

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}


$(document).on('click','.work',function(){
    // jquery each function to get all the values of the input fields
    var sum = 0;
    $('.workval').each(function(){
        var value = $(this).val().replace(/,/g , '');
        // add only if the value is number
        if(!isNaN(value) && value.length != 0) {
            sum += parseInt(value);
        }
    });
    console.log(Number(sum),Number(totalinvoicevalue.replace(/,/g , '')))
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
    $('.inv-main-file').each(function(){
            var val=$(this).val()
            if (val == ""){
                //$(this).addClass('add-error-cls')
                count ++;
            }
            else{
                //$(this).removeClass('add-error-cls')
            }
        })
    // alert(count)
    if (count > 0){
        // swal.fire('Invoice File Missing or Wcc Value Missing')
        // $('.dis-cls').attr('disabled',true) 
    }
    else{
        // $('.dis-cls').removeAttr('disabled')
        
    }
  /*  if ($('.wrk-main').is(':checked')){
    if (Number(sum) != Number(totalinvoicevalue.replace(/,/g , ''))){
        swal.fire('WCC Value should match with total value of invoice Submitted')
        //$(this).addClass('add-error-cls')
        //$(this).val('')
        return false
        // $('.dis-cls').attr('disabled',true) 
    }
    else{
        //$(this).removeClass('add-error-cls')
        // $('.dis-cls').removeAttr('disabled')
    }}*/
})


$(document).on('click','#final_Save_id',function(e){
    e.preventDefault()
   var sum = 0;
   $('.workval').each(function(){
       var value = $(this).val().replace(/,/g , '');
       // add only if the value is number
       if(!isNaN(value) && value.length != 0) {
           sum += parseInt(value);
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
    }}*/
    var error_value=save_func()
    //alert(error_value)
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


//$(document).on('click','#draftsub',function(e){
//    e.preventDefault()
//    var error_value=save_func()
//    //alert(error_value)
//    if (error_value == 0){
//        return true
//    }
//     e.preventDefault()
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
//                 // window.location.href = '../invoicelist';
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
// })

$(document).on('change','.work_cls',function(){
        // $(this).next('span').remove();
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