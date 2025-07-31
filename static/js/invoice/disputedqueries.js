jQuery.noConflict();

    $(document).on('change','.percentage_val',function(){
        if(parseFloat($(this).val()) > 100){
           swal.fire('Max Percentage Reached')
           $(this).val('')
        }
        else{
            $('#submit_id').attr('disabled',false)
            $('.settlement_val').val($(this).val())
        } 
      })


$(document).ready(function () {
    $('#summernote').summernote({
        toolbar: false,
    });

    $(document).on('click','.querydenied',function(){
        if ($('#summernote').summernote('isEmpty')) {
            // Add a CSS class to indicate error
            $('#summernote').addClass('error-border');
            // Show error message
            $('.note-frame').next().append('<span>Please enter the message</span>');
            return false;
        } else {
            // Remove the CSS class if validation passes
            $('#summernote').removeClass('error-border');   
            $('.note-frame').next().find('span').remove();
            let get_file= $('.files_upload').find('option:selected').val();
            if(get_file !='') {
                $('.qry-chos').each(function(){
                    if($(this)[0].files.length == 0){
                        $(this).addClass('con_error');
                    } else {
                        $(this).removeClass('con_error');
                    }
                });
                if($('.con_error').length !=0){
                    return false;
                } else {
                    return true;
                }
            } else {
                return true;
            }
        }
    });
});



    $('#queryform').submit(function() {
        // Disable the submit button to prevent multiple submissions
        $('.querydenied').prop('disabled', true);
        $('.submit_cls').prop('disabled','disabled')
      });
    $('#summernote').on('summernote.change', function() {
        console.log('summernote change');
        // Check if the editor content is empty
        if ($('#summernote').summernote('isEmpty')) {
          // Add a CSS class to the editor element to show the red outline
          $('#summernote').addClass('error');
        } else {
          // Remove the CSS class to hide the red outline
          $('#summernote').removeClass('warning');
        }
      });


      $(document).ready(function(){
        $('.utctolocal').each(function(){
            var utc_time = $(this).text();
            var local_time = moment.utc(utc_time).toDate();
            // var local_time_format = moment(local_time).local().format('DD-MM-YYYY hh:mm A');
            var local_time_format = moment(local_time).local().format('DD-MM-YYYY');
            $(this).text(local_time_format);
        });
    });
    

    
$(document).on('change','.files_upload',function(){
  let files='<div><div><input type="file" name="file" class="qry-chos attachfile"><button class="btn btn-clr add_file"><i class="fa fa-plus"></i></button></div></div>'
  $('.document_type').val($(this).val())
  $('.document_name').val($(this).find('option:selected').text())
  if($(this).val() != ''){
      $(this).closest('div').find('.upload_file_data').html(files)
  }
  else{
      $(this).closest('div').find('.upload_file_data').html('')
  }
  
})

let submit_val='';

$(document).on('click','.status_cls',function(e){
  e.preventDefault();
  submit_val=$(this).val();
  addition_content=`<div><h4>Settlement</h4></div>`
  if(submit_val == '10'){
      addition_content+=`<table class="w-100"><tr><td>Settlement Percentage %</td><td><input type='text' oninput="$(this).val(($(this).val().replace(/[^0-9]/g,'')))" class='percentage_val form-control' name='percentage_val'></td></tr></table>`
      $('.excp_content').html('')
      $('.get_reason').html(addition_content)
  }
  else if(submit_val == '8'){
      let html = '<div class="mt-2"><b>Reasons :</b></div>';
      $('.main_comments').html('')
      let data=exceptional_func(submit_val)
      data.forEach(element => {
          html +='<div><label for ="'+element.value+'"><input type="checkbox" name="exceptional" value="'+element.value+'" id="'+element.value+'"> '+element.name+'</label></div>'
      })
      console.log({'html':html})
      $('.excp_content').html(html)
      
  }
  else{
      $('.get_reason').html('<textarea name="main_comments" class="form-control"></textarea><div class="excp_content"></div>')
      $('.excp_content').html('')
  }
  $('#submit_id').attr('type','submit')

})

