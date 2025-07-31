var global=$('.taxnamecls').val();
$(document).ready(function(){

    $('#addtaxformid').validate();
    $("[name=taxname]").rules("add", {
        required: true,
        });   
});

//$(document).on('keyup','.taxnamecls',function(){
    var ajaxData = false;
    $(".taxnamecls").focusout(function(){
        var val=$(this).val()
        if (global != val){
            $('.waring-err').remove()
            var currentelement=$(this)
            $.ajax({
                type: "POST",
                headers: { "X-CSRFToken": csrf_token},
                url: "/invoiceguard/validaterole/",
                async:false,
                data: {'role_name':$.trim(val),'role_id':'{{role.id}}'},
                success: function(data){
                    console.log({'checktaxname':data})
                    if (data.status){
                        ajaxData = true;
                        currentelement.after('<span class="waring-err">Role Already Exists</span>')
                        $('.final-cls').prop('disabled',true)
                    }
                    else{
                        ajaxData = false;
                        $('.final-cls').prop('disabled',false)
                    }
                }
            });
        }
        else{
            $('.waring-err').remove()
            ajaxData = false;
            $('.final-cls').prop('disabled',false)
        }
    })
    $('.taxnamecls').keyup(function() {
        var $th = $(this);
        $th.val($th.val().replace(/(\s{2,})/g, ' '));
        $th.val($th.val().replace(/^\s*/, ''));
        });

$('.final-cls').click(function(e){
    console.log({'ajaxData':ajaxData})
    if (ajaxData){
e.preventDefault();
}
})
