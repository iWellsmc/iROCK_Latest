
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

$(document).ready(function(){
    $('#exampleModalCenter').modal({
        backdrop: 'static', 
        keyboard: false
    });
})

$(document).on('click','#submit_id',function(e){
    e.preventDefault();
    get_type=$(this).attr('type')
    var selectedMessages = '';
    selected_count=$('input.check_box_list:checked').length
    current_count=$('input.confirm_chk_cls:checked').length
    let err_count=0
    let select_count=0
    let reject_reason=0
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
        let getformid=$(this).parents("form").attr("id")
        let form=$("#"+getformid);
        $("<input>").attr({
            name: "selected_messages",
            type: "hidden",
            value: JSON.stringify(selectedMessages)  // Convert array to JSON string
        }).appendTo("form");
        $("<input>").attr({name: "submit_type",id: "hiddenId",type: "hidden",value: submit_val}).appendTo("form");
        $("<input>").attr({name: "submit_name",id: "nameId",type: "hidden",value: submit_name}).appendTo("form");
        var textareaContent = $(".comnts").val();
        // if (textareaContent.trim() === '') {
        //     $(".comnts").addClass('con_error')
        //     err_count++
        // }
        if(select_count > 0){
            Swal.fire("Select reason for Returning Invoice")
        }
        if(reject_reason > 0){
            Swal.fire("Select reason for Rejecting Invoice")
        }
        if (err_count == 0 && select_count == 0  && user_signature == '0' && reject_reason == 0){
            form.submit();
            $('.status_cls').attr('disabled','disabled');
            $(this).attr('disabled',true)
        }
        else if(user_signature == '1'){
            swal.fire('Add Signature')
            let currentUrl = window.location.href;
            let baseUrl = currentUrl.split('/').slice(0, 3).join('/');
            setTimeout(function(){
                window.location.href = baseUrl+redirect_user_signature_url;
            }, 1000);
            
            return false
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






$(document).on('keyup','.comnts',function(){
    $(this).removeClass('con_error')
})

$(document).on('click','.inv_file',function(){

    $('.commonbtn').removeClass('support_high-cls')
    let inv_name=$(this).closest('tr').find('.inv_name').text()
    $('.hd-inv').text(inv_name)
    let url=$(this).attr('value')
    $(this).addClass('support_high-cls')
    let setfullurl= url.slice((url.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/invoicedocuments/${url}` : `${currentdomain}/media/invoicedocuments/${url}`

    $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'})
})

$(document).on('click','.commonbtn',function(){

    $('.commonbtn').removeClass('support_high-cls')
    let val=$(this).attr('dataid')
    $(this).addClass('support_high-cls')
    let gettext=$(this).text()
    $('.doc_selinvhidcls').attr('src','')
    console.log({'val':val})
    console.log({'invoiceid':invoiceid})
    $.ajax({
            type:"GET",
            data:{'supportid':val,'invoiceid':invoiceid , "wcc_id":wcc_id},
            url:'/invoice/getsupportfiles',
            success: function(data){
                let html="" 
        
                if (val == "9"){
                    if(data.contracttype != 'original'){
                        if (data.con_file.length > 1){
                            $(data.con_file).each(function(index,value){
                                if (value.amendment_addendum_id != null){
                                    html +='<div class="confile-cls file-style" type='+1+'>Amendment/Addendum : '+value.original_file_name+'</div>'
                                }
                                else{
                                html +='<div class="confile-cls file-style" type='+0+'>Original Contract : '+value.original_file_name+'</div>'
                                }
                            })
                        }                    
                    }
                    else{
                    // console.log(currentdomain,'arc2',data.con_file)
                    // $('.doc_selinvhidcls').attr('src','')
                    // // let setfullurl=currentdomain+'/media/'+data.con_file+'#toolbar=0'
                    // let setfullurl= data.con_file.slice((data.con_file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${data.con_file}` : `${currentdomain}/media/${data.con_file}`
                    // console.log({'setfullurl':setfullurl})

                    // $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'}) 
                        $(data.con_file).each(function(index,value){
                            html +='<div class="confile-cls file-style" type='+index+'>'+value.original_file_name+'</div>'    
                        })
                    }
                }
                else if (val == "10"){
                    if(data.contracttype != 'original'){
                        if (data.price_file.length > 1){
                            $(data.price_file).each(function(index,value){
                                if (value.amendment_addendum_id != null){
                                    html +='<div class="confile-cls file-style" type='+1+'>Amendment/Addendum : '+value.original_file_name+'</div>'
                                    }
                                    else{
                                    html +='<div class="confile-cls file-style" type='+0+'>Original Price Table : '+value.original_file_name+'</div>'
                                    }
                            })
                        }
                    }
                    else{
                    //     console.log(2,data.price_file)
                    // $('.doc_selinvhidcls').attr('src','')
                    // // let setfullurl=currentdomain+'/media/'+data.price_file+'#toolbar=0'
                    // let setfullurl= data.price_file.slice((data.price_file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${data.price_file}` : `${currentdomain}/media/${data.price_file}`

                    // $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'}) 
                        $(data.price_file).each(function(index,value){
                            html +='<div class="confile-cls file-style" type='+index+'>'+value.original_file_name+'</div>'
                        
                        })
                    }
                }
                else{
                    console.log(data)

                    if (data.filecount > 1){
                        // alert(data.data)
                        // console(data)
                        if (val == "2"){
                            $(data.files).each(function(index,value){
                                if (value.wcc_file_name){
                                    console.log("value",value)
                                    if (value.disputedquery_id != null ){
                                        // remove_name=(value.file).replace("invoicedocuments/","")
                                        // html +='<div class="fil-cls file-style">'+remove_name+'</div>'
                                     }  
                                    else {
                                        if (value.return_status == 2 ){
                                            remove_name=(value.wcc_file_name).replace("invoicedocuments/","")
                                            html +='<div class="new-fil-cls file-style  ">'+remove_name+'</div>'
                                       
                                        
                                         }
                                        else{
                                        
                                             remove_name=(value.wcc_file_name).replace("invoicedocuments/","")
                                             html +='<div class="fil-cls file-style  ">'+remove_name+'</div>'
                                      
                                       
                                        }
                                    }
                                // alert(remove_name)
                                }
                                else{
                                    console.log("value",value)
                                    if (value.disputedquery_id != null ){
                                        // remove_name=(value.file).replace("invoicedocuments/","")
                                        // html +='<div class="fil-cls file-style">'+remove_name+'</div>'
                                     }
                                    else {
                                        if (value.return_status == 2 ){
                                            remove_name=(value.file_name).replace("invoicedocuments/","")
                                            html +='<div class="new-fil-cls file-style  ">'+remove_name+'</div>'
                                       
                                        
                                        }
                                        else{
                                        
                                            remove_name=(value.file_name).replace("invoicedocuments/","")
                                            html +='<div class="fil-cls file-style  ">'+remove_name+'</div>'
                                      
                                       
                                        }
                                        }
                                    }
                                
                            })

                        }
                        else{
                        
                            $(data.files).each(function(index,value){
                                if (value.wcc_file_name){
                                    console.log("value",value)
                                    if (value.disputedquery_id != null ){
                                        // remove_name=(value.file).replace("invoicedocuments/","")
                                        // html +='<div class="fil-cls file-style">'+remove_name+'</div>'
                                     }  
                                    else {
                                        if (value.return_status == 2 ){
                                            remove_name=(value.wcc_file_name).replace("invoicedocuments/","")
                                            html +='<div class="new-fil-cls file-style  ">'+remove_name+'</div>'
                                       
                                        
                                         }
                                        else{
                                        
                                             remove_name=(value.wcc_file_name).replace("invoicedocuments/","")
                                             html +='<div class="fil-cls file-style  ">'+remove_name+'</div>'
                                      
                                       
                                        }
                                    }
                                // alert(remove_name)
                                }
                                else{
                                    console.log("value",value)
                                    if (value.disputedquery_id != null ){
                                        // remove_name=(value.file).replace("invoicedocuments/","")
                                        // html +='<div class="fil-cls file-style">'+remove_name+'</div>'
                                     }
                                    else {
                                        if (value.return_status == 2 ){
                                            remove_name=(value.file_name).replace("invoicedocuments/","")
                                            html +='<div class="new-fil-cls file-style  ">'+remove_name+'</div>'
                                       
                                        
                                        }
                                        else{
                                        
                                            remove_name=(value.file_name).replace("invoicedocuments/","")
                                            html +='<div class="fil-cls file-style  ">'+remove_name+'</div>'
                                      
                                       
                                        }
                                        }
                                    }
                                
                            })
                    }
                }
                    else if (data.filecount == 1){
                        
                        $('.doc_selinvhidcls').attr('src','')
                        let setfullurl=""
                        $(data.files).each(function(index,value){
                           console.log("lamiaaa",data.files);
                            let file_path="";

                            if (wcc_id && val == "2"){
                              
                                file_path=value.wcc_file
                                setfullurl= file_path.slice((file_path.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${file_path}` : `${currentdomain}/media/${file_path}`
                              
                            }
                            else{
                                file_path=value.support_file
                                setfullurl= value.support_file.slice((value.support_file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${value.support_file}` : `${currentdomain}/media/${value.support_file}`
                           
                            }
                        })
                        $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'})  
                    }
                    else{
                        html +='<div class="file-style">No Files in '+gettext+'</div>'
                    }
                }
                $('.show_file_cls').html(html)
                $('.fil-cls:first').click();
            }
            })
})
function cleanFileName(fileName) {
    return fileName.replace(/[^.-\w\s]/gi, '').replace(/\s+/g, '_');
}
$(document).on('click','.fil-cls',function(){
    $('.fil-cls').removeClass('sel-file-cls')
    $(this).addClass('sel-file-cls')

    $('.doc_selinvhidcls').attr('src','')

    
    let file=$(this).text()
    
    file = file.replace(/[,+]/g, '');
   
    // let setfullurl=currentdomain+'/media/invoicedocuments/'+file+'#toolbar=0'
    // Function to remove brackets and special characters from the filename


    // Construct the setfullurl variable with cleaned filename
    let setfullurl = file.slice((file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ?
        `${package_src}?file=${currentdomain}/media/invoicedocuments/${cleanFileName(file)}` :
        `${currentdomain}/media/invoicedocuments/${cleanFileName(file)}`;
       
    
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
$(document).ready(function(){
    $('.commonbtn:first').click();
})

$(document).on('click','.confile-cls',function(){
    $('.confile-cls').removeClass('sel-file-cls')
    $(this).addClass('sel-file-cls')
    $('.doc_selinvhidcls').attr('src','')
    let file=$(this).text()
    let type=$(this).attr('type')
    if (type == 1){
        file=file.replace("Amendment/Addendum : ","")
    }
    else{
        file=file.replace("Original Contract : ","")
        file=file.replace("Original Price Table : ","")
    }
    file = file.replace(/[()]/g, '');
    // let setfullurl=currentdomain+'/media/invoicedocuments/'+file+'#toolbar=0'
    var setfullurl = file.slice((file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${encodeURIComponent(currentdomain + "/media/" + file.replace(/ /g, "_"))}` : `${currentdomain}/media/${file}`;
 
    $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'})
})

$(document).on('click','.check_box_list',function(){
    return false
})

$(document).ready(function(){
    $("input:checkbox[class=check_box]:checked").each(function () {
        console.log('this',$(this))
    })
})

$(document).ready(function() {
    // Make the modal draggable only by its header
    $('#exampleModalCenter2').draggable({
        handle: ".modal-header",
        containment: "#container", // Limit dragging within the element with id="container"
    });
});
$(document).on('click', '.confirm_chk_cls', function (e) {
    var check_conform_costcode=$('#check_conform_costcode').val()
    // alert(check_conform_costcode)
    if(check_conform_costcode){
        if(conform_costcode === 'False'){
            e.preventDefault();
            swal.fire('Confirm Cost Code')
            
        }
    }



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