$(document).on('click','#submit_id',function(e){
  get_type=$(this).attr('type')
  let submit_name="";
  let check_err=0
  if (get_type == "submit"){
      if(submit_val == '10'){
          $('.percentage_val').each(function(){
              if($.trim($(this).val())==''){
                  $(this).addClass('con_error')
                  check_err++
              }
          })
          
          e.preventDefault();
          if(check_err == 0){
          submit_val=6
          $('.status_cls').val('6')
          $(document).trigger('.status_cls');
          $('.get_reason').html('<textarea name="main_comments"  id="main_comments" class="form-control"></textarea>')
          }
          else{
              return false
          }
      }
      else{
      if (submit_val == "5"){
          submit_name = "Disputed"
      }
      else if(submit_val == "6"){
          submit_name  = "Settlement"
      }
      else if(submit_val == "8"){
          submit_name  = "Dispute Committee"
      }
      else if(submit_val == "A1"){
          submit_name  = "Vendor Accepted"
      }
      else if(submit_val == "A2"){
          submit_name  = "Vendor Declined"
      }
      $(this).attr('disabled',true)
      let getformid=$(this).parents("form").attr("id")
      let form=$("#"+getformid);
      $('.status_cls').attr('disabled','disabled');
      $("<input>").attr({name: "submit_type",id: "hiddenId",type: "hidden",value: submit_val}).appendTo("form");
      $("<input>").attr({name: "submit_name",id: "nameId",type: "hidden",value: submit_name}).appendTo("form");
      // //use for generate payment
      if ($('.confirm_action').length  > 0){
          $('.confirm_action').val('confirm')
      }
      if(check_err == 0){
      form.submit();
      }
      else{
          return false
      }
  }
  }
})

function exceptional_func(type){
  let data="";
  let return_data=[{'name':'Changes in Supporting Documents','value':'1'},{'name':'Work Completion Certificate or Timesheet mismatch with Invoice billing details.','value':'2'},{'name':'Material Delivery Ticket or Certificate Mismatch with Invoice Billing details','value':'3'},,{'name':'Mismatch between price quoted on invoice and selected contract','value':'4'},{'name':'Asking for Credit Note','value':'5'},{'name':'Other Reasons','value':'6'}]

  let reject_data=[{'name':'Supporting Documents Missing','value':'7'},{'name':'Wrong Supporting Documents','value':'8'},{'name':'Irrelevant Invoice','value':'9'},,{'name':'Relevant Contract not selected for invoice','value':'10'},{'name':'Work Done previously Invoiced','value':'11'},{'name':'Other Reasons','value':'12'}]

  let dispute_data=[{'name':'Invoice details interpretation issues','value':'13'},{'name':'Supporting document issues','value':'14'},{'name':'Issues due to Verbal communication for work invoiced','value':'15'},,{'name':'Work done outside of approval limits','value':'16'},{'name':'Dispute on contract execution','value':'17'},{'name':'Dispute coming out of Audit findings','value':'18'},{'name':'Inability to clarify through normal methods','value':'19'},{'name':'Other Reasons','value':'20'}]
  if (type == "3"){
      data = return_data
  }
  else if (type == "4"){
      data = reject_data      
  }
  else if (type == "8"){
      data = dispute_data
  }
  return data
}

$(document).on('click','.empty_user',function(e){
  e.preventDefault();
  swal.fire('No designated dispute users')
})

$(document).on('click','.add_file',function(e){
  e.preventDefault();
  $(this).closest('div').parent().append('<div><input type="file" name="file" class="qry-chos attachfile filesize"><span class="maxmp">(Max: 25MB)</span><br><span class="file-error-message"></span><button class="btn btn-clr add_file"><i class="fa fa-plus"></i></button> <button class="btn btn-clr del_file"><i class="fa fa-minus"></i></button></div>')
})

$(document).on('click','.del_file',function(e){
  e.preventDefault();
  $(this).closest('div').remove()
})

$(document).on('change','.qry-chos',function(){
  $(this).removeClass()
})

let vendor
$(document).on('click','.vendor_acceptance',function(){

    Swal.fire({
            text: 'Do you want to Accept Query?',
            showDenyButton: true,
            confirmButtonColor: '#77d61f',
            allowOutsideClick:false,
            denyButtonColor:'#AF2B50',
            confirmButtonText: 'Yes',
            denyButtonText: 'No',
            customClass: {
                actions: 'my-actions',
                confirmButton: 'order-2',
                denyButton: 'order-3',
            }
            }).then((result) => {
            if (result.isConfirmed) {
                vendor=1
                $("<input>").attr({name: "vendor_comfirmation",id: "vendor_comfirmation",type: "hidden",value: vendor}).appendTo("form");
                $('form').submit();
                $(this).attr('disabled','disabled')
            }
            else{
                vendor=2
                $("<input>").attr({name: "vendor_comfirmation",id: "vendor_comfirmation",type: "hidden",value: vendor}).appendTo("form");
                $('form').submit();
                $(this).attr('disabled','disabled')
            }
    })
});


$(document).ready(function() {
    $(document).on('click','.showtoggle',function() {
    let nxttr = $(this).closest('div').closest('div').next('div');
    $('.collapse').not(nxttr.find('.collapse')).removeClass('show');
    });
});


$(document).ready(function () {
    $('#submit_id').click(function () {
        var comments = $('#main_comments').val().trim();
        if (comments === '') {
            // Add a CSS class to indicate error
            $('#main_comments').addClass('error-border');
            return false; // Prevent form submission
        } else {
            // Remove the CSS class if validation passes
            $('#main_comments').removeClass('error-border');
        }
    });
});
