$(document).on('click','.commonbtn',function(){
  $('.commonbtn').removeClass('support_high-cls')
  let val=$(this).attr('dataid')
  $(this).addClass('support_high-cls')
  let gettext=$(this).text()
  $('.doc_selinvhidcls').attr('src','')
  console.log({'val':val})
  console.log({'invoiceid':invoiceid})
  console.log({'credit_id':credit_id})
  if(!$(this).hasClass('invoice_docs')){
  $.ajax({
          type:"GET",
          data:{'supportid':val,'invoiceid':invoiceid,'credit_id':credit_id},
          url:'/credit/getsupportfilescredit',
          success: function(data){
              console.log({'data':data})
              // let html="<div><h5>"+gettext+"</h5>"
              let html="" 
              if (val == "3"){
                  if(data.contracttype != 'original'){
                     
                      console.log('original')
                      if (data.con_file.length > 1){
                          console.log('length > 1')
                          $(data.con_file).each(function(index,value){
                            if (value.amendment_addendum_id != null){
                                html +='<div><span>Amendment/Addendum : </span><span class="confile-cls file-style" type='+index+'>'+value.original_file_name+'</span></div>'
                            }
                            else{
                            html +='<div><span>Original Contract : </span><span class="confile-cls file-style" type='+index+'>'+value.original_file_name+'</span></div>'
                            }
                          })
                      }                    }
                  else{
                //   console.log(currentdomain,'arc2',data.con_file)
                //   $('.doc_selinvhidcls').attr('src','')
                //   // let setfullurl=currentdomain+'/media/'+data.con_file+'#toolbar=0'
                //   let setfullurl= data.con_file.slice((data.con_file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${data.con_file}` : `${currentdomain}/media/${data.con_file}`
                //   console.log({'setfullurl':setfullurl})
                //   console.log({'eeee':setfullurl})

                //   $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'}) 

                $(data.con_file).each(function(index,value){
                    html +='<div class="confile-cls file-style" type='+index+'>'+value.original_file_name+'</div>'    
                })
                  }
              }
              else if (val == "4"){
                  if(data.contracttype != 'original'){
                  if (data.price_file.length > 1){
                      console.log('length > 1')
                      $(data.price_file).each(function(index,value){
                        if (value.amendment_addendum_id != null){
                            html +='<div><span>Amendment/Addendum : </span><span class="confile-cls file-style" type='+index+'>'+value.original_file_name+'</span></div>'
                        }
                        else{
                        html +='<div><span>Original Price Table : </span><span class="confile-cls file-style" type='+index+'>'+value.original_file_name+'</span></div>'
                        }
                      })
                  }
              }
                  else{
                //       console.log(2,data.price_file)
                //   $('.doc_selinvhidcls').attr('src','')
                //   // let setfullurl=currentdomain+'/media/'+data.price_file+'#toolbar=0'
                //   let setfullurl= data.price_file.slice((data.price_file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${data.price_file}` : `${currentdomain}/media/${data.price_file}`

                //   $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'}) 

                $(data.price_file).each(function(index,value){
                    html +='<div class="confile-cls file-style" type='+index+'>'+value.original_file_name+'</div>'    
                })
              }
              }
              else if (val == "2"){
                console.log(data)
                if (data.filecount > 1){
                    console.log({'data.files':data.files})
                    $(data.files).each(function(index,value){
                        remove_name=(value.file).replace("invoicedocuments/","")
                        html +='<div class="fil-cls file-style" file_type="credit">'+remove_name+'</div>'
                    })
                    console.log({'html':html})
                }
                else if (data.filecount == 1){
                    $('.doc_selinvhidcls').attr('src','')
                    let setfullurl=""
                    $(data.files).each(function(index,value){
                        // setfullurl=currentdomain+'/media/'+value.support_file+'#toolbar=0'
                        setfullurl= value.file.slice((value.file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${value.file}` : `${currentdomain}/media/${value.file}`

                    })
                    console.log({'444':setfullurl})
                    $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'})  
                
                }
                else{
                    if(val != undefined){
                    html +='<div class="file-style">No Files in '+gettext+'</div>'
                    }
                }

           
              }
              else{
                  console.log(data)
                  if (data.filecount > 1){
                      $(data.files).each(function(index,value){
                          remove_name=(value.original_file_name).replace("creditdocuments/","")
                          html +='<div class="fil-cls file-style" file_type="invoice">'+remove_name+'</div>'
                      })
                  }
                  else if (data.filecount == 1){
                      $('.doc_selinvhidcls').attr('src','')
                      let setfullurl=""
                      $(data.files).each(function(index,value){
                          // setfullurl=currentdomain+'/media/'+value.support_file+'#toolbar=0'
                          setfullurl= value.file.slice((value.file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${value.file}` : `${currentdomain}/media/${value.file}`

                      })
                      $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'})  
                  }
                  else{
                    if(val != undefined){
                      html +='<div class="file-style">No Files in '+gettext+'</div>'
                    }
                  }
              }
            //   alert(html)
              $('.show_file_cls').html(html)
              $('.fil-cls:first').click();
          }
          })
    }
})

$(document).on('click','.confile-cls',function(){
    $('.fil-cls').removeClass('sel-file-cls')
    $(this).addClass('sel-file-cls')
    $('.doc_selinvhidcls').attr('src','')
    var file=$(this).text()
    // var setfullurl=currentdomain+'/media/invoicedocuments/'+file+'#toolbar=0'
    //var setfullurl=currentdomain+'/media/invoicedocuments/'+file+''
    var setfullurl= file.slice((file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/invoicedocuments/${file}` : `${currentdomain}/media/invoicedocuments/${file}`
    setfullurl = setfullurl.replace(/ /g, "_");
    $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'})
})

$(document).on('click','.check_box_list',function(){
    return false
})

let submit_val='';
$(document).on('click','.status_cls',function(e){
    e.preventDefault();
    submit_val=$(this).val();
    let html = '<div class="mt-2"><b>Reasons :</b></div>';
    let data=exceptional_func(submit_val)
    console.log(data)
    selected_count=$('input.check_box_list:checked').length
    current_count=$('input.confirm_chk_cls:checked').length
    // alert(check_conform_costcode)
    if (selected_count != current_count){
        e.preventDefault();
        Swal.fire("Please (Select to Confirm Okay)")
    }else{
        $(".status_cls").attr("data-target", "#exampleModalCenter");
    }
    if (submit_val == "3" || submit_val == "4"){
        // html=`<label for="one">
        // <input type="checkbox" name="exceptional" value="1" id="one"> Changes in Supporting Documents</label>`
        data.forEach(element => {
            html +='<div><label for="'+element.value+'"><input type="checkbox" name="exceptional" value="'+element.value+'"  id="'+element.value+'"><span>'+element.name+'</span></label></div>'
        })
        $('.excp_content').html(html)
    }
    else{
        $('.excp_content').html('')
    }
    $('#submit_id').attr('type','submit')

}) 

function exceptional_func(type){
    let data="";
    let return_data=[{'name':'Incomplete Information','value':'1'},{'name':'Ambiguous Descriptions on Credit Note.','value':'2'},{'name':'Inconsistencies with Supporting Documentation','value':'3'},,{'name':'Discrepancies with Original Invoice Transaction','value':'4'},{'name':'Insufficient Supporting Evidence','value':'5'},{'name':'Other Reasons','value':'6'}]

    let reject_data=[{'name':'Incorrect Information','value':'7'},{'name':'Wrong Credit Note Amount','value':'8'},{'name':'Lack of Supporting Documentation','value':'9'},,{'name':'Duplicate Submission','value':'10'},{'name':'Disputed Claims','value':'11'},{'name':'Non-Compliance with Terms and Conditions of Contract','value':'12'},{'name':'Other Reasons','value':'13'}]

    let dispute_data=[{'name':'Invoice details interpretation issues','value':'14'},{'name':'Supporting document issues','value':'15'},{'name':'Issues due to Verbal communication for work invoiced','value':'16'},,{'name':'Work done outside of approval limits','value':'17'},{'name':'Dispute on contract execution','value':'18'},{'name':'Dispute coming out of Audit findings','value':'19'},{'name':'Inability to clarify through normal methods','value':'20'},{'name':'Other Reasons','value':'21'}]
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


$(document).on('click','#submit_id',function(e){
    e.preventDefault();
    get_type=$(this).attr('type')
    selected_count=$('input.check_box_list:checked').length
    current_count=$('input.confirm_chk_cls:checked').length
    let err_count=0
    let select_count=0
    var selectedMessages = '';
    if (selected_count == current_count){
    let submit_name="";
    if (get_type == "submit"){
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
               
                selectedMessages += message + ',';
               
            });
            var checkedCheckboxes = $("input[type='checkbox'][name='exceptional']:checked").length;

            if (checkedCheckboxes === 0) {
                select_count++
            }
        }
        else if (submit_val == "4"){
            submit_name = "Rejected"
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
        
        var textareaContent = $(".comnts,.cmnts").val();
        // if (textareaContent.trim() === '') {
        //     $(".comnts").addClass('con_error')
        //     err_count++
        // }
        if(select_count > 0){
            Swal.fire("Select reason for Returning Invoice")
        }
        if (err_count == 0 && select_count == 0){
            form.submit();
            $('.status_cls').attr('disabled','disabled');
            $(this).attr('disabled',true)
        }
        else{
            return false

        }
        // form.submit();
    }
    }
    else{
        Swal.fire("Please (Select to Confirm Okay)")
    }
})

$(document).ready(function(){
    $('.inv_file:first').click()
})

$(document).on('click','.inv_file',function(){
    $('.inv_file').removeClass('inv-high-cls')
    var inv_name=$(this).closest('tr').find('.inv_name').text()
    $('.hd-inv').text(inv_name)
    var url=$(this).attr('value')
    $(this).addClass('inv-high-cls')
    let setfullurl= url.slice((url.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${url}` : `${currentdomain}/media/${url}`
    console.log({'1111':setfullurl})
    $('.doc_invhidcls').attr({'src':setfullurl,height:'590px !important'})
})
function cleanFileName(fileName) {
    return fileName.replace(/[^.-\w\s]/gi, '').replace(/\s+/g, '_');
}

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
    if ($(this).attr('file_type') == 'invoice'){
        // var setfullurl=currentdomain+'/media/invoicedocuments/'+file+'#toolbar=0'
        let setfullurl= file.slice((file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/creditdocuments/${cleanFileName(file)}` : `${currentdomain}/media/creditdocuments/${cleanFileName(file)}`
      
        $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'})
    }
    else if ($(this).attr('file_type') == 'credit') {
        // var setfullurl=currentdomain+'/media/invoicedocuments/'+file+'#toolbar=0'
        let setfullurl= file.slice((file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${cleanFileName(file)}` : `${currentdomain}/media/${cleanFileName(file)}`
      
        $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'})
    }
    
})


$(document).on('click','.return_same_user',function(e){
    e.preventDefault();
    swal.fire('Return from Other User')
  })


$(document).on('click','.invoice_docs',function(){
    var html="<div>"
    $('.invoice_num').each(function(){
        html+=vendor_name+' - '+$(this).val()
    })
    html+=' </div><div><a href="/invoice/invoiceview/'+invoiceid+'" target="_blank"> View Expanded Details</a></div>'
        $('.show_file_cls').html(html)
        $('.doc_selinvhidcls').attr('src','')
})
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
