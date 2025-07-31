
function cleanFileName(fileName) {
    // Check if fileName is undefined or null
    if (fileName === undefined || fileName === null) {
        return '';  // or handle the case accordingly
    }
    // Perform the replace operations
    return fileName.replace(/[^.-\w\s()]/g, '').replace(/ /g, '_');
}

function newcleanFileName(fileName) {
    // Check if fileName is undefined or null
    if (fileName === undefined || fileName === null) {
        return '';  // or handle the case accordingly
    }
    // Perform the replace operations
    return fileName.replace(/[^.-\w\s]+/gi, '').replace(/\s+/g, '_');
}


$(document).on('click','.inv_file',function(){
    $('.inv_file').removeClass('inv-high-cls')
    var inv_name=$(this).closest('tr').find('.inv_name').text()
    $('.hd-inv').text(inv_name)
    var url=$(this).attr('value')
    $(this).addClass('inv-high-cls')
    var setfullurl = url.slice((cleanFileName(url).lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ?
    `${package_src}?file=${currentdomain}/media/invoicedocuments/${cleanFileName(url).replace(/ /g, "_")}` :
    `${currentdomain}/media/invoicedocuments/${cleanFileName(url).replace(/ /g, "_")}`;
    $('.doc_invhidcls').attr({'src':setfullurl,height:'590px !important'})
})

$(document).on('click','.inv_file1',function(){
    $('.inv_file1').removeClass('inv-high-cls')
    var inv_name=$(this).closest('tr').find('.inv_name').text()
    $('.hd-inv').text(inv_name)
    var url=$(this).attr('value')
    $(this).addClass('inv-high-cls')
})

$(document).on('click','.commonbtn',function(){
    $('.commonbtn').removeClass('support_high-cls')
    $('.doc_selinvhidcls').attr('src','')
    var val=$(this).attr('dataid')
    $(this).addClass('support_high-cls')
    var gettext=$(this).text()
    // alert(val)
    $.ajax({
            type:"GET",
            data:{'supportid':val,'invoiceid':invoiceid,'wcc_id':wcc_id},
            url:'/invoice/getsupportfiles',
            success: function(data){
                console.log({'getsupportfiles':data})
                var html="" 
                if (val == "9"){
                    if(data.contracttype != 'original'){
                        console.log('original')
                        if (data.con_file.length > 1){
                            console.log('length > 1')
                            $(data.con_file).each(function(index,value){
                                if (value.amendment_addendum_id != null){
                                    html +='<div class="confile-cls file-style" type='+index+'>Amendment/Addendum : '+value.original_file_name+'</div>'
                                    }
                                    else{
                                    html +='<div class="confile-cls file-style" type='+index+'>Original Contract : '+value.original_file_name+'</div>'
                                    }
                            })
                        }                    }
                    else{
                    // $('.doc_selinvhidcls').attr('src','')
                    // let setfullurl= data.con_file.slice((data.con_file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${data.con_file}` : `${currentdomain}/media/${data.con_file}`

                    // $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'}) 
                    $(data.con_file).each(function(index,value){
                 
                        html +='<div class="confile-cls file-style" type='+index+'>'+value.original_file_name+'</div>'
                            
                    })
                }}
                else if (val == "10"){
                    // $(data.price_file).each(function(index,value){
                    //     if (value.amendment_addendum_id != null){
                    //         html +='<div class="confile-cls file-style" type='+index+'>Amendment/Addendum : '+value.original_file_name+'</div>'
                    //         }
                    //         else{
                    //         html +='<div class="confile-cls file-style" type='+index+'>Original Price : '+value.original_file_name+'</div>'
                    //         }
                      
                    // })
                    if(data.contracttype != 'original'){
                        if (data.price_file.length > 1){
                            console.log('length > 1')
                            $(data.price_file).each(function(index,value){
                                if (value.amendment_addendum_id != null){
                                    html +='<div class="confile-cls file-style" type='+index+'>Amendment/Addendum : '+value.original_file_name+'</div>'
                                    }
                                    else{
                                    html +='<div class="confile-cls file-style" type='+index+'>Original Price Table : '+value.original_file_name+'</div>'
                                    }
                            })
                        }
                    }
                        else{
                        // $('.doc_selinvhidcls').attr('src','')
                        // let setfullurl= data.price_file.slice((data.price_file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${data.price_file}` : `${currentdomain}/media/${data.price_file}`

                        // $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'}) 
                        $(data.price_file).each(function(index,value){
                            html +='<div class="confile-cls file-style" type='+index+'>'+value.original_file_name+'</div>'
                        
                        })
                    } 
                }
                else{
                    if (data.filecount > 1){
                       
                        if (val == "2"){
                            $(data.files).each(function(index,value){
                          
                                if (value.wcc_file_name) {
                                   
                                    if (value.return_status == 2 ){
                                    remove_name = value.wcc_file_name.replace("invoicedocuments/", "");
                                    html += '<div class="new-fil-cls file-style">' + remove_name + '</div>';
                                 
    
                                    }
                                    else {
    
                                        remove_name = value.wcc_file_name.replace("invoicedocuments/", "");
                                        html += '<div class="fil-cls file-style">' + remove_name + '</div>';
                                       
                                    }
                                } else {
                                    if (value.return_status == 2 ){
                                        remove_name = value.file_name.replace("invoicedocuments/", "");
                                        html += '<div class="new-fil-cls file-style">' + remove_name + '</div>';
                                     
        
                                        }
                                        else {
                                            remove_name = value.file_name.replace("invoicedocuments/", "");
                                            html += '<div class="fil-cls file-style">' + remove_name + '</div>';
                                           
                                        }
                                }
                                
                             
                            })

                        }
                        else{
                        $(data.files).each(function(index,value){
                          
                            if (value.wcc_support_file_name) {
                               
                                if (value.return_status == 2 ){
                                remove_name = value.wcc_support_file_name.replace("invoicedocuments/", "");
                                html += '<div class="new-fil-cls file-style">' + remove_name + '</div>';
                             

                                }
                                else {

                                    remove_name = value.wcc_support_file_name.replace("invoicedocuments/", "");
                                    html += '<div class="fil-cls file-style">' + remove_name + '</div>';
                                   
                                }
                            } else {
                                if (value.return_status == 2 ){
                                    remove_name = value.file_name.replace("invoicedocuments/", "");
                                    html += '<div class="new-fil-cls file-style">' + remove_name + '</div>';
                                 
    
                                    }
                                    else {
                                        remove_name = value.file_name.replace("invoicedocuments/", "");
                                        html += '<div class="fil-cls file-style">' + remove_name + '</div>';
                                       
                                    }
                            }
                            
                         
                        })
                    }
                    }
                    else if (data.filecount == 1){
                      
                        $('.doc_selinvhidcls').attr('src','')
                        var setfullurl=""
                        $(data.files).each(function(index,value){
                          
                            if (wcc_id && val == "2"){
                                console.log("Okay")
                                file_path=value.wcc_file
                               
                                setfullurl= file_path.slice((file_path.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${file_path}` : `${currentdomain}/media/${file_path}`
                            }else{
                                if(value.return_status ==1 ){
                                    file_path=value.file_name
                                    setfullurl= file_path.slice((newcleanFileName(file_path).lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/invoicedocuments/${newcleanFileName(file_path)}` : `${currentdomain}/media/invoicedocuments/${newcleanFileName(file_path)}`
                                   

                                }else {
                                    
                                    file_path=value.support_file
                                    // setfullurl= file_path.slice((newcleanFileName(file_path).lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${newcleanFileName(file_path)}` : `${currentdomain}/media/${newcleanFileName(file_path)}`
                                    var setfullurl = file_path.slice((file_path.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${file_path}` : `${currentdomain}/media/${file_path}`;
                                }

                            }
                          
                            $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'}) 
                        })
                    }
                    else{
                        
                        html +='<div class="file-style">No Files in '+gettext+'</div>'
                    }
                }
                $('.show_file_cls').html(html)
            }
            })
})

$(document).on('click','.fil-cls',function(){
    $('.fil-cls').removeClass('sel-file-cls')
    $(this).addClass('sel-file-cls')
    $('.doc_selinvhidcls').attr('src','')
    var file=$(this).text()
    let type=$(this).attr('type')
    if (type == 1){
        file=file.replace("Amendment/Addendum : ","")
    }
    else{
        file=file.replace("Original Contract : ","")
    }
   
    // var setfullurl=currentdomain+'/media/invoicedocuments/'+file+'#toolbar=0'
    let setfullurl = file.slice((file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ?
    `${package_src}?file=${currentdomain}/media/invoicedocuments/${newcleanFileName(file)}` :
    `${currentdomain}/media/invoicedocuments/${newcleanFileName(file)}`;

    $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'})
})

$(document).on('click','.new-fil-cls',function(){
    $('.fil-cls').removeClass('sel-file-cls')
    $(this).addClass('sel-file-cls')

    $('.doc_selinvhidcls').attr('src','')

    
    let file=$(this).text()
    
    file = file.replace(/[,+]/g, '');
   
    // let setfullurl=currentdomain+'/media/invoicedocuments/'+file+'#toolbar=0'
    // Function to remove brackets and special characters from the filename


    // Construct the setfullurl variable with cleaned filename
    let setfullurl = file.slice((file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ?
        `${package_src}?file=${currentdomain}/media/${(file)}` :
        `${currentdomain}/media/${(file)}`;
       
    $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'})
}) 

$(document).on('click','.confile-cls',function(){
    $('.confile-cls').removeClass('sel-file-cls')
    $(this).addClass('sel-file-cls')
    $('.doc_selinvhidcls').attr('src','')
    var file = $(this).text();

    // Check if the file name contains a colon
    if (file.includes(":")) {
        file = file.split(':')[1].trim();
    }
    let type=$(this).attr('type')
    if (type == 1){
        file=file.replace("Amendment/Addendum : ","")
    }
    else{
        file=file.replace("Original Contract : ","")
        file=file.replace("Original Price Table : ","")
    }
    file = file.replace(/[()]/g, '');
    // var setfullurl=currentdomain+'/media/invoicedocuments/'+file+'#toolbar=0'
    var setfullurl = file.slice((file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${encodeURIComponent(currentdomain + "/media/" + file.replace(/ /g, "_"))}` : `${currentdomain}/media/${file}`;
    $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'})
})


let submit_val='';
$(document).on('click','.status_cls',function(e){
    e.preventDefault();
    submit_val=$(this).val();
    addition_content=`<div><h4>Settlement</h4></div>`
    if(submit_val == '10'){
        addition_content+=`<table><tr><td>Settlement Amount</td><td><input type='text' oninput="$(this).val(($(this).val().replace(/[^0-9]/g,'')))" class='percentage_val' name='percentage_val'>%</td></tr></table>`
        $('.get_reason').html(addition_content)
    }
    else{
        $('.get_reason').html('<textarea name="main_comments" class="form-control"></textarea>')
    }
    let html = '';
    let data=exceptional_func(submit_val)
    if (submit_val == "3" || submit_val == "4"){
        data.forEach(element => {
            html +='<div><label for='+element.value+'><input type="checkbox" name="exceptional" value="'+element.value+'"  id='+element.value+'><span>'+element.name+'</span></label></div>'
        })
        $('.excp_content').html(html)
    }
    else{
        $('.excp_content').html('')
    }
    let bal_list=[]
      $('.balance_credit_note').each(function(){
        bal_list.push($(this).val())
      })
      $('.bal_cn').val(bal_list);
    $('#submit_id').attr('type','submit')

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
    else if (type == "5"){
        data = dispute_data
    }
    return data
}

$(document).on('click','.cmt_cls',function(){
    $('#submit_id').attr('type','button')
})

$(document).on('click','#submit_id',function(e){
    get_type=$(this).attr('type')
    let submit_name="";
    let check_err=0
    let err_count=0
    let select_count=0
    let reject_reason=0
    var selectedMessages = '';
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
            $('.status_cls').trigger('click');
            $('.get_reason').html('<textarea name="main_comments" class="form-control"></textarea>')
            }
            else{
                return false
            }
        }
        else{
            e.preventDefault();
        if (submit_val == '1'){
            submit_name = "Approved"
        }
        else if (submit_val == "2"){
            submit_name = "Proceed"
        }
        else if (submit_val == "3"){
            submit_name = "Returned"
            $("input[type='checkbox'][name='exceptional']:checked").each(function() {
                // Get the text content of the adjacent element
                var message = $(this).next('span').text();
                // Push the message to the selectedMessages array
                // selectedMessages.push(message);
                // alert(selectedMessages)
                selectedMessages += message + ',';
                
            });
            var checkedCheckboxes = $("input[type='checkbox'][name='exceptional']:checked").length;
            if (checkedCheckboxes === 0) {
                select_count++
            }
        }
        else if (submit_val == "4"){
            submit_name = "Rejected"
            var checkedCheckboxes = $("input[type='checkbox'][name='exceptional']:checked").length;

            if (checkedCheckboxes === 0) {
                reject_reason++
            }
        }
        else if (submit_val == "5"){
            submit_name = "Disputed"
        }
        else if(submit_val == "6"){
            submit_name  = "Settlement"
        }
        let getformid=$(this).parents("form").attr("id")
        let form=$("#"+getformid);
        $("<input>").attr({
            name: "selected_messages",
            type: "hidden",
            value: JSON.stringify(selectedMessages)  // Convert array to JSON string
        }).appendTo("form"); 
        $("<input>").attr({name: "submit_type",id: "hiddenId",type: "hidden",value: submit_val}).appendTo("form");
        $("<input>").attr({name: "submit_name",id: "nameId",type: "hidden",value: submit_name}).appendTo("form");
        // //use for generate payment
        if ($('.confirm_action').length  > 0){
            $('.confirm_action').val('confirm')
        }
        // var textareaContent = $(".cmnts").val();
        // if (textareaContent.trim() === '') {
        //     $(".cmnts").addClass('con_error')
        //     err_count++
        // }
        if(select_count > 0){
            Swal.fire("Select reason for Returning Invoice")
        }
        if(reject_reason > 0){
            Swal.fire("Select reason for Rejecting Invoice")
        }
        if(check_err == 0 && err_count == 0 && select_count == 0 && user_signature == '0' && reject_reason == 0){
        $('.status_cls').attr('disabled','disabled');
        $(this).attr('disabled',true)
        form.submit();
        }
        else if(user_signature == '1'){
            swal.fire('Add Signature')
            return false
        }
        else{
            e.preventDefault();
            return false
        }
    }
    }

})

$(document).on('keyup','.cmnts',function(){
    $(this).removeClass('con_error')
})
$(document).on('click', '.generate_payment', function(){
    let dataId = $(this).attr('data-id');
    var paycount = $(this).attr('data-value');
    let table = $(this).closest('.invoice-summary-table-width');
    let pdfViewer = table.next('.payment_pdf_viewer'); 
    // alert(paycount)
    $.ajax({
        type: "POST",
        url: `/invoice/getpaymentinstruction/${invoiceid}`,
        headers: { "X-CSRFToken":  csrf_token },
        data: {'payment_instruction': dataId,'payment_count':paycount },
        dataType: "json",
        success: function(data){
            if (data.success){
                if (pdfViewer.length) {
                    pdfViewer.attr('src', `${package_src}?file=${data.pdf_file_url}`);
                    // Set the src attribute and display style of #payment_instruction
                    $('#payment_instruction').attr({'src':`${package_src}?file=${data.pdf_file_url}`,'style':'display:block !important'});
                } else {
                    // Create a new PDF viewer with class
                    pdfViewer = $('<iframe>', {
                        class: 'payment_pdf_viewer',
                        src: `${package_src}?file=${data.pdf_file_url}`,
                        style: 'width: 100%; height: 500px; display: block !important;'
                    });
                    table.after(pdfViewer);
                    $('#payment_instruction').attr({'src':`${package_src}?file=${data.pdf_file_url}`,'style':'display:block !important'});
                }
            }
            else{
                console.log("Failed to retrieve PDF content.");
            }
        },
        error: function(xhr, status, error) {
            // Handle error
            console.error(xhr, status, error);
            console.log("Error occurred while fetching PDF content.");
        }
    });
});

$(document).on('click','.generate_payment_approval',function(){
    let dataId = $(this).attr('data-id');
    let pay_count = $(this).attr('data-value');
    $.ajax({
        type:"POST",
        url:`/invoice/getpaymentinstruction/${invoiceid}`,
        headers: { "X-CSRFToken":  csrf_token },
        data:{'payment_instruction':dataId ,'payment_count':pay_count },
        dataType: "json",
        success: function(data){
            if (data.success){
                $('#payment_instruction').attr({'src':`${package_src}?file=${data.pdf_file_url}`,'style':'display:block !important'})
            }
        }
    })
})
// document on ready
/*
$(document).ready(function(){
    console.log('payment_details',payment_details)
    //parsed  = JSON.parse(payment_details);
    // each loop
    //console.log('parsed',parsed)
    $.each(payment_details, function(key, value){
        console.log(key,value)
    });
})
*/
// $(document).on('click', '.calbtn', function () {
//     console.log({"modal-backdrop": $('.modal-backdrop')});
//     $('.modal-backdrop').css('display', 'none');
//     $('body').removeClass('modal-open'); 
// });
$(document).ready(function(){
$(function () {
    $(".exchange-draggable").draggable();
   
    // $('body').removeClass('modal-open'); 
     
  });

  


$(function () {
    
    $(".calculator-draggable").draggable();
  });

  $(document).on('click','.calbtn',function () {
    console.log({"modal-backdrop": $('.modal-backdrop')});
    $('.modal-backdrop').css('display', 'none');
    $('body').removeClass('modal-open');  
});

});
 
// Path to the PDF file
// const pdfUrl = 'http://127.0.0.1:8000/media/Invoice_PDF_18.pdf';

// // PDF.js viewer options
// const viewerOptions = {
//   viewerContainer: document.getElementById('pdf-viewer'),
// };

// // Initialize PDF.js viewer
// pdfjsLib.getDocument(pdfUrl).promise.then(function(pdfDoc) {
//   // Set the PDF document in the viewer
//   viewerOptions.pdfDocument = pdfDoc;

//   // Create a PDF.js viewer instance
//   const pdfViewerInstance = new pdfjsViewer.PDFViewer(viewerOptions);

//   // Set the viewer instance as the active viewer
//   pdfViewerInstance.setDocument(pdfDoc);

//   // Optional: Enable text search functionality
//   pdfViewerInstance.eventBus.on('textlayerrendered', function() {
//     const searchInput = document.getElementById('pdf-search');
//     searchInput.addEventListener('input', function() {
//       pdfViewerInstance.findController.executeCommand('find', {
//         query: searchInput.value,
//         phraseSearch: true,
//       });
//     });
//   });
// });

$(document).ready(function() {
$(document).on('click','.exchangeratecal',function(e){
    e.preventDefault();
    get_data()
})
});

function get_data(){
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken":  csrf_token },
      url: "/invoice/getexchangerate",
      data: {'pk':invoiceid},
      success: function(data){
        console.log('datasssss',data.payment_instruction_template)
        $('.exchange-rate-data').empty()
        $('.exchange-rate-data').append(data.payment_instruction_template)
      }
  });
  }



  $(document).on('click','.gen-confirm-cls',function(event){
    event.preventDefault()
    const notyf = new Notyf({
        duration: 5000,
        position: {
            x: 'center',
            y: 'center',
        },
        icon: {
            className: 'notyf-icon',
            tagName: 'i',
        },
        types: [
            {
            type: 'warning',
            background: '#D3D3D3',
            duration: 4000,
            icon: {
                className: 'material-icons',
                tagName: 'i',
                // text: 'warning',
                // dismissible: true
            }
            },
            {
            type: 'error',
            background: '#D3D3D',
            duration: 4000,
            // dismissible: true
            },
            {
            type: 'success',
            background: '#D3D3D',
            // background: '#7eff7c',
            duration: 4000,
            // dismissible: true
            }
        ]
        });

    form_data = $('#exchangerate').serialize()
    let is_error = false
    $('.exchangeratecls').not(':hidden').each(function(){
        var new_val=$(this).val()
      if($.trim(new_val) == ''){
        $(this).addClass('con_error')
        is_error = true
      }
    })
    if(!is_error){
    post_data(form_data)
    if($(this).val() == '3'){
        notyf.success({
            message: 'Exchange rate updated',
            icon: {
              className: 'fas fa-thumbs-up',
              tagName: 'i',
            },
          });
    }
    else if($(this).val() == '2'){
        notyf.success({
            message: 'Exchange Rate Confirmed Okay',
            icon: {
              className: 'fas fa-thumbs-up',
              tagName: 'i',
            },
          });
    }
    }
    return false
  })

  

  function post_data(form_data){
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: "/invoice/postexchangerate",
      data: form_data, 
      success: function(data){
        $('.close').trigger('click');
        window.location.reload();
      }
  });
  }

  $(document).on('change','.exchangeratecls',function(){
    var current=$(this)
    var base_amount=current.closest('tr').find('.invdisval').attr('data-id').replace(/[^0-9.]/g, "")
    var settlement_amount=current.closest('tr').find('.settlement_amount').val().replace(/[^0-9.]/g, "")
    var added_exchange=current.closest('tr').find('.added_exchange').attr('data-id')
    console.log('settlement_amount',settlement_amount)
    var tax=current.closest('tr').find('.invexcval').attr('data-id').replace(',', '')
    var currency=current.closest('tr').find('.final_amount').attr('data')
    var current_val=current.val()
    console.log(typeof tax,'type')
    var final=(base_amount*current_val)
    var final_amount= numeral(final).format('0,0.00');
    var final_set=(settlement_amount*current_val)
    var final_settlement= numeral(final_set).format('0,0.00');
    if ($.trim(current_val) == ''){
        current.closest('tr').find('.final_amount').text('')
        current.closest('tr').find('.invoice_total_amount').val(added_exchange)
    }
    else{
    amount=currency+' '+final_amount
    final_settlement=currency+' '+final_settlement
    current.closest('tr').find('.final_amount').text(final_settlement)
    current.closest('tr').find('.final_amount').val(amount)
    current.closest('tr').find('.invoice_total_amount').val(amount)
    }
  })


  $(document).on('click','.payment_instruction_pdf',function(){

    let dataid=$(this).attr('data_id')
    let setfullurl= dataid.slice((dataid.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${dataid}` : `${currentdomain}/media/${dataid}`
    console.log(setfullurl)
    $('.pi_doc_invhidcls').attr({'src':setfullurl,height:'590px !important'}).show();
})
  $(document).ready(function(){
    $('.inv_file:first').click()
  })


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

  $(document).on('keyup','.percentage_val',function(){
    $(this).removeClass('con_error')
  })

  $(document).on('click','.return_same_user',function(e){
    e.preventDefault();
    swal.fire('Return from Other User')
  })

  $(document).on('click','.confirmation_cls',function(e){
    const notyf = new Notyf({
        duration: 5000,
        position: {
            x: 'center',
            y: 'center',
        },
        icon: {
            className: 'notyf-icon',
            tagName: 'i',
        },
        types: [
            {
            type: 'warning',
            background: '#D3D3D3',
            duration: 4000,
            icon: {
                className: 'material-icons',
                tagName: 'i',
                // text: 'warning',
                // dismissible: true
            }
            },
            {
            type: 'error',
            background: '#D3D3D',
            duration: 4000,
            // dismissible: true
            },
            {
            type: 'success',
            background: '#D3D3D',
            // background: '#7eff7c',
            duration: 4000,
            // dismissible: true
            }
        ]
        });

    e.preventDefault();
    var confirm_check=$(this).val()
    if(confirm_check == '1' || confirm_check == '2'){
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": csrf_token },
            url: "/invoice/exchangerateconfirmation",
            data: {'pk':invoiceid,'confirm_check':confirm_check,'invoice_flow_id':Invoice_flow_id},
            success: function(data){
              if(confirm_check == '1'){
                notyf.success({
                    message: 'Exchange Rate Confirmed Okay',
                    icon: {
                      className: 'fas fa-thumbs-up',
                      tagName: 'i',
                    },
                  });
                  $('.close').trigger('click');
                  window.location.reload();
               }
               else if (confirm_check == '2'){
                $('.not_satisfied').removeAttr('style')
                $('.if_not_satisfied').removeAttr('style')
                $('.cofirmselect').css('display','none')
                $('.exchangerate_update').removeAttr('style')
               }
              
            }
        })
    }
    // if (confirm_check == '1'){
    // }
    // else if(confirm_check == '2'){
    //     window.location.reload();
    //     $('.exchangeratecal').trigger("click");
    //    $('.if_not_satisfied').removeAttr('style')
    //    $('.cofirmselect').css("display", "none");
    //    $('.gen-confirm-cls').removeAttr('style')
    // }
  })


  $(document).ready(function() {
    $('#exchangeratecal').modal({ 
      backdrop: 'static', // Optional: prevents closing by clicking outside the modal
    //   keyboard: false     // Optional: prevents closing by pressing the Esc key
    });

    $('#exampleModalCenter2').modal({
      backdrop: 'static',
    //   keyboard: false
    });
  });

  $(document).on('change','#deductions',function(){
    $('.total_value').each(function(){
        const data_id=$(this).attr('data-id')
        console.log("data_iddata_id"+data_id)

        let addition_amount=0 
        $('.addition_amount').each(function() {
            addition_amount = $('.addition_amount[data-id="'+data_id+'"]').val();
        })
        addition_amount=removecurrency(addition_amount)
        if(addition_amount == null || addition_amount == "" ){
            addition_amount=0;
        }
        var final_value =parseFloat(decimal_value($(this).attr('org_val')))+parseFloat(addition_amount)

        let html=''+$(this).attr('currency_symbol')+' '+numberWithCommas(decimal_value(final_value))+''
        // html+='<input type="hidden" value='+numberWithCommas(decimal_value(final_value))+' name="new_net_payable">'
        console.log({'8':html})
        $(this).html(html)
    })
    $('.balance_value').each(function(){
        $(this).text($(this).closest('td').attr('org_val'))
    })
    $('.deduction_amount').val('')
    $('.deduct').val('')
    if($(this).is(':checked')){
        $('.deduction_check').val('1')
        $('.other_deduction').closest('tr').removeAttr('style')
    }
    else{
        $('.deduction_check').val('0')
        $('.other_deduction').closest('tr').css('display','none')
    }
  })
  $(document).on('change','#additions',function(){
    
    $('.total_value').each(function(){
        const data_id=$(this).attr('data-id')
        console.log("data_iddata_id"+data_id)
        var deduction_amount=0
        $('.deduction_amount').each(function() {
            deduction_amount = $('.deduction_amount[data-id="'+data_id+'"]').val();
        })
        deduction_amount=removecurrency(deduction_amount)
        if(deduction_amount == null || deduction_amount == "" ){
            deduction_amount=0;
        }

        var final_value =parseFloat((decimal_value($(this).attr('org_val'))))-parseFloat(deduction_amount)


        let html=''+$(this).attr('currency_symbol')+' '+numberWithCommas(decimal_value(final_value))+''
        // html+='<input type="hidden" value='+numberWithCommas(decimal_value(final_value))+' name="new_net_payable">'
        console.log({'8':html})
        $(this).html(html)
    })
    $('.balance_value').each(function(){
        $(this).text($(this).closest('td').attr('org_val'))
    })
    $('.addition_amount').val('')
    $('.include').val('')
    if($(this).is(':checked')){
        $('.additions_check').val('1')
        $('.other_additions').closest('tr').removeAttr('style')
    }
    else{
        $('.additions_check').val('0')
        $('.other_additions').closest('tr').css('display','none')
    }
  })


  $(document).on('change','.deduction_amount',function(){
    const $this=$(this)
    let curren_value=$(this).val()
    const data_id=$(this).attr('data-id')
    let currency=$(this).attr('data-symbol')
    var getval=$(this).val()
    // let addition_amount = document.getElementsByClassName('addition_amount')[0].value;
    let addition_amount=0 
    $('.addition_amount').each(function() {
        addition_amount = $('.addition_amount[data-id="'+data_id+'"]').val();
    })
    if(addition_amount == null || addition_amount == "" ){
        addition_amount=0;
    }
    var val=removecommaonly(getval)
    $(this).val(('('+currency+' '+numberWithCommas(new_decimal_value(val))+')'))
    if( $.trim(curren_value) == ''){
        curren_value = 0
    }
    var final_value=parseFloat(removecommaonly($(this).closest('td').find('.final_value').val()))
    total_value=final_value-parseFloat(curren_value)+parseFloat(removecommaonly(removecurrency(addition_amount)))
    $('.total_value').each(function(){
        let current_data=$(this).attr('data-id')
        if (current_data == data_id){
            if (final_value < parseFloat(curren_value)){
                swal.fire('Exceeds Invoice Amount')
                $this.val('')
                
                let balance_value=final_value+parseFloat(removecommaonly(removecurrency(addition_amount)))
               


                let html=''+currency+' '+numberWithCommas(decimal_value(balance_value))+''
                // html+='<input type="hidden" value='+numberWithCommas(decimal_value(balance_value))+' name="new_net_payable">'
                $(this).html(html)

                $(this).closest('td').find('.balance_value').val(currency+' '+numberWithCommas(decimal_value(balance_value)))

            }
            else{
                let html=''+currency+' '+numberWithCommas(decimal_value(total_value))+''
                // html+='<input type="hidden" value='+numberWithCommas(decimal_value(total_value))+' name="new_net_payable">'
                $(this).html(html)

                // $(this).text(currency+' '+numberWithCommas(decimal_value(total_value)))
                $(this).closest('td').find('.balance_value').val(currency+' '+numberWithCommas(decimal_value(total_value)))
            }
        }
    })
    
  })

  $(document).on('change','.addition_amount',function(){
    const $this=$(this)
    let curren_value=$(this).val()
    const data_id=$(this).attr('data-id')
    let currency=$(this).attr('data-symbol')
    var getval=$(this).val()
    var val=removecommaonly(getval)
    $(this).val((''+currency+' '+numberWithCommas(new_decimal_value(val))+''))
    if( $.trim(curren_value) == ''){
        curren_value = 0
    }
    // let deduction_amount = document.getElementsByClassName('deduction_amount')[0].value;
    var deduction_amount=0
    $('.deduction_amount').each(function() {
        deduction_amount = $('.deduction_amount[data-id="'+data_id+'"]').val();
    })
    deduction_amount=removecurrency(deduction_amount)
    if(deduction_amount == null || deduction_amount == "" ){
        deduction_amount=0;
    }
    var final_value=parseFloat(removecommaonly($(this).closest('td').find('.final_value').val()))
    total_value=final_value+parseFloat(curren_value)-parseFloat(removecommaonly(removecurrency(deduction_amount)))
    $('.total_value').each(function(){
        let current_data=$(this).attr('data-id')
        if (current_data == data_id){
            if (final_value < parseFloat(curren_value)){
                swal.fire('Exceeds Invoice Amount')
                $this.val('')
                let balance_value=final_value-parseFloat(removecommaonly(removecurrency(deduction_amount)))
                let html=''+currency+' '+numberWithCommas(decimal_value(balance_value))+''
                html+='<input type="hidden" value='+numberWithCommas(decimal_value(balance_value))+' name="new_net_payable">'
                $(this).html(html)

                $(this).closest('td').find('.balance_value').val(currency+' '+numberWithCommas(decimal_value(balance_value)))

            }
            else{
                let html=''+currency+' '+numberWithCommas(decimal_value(total_value))+''
                html+='<input type="hidden" value='+numberWithCommas(decimal_value(total_value))+' name="new_net_payable">'
                $(this).html(html)

                // $(this).text(currency+' '+numberWithCommas(decimal_value(total_value)))
                $(this).closest('td').find('.balance_value').val(currency+' '+numberWithCommas(decimal_value(total_value)))
            }
        }
    })
    
  })


function removecommaonly(x) {
    if (typeof x !== 'string') {
        // If x is not a string, convert it to a string
        x = String(x);
    }
return x.replace(/[^a-zA-Z0-9.]/g, '')
}


function removecurrency(x) {
    if(typeof x !== 'string') {
        // If x is not a string, convert it to a string
        x = String(x);
    }
    values= x.replace(/[^0-9.]/g, '');
    if(values !=''){
        return values
    }else{
        return 0.00
    }
}


function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}


function newRoundOfTwoValues(number) {
    var numberStr = number.toString();
    var decimalPos = numberStr.indexOf('.');

    // If there is no decimal point, simply return the number with two decimal places
    if (decimalPos === -1) {
        return parseFloat(number).toFixed(2);
    }

    var integerPart = numberStr.substring(0, decimalPos);
    var decimalPart = numberStr.substring(decimalPos + 1);
    var newDecimalPart;
    
    if (decimalPart.length > 2) {
        // Check the third digit to determine whether to round up or not
        if (parseInt(decimalPart.charAt(2)) >= 5) {
            newDecimalPart = (parseInt(decimalPart.substring(0, 2)) + 1).toString().padStart(2, '0');
            
            // Check if rounding causes the decimal part to be "100", meaning we need to carry over to the integer part
            if (newDecimalPart === '100') {
                newDecimalPart = '00';
                integerPart = (parseInt(integerPart) + 1).toString();
            }
        } else {
            newDecimalPart = decimalPart.substring(0, 2);
        }
    } else if (decimalPart.length === 2) {
        // If the decimal part has exactly two digits, use them as they are
        newDecimalPart = decimalPart;
    } else {
        // If the decimal part has fewer than two digits, pad it with zeros
        newDecimalPart = decimalPart.padEnd(2, '0');
    }

    var result = integerPart + '.' + newDecimalPart;

    
    return parseFloat(result).toFixed(2);
}

function decimal_value(val){
    if (val != ''){
        var con_val=val.toString()
        var remove_commas= con_val.replace(/,/g, "");
        console.log(remove_commas)
        if (remove_commas == Math.floor(remove_commas)){
            console.log('if',val)

            return newRoundOfTwoValues(remove_commas)
        }
        else{
            console.log('else',val)

            return newRoundOfTwoValues(remove_commas)
        }
    }
    else{
        return val
    }
}

function new_decimal_value(val){
    if (val != ''){
        var con_val=val.toString()
        var remove_commas= con_val.replace(/,/g, "");
        console.log(remove_commas)
        if (remove_commas == Math.floor(remove_commas)){
            console.log('if',val)

            return newRoundOfTwoValues(remove_commas)
        }
        else{
            console.log('else',val)

            return newRoundOfTwoValues(remove_commas)
        }
    }
    else{
        return val
    }
}
    
    $(document).on('click','.nothing_confirmed',function(e){
        e.preventDefault();
        swal.fire('Confirm Exchange Rate')
    })

   
   
    $(document).on('click','.confirm_tax',function(e){
        e.preventDefault();
        swal.fire('Confirm Taxes')
    }) 


    $(document).on('click','.payment_confirm',function(e){
        e.preventDefault();
        let count_num=0
        const notyf = new Notyf({
            duration: 5000,
            position: {
                x: 'center',
                y: 'center',
            },
            icon: {
                className: 'notyf-icon',
                tagName: 'i',
            },
            types: [
                {
                type: 'warning',
                background: '#D3D3D3',
                duration: 4000,
                icon: {
                    className: 'material-icons',
                    tagName: 'i',
                    // text: 'warning',
                    // dismissible: true
                }
                },
                {
                type: 'error',
                background: '#D3D3D',
                duration: 4000,
                // dismissible: true
                },
                {
                type: 'success',
                background: '#D3D3D',
                // background: '#7eff7c',
                duration: 4000,
                // dismissible: true
                }
            ]
            });
        if($('#deductions').is(':checked')){
            if($.trim($('.deduct').val()) == ''){
                $('.deduct').addClass('con_error')
                count_num++
            }
            $('.deduction_amount').each(function(){
                if($.trim($(this).val()) == ''){
                    $(this).addClass('con_error')
                    count_num++
                }
            })
        }
        if($('#additions').is(':checked')){
            if($.trim($('.include').val()) == ''){
                $('.include').addClass('con_error')
                count_num++
            }
            $('.addition_amount').each(function(){
                if($.trim($(this).val()) == ''){
                    $(this).addClass('con_error')
                    count_num++
                }
            })
        }
        if(count_num == 0){
            notyf.success({
                message: 'Taxes confirmed',
                icon: {
                  className: 'fas fa-thumbs-up',
                  tagName: 'i',
                },
              });
            $('#taxconfirm').submit()
        }
        else{
            return false
        }
    })

    $(document).on('change','.include,addition_amount,.deduct,.deduction_amount',function(){
        $(this).removeClass('con_error')
    })

    function goBack() {
        window.history.back();
    }
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



    $('.view_file').click(function(){
        let val=$(this).attr('data_id')
        // let setfullurl=currentdomain+'/media/'+filename+''
        let setfullurl= val.slice((val.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${val}` : `${currentdomain}/media/${val}`
        console.log('setfullurl',setfullurl)
        $('.doc_pay_ins_cls').attr({'src':setfullurl,height:'590px !important'})    
    })
      
