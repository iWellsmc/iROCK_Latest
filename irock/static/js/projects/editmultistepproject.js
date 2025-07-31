

/*button scroll*/ 
$(document).on('change','input[type="checkbox"]',function(){
    // $('.main_scroll').scrollTop($('.main_scroll')[0].scrollHeight);
    console.log($('.main_scroll1'))
    if($(this)[0].checked){
        // alert('erroe');
    
        $('.main_scroll1').animate({scrollTop: $('.main_scroll1').height()}, 'slow'); 
        
    }

    
}) 

/*button project decription*/
// $(document).on('change','input[type="checkbox"]',function(){
//     //  $('.scroll-main-prj').scrollTop($('.scroll-main-prj')[0].scrollHeight);
//      console.log($('.scroll-main-prj1'))
//     if($(this)[0].checked){
//     //     // alert('erroe');
    
//         $('.scroll-main-prj1').animate({scrollTop: $('.scroll-main-prj1').height()}, 'slow'); 
        
//     }

    
// })


/*14-02-22* top scroll*/ 

$(document).ready(function(){
    $(".scroll-top-proj").click(function() {
        $(".crt-table1.main_scroll1,.scroll-main-prj1,html,body").animate({ 
            scrollTop: 0 
        }, "slow");
        return false;
    });
});

