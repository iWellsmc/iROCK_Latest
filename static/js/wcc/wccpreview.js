$(document).ready(function(){
  
    $('.inv_file:first').click()
})
$(document).on('click','.inv_file',function(){
    $('.inv_file').removeClass('inv-high-cls')
    var inv_name=$(this).closest('tr').find('.inv_name').text()
    $('.hd-inv').text(inv_name)
    var url=$(this).attr('value')
    $(this).addClass('inv-high-cls')
    // var setfullurl=currentdomain+'/media/wccfile/'+url+'#toolbar=0'
    //var setfullurl=currentdomain+'/media/wccfile/'+url+''
    var setfullurl= url.slice((url.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${url}` : `${currentdomain}/media/${url}`
    // console.log(setfullurl)
    $('.doc_invhidcls').attr({'src':setfullurl,height:'590px !important'})
})

$(document).on('click','.commonbtn',function(){
    $('.commonbtn').removeClass('support_high-cls')
    $('.doc_selinvhidcls').attr('src','')
    var val=$(this).attr('dataid')
    $(this).addClass('support_high-cls')
    var gettext=$(this).text()
    // console.log(gettext)
    $.ajax({
            type:"GET",
            data:{'supportid':val,'wcc_id':wcc_id},
            url:'/wcc/getsupportfiles',
            success: function(data){
                console.log({'getsupportfiles':data})
                var html="" 
                if (val == "9"){
                    if(data.contracttype != 'original'){
                        if (data.con_file.length > 1){
                            $(data.con_file).each(function(index,value){
                                if (value.amendment_addendum_id != null){
                                    html +='<div class="confile-cls file-style" type='+1+'>Amendment/Addendum : '+value.original_file_name+'</div>'
                                }
                                else{
                                    html +='<div class="confile-cls file-style" type='+2+'>Original Contract : '+value.original_file_name+'</div>'
                                }
                            })
                        }                    
                    }
                    else{
                        // $('.doc_selinvhidcls').attr('src','')
                        // var setfullurl= data.con_file.slice((data.con_file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${data.con_file}` : `${currentdomain}/media/${data.con_file}`

                        // $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'}) 
                        $(data.con_file).each(function(index,value){
                            html +='<div class="confile-cls file-style" type='+index+'>'+value.original_file_name+'</div>'    
                        })

                    }
                }
                else if (val == "10"){
               
                    if(data.contracttype != 'original'){
                        if (data.price_file.length > 1){
                            console.log('length > 1')
                            $(data.price_file).each(function(index,value){
                                if (value.amendment_addendum_id != null){
                                    html +='<div class="confile-cls file-style" type='+1+'>Amendment/Addendum : '+value.original_file_name+'</div>'
                                    }
                                    else{
                                    html +='<div class="confile-cls file-style" type='+2+'>Original Price Table : '+value.original_file_name+'</div>'
                                    }
                            })
                        }
                    }
                    else{
                        // $('.doc_selinvhidcls').attr('src','')
                        // // var setfullurl=currentdomain+'/media/'+data.price_file+'#toolbar=0'
                        // var setfullurl= data.price_file.slice((data.price_file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${data.price_file}` : `${currentdomain}/media/${data.price_file}`
    
                        // $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'}) 
                        $(data.price_file).each(function(index,value){
                            html +='<div class="confile-cls file-style" type='+index+'>'+value.original_file_name+'</div>'
                          
                        })
                    } 
                }
                else{
                    if (data.filecount > 1){
                        $(data.files).each(function(index,value){
                            let remove_name1 = value.wcc_support_file.replace("wccfile/", "");
                            let remove_name = value.wcc_support_file_name.replace("wccfile/", "");
                            html += `<div class="fil-cls file-style" data-id="${remove_name1}" type="${value.type}">${remove_name}</div>`;
                        });
                    }
                    else if (data.filecount == 1){
                        $('.doc_selinvhidcls').attr('src','')
                        var setfullurl=""
                        $(data.files).each(function(index,value){
                            //var setfullurl=currentdomain+'/media/'+value.wcc_support_file+'#toolbar=0'
                            setfullurl= value.wcc_support_file.slice((value.wcc_support_file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${value.wcc_support_file}` : `${currentdomain}/media/${value.wcc_support_file}`
                            console.log({'setfullurl':setfullurl})
                            $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'})  
                        })
                    }
                    else{
                        html +='<div class="file-style">No Files in '+gettext+'</div>'
                    }
                }
                console.log('html',html)
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
    new_file=$(this).attr('data-id')
    if (type == 1){
        new_file=new_file.replace("Amendment/Addendum : ","")
    }
    else{
        new_file=new_file.replace("Original Contract : ","")
    }
    // var setfullurl=currentdomain+'/media/wccfile/'+file+'#toolbar=0'
    var setfullurl= new_file.slice((new_file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/wccfile/${new_file}` : `${currentdomain}/media/wccfile/${new_file}`

    $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'})
})
$(document).on('click','.confile-cls',function(){
    $('.confile-cls').removeClass('sel-file-cls')
    $(this).addClass('sel-file-cls')
    $('.doc_selinvhidcls').attr('src','')
    var file=$(this).text()
    let type=$(this).attr('type')
    if (type == 1){
        file=file.replace("Amendment/Addendum : ","")
    }
    else{
        file=file.replace("Original Contract : ","")
        file=file.replace("Original Price Table : ","")
    }
    file = file.replace(/[()]/g, '');
    // var setfullurl=currentdomain+'/media/wccfile/'+file+'#toolbar=0'
    var setfullurl = file.slice((file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${encodeURIComponent(currentdomain + "/media/" + file.replace(/ /g, "_"))}` : `${currentdomain}/media/${file}`;
    $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'})
})
