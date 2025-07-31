// $(document).on('click','.status_cls',function(e){
//     e.preventDefault();
//     let get_value=$(this).val();
//     $("<input>").attr({name: "submit_type",id: "hiddenId",type: "hidden",value: get_value}).appendTo("form");
//     // $('#wccapprovalid')[0].submit();
// })


let submit_val='';
$(document).on('click','.status_cls',function(e){
    e.preventDefault();
    submit_val=$(this).val();
    $('#submit_id').attr('type','submit')

}) 

$(document).on('click','.cmt_cls',function(){
    $('#submit_id').attr('type','button')
})

$(document).on('click','#submit_id',function(){
    get_type=$(this).attr('type')
    if (get_type == "submit"){
        let getformid=$(this).parents("form").attr("id")
        // let form=$("#"+getformid);
        $('.status_cls').attr('disabled','disabled');
        $("<input>").attr({name: "submit_type",id: "hiddenId",type: "hidden",value: submit_val}).appendTo("form");
        $('#wccapprovalid')[0].submit();
    }

})
$(document).on('click','.status_cls',function(e){
    e.preventDefault();
    submit_val=$(this).val();
    let html = '<div class="mt-2"><b>Reasons :</b></div>';
    let data=exceptional_func(submit_val)

    
    if (submit_val == "2" || submit_val == "3"){
        // html=`<label for="one">
        console.log("data",data);
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
    let return_data=[{'name':'Incomplete Information.','value':'1'},{'name':'Discrepancies with Contractual Requirements.','value':'2'},{'name':'Clarification for Supporting Documentation.','value':'3'},,{'name':'Non-Compliance with Quality Standards.','value':'4'},{'name':'Unresolved Issues or Deficiencies','value':'5'},{'name':'Inconsistencies with Inspection Reports.','value':'6'},{'name':'Incomplete Approvals or Authorizations from Contractor’s end.','value':'7'},{'name':'Other Reasons.','value':'8'}]

    let reject_data=[{'name':'Incorrect Information','value':'9'},{'name':'Non-Compliance with Contractual Requirements/Obligations','value':'10'},{'name':'Safety or Regulatory Violations.','value':'11'},,{'name':'Lack of Supporting Documentation','value':'12'},{'name':'Unauthorized Changes or Alterations for Work Done','value':'13'},{'name':'Failure to Meet Acceptance Criteria as per Contractual Terms','value':'14'},{'name':'Disputed Claims or Unresolved Issues or Deficiencies.','value':'15'},{'name':'Missing Approvals or Authorizations from Contractor’s end.','value':'16'},{'name':'Other Reasons.','value':'17'}]

    let dispute_data=[{'name':'Invoice details interpretation issues','value':'18'},{'name':'Supporting document issues','value':'19'},{'name':'Issues due to Verbal communication for work invoiced','value':'20'},,{'name':'Work done outside of approval limits','value':'21'},{'name':'Dispute on contract execution','value':'22'},{'name':'Dispute coming out of Audit findings','value':'23'},{'name':'Inability to clarify through normal methods','value':'24'},{'name':'Other Reasons','value':'25'}]
    if (type == "2"){
        data = return_data
    }
    else if (type == "3"){
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
    var selectedMessages = '';
    let err_count=0
    let select_count=0
    let reject_reason=0
    if (selected_count == current_count){
    let submit_name="";
    if (get_type == "submit"){
        if (submit_val == '1'){
            submit_name = "Approved"
        }
        else if (submit_val == "4"){
            submit_name = "Proceed"
        }
        else if (submit_val == "2"){
            submit_name = "Returned"
            // var checkedCheckboxes = $("input[type='checkbox'][name='exceptional']:checked").length;

            // if (checkedCheckboxes === 0) {
            //     select_count++
            // }

            $("input[type='checkbox'][name='exceptional']:checked").each(function() {
                var message = $(this).next('span').text();
                selectedMessages += message + ',';
            });
            var checkedCheckboxes = $("input[type='checkbox'][name='exceptional']:checked").length;
            if (checkedCheckboxes === 0) {
                select_count++
            }

        }
        else if (submit_val == "3"){
            submit_name = "Rejected"
            $("input[type='checkbox'][name='exceptional']:checked").each(function() {
                var message = $(this).next('span').text();
                selectedMessages += message + ',';
            });
            var checkedCheckboxes = $("input[type='checkbox'][name='exceptional']:checked").length;

            if (checkedCheckboxes === 0) {
                reject_reason++
            }
        }
        let getformid=$(this).parents("form").attr("id")
        let form=$("#"+getformid);
        $("<input>").attr({name: "selected_messages",type: "hidden", value: JSON.stringify(selectedMessages)}).appendTo("form");
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