// $(function (){

    // var $input = $('<input type="submit" value="test" />');
    // $('.clearfix').append($input)
    // // 
    // //       $input.appendTo($('ul[aria-label=Pagination]'));

    // form.children("div").steps({
    //     headerTag: "h3",
    //     bodyTag: "section",
    //     transitionEffect: "slideLeft",
    //     onFinished: function (event, currentIndex)
    //     {
    //         console.log(form)
        
    //         form.submit();
    //     },
    //     onInit: function (event, current) {
    //         $('ul[aria-label=Pagination] li:nth-child(2)').addClass('next-cls');
    //     },
    //     onContentLoaded: function (event, currentIndex){
    //         alert(currentIndex)

    //     } ,
        // onStepChanging: function (event, currentIndex, newIndex) {
            // if (currentIndex == 0){
                // $.fn.steps.reset = function () {
                //     var wizard = this,
                //     options = getOptions(this),
                //     state = getState(this);
                //     goToStep(wizard, options, state, 0);
                  
                //     for (i = 1; i < state.stepCount; i++) {
                //       var stepAnchor = getStepAnchor(wizard, i);
                //       stepAnchor.parent().removeClass("done")._enableAria(false);
                //     }
                //   };
            // }

        // },
            
        //     var block_field_data=[]
        //     if(currentIndex==0){
        //         var html=''
        //         var fieldenvironment_id= '';


        //         $('input.master_blk_cls:checkbox:checked').each(function () {
        //             block_id=$(this).val()
        //             block_name=$(this).next('label').text()
        //             html +='<div id="block_div'+block_id+'"><label class="pd-blkname">Block Name:</label><span class="pd-blkname1">'+block_name+'</span>'
        //             $('input[name="field'+$(this).val()+'"]:checkbox:checked').each(function () {
        //                 field_id=$(this).val()
        //                 field_name=$(this).next('label').text()
        //                 html +='<div ><label class="pd-field">Field Name:</label><span class="pd-field1">'+field_name+'</span>';
        //                 $('input[name="fieldenvironment-'+$(this).val()+'"]:checkbox:checked').each(function () {

        //                     fieldenvironment_id=$(this).val()
        //                     // console.log(fieldenvironment_id);
        //                     current_element=$(this)
        //                     fieldenvironment_name=$(this).next('label').text()
        //                     html +='<div class="eye-iconview"><div><h5 class="icon-hd">Field Environment</h5><h5 class="icon-tlt">'+fieldenvironment_name+'</h5></div><a class="btn ac-editfocus getdata-cls" data-toggle="collapse" href="#field_env_acc'+fieldenvironment_id+'" role="button" aria-expanded="false" aria-controls="collapseExample"><span class="action-edit "><i class="fa fa-eye" style="font-size:17px; color:#95183a;"></i></span> </a></div>'
        //                     html +='<div  class="collapse" id="field_env_acc'+fieldenvironment_id+'"><div id="clusterdiv'+fieldenvironment_id+'" class="clusterdiv'+fieldenvironment_id+'">';
                            

        //                     $.ajax({
        //                         type: "GET",
        //                         url:"/projects/checkfieldenvironmentcluster",
        //                         data: {
        //                             "field_environmentid":fieldenvironment_id,
        //                             "projectid":projectid,
        //                         },
        //                         // async:false,
        //                         cache: false,
        //                         success: function(data)
        //                         {
        //                             var clusterarrayid1= [];
        //                             var obj={}
        //                             var arr=[]
        //                             var cluster = '';
        //                             var development;
        //                             // console.log(data.data)
        //                             var env_id=data.environmentid

        //                             $.each(data.data,function(key,val){
        //                                 $.each(val,function(key1,val1){
        //                                     cluster +='<h6 class="project-clu">'+key1+'</h6>'
        //                                     $.each(val1,function(key2,val2){
        //                                         if (val2.check == true){
        //                                             obj[fieldenvironment_id]=val2.id
        //                                             arr.push(obj)
        //                                             clusterarrayid1.push(val2.id)
        //                                             cluster +='<input type="checkbox" name="cluster-'+env_id+'" data-id="'+env_id+'" checked=checked class="clusterclass'+env_id+' clusters-cls" value="'+val2.id+'">&emsp;<label class="clu-subname">'+val2.cluster_subname+'</label><br>' 
        //                                         }
        //                                         else{
        //                                             cluster +='<input type="checkbox" name="cluster-'+env_id+'" data-id="'+env_id+'" class="clusterclass'+env_id+' clusters-cls" value="'+val2.id+'">&emsp;<label class="clu-subname">'+val2.cluster_subname+'</label><br>'
        //                                         }
        //                                     })
        //                                 })
        //                             })
        //                             // clusterids = clusterarrayid1.toString();
        //                             var development = JSON.stringify(arr);
        //                             $( "#checkclusterid-cls" ).val(development)
        //                             // alert(cluster)
        //                             $('.clusterdiv'+env_id+'').append(cluster)                                  
        //                         }
        //                     })
        //                     $(document).on('click','.getdata-cls',function(){
        //                         var cluster=$('#checkclusterid-cls').val()
        //                         clusterlist = JSON.parse(cluster);
        //                         console.log(clusterlist);
        //                         $.each(clusterlist,function(key,val){
        //                         $.each(val,function(key1,val1){
        //                             $('input[name="cluster-'+val1+'"]:checkbox:checked').each(function(){
        //                                 var clusterid=$(this).val()
        //                                 var current_element=$(this)
        //                                 var envid=key1
        //                                 var development=''
        //                                 $.ajax({
        //                                     type: "GET",
        //                                     url:'/projects/checkdevelopmenttype',
        //                                     data:{'clustersub_id':clusterid,
        //                                         'projectid':projectid},
        //                                     cache: false,
        //                                     success: function(data)
        //                                     {
        //                                         console.log((data.data).length)
        //                                         if ((data.data).length == 4){
        //                                             development+='<div id="development-'+envid+'-'+clusterid+'" class="col-12 development-cls accord-tab"><label for="staticEmail" class="col-12 dev-type" >Development Type</label><div class="row">'
        //                                             $.each(data.data,function (key,val) {
        //                                                 var dev_name=(val.development_type).replace("_"," ")
        //                                                 development+='<div class="col-3">'
        //                                                 development +='<input type="checkbox" name="development_type-'+envid+'-'+clusterid+'" clusterid="'+clusterid+'" data-id="'+envid+'" data-type="'+val.id+'" class="development-type" value="'+val.id+'">&emsp;<label class="col-form-label-dev devel-types">'+dev_name+'</label>'
        //                                                 development+='</div>'
        //                                             })
        //                                             development +='</div></div>'
        //                                             if (current_element.is(':checked')){
        //                                                 current_element.next('label').next('br').after(development)
        //                                             }
        //                                             else{
        //                                                 $('#development-'+envid+'-'+clusterid+'').remove()
        //                                             }
        //                                         }
        //                                         else if ((data.data).length == 3){
        //                                             development+='<div id="development-'+envid+'-'+clusterid+'" class="col-12 development-cls accord-tab"><label for="staticEmail" class="col-12 dev-type" >Development Type</label><div class="row">'
        //                                             $.each(data.data,function (key,val) {
        //                                                 var dev_name=(val.development_type).replace("_"," ")
        //                                                 development+='<div class="col-4">'
        //                                                 development +='<input type="checkbox" name="development_type-'+envid+'-'+clusterid+'" clusterid="'+clusterid+'" data-id="'+envid+'" data-type="'+val.id+'" class="development-type" value="'+val.id+'">&emsp;<label class="col-form-label-dev devel-types">'+dev_name+'</label>'
        //                                                 development+='</div>'
        //                                             })
        //                                             development +='</div></div>'
        //                                             if (current_element.is(':checked')){
        //                                                 current_element.next('label').next('br').after(development)
        //                                             }
        //                                             else{
        //                                                 $('#development-'+envid+'-'+clusterid+'').remove()
        //                                             }
        //                                         }
        //                                         else if ((data.data).length == 2){
        //                                             development+='<div id="development-'+envid+'-'+clusterid+'" class="col-12 development-cls accord-tab"><label for="staticEmail" class="col-12 dev-type" >Development Type</label><div class="row">'
        //                                             $.each(data.data,function (key,val) {
        //                                                 var dev_name=(val.development_type).replace("_"," ")
        //                                                 development+='<div class="col-6">'
        //                                                 if (val.check == true){
        //                                                     development +='<input type="checkbox" name="development_type-'+envid+'-'+clusterid+'" checked=checked clusterid="'+clusterid+'" data-id="'+envid+'" data-type="'+val.id+'" class="development-type" value="'+val.id+'">&emsp;<label class="col-form-label-dev devel-types">'+dev_name+'</label>'
        //                                                 }
        //                                                 else{
        //                                                     development +='<input type="checkbox" name="development_type-'+envid+'-'+clusterid+'" clusterid="'+clusterid+'" data-id="'+envid+'" data-type="'+val.id+'" class="development-type" value="'+val.id+'">&emsp;<label class="col-form-label-dev devel-types">'+dev_name+'</label>'
        //                                                 }

        //                                                 development+='</div>'
        //                                             })
        //                                             development +='</div></div>'
        //                                             if (current_element.is(':checked')){

        //                                                 current_element.next('label').next('br').after(development)

        //                                             }
        //                                             else{
        //                                                 $('#development-'+envid+'-'+clusterid+'').remove()
        //                                             }
        //                                         }
        //                                         else if ((data.data).length == 1) {
        //                                             development+='<div id="development-'+envid+'-'+clusterid+'" class="col-12 development-cls accord-tab"><label for="staticEmail" class="col-12 dev-type" >Development Type</label><div class="row">'
        //                                             $.each(data.data,function (key,val) {
        //                                                 var dev_name=(val.development_type).replace("_"," ")
        //                                                 development+='<div class="col-6">'
        //                                                 development +='<input type="checkbox" name="development_type-'+envid+'-'+clusterid+'" clusterid="'+clusterid+'" data-id="'+envid+'" data-type="'+val.id+'" class="development-type" value="'+val.id+'">&emsp;<label class="col-form-label-dev devel-types">'+dev_name+'</label>'
        //                                                 development+='</div>'
        //                                             })
        //                                             development +='</div></div>'
        //                                             if (current_element.is(':checked')){
        //                                                 current_element.next('label').next('br').after(development)
        //                                             }
        //                                             else{
        //                                                 $('#development-'+envid+'-'+clusterid+'').remove()
        //                                             }
        //                                         }
        //                                     }
        //                                 })  
        //                             //    $(this).next('label').after('<h2>hii</h2>')
        //                                 // alert($(this).val())
        //                             })
                                        
        //                         })  
        //                         })
        //                     })

        //                     html += '</div>'
        //                     html +='</div></div>'
                            
        //                 });
                        
        //             });
        //            html +='</div>'
        //         });
        //         $('#field-form').html(html)
        //     }
        //     return true
        // },
        
    // });
