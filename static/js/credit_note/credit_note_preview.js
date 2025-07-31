var credit_id=$('#pk').val()  
var scheme=$('#scheme').val()
var gethost=$('#gethost').val()
var currentdomain=scheme+'://'+gethost


$(document).ready(function(){
    $('.inv_file:first').click();
})


$(document).on('click','.inv_file',function(){
    $('.inv_file').removeClass('inv-high-cls')
    var inv_name=$(this).closest('tr').find('.inv_name').text()
    $('.hd-inv').text(inv_name)
    var url=$(this).attr('value')
    if (url != ''){
        $(this).addClass('inv-high-cls')
        // var setfullurl=currentdomain+'/media/'+url+'#toolbar=0'
        var setfullurl= url.slice((url.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${url}` : `${currentdomain}/media/${url}`

        // console.log(setfullurl)
        $('.doc_invhidcls').attr({'src':setfullurl,height:'590px !important'})
    }
    else{
        $('.doc_invhidcls').attr({'src':''})
    }

})

$(document).on('click','.commonbtn',function(){
    $('.commonbtn').removeClass('support_high-cls')
    $('.invcls').removeClass('support_high-cls')
    $('.doc_selinvhidcls').attr('src','')
    var val=$(this).attr('dataid')
    $(this).addClass('support_high-cls')
    var gettext=$(this).text()
    // console.log(gettext)
    $.ajax({
            type:"GET",
            data:{'support_id':val,'credit_id':credit_id},
            url:'/credit/getsupportfiles',
            success: function(data){
                // console.log(data)

                var html="" 
                if (val == "8"){
                    if (data.filecount > 1){
                        $(data.files).each(function(index,value){
                            // alert(value.file)
                            remove_name=(value.file).replace("creditdocuments/","")
                            // alert(remove_name)
                            html +='<div class="fil-cls file-style">'+remove_name+'</div>'
                        })
                    }
                    else if (data.filecount == 1){
                        $('.doc_selinvhidcls').attr('src','')
                        var setfullurl=""
                        $(data.files).each(function(index,value){
                            // setfullurl=currentdomain+'/media/'+value.file+'#toolbar=0'
                            setfullurl= value.file.slice((value.file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${value.file}` : `${currentdomain}/media/${value.file}`

                        })
                        $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'})  
                    }
                    else{
                        html +='<div class="file-style">No Files in '+gettext+'</div>'
                    }}
                else if (val == "9"){
                    // $('.doc_selinvhidcls').attr('src','')
                    // // var setfullurl=currentdomain+'/media/'+data.con_file+'#toolbar=0'
                    // var setfullurl= data.con_file.slice((data.con_file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${data.con_file}` : `${currentdomain}/media/${data.con_file}`

                    // $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'}) 

                    if(data.contracttype != 'original'){
                        if (data.con_file.length > 1){
                            console.log('length > 1')
                            $(data.con_file).each(function(index,value){
                                remove_name=(value.original_file_name).replace("creditdocuments/","")
                                html +='<div class="inv-cls file-style">'+remove_name+'</div>'
                            })
                        }                    
                    }
                    else{

                    // $('.doc_selinvhidcls').attr('src','')
                    // // var setfullurl=currentdomain+'/media/'+data.con_file+'#toolbar=0'
                    // var setfullurl= data.con_file.slice((data.con_file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${data.con_file}` : `${currentdomain}/media/${data.con_file}`
                    // $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'}) 
                        $(data.con_file).each(function(index,value){
                            // html +='<div class="confile-cls file-style" type='+index+'>'+value.original_file_name+'</div>'    
                            remove_name=(value.original_file_name).replace("creditdocuments/","")    
                            html +='<div class="inv-cls file-style">'+remove_name+'</div>'
                        })
                    }
                }
                else if (val == "10"){
                    // $('.doc_selinvhidcls').attr('src','')
                    // // var setfullurl=currentdomain+'/media/'+data.price_file+'#toolbar=0'
                    // var setfullurl=currentdomain+'/media/'+data.price_file+''
                    // var setfullurl= data.price_file.slice((data.price_file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${data.price_file}` : `${currentdomain}/media/${data.price_file}`

                    // $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'}) 
                    if(data.contracttype != 'original'){
                        if (data.price_file.length > 1){
                            $(data.price_file).each(function(index,value){
                                remove_name=(value.original_file_name).replace("creditdocuments/","")    
                                html +='<div class="inv-cls file-style">'+remove_name+'</div>'
                                
                            })
                        }
                    }
                    else{
                        // $('.doc_selinvhidcls').attr('src','')
                        // // var setfullurl=currentdomain+'/media/'+data.price_file+'#toolbar=0'
                        // var setfullurl= data.price_file.slice((data.price_file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${data.price_file}` : `${currentdomain}/media/${data.price_file}`

                        // $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'}) 
                        $(data.price_file).each(function(index,value){
                            // html +='<div class="confile-cls file-style" type='+index+'>'+value.original_file_name+'</div>'    
                            remove_name=(value.original_file_name).replace("creditdocuments/","")    
                            html +='<div class="inv-cls file-style">'+remove_name+'</div>'
                        })
                    }
                }
                else{
                    if (data.filecount > 1){
                        $(data.files).each(function(index,value){
                            remove_name=(value.support_file).replace("creditdocuments/","")
                            html +='<div class="fil-cls file-style">'+remove_name+'</div>'
                        })
                    }
                    else if (data.filecount == 1){
                        $('.doc_selinvhidcls').attr('src','')
                        var setfullurl=""
                        $(data.files).each(function(index,value){
                            // setfullurl=currentdomain+'/media/'+value.support_file+'#toolbar=0'
                            setfullurl= value.support_file.slice((value.support_file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${value.support_file}` : `${currentdomain}/media/${value.support_file}`


                        })
                        $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'})  
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
    // var setfullurl=currentdomain+'/media/creditdocuments/'+file+'#toolbar=0'
    var setfullurl= file.slice((file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/creditdocuments/${file}` : `${currentdomain}/media/creditdocuments/${file}`
    $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'})
})

$(document).on('click','.inv-cls',function(){
    
    $('.fil-cls').removeClass('sel-file-cls')
    $(this).addClass('sel-file-cls')
    $('.doc_selinvhidcls').attr('src','')
    var file=$(this).text()
    // var setfullurl=currentdomain+'/media/creditdocuments/'+file+'#toolbar=0'
    var setfullurl= file.slice((file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/invoicedocuments/${file}` : `${currentdomain}/media/invoicedocuments/${file}`
    $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'})
})
function cleanFileName(fileName) {
    return fileName.replace(/[^.-\w\s]/gi, '').replace(/\s+/g, '_');
}
$(document).on('click','.invcls',function(){
    var invoice_id=$(this).attr('data_id')
    $('.commonbtn').removeClass('support_high-cls')
    $('.invcls').removeClass('support_high-cls')
    $('.doc_selinvhidcls').attr('src','')
    $(this).addClass('support_high-cls')
    $.ajax({
        type:"GET",
        data:{'invoice_id':invoice_id},
        url:'/credit/getinvoicefiles',
        success: function(data){
            console.log(data)
            var html='';
            if (Object.values(data.file_names_and_support).includes('1')) {
                html += '<h5><b>Invoice Files</b></h5>';
                Object.entries(data.file_names_and_support).forEach(([fileName, supportId]) => {
                    if (supportId === '1') {
                        var remove_name = fileName.replace("invoicedocuments/", "");
                        html += '<div class="invfil-cls file-style">' + remove_name + '</div>';
                    }
                });
            }
            if (Object.values(data.file_names_and_support).some(supportId => supportId !== '1')) {
                html += '<h5><b>Invoice Supporting Documents</b></h5>';
                Object.entries(data.file_names_and_support).forEach(([fileName, supportId]) => {
                    if (supportId !== '1') {
                        var remove_name = fileName.replace("invoicedocuments/", "");
                        html += '<div class="invfil-cls file-style">' + remove_name + '</div>';
                    }
                });
            }
            // html +='<h5><b>Invoice Files</b><h5>'
            // $(data.file_name).each(function(index,value){
            //     // $(value).each(function(index1,value1){
            //         // alert(value)
            //         // setfullurl=cleanFileName(value)
            //         // alert(setfullurl)
            //         remove_name=(value).replace("invoicedocuments/","")
            //         // alert(remove_name)
            //         html +='<div class="invfil-cls file-style">'+remove_name+'</div>'
            //     // })
            // })
            // if (data.file_name.length > 0){
            //     html +='<h5><b>Invoice Supporting Documents</b><h5>'
            //     $(data.file_name).each(function(index,value){
            //         // $(value).each(function(index1,value1){
            //             // setfullurl=cleanFileName(value)
            //             remove_name=(value).replace("invoicedocuments/","")
            //             html +='<div class="invfil-cls file-style">'+remove_name+'</div>'
            //         // })
            //     })
                
            // }
            $('.show_file_cls').html(html)
        }
    })

})

$(document).on('click','.invfil-cls',function(){
    $('.invfil-cls').removeClass('sel-file-cls')
    $(this).addClass('sel-file-cls')
    $('.doc_selinvhidcls').attr('src','')
    var file=$(this).text()
    // var setfullurl=currentdomain+'/media/invoicedocuments/'+file+'#toolbar=0'
    var setfullurl= file.slice((file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/invoicedocuments/${cleanFileName(file)}` : `${currentdomain}/media/invoicedocuments/${cleanFileName(file)}`
    $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'})
})