// })

$(document).ready(function(){
    var projectid=$('#projectid').val()

    $(document).on('click','.next-cls',function(){
        var form=$("#project_edit");
        $(this).prop('disabled', true);
        var project_id=$('#projectid').val();
        $.ajax({
            type:"POST",
            // container:"#create-masterblock",
            url:'/projects/createprojectcreation/'+project_id,
            data:form.serialize(),
            success: function(data){
                console.log(data);
                if (data.status="success"){
                    var current_url=$(location).attr("href")
                    var replace_url=current_url.replace("editproject/"+project_id+"","editprojectnextstep/"+project_id+"")
                    window.location.href = replace_url;
                }
            }
        })
    })
    
    $(document).on('click','.prev-cls',function(){
        var project_id=$(this).attr('projectid')
        var current_url=$(location).attr("href")
        var replace_url=current_url.replace("editprojectnextstep/"+project_id+"","editproject/"+project_id+"")
        window.location.href = replace_url;
    })

    $(document).on('change', '#country_id', function() {
        var country_id=$(this).val();
        $('#block_name_id').html(' ');
        $('#field_name_id').html(' ');
        $.ajax({
                type: "GET",
                url:"/projects/getmasterproject",
                data: {
                    "country_id":country_id,
                },
                cache: false,
                success: function(data)
                {
                    //console.log(data)
                    var html=''
                    html +='<option value=" " selected>---Select Project---</option>'
                    $.each(data.projects,function (key,val) {
                        html+='<option value='+val.id+'>'+val.name+'</option>'
                    })
                    $('#project_id').html(html);
                }
        })
    })

    $(document).on('change', '#project_id', function() {
        var project_id=$(this).val();
        $('#block_name_id').html(' ');
        // alert(project_id)
        $.ajax({
                type: "GET",
                url:"/projects/getprojectblock",
                data: {
                    "project_id":project_id,
                },
                cache: false,
                success: function(data)
                {
                    console.log(data)
                    var html='<label for="staticEmail" class="col-2 col-form-label-project">Block Name</label><br>'
                    $.each(data.projects,function (key,val) {
                        html+='<input type="checkbox" name="block" class="master_blk_cls" value='+val.id+'>&emsp;<label>'+val.block_name+'</label><br><div id="field_block'+val.id+'"></div>'
                    })
                    $('#block_name_id').html(html);
                } 
        })
    })

    $(document).on('change', '.master_blk_cls', function() {
        var block_id=$(this).val();
        var block_name=$(this).next('label').text();
        var current_element=$(this)
        $.ajax({
                type: "GET",
                url:"/projects/getprojectfield",
                data: {
                    "block_id":block_id,
                },
                cache: false,
                success: function(data)
                {
                    console.log((data.projects).length)
                    var html=''
                    html +='<div id=master_block-'+block_id+' class="master-block-field"><label class="col-2 col-form-label-project">Field Name</label><br>'
                    
                    $.each(data.projects,function (key,val) {
                        html+='<input type="checkbox" name="field'+block_id+'" class="field_blk_cls" block="'+block_name+'" value='+val.id+'>&emsp;<label>'+val.field_name+'</label><br><div id="field_environemnt'+val.id+'"></div>'
                    })
                    html +='</div>'
                    if (current_element.is(':checked')){
                        if ((data.projects).length> 0){
                            $('#field_block'+block_id+'').html(html);
                        }
                    }
                    else{
                        $('#master_block-'+block_id+'').remove();
                    }
                    if ($('#field_name_id').find('div').length !=0 ){
                        $('#field_name_id').show();
                      }
                      else{
                        $('#field_name_id').hide();
                        // console.log($('#field_name_id').find('div').length);
                      }
                }
        })
    })

    $(document).on('change','.field_blk_cls',function(){
        field_id=$(this).val()
        block=$(this).attr('block')
        field_name=$(this).next('label').text();
        var current_element=$(this)
        $.ajax({
            type: "GET",
            url:"/projects/getfieldenvironment",
            data: {
                "field_id":field_id,
            },
            cache: false,
            success: function(data)
            {
                console.log(data.data);
                var html=''
                html +='<div id=environment-'+field_id+' class="environement-cls"><label class="col-2 col-form-label-project">Field Environment</label><br>'
                $.each(data.data,function(key,val){
                    html +='<input type="checkbox" name="fieldenvironment-'+field_id+'" block="'+block+'" field="'+field_name+'" class="fieldenv-cls" value="'+val.id+'">&emsp;<label>'+val.project_environment+'-'+val.project_environment_subtype+'</label><br>'
                })
                html +='</div>'
                if (current_element.is(':checked')){
                    if ((data.data).length > 0){
                        $('#field_environemnt'+field_id+'').html(html)
                    }
                }
                else{
                    $('#environment-'+field_id+'').remove();
                }
            }
        })
    })

    $(document).on('change','.clusters-cls',function(){
        var envid=$(this).attr('data-id')
        var clusterid=$(this).val()
        var current_element=$(this)
        var development=''
        $.ajax({
            type: "GET",
            url:'/projects/get_development',
            data:{'clustersub_id':clusterid},
            cache: false,
            success: function(data)
            {
                // console.log((data.data).length)
                if ((data.data).length == 4){
                    development+='<div id="development-'+envid+'-'+clusterid+'" class="col-12 development-cls accord-tab"><label for="staticEmail" class="col-12 dev-type" >Development Type</label><div class="row">'
                    $.each(data.data,function (key,val) {
                        var dev_name=(val.development_type).replace("_"," ")
                        development+='<div class="col-3">'
                        development +='<input type="checkbox" name="development_type-'+envid+'-'+clusterid+'" clusterid="'+clusterid+'" data-id="'+envid+'" data-type="'+val.id+'" class="development-type" value="'+val.id+'">&emsp;<label class="col-form-label-dev devel-types">'+dev_name+'</label>'
                        development+='</div>'
                    })
                    development +='</div></div>'
                    if (current_element.is(':checked')){
                        current_element.next('label').next('br').after(development)
                    }
                    else{
                        $('#development-'+envid+'-'+clusterid+'').remove()
                    }
                }
                else if ((data.data).length == 3){
                    development+='<div id="development-'+envid+'-'+clusterid+'" class="col-12 development-cls accord-tab"><label for="staticEmail" class="col-12 dev-type" >Development Type</label><div class="row">'
                    $.each(data.data,function (key,val) {
                        var dev_name=(val.development_type).replace("_"," ")
                        development+='<div class="col-4">'
                        development +='<input type="checkbox" name="development_type-'+envid+'-'+clusterid+'" clusterid="'+clusterid+'" data-id="'+envid+'" data-type="'+val.id+'" class="development-type" value="'+val.id+'">&emsp;<label class="col-form-label-dev devel-types">'+dev_name+'</label>'
                        development+='</div>'
                    })
                    development +='</div></div>'
                    if (current_element.is(':checked')){
                        current_element.next('label').next('br').after(development)
                    }
                    else{
                        $('#development-'+envid+'-'+clusterid+'').remove()
                    }
                }
                else if ((data.data).length == 2){
                    development+='<div id="development-'+envid+'-'+clusterid+'" class="col-12 development-cls accord-tab"><label for="staticEmail" class="col-12 dev-type" >Development Type</label><div class="row">'
                    $.each(data.data,function (key,val) {
                        var dev_name=(val.development_type).replace("_"," ")
                        development+='<div class="col-6">'
                        development +='<input type="checkbox" name="development_type-'+envid+'-'+clusterid+'" clusterid="'+clusterid+'" data-id="'+envid+'" data-type="'+val.id+'" class="development-type" value="'+val.id+'">&emsp;<label class="col-form-label-dev devel-types">'+dev_name+'</label>'
                        development+='</div>'
                    })
                    development +='</div></div>'
                    if (current_element.is(':checked')){

                        current_element.next('label').next('br').after(development)
                        // $(window).scrollTop( current_element.offset().top - ($(window).height()/2) );
                    }
                    else{
                        $('#development-'+envid+'-'+clusterid+'').remove()
                    }
                }
                else if ((data.data).length == 1) {
                    development+='<div id="development-'+envid+'-'+clusterid+'" class="col-12 development-cls accord-tab"><label for="staticEmail" class="col-12 dev-type" >Development Type</label><div class="row">'
                    $.each(data.data,function (key,val) {
                        var dev_name=(val.development_type).replace("_"," ")
                        development+='<div class="col-6">'
                        development +='<input type="checkbox" name="development_type-'+envid+'-'+clusterid+'" clusterid="'+clusterid+'" data-id="'+envid+'" data-type="'+val.id+'" class="development-type" value="'+val.id+'">&emsp;<label class="col-form-label-dev devel-types">'+dev_name+'</label>'
                        development+='</div>'
                    })
                    development +='</div></div>'
                    if (current_element.is(':checked')){
                        current_element.next('label').next('br').after(development)
                        // $(window).scrollTop( current_element.offset().top - ($(window).height()/2) );
                    }
                    else{
                        $('#development-'+envid+'-'+clusterid+'').remove()
                    }
                }
            }
        })  
    })


    $(document).on('change','.development-type',function(){
        var env_id=$(this).attr('data-id')
        var type=$(this).attr('data-type')
        var clusterid=$(this).attr('clusterid')
        var html='<div id="project_dis-'+type+'-'+env_id+'-'+clusterid+'" class="check-txt">'
        html +='<label for="staticEmail" class="col-form-label proj-dis" >Project Discipline</label><br><input type="checkbox"  name="project_discipline-'+env_id+'-'+clusterid+'-'+type+'" clusterid="'+clusterid+'" data-type="'+type+'" data-id="'+env_id+'" class=" project_dis-cls"  value="1">&emsp;<label class="dev-lists">Green Field Development</label><br><input type="checkbox"  name="project_discipline-'+env_id+'-'+clusterid+'-'+type+'" clusterid="'+clusterid+'" data-type="'+type+'" data-id="'+env_id+'" class="project_dis-cls" value="2">&emsp;<label class="dev-lists">Brown Field Development</label><br><input type="checkbox"  name="project_discipline-'+env_id+'-'+clusterid+'-'+type+'" clusterid="'+clusterid+'" data-type="'+type+'" data-id="'+env_id+'" class="project_dis-cls" value="3">&emsp;<label class="dev-lists">Others</label>'
        html +='</div>'
        if ($(this).is(':checked')){
            $(this).next('label').after(html)
        }
        else{
            $('#project_dis-'+type+'-'+env_id+'-'+clusterid+'').html(' ')
        }
    
    })

    
$(document).on('change','.project_dis-cls',function(){
    var value=$(this).val();
    var environment_id=$(this).attr('data-id')
    var type=$(this).attr('data-type')
    var clusterid=$(this).attr('clusterid')
    var current_element=$(this)
    var html=''
    if (value=="3"){
        $.ajax({
            type: "GET",
            url:"/projects/disciplinesubtype",
            data: {
              "id":value,
            },
            cache: false,
            success: function(data)
            {   
                console.log(data);
                html += '<div id="disciplinetype-'+environment_id+'-'+clusterid+'-'+type+'-'+value+'" class="check-txt dis-type-cls">'
                $.each(data.data,function(key,val){
   
                    html +='<div class="disc-subtype"><input type="checkbox" name="otherdisciplinesubtype-'+environment_id+'-'+clusterid+'-'+type+'-'+value+'" clusterid="'+clusterid+'"  environment_id="'+environment_id+'" class="others_subact" data-type="'+type+'" discipline_id='+value+' value='+val.id+'>&emsp;<label >'+val.discipline_subtype+ '</label></div>'
                    });
                html+='</div>'
                if (current_element.is(':checked')){
                   current_element.next('label').after(html)
                //    $(window).scrollTop( current_element.offset().top - ($(window).height()/2) );
                   // $('#discipline_col'+environment_id+'-'+datatype+'').append(html)
                }
                else{
                    $('#disciplinetype-'+environment_id+'-'+clusterid+'-'+type+'-'+value+'').remove();
                }
            }
        })

    }else{ 
            
            $.ajax({
                type: "GET",
                url:"/projects/disciplinesubtype",
                data: {
                  "id":value,
                },
                cache: false,
                success: function(data)
                {   
                    console.log(data.data);
                    html += '<div id="disciplinetype-'+environment_id+'-'+clusterid+'-'+type+'-'+value+'" class="check-txt dis-type-cls">'
                     $.each(data.data,function(key,val){
        
                         html +='<div class="disc-subtype"><input type="checkbox" name="developmentsubtype-'+environment_id+'-'+clusterid+'-'+type+'-'+value+'" clusterid="'+clusterid+'"  environment_id="'+environment_id+'" class="projects_subtype" data-type="'+type+'" discipline_val='+value+' value='+val.id+'>&emsp;<label >'+val.discipline_subtype+ '</label></div>'
                         });
                     html+='</div>'
                     if (current_element.is(':checked')){
                        current_element.next('label').after(html)
                        // current_element.parent().after(html)
                        // $(window).scrollTop( current_element.offset().top - ($(window).height()/2) );
                        // $('.disc-subtype').scrollTop( current_element.offset().top - ($('.disc-subtype').height()/2) );
                        $(".disc-subtype").animate({top: "100px"}, 1000);
                        // $('#discipline_col'+environment_id+'-'+datatype+'').append(html)
                     }
                     else{
                         $('#disciplinetype-'+environment_id+'-'+clusterid+'-'+type+'-'+value+'').remove();
                     }
                }
            })
        }
        })


        $(document).on('change','.others_subact',function(){
            var environment_id=$(this).attr('environment_id');
            var type=$(this).attr('data-type');
            var discipline_id=$(this).attr('discipline_id')
            var clusterid=$(this).attr('clusterid')
            var value=$(this).val();
            var current_element=$(this)
            var html =' '
            $.ajax({
                type: "GET",
                url:"/projects/typessubtypes",
                data: {
                  "id":value,
                },
                cache: false,
                success: function(data)
                {   
                    console.log(data)
                    html +='<div id="disciplinesubdiv'+environment_id+'-'+clusterid+'-'+type+'-'+discipline_id+'-'+value+'"  class="check-txt dev-subdiv-class"><input type="checkbox" id="check_all" name="other_check_all_types" clusterid="'+clusterid+'" data-type="'+type+'" disciplineid="'+discipline_id+'" data-id="'+value+'" >&emsp;<label for="check_all">All</label><br>';
                    $.each(data.data,function(key,val){
                    html +='<div class="disc-subtype"><input type="checkbox" name="otherstypeactivities-'+environment_id+'-'+clusterid+'-'+type+'-'+discipline_id+'-'+value+'"  class="other_subtype-'+clusterid+'-'+type+'-'+discipline_id+'-'+value+' subsubtype-divison-cls" value='+val.id+'><label class="disc-left">'+val.name+ '</label></div>'
                    });
                        html +='<br></div>';
                    if ((data.data).length > 0){
                        if (current_element.is(':checked')){
                            current_element.parent().after(html)
                            // $(window).scrollTop( current_element.offset().top - ($(window).height()/2) );
                        }
                        else{
                            $('#disciplinesubdiv'+environment_id+'-'+clusterid+'-'+type+'-'+discipline_id+'-'+value+'').remove();
                        
                    } 
}
                }
            })
        
        })

        $(document).on('change', '.projects_subtype', function() {
            var environment_id=$(this).attr('environment_id');
            var value=$(this).val();
            var discipline_id=$(this).attr('discipline_val');
            var type=$(this).attr('data-type')
            var clusterid=$(this).attr('clusterid')
            var develop_subname=$(this).next('label').text();
            var current_element=$(this)
            // alert($(this).parent().parent().parent().parent().parent().parent().parent().find('input').val())
            var subtypearray=[]
            var subtypesarrays=[]
            if (value ==2){
                    var well=''
                    $.ajax({
                        type: "GET",
                        url:"/projects/getwell",
                        data: {
                          "development_id":type,
                        },
                        cache: false,
                        success: function(data)
                        {   
                            console.log(data.data);
                            well +='<div id="well'+discipline_id+'-'+type+'-'+value+'" class="development-wells">'
                            $.each(data.data,function(key,val){
                                console.log(val);
                                well +='<div class="disc-subtype"><input type="checkbox" name="wells-'+discipline_id+'-'+type+'-'+value+'" data-type="'+type+'" data-id='+value+' class="wellclass" value="'+val.id+'"><label class="disc-left">'+val.well_name+'</label></div>'
                            })
                            well +='</div>'
                            if (current_element.is(':checked')) {
                                current_element.parent().after(well)
                            }
                            else{
                                $('#well'+discipline_id+'-'+type+'-'+value  +'').remove();
                               }
                        }
                        })
            }
            else if (value == 6){
    
                var well=''
                $.ajax({
                    type: "GET",
                    url:"/projects/getwellbrownfield",
                    data: {
                      "development_id":type,
                    },
                    cache: false,
                    success: function(data)
                    {   
                        if (data.data){
                            console.log(data.data);
                            well +='<div id="well'+discipline_id+'-'+type+'-'+value+'" class="development-wells">'
                            well += '<div class=""><input type="checkbox" name="wellsubtype-'+discipline_id+'-'+type+'-'+value+'" clusterid="'+clusterid+'" data-type="'+type+'" environment_id="'+environment_id+'" discipline_id="'+discipline_id+'"  data-id="14" subtype="'+value+'" class="wellsub-activities-cls" value="14"><label class="disc-left">Full Field Development</label></div>'
                            $.each(data.data,function(key,val){
                                well +='<div class="disc-subtype"><input type="checkbox" name="wells-'+discipline_id+'-'+type+'-'+value+'" data-type="'+type+'" data-id='+value+' class="wellclass" value="'+val.id+'"><label class="disc-left">'+val.well_name+'</label></div>'
                            })
                            well +='</div>'
                            if (current_element.is(':checked')) {
    
                                current_element.parent().after(well)
                            }
                            else{
                                $('#well'+discipline_id+'-'+type+'-'+value  +'').remove();
                            }
                        }
                        else{
                            console.log('no values');
                        }
                    }
                    })
            }
    
            else if (value == 7) {
                var well=''
                $.ajax({
                    type: "GET",
                    url:"/projects/getwellbrownfielddrill",
                    data: {
                      "development_id":type,
                    },
                    cache: false,
                    success: function(data)
                    { 
                        if (data.data){
                            console.log(data.data);
                            well +='<div id="well'+discipline_id+'-'+type+'-'+value+'" class="development-wells">'
                            
                            $.each(data.data,function(key,val){
                                well +='<div class="disc-subtype"><input type="checkbox" name="wells-'+discipline_id+'-'+type+'-'+value+'" data-type="'+type+'" data-id='+value+' class="wellclass" value="'+val.id+'"><label class="disc-left">'+val.well_name+'</label></div>'
                            })
                            well +='</div>'
                            if (current_element.is(':checked')) {
    
                                current_element.parent().after(well)
                            }
                            else{
                                $('#well'+discipline_id+'-'+type+'-'+value  +'').remove();
                            }
                        }
                        else{
                            console.log('no values');
                        }
                    }
                })
            }
            else{
                
            $.ajax({
                type: "GET",
                url:"/projects/disciplinesubsubtypes",
                data: {
                  "id":value,
                },
                cache: false,
                success: function(data)
                {   
                    console.log(data)
                    var html='';
                    html +='<div id=id_disciplinesubtype-'+environment_id+'-'+clusterid+'-'+type+'-'+discipline_id+'-'+value+' class="check-txt dev-subsubtype-cls" data-id='+value+'><input type="checkbox" id="check_all" name="check_all" environment_id='+environment_id+' clusterid='+clusterid+'  discipline_id='+discipline_id+'  data-id='+value+' devid='+type+'>&emsp;<label for="check_all">All</label><br>';
                    $.each(data.data,function(key,val){
    
                  html +='<div class="disc-subtype"><input type="checkbox" name="disciplinesubsubtype-'+environment_id+'-'+clusterid+'-'+type+'-'+discipline_id+'-'+value+'" check_text="'+val.sub_subtype_name+'"  id="discipline_sub_subtype'+val.id+'" class="discipline_subdiv-'+type+'-'+discipline_id+'-'+value+' dev-sub-cls"  clusterid="'+clusterid+'" environment_id="'+environment_id+'" data-type="'+type+'" discipline_id="'+discipline_id+'" subtype="'+value+'"  data-id='+val.id+'  value='+val.id+' ><label class="disc-left">'+val.sub_subtype_name+ '</label></div>'
                //   html +='<div id=cluster_'+discipline_id+'_'+val.id+'></div>'
                  });
                  
                   html +='</div>';
                if ((data.data).length > 0){
                    if (current_element.is(':checked')) {
                        console.log( ) 
                        current_element.parent().after(html)
                        // $(window).scrollTop( current_element.offset().top - ($(window).height()/2) );
                        // current_element.next('label').after(html)
                    }
                    else{
                        $('#id_disciplinesubtype-'+environment_id+'-'+clusterid+'-'+type+'-'+discipline_id+'-'+value+'').remove();
                       }
                } 

                }
            })
        }
        })

/* full field*/
$(document).on('change','.wellsub-activities-cls',function(){
    var environment_id=$(this).attr('environment_id');
    var type=$(this).attr('data-type');
    var discipline_id=$(this).attr('discipline_id')
    var subtype=$(this).attr('subtype');
    var data_id=$(this).attr('data-id');
    var clusterid=$(this).attr('clusterid')
    var current_element=$(this)
    $.ajax({
        type: "GET",
        url:"/projects/typessubtypes",
        data: {
          "id":subtype,
        },
        cache: false,
        success: function(data)
        {   
            console.log(data)
            var html='';
            html +='<div id="disciplinesubdiv'+environment_id+'_'+type+'_'+discipline_id+'-'+subtype+'-'+data_id+'"  class="check-txt dev-subdiv-class"><input type="checkbox" id="check_all" name="check_all_types" clusterid="'+clusterid+'" subtype="'+subtype+'" data-id="'+data_id+'" data-type="'+type+'" >&emsp;<label for="check_all">All</label><br>';
            $.each(data.data,function(key,val){
            html +='<div class="disc-subtype"><input type="checkbox" name="wellsubtype_activity-'+environment_id+'-'+clusterid+'-'+type+'-'+discipline_id+'-'+subtype+'-'+data_id+'" id="types_subtype" class="types_subtype-'+clusterid+'-'+type+'-'+subtype+'-'+data_id+' subsubtype-divison-cls" value='+val.id+'><label class="disc-left">'+val.name+'</label></div>'
          });
            html +='<br></div>';
          if (current_element.is(':checked')){

              current_element.next('label').after(html)
            //   $(window).scrollTop( current_element.offset().top - ($(window).height()/2) );
              
          }
          else{
              $('#disciplinesubdiv'+environment_id+'_'+type+'_'+discipline_id+'-'+subtype+'-'+data_id+'').remove();
          }
        }
    })
})

var dataid={}
$(document).on('change', '.wellclass', function() {
    var wellcheckid=$(this).attr('wellcheckid')
    // alert(projectid)
    var well_id=$(this).val();
    var data_id=$(this).attr('data-id')
    var current_element=$(this)
    var type=$(this).attr('data-type')

    $.ajax({
        type: "GET",
        url:"/projects/welltype",
        data: {
          "well_id":well_id,
        },
        cache: false,
        success: function(data)
        {
            // console.log(data.data);
            var well_type='<div id="welltypes'+type+'-'+well_id+'-'+data_id+'" class="wellstype-wellname">'
            $.each(data.data,function(key,val){
                if (val.id in dataid){

                }
                else{
                    dataid[val.id]=0
                }
                well_type +='<input type="checkbox" name="welltype'+well_id+'-'+data_id+'" wellcheckid="" class="welltypes" data-id='+data_id+' value="'+val.id+'">&emsp;<label>'+val.well_subname+'</label><br>'
            })
            well_type +='</div>'
            if (current_element.is(':checked')) {
                
                current_element.parent().after(well_type)
            }
            else{
                $.ajax({
                    type: "GET",
                    url:"/projects/welltype",
                    data: {
                      "well_id":well_id,
                    },
                    cache: false,
                    success: function(data)
                    {
                        $.each(data.data,function(key,val){
                            if(val.id in dataid){
                                // if (dataid[val.id] >1 ){
                                //     dataid[val.id]=1
                                // }
                                // else if(dataid[val.id] == 1){
                                //     dataid[val.id]=0
                                // }
                                dataid[val.id]=0 
                            }
                        })
                        console.log(dataid) 
                    }
                    
                })
                 
                //$.each(dataid,function(key,val){
                    //if(val == 2){
                     //   dataid[key]=1
                   // }
                   // else{
                //        dataid[key]=0
                   // }

                //})

                // dataids = $.map( dataid, function( value, index ) {
                //     return value *  2 ;
                //   });

                $('#welltypes'+type+'-'+well_id+'-'+data_id+'').remove();
               }
        }
        })

    
    
})




var z=0
$(document).on('change', '.welltypes', function() {
    var wellcheckid=$(this).attr('wellcheckid')
    // alert(wellcheckid)
    var value=$(this).val()
    var current_element=$(this)
    var apppenddata = true;
    if ($(this).is(':checked')) {
        dataid[value]=dataid[value]+1; 
    }
    else{
        dataid[value]=0;
    }
    console.log(dataid);

    if (dataid[value] > 1 && !NaN){
        $(this).prop('checked', false);
        // z-=1
        Swal.fire("Well Already Checked")
    }

    if ( wellcheckid =='' || wellcheckid ==' '){
        console.log('no val')
        $.ajax({
        type: "GET",
        url:"/projects/welldupcheck",
        data: {
          "well_id":value,
          "projectid":projectid,
          "wellcheckid":wellcheckid,
        },
        cache: false,
        success: function(data)
        {
            console.log(data)
                if (data.data =="exists"){
                    current_element.prop('checked', false);
                    Swal.fire("Well Already Checked")
                    apppenddata = data.status;
                }
                else{
                    apppenddata = data.status;
                }
                // alert(apppenddata)
        }
    })
    }
    else{
        // alert(wellcheckid)
            $.ajax({
            type: "GET",
            url:"/projects/welldupcheck",
            data: {
            "well_id":value,
            "projectid":projectid,
            "wellcheckid":wellcheckid,
            },
            cache: false,
            success: function(data)
            {
                console.log(data)
                current_element.attr('wellchecked',' ');
                // current_element.removeAttr(" ");
            }
        })
    }
// else{

// }


    
    var data_id=$(this).attr('data-id')
    // alert(apppenddata)
    if (apppenddata == true){
        $.ajax({
            type: "GET",
            url:"/projects/typessubtypes",
            data: {
              "id":data_id,
            },
            cache: false,
            success: function(data)
            {   
                var html=''
                html +='<div id=types_subtype'+value+'-'+data_id+' class="well-activity-cls"><input id="check_all" name="check_all_welltypes" data-id='+value+' type="checkbox">&emsp;<label for="check_all">All</label><br>';
                $.each(data.data,function(key1,val){
                   html +='<div class="disc-subtype"><input type="checkbox" name="typessubtype-'+value+'-'+data_id+'" id="types_subtype" class="types_subtype-'+value+'" value='+val.id+'><label class="disc-left">'+val.name+ '</label></div>'
                })
                html +='</div>';
                if (current_element.is(':checked')){
                    current_element.next('label').after(html)
                    
                }
                else {
                    $('#types_subtype'+value+'-'+data_id+'').remove()
                }
            }
        })
    }

})


//check all dis sub subtype
$(document).on('change','input[name="check_all"]',function() {
    // var subtypes=$(this).attr('subtype').split(",")
    var id=$(this).attr('data-id');
    var discipline_id=$(this).attr('discipline_id');
    var environment_id=$(this).attr('environment_id')
    var clusterid=$(this).attr('clusterid');
    var devid=$(this).attr('devid')

    if ($(this).is(':checked')) {
    $('.discipline_subdiv-'+devid+'-'+discipline_id+'-'+id+'').prop("checked",this.checked);
    var count=0 
    $('.discipline_subdiv-'+devid+'-'+discipline_id+'-'+id+'').each(function(){
        // $('.dev-subdiv-class').remove()
        // $('.discipline_subdiv-'+devid+'-'+discipline_id+'-'+id+'').prop("checked",this.checked);
        
        var current_element=$(this)
        var data_id=$(this).attr('subtype');
        var value=$(this).val()
        $('#disciplinesubdiv'+environment_id+'_'+devid+'_'+discipline_id+'-'+id+'-'+value+'').remove()
        $.ajax({
            type: "GET",
            url:"/projects/typessubtypes",
            data: {
            "id":data_id,
            },
            cache: false,
            success: function(data)
            {  
                count += 1;
                
                console.log(data);
                var html=''
                html +='<div id="disciplinesubdiv'+environment_id+'_'+devid+'_'+discipline_id+'-'+id+'-'+value+'"  class="check-txt dev-subdiv-class"><input type="checkbox" id="check_all" name="check_all_types" clusterid="'+clusterid+'" subtype="'+value+'" data-id="'+id+'" data-type="'+devid+'" >&emsp;<label for="check_all">All</label><br>';
                $.each(data.data,function(key,val){
                html +='<div class="disc-subtype"><input type="checkbox" name="typessubtype-'+environment_id+'-'+clusterid+'-'+devid+'-'+discipline_id+'-'+value+'-'+id+'" id="types_subtype" class="types_subtype-'+clusterid+'-'+devid+'-'+value+'-'+id+' subsubtype-divison-cls" value='+val.id+'><label class="disc-left">'+val.name+ '</label></div>'
              });
                html +='<br></div>';
                console.log(count)
                if ((data.data).length > 0){
                current_element.parent().after(html)
                // $(window).scrollTop( current_element.offset().top - ($(window).height()/2) );
                }
            }
            })
    });
    }
    else{
        $('.discipline_subdiv-'+devid+'-'+discipline_id+'-'+id+'').prop("checked",false);
        $('.discipline_subdiv-'+devid+'-'+discipline_id+'-'+id+'').each(function(){
            var data_id=$(this).attr('subtype');
            var value=$(this).val()
            $('#disciplinesubdiv'+environment_id+'_'+devid+'_'+discipline_id+'-'+id+'-'+value+'').remove()
        })
    }
})


$(document).on('change','.dev-sub-cls',function() {
    var environment_id=$(this).attr('environment_id');
    var type=$(this).attr('data-type');
    var discipline_id=$(this).attr('discipline_id')
    var subtype=$(this).attr('subtype');
    var data_id=$(this).attr('data-id');
    var clusterid=$(this).attr('clusterid')
    var value=$(this).val();
    var current_element=$(this)
    var field_array=[]
    $('.field_blk_cls').each(function(){
        if ($(this).is(':checked')){
            field_array.push($(this).val())
        }
        
    })
    console.log(field_array)
    $.ajax({
        type: "GET",
        url:"/projects/typessubtypes",
        data: {
          "id":subtype,
        },
        cache: false,
        success: function(data)
        {   
            console.log(data)
            var html='';
            html +='<div id="disciplinesubdiv'+environment_id+'_'+type+'_'+discipline_id+'-'+subtype+'-'+data_id+'"  class="check-txt dev-subdiv-class"><input type="checkbox" id="check_all" name="check_all_types" clusterid="'+clusterid+'" subtype="'+subtype+'" data-id="'+data_id+'" data-type="'+type+'" >&emsp;<label for="check_all">All</label><br>';
            $.each(data.data,function(key,val){
            html +='<div class="disc-subtype"><input type="checkbox" name="typessubtype-'+environment_id+'-'+clusterid+'-'+type+'-'+discipline_id+'-'+subtype+'-'+data_id+'" id="types_subtype" class="types_subtype-'+clusterid+'-'+type+'-'+subtype+'-'+data_id+' subsubtype-divison-cls" value='+val.id+'><label class="disc-left">'+val.name+ '</label></div>'
          });
            html +='<br></div>';
            if ((data.data).length > 0){
          if (current_element.is(':checked')){
            current_element.parent().after(html)
            // $(window).scrollTop( $(this).offset().top - ($(window).height()/2) );
            //   current_element.next('label').after(html)
          }
          else{
              $('#disciplinesubdiv'+environment_id+'_'+type+'_'+discipline_id+'-'+subtype+'-'+data_id+'').remove();
          }
        }
        }
    })
    
})
$(document.body).on('change','input[name=check_all_types]',function() {
    // alert("sdfdf")
    var clusterid=$(this).attr('clusterid')
    var type=$(this).attr('data-type');
    var subtype=$(this).attr('subtype');
    var data_id=$(this).attr('data-id');
    if ($(this).is(':checked')){
        $('.types_subtype-'+clusterid+'-'+type+'-'+subtype+'-'+data_id+'').prop('checked',this.checked);
        // console.log('types_subtype-'+ids+'')
    }
    else{
        $('.types_subtype-'+clusterid+'-'+type+'-'+subtype+'-'+data_id+'').prop('checked',false);
    }
    
})

//others development all 
$(document.body).on('change','input[name=other_check_all_types]',function() {
    var clusterid=$(this).attr('clusterid')
    var type=$(this).attr('data-type');
    var discipline_id=$(this).attr('disciplineid');
    var data_id=$(this).attr('data-id');
    if ($(this).is(':checked')){
        $('.other_subtype-'+clusterid+'-'+type+'-'+discipline_id+'-'+data_id+'').prop('checked',this.checked);
        // console.log('types_subtype-'+ids+'')sss
        // $(window).scrollTop( $(this).offset().top - ($(window).height()/2) );
    }
    else{
        //alert('other_subtype-'+clusterid+'-'+type+'-'+discipline_id+'-'+data_id+'')
        $('.other_subtype-'+clusterid+'-'+type+'-'+discipline_id+'-'+data_id+'').prop('checked',false);
    }
    
})

$(document.body).on('change','input[name="check_all_welltypes"]',function() {
    var data_id=$(this).attr('data-id');
    if ($(this).is(':checked')){
        $('.types_subtype-'+data_id+'').prop('checked',this.checked);
    }
    else {
        $('.types_subtype-'+data_id+'').prop('checked',false);
    }

})



$('#projectstep_edit').submit(function()
 {
    $(".final_submit_cls", this)
      .val("Please Wait...")
      .attr('disabled', 'disabled');

    return true;
  });
})