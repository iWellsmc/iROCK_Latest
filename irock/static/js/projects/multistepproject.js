$(function (){
    var countid = false;
    var form = $("#project_create")
    form.validate({
        // errorPlacement: function errorPlacement(error, element) { element.before(error); },
        rules: {
            master_country_list: {
                required: true
            },
            project_list: {
                required: true
            },
            // projecttype: {
            //     required: true
            // }
        },
        messages: {
            master_country_list:{
                required:"Please Provide Country Name",
            },
            project_list:{
                required:"Please Provide Project Name",
            },            
            // projecttype:{
            //     required:"This Field is  Required",
            // }
        }
    });
;
    form.children("div").steps({
        headerTag: "h3",
        bodyTag: "section",
        transitionEffect: "slideLeft",
        labels: {
            finish: "Submit",
        },
        onInit: function (event, current) {
            if (current == 0){
            var $input = $('<button type="button" value="draft" class="btn btn-clr text-center pc-draft-cls">Save as Draft</button>');
            $input.insertBefore($('ul[aria-label=Pagination]'));
            }
            $('.pc-draft-cls').show();
            
            $('ul[aria-label=Pagination] li:first').addClass('intro');
        },
        onFinished: function (event, currentIndex)
        {
            console.log(form)
        
            form.submit();
        },
        onStepChanging: function (event, currentIndex, newIndex) {
         
            $('#count-err').remove()
            $('#pro-err').remove()
            $('ul[aria-label=Pagination] li:last').addClass('final-cls');
            var block_field_data=[]
            if(currentIndex==0){
                var countryid=$('#country_id').val()
                var projectid=$('#project_id').val()
                var type=$('#project_type').val()
                var html=''
                var development= ''
                var fieldenvironment_id= '';
                $('input.master_blk_cls:checkbox:checked').each(function () {
                    block_id=$(this).val()
                    block_name=$(this).next('label').text()
                    html +='<div id="block_div'+block_id+'"><label class="pd-blkname">Block Name:</label><span class="pd-blkname1">'+block_name+'</span>'
                    $('input[name="field'+$(this).val()+'"]:checkbox:checked').each(function () {
                        field_id=$(this).val()
                        field_name=$(this).next('label').text()
                        html +='<div ><label class="pd-field">Field Name:</label><span class="pd-field1">'+field_name+'</span>';
                        $('input[name="fieldenvironment-'+$(this).val()+'"]:checkbox:checked').each(function () {

                            fieldenvironment_id=$(this).val()
                            console.log(fieldenvironment_id);
                            current_element=$(this)
                            fieldenvironment_name=$(this).next('label').text()
                            html +='<div class="eye-iconview"><div><h5 class="icon-hd">Field Environment</h5><h5 class="icon-tlt">'+fieldenvironment_name+'</h5></div><a class="btn ac-editfocus" data-toggle="collapse" href="#field_env_acc'+fieldenvironment_id+'" role="button" aria-expanded="false" aria-controls="collapseExample"><span class="action-edit "><i class="fa fa-eye" style="font-size:17px; color:#95183a;"></i></span> </a></div>'
                            html +='<div  class="collapse" id="field_env_acc'+fieldenvironment_id+'"><div id="clusterdiv'+fieldenvironment_id+'" class="clusterdiv'+fieldenvironment_id+'">';
                            
                            $.ajax({
                                type: "GET",
                                url:"/projects/getfieldenvironmentcluster",
                                data: {
                                    "field_environmentid":fieldenvironment_id,
                                },
                                cache: false,
                                success: function(data)
                                {
                                    var cluster = '';
                                    console.log(data.data)
                                    var env_id=data.environmentid
                                    $.each(data.data,function(key,val){
                                        $.each(val,function(key1,val1){
                                            cluster +='<h6 class="project-clu">'+key1+'</h6>'
                                            $.each(val1,function(key2,val2){
                                                console.log(val2)
                                                cluster +='<input type="checkbox" name="cluster-'+env_id+'" data-id="'+env_id+'" class="clusterclass'+env_id+' clusters-cls" value="'+val2.id+'">&emsp;<label class="clu-subname">'+val2.cluster_subname+'</label><br>'
                                                // cluster +='<div id="discipiline_data'+fieldenvironment_id+'" class="col-12 development-cls accord-tab">'
                                                // cluster +='<div id="development-'+fieldenvironment_id+'">'
                                                // cluster +='<label for="staticEmail" class="col-12 dev-type" >Development Type</label><div class="row"><div class="col-3" id="discipline_col'+fieldenvironment_id+'-'+val2.id+'-oil"><input type="checkbox" name="development_type-'+fieldenvironment_id+'-'+val2.id+'" value="Oil_Development" data-id='+fieldenvironment_id+' clusterid='+val2.id+' data-type="Oil_Development"  class="development-type">&emsp;<label class="col-form-label-dev devel-types">Oil Development</label></div><div class="col-3" id="discipline_col'+fieldenvironment_id+'-'+val2.id+'-gas"><input type="checkbox" name="development_type-'+fieldenvironment_id+'-'+val2.id+'"  clusterid='+val2.id+' data-type="Gas_Development" value="Gas_Development"  data-id='+fieldenvironment_id+' class="development-type">&emsp;<label class="col-form-label-dev devel-types">Gas Development</label></div><div class="col-3" id="discipline_col'+fieldenvironment_id+'-'+val2.id+'-unoil"><input type="checkbox" name="development_type-'+fieldenvironment_id+'-'+val2.id+'" value="Unconventional_Oil"  clusterid='+val2.id+' data-type="Unconventional_Oil" data-id='+fieldenvironment_id+' class="development-type">&emsp;<label class="col-form-label-dev devel-types">Unconventional Oil</label></div><div class="col-3" id="discipline_col'+fieldenvironment_id+'-'+val2.id+'-ungas"><input type="checkbox" name="development_type-'+fieldenvironment_id+'-'+val2.id+'" value="Unconventional_Gas"  clusterid='+val2.id+' data-type="Unconventional_Gas" data-id='+fieldenvironment_id+' class="development-type">&emsp;<label class="col-form-label-dev devel-types">Unconventional Gas</label></div></div>'
                                                // cluster +='</div>'
                                                // cluster+='</div>'
                                            })
                                        })
                                    })

                                    $('.clusterdiv'+env_id+'').append(cluster)
                                }
                            })
                            html += '</div>'
                            //html +='<label for="staticEmail" class="col-form-label proj-dis" >Project Discipline</label><select name="project_discipline'+fieldenvironment_id+'" data-id="'+fieldenvironment_id+'" class="form-control project_dis-cls" required id="id_project_discipline"><option value="" selected>---Select Discipline---</option><option value="1">Green Field Development</option><option value="2">Brown Field Development</option><option value="3">Others</option></select>'
                            // html +='<div id="discipiline_data'+fieldenvironment_id+'" class="col-12 development-cls accord-tab">'
                            // html +='<div id="development-'+fieldenvironment_id+'">'
                            // html +='<label for="staticEmail" class="col-12 dev-type" >Development Type</label><div class="row"><div class="col-3" id="discipline_col'+fieldenvironment_id+'-oil"><input type="checkbox" name="development_type-'+fieldenvironment_id+'" value="Oil_Development" data-id='+fieldenvironment_id+' data-type="Oil_Development"  class="development-type">&emsp;<label class="col-form-label-dev devel-types">Oil Development</label></div><div class="col-3" id="discipline_col'+fieldenvironment_id+'-gas"><input type="checkbox" name="development_type-'+fieldenvironment_id+'"  data-type="Gas_Development" value="Gas_Development"  data-id='+fieldenvironment_id+' class="development-type">&emsp;<label class="col-form-label-dev devel-types">Gas Development</label></div><div class="col-3" id="discipline_col'+fieldenvironment_id+'-unoil"><input type="checkbox" name="development_type-'+fieldenvironment_id+'" value="Unconventional_Oil"  data-type="Unconventional_Oil" data-id='+fieldenvironment_id+' class="development-type">&emsp;<label class="col-form-label-dev devel-types">Unconventional Oil</label></div><div class="col-3" id="discipline_col'+fieldenvironment_id+'-ungas"><input type="checkbox" name="development_type-'+fieldenvironment_id+'" value="Unconventional_Gas"  data-type="Unconventional_Gas" data-id='+fieldenvironment_id+' class="development-type">&emsp;<label class="col-form-label-dev devel-types">Unconventional Gas</label></div></div>'
                            // html +='</div>'
                            // html+='</div>'
                            html +='</div></div>'
                            
                        });
                        
                    });
                   html +='</div>'
                });
                $('#field-form').html(html)
                if (form.validate()){
                    form.validate().settings.ignore = ":disabled,:hidden";
                    return form.valid();
                }
                else{
                    return true
                }
            }
            return true
        },

        
    });
})


/**************************************** */
/*button scroll*/ 

// $(document).on('change','input[type="checkbox"]',function(){
//     // $('.main_scroll').scrollTop($('.main_scroll')[0].scrollHeight);
//     console.log($(this))
//     if($(this)[0].checked){
//         // alert('erroe');
//         $('.main_scroll').animate({scrollTop: $('.main_scroll').height()}, 'slow'); 
        
//     }

    
// })



/*14-02-22* top scroll*/ 

 $(document).ready(function(){
    $(".scroll-top-proj").click(function() {
        $(".crt-table.main_scroll,.scroll-main-prj,html,body").animate({ 
            scrollTop: 0 
        }, "slow");
        return false;
    });
});
 





$(document).ready(function () {


    $('.intro').click(function(){
        $('.pc-draft-cls').show();
    })

    $('.pc-draft-cls').click(function(){
        $('#country_id-error').remove()
        $('#project_id-errorerror').remove()
        var countryid=$('#country_id').val()
        var projectid=$('#project_id').val()
        var form = $("#project_create")
        var type_Val;
        // if ($('#project_type').is(':checked')){
        //     type_Val =true;
        // }
        // else{
        //     type_Val =false;
        // }
        if (countryid !='' && projectid !=''){
            $(this).prop('disabled', true);
            $.ajax({
                type:"POST",
                // container:"#create-masterproject",
                url:'/projects/draftproject',
                data:form.serialize(),
                success: function(data){
                    console.log(data);
                    if (data.data="success"){
                        var current_url=$(location).attr("href")
                        var url=current_url.replace("create/","projectlist");
                        document.location.href = url;
                    }
                }
            })
        }
        else{
                $("#project_create").validate ();
                if (countryid ==''){
                    $('#count-err').remove()
                    $('#country_id').after('<span id="count-err" class="error er-left" >Please Provide Country Name</span>')
                }
                if (projectid == ''){
                    $('#pro-err').remove()
                    $('#project_id').after('<span id="pro-err" class="error er-left">Please Provide Project Name</span>')

                }
                if (type_Val == false){
                    $('#type-err').remove()
                    $('.types').after('<span id="type-err" class="error">This Field is Required</span>')
                }

            // return form.valid();
        }

        // $.ajax({
        //     type:"POST",
        //     // container:"#create-masterproject",
        //     url:'/projects/draftproject',
        //     data:form.serialize(),
        //     success: function(data){
        //         console.log(data);
        //         if (data.data="success"){
        //             var current_url=$(location).attr("href")
        //             var url=current_url.replace("create/","projectlist");
        //             document.location.href = url;
        //         }
        //     }
        // })
    })

// $(document).on('click','#project_type',function(){
//     $('#type-err').remove()
//     $('.pc-draft-cls').prop("disabled",false);

// })
    
    var field_id = [];
    var json_field={}
    // $(".lbl-field-cls").hide();
    $('#field_name_id').hide();

    $(document).on('change', '#country_id', function() {
        $('#count-err').remove()
        $('.pc-draft-cls').prop("disabled",false);
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
                    console.log(data)
                    var html=''
                    html +='<option value="">---Select Project---</option>'
                    $.each(data.projects,function (key,val) {
                        html+='<option value='+val.id+'>'+val.name+'</option>'
                    })
                    $('#project_id').html(html);
                }
        })
    })

    $(document).on('change', '#project_id', function() {
        var project_id=$(this).val();
        $('#pro-err').remove()
        $('.pc-draft-cls').prop("disabled",false);
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
                }
                else{
                    $('#development-'+envid+'-'+clusterid+'').remove()
                }
            }
        }
    })  
})

// project_discipline for development
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
                   //$('.scroll-main-prj').animate({
                   // scrollTop: $('#disciplinetype-'+environment_id+'-'+clusterid+'-'+type+'-'+value+'').offset().top
                //},2000);
                   //$('.crt-table').scrollTop(current_element.offset().top - ($('.crt-table').height()/2) );
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
                        //$(window).scrollTop($('.collapse').position().top);
                        //var w = $(window);
                        // $('.crt-table').animate({
                        //     scrollTop: $('#disciplinetype-'+environment_id+'-'+clusterid+'-'+type+'-'+value+'').offset().top
                        // },2000);
                        //$('.scroll-main-prj').scrollTop(current_element.offset().top - ($('.scroll-main-prj').height()/2) );
                        // $('#discipline_col'+environment_id+'-'+datatype+'').append(html)
                     }
                     else{
                         $('#disciplinetype-'+environment_id+'-'+clusterid+'-'+type+'-'+value+'').remove();
                     }
                }
            })
        }
        })
/* disciplinetype ends here*/
/* others sub activities*/

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
                    //$('.crt-table').scrollTop( current_element.offset().top - ($('.crt-table').height()/2) );
                }
                else{
                    $('#disciplinesubdiv'+environment_id+'-'+clusterid+'-'+type+'-'+discipline_id+'-'+value+'').remove();
                }
            }

        }
    })

})



/* discipline subtype starts */
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
                            //$('.crt-table').scrollTop( current_element.offset().top - ($('.crt-table').height()/2) );
                        }
                        else{
                            $('#well'+discipline_id+'-'+type+'-'+value  +'').remove();
                           }
                    }
                    })
        }
        else if (value == 4) {
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
                if (current_element.is(':checked')) {
                    console.log( ) 
                    current_element.parent().after(html)
                    //$('.crt-table').scrollTop( current_element.offset().top - ($('.crt-table').height()/2) );
                    // current_element.next('label').after(html)
                }
                else{
                    $('#id_disciplinesubtype-'+environment_id+'-'+clusterid+'-'+type+'-'+discipline_id+'-'+value+'').remove();
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
                            //$('.crt-table').scrollTop( current_element.offset().top - ($('.crt-table').height()/2) );
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

                            //$('.crt-table').scrollTop( current_element.offset().top - ($('.crt-table').height()/2) );

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
                console.log('asd',data)
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

                    //$('.crt-table').scrollTop( current_element.offset().top - ($('.crt-table').height()/2) );

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

/* full field development*/
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
             // $('.crt-table').scrollTop( current_element.offset().top - ($('.crt-table').height()/2) );

          }
          else{
            dataid={}
              $('#disciplinesubdiv'+environment_id+'_'+type+'_'+discipline_id+'-'+subtype+'-'+data_id+'').remove();
          }
        }
    })
})


var  dataid={}
$(document).on('change', '.wellclass', function() {

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
            console.log(data.data);
            var well_type='<div id="welltypes'+type+'-'+well_id+'-'+data_id+'" class="wellstype-wellname">'
            $.each(data.data,function(key,val){
                if (val.id in dataid){

                }
                else{
                    dataid[val.id]=0
                }
                
                well_type +='<input type="checkbox" name="welltype'+well_id+'-'+data_id+'" class="welltypes" data-id='+data_id+' value="'+val.id+'">&emsp;<label>'+val.well_subname+'</label><br>'
            })
            well_type +='</div>'

            if (current_element.is(':checked')) {
                console.log(dataid)
                current_element.parent().after(well_type)
               // $('.crt-table').scrollTop( current_element.offset().top - ($('.crt-table').height()/2) );
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
    var value=$(this).val()
    //console.log(value)
    // dataid[value]=0;
    //var count=0
    if ($(this).is(':checked')) {
        dataid[value]=dataid[value]+1; 
        //count ++;
    }
    else{
        dataid[value]=0; 
    }
    console.log(dataid);

    if (dataid[value] > 1 ){
        $(this).prop('checked', false);
        // z-=1
        Swal.fire("Well Already Checked")
    }

    var data_id=$(this).attr('data-id')

    var current_element=$(this)
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

               // $('.crt-table').scrollTop( current_element.offset().top - ($('.crt-table').height()/2) );

            }
            else {
                $('#types_subtype'+value+'-'+data_id+'').remove()
            }
        }
    })
})




//check all dis sub subtype
$(document).on('change','input[name="check_all"]',function() {
    // var subtypes=$(this).attr('subtype').split(",")
    var id=$(this).attr('data-id');
    var discipline_id=$(this).attr('discipline_id');
    var environment_id=$(this).attr('environment_id')
    var clusterid=$(this).attr('clusterid');
    var devid=$(this).attr('devid')
    // $('.dev-subdiv-class').html(' ')
    // $('.discipline_subdiv-'+devid+'-'+discipline_id+'-'+id+'').remove()
    if ($(this).is(':checked')) {
    $('.discipline_subdiv-'+devid+'-'+discipline_id+'-'+id+'').prop("checked",this.checked);
    var count=0 
    $('.discipline_subdiv-'+devid+'-'+discipline_id+'-'+id+'').each(function(){
        // $('.discipline_subdiv-'+devid+'-'+discipline_id+'-'+id+'').remove()
        // $('.discipline_subdiv-'+devid+'-'+discipline_id+'-'+id+'').prop("checked",false);
        
        var current_element=$(this)
        var data_id=$(this).attr('subtype');
        var value=$(this).val()
        console.log(value);
        //console.log('disciplinesubdiv'+environment_id+'_'+devid+'_'+discipline_id+'-'+id+'-'+value+'')
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
                html +='<div class="disc-subtype"><input type="checkbox" name="typessubtype-'+environment_id+'-'+clusterid+'-'+devid+'-'+discipline_id+'-'+id+'-'+value+'" id="types_subtype" class="types_subtype-'+clusterid+'-'+devid+'-'+value+'-'+id+' subsubtype-divison-cls" value='+val.id+'><label class="disc-left">'+val.name+ '</label></div>'
              });
                html +='<br></div>';
                console.log(count)
                if ((data.data).length > 0){
                    current_element.parent().after(html)
                   // $('.crt-table').scrollTop( current_element.offset().top - ($('.crt-table').height()/2) );

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
    // if (id=="2"){
    //     var sub_typearray=[]
    //     var field_array=[]
    //     $('.discipline_subsubtype_'+dev_name+'_'+id+'').each(function () {
    //         // arr.push();
    //        var value=$(this).val() 
    //        sub_typearray.push($(this).attr('check_text'))
    //     })
    //     $('.field_blk_cls').each(function(){
    //         if ($(this).is(':checked')){
    //             field_array.push($(this).val())
    //         }
            
    //     })
    //     console.log(field_array)
    //     $.ajax({
    //         type: "POST",
    //         url:"/projects/wellsnamelist",
    //         data: {
    //           "wells":sub_typearray,
    //           'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
    //         },
    //         cache: false,
    //         success: function(data)
    //         {

    //             var html=''
    //             console.log(data)
    //             //     $.each(data.data,function(key1,val1){

    //             //         $.each(val1,function(key2,val2){
    //             //             html +='<label>'+key2+'</label><br>'
    //             //             $.each(val2,function(key3,val3){
    //             //                 html+='<input type="checkbox" name="cluster-checkbox-'+dev_name+'-'+id+'" class="cluster_class" well="type_name" dev_name='+dev_name+' data-id='+id+' value="'+val3.id+'">&emsp;<label>'+val3.clustersubname+'</label><div id=wellsub_'+dev_name+'_'+id+'_'+val3.id+'></div>'
    //             //             })
    //             //         })
    //             // })

    //             // $.each(subtypes,function (key,val) {
    //             // $('#cluster_'+dev_name+'_'+val+'').append(html)
    //             // })
    //         }
    //     })
    //     // alert($(this).next('label').next('br').next('input').next('label').text())
    // }
    // else{

            // var arr = [];
            
            // $('.discipline_subsubtype_'+dev_name+'_'+id+'').each(function () {
            //     // arr.push();
            //    var value=$(this).val() 
            //    var environment_id=$(this).attr('environment_id')
            // //    alert(environment_id)
            //    var subtype_name=$(this).attr('check_text')
            //    html +='<div id=types_subtype_'+devid+'_'+id+'_'+value+' class="check-txt"><h4>'+develop_subname+'</h4><h5>'+subtype_name+'</h5><input id="check_all" name="check_all_types" data-id='+id+'-'+value+' type="checkbox">&emsp;<label for="check_all">All</label><br>';
            //     $.each(data.data,function(key1,val){
            //        html +='<div class="disc-subtype"><input type="checkbox" name="typessubtype-'+devid+'-'+environment_id+'-'+id+'-'+value+'" id="types_subtype" class="types_subtype-'+id+'-'+value+'" value='+val.id+'><label class="disc-left">'+val.name+ '</label></div>'
            //     })
            //     html +='</div>';
            // });
            // // $.each(subtypes,function(key,value) {
            // //     console.log(value)
            // //    
                
            // // })
            // if ((data.data).length !=0 ){
            // $("#"+devid+"").append(html);
            // // else{

            // }
            

     
    // }
    // else{
    //     $('.discipline_subsubtype_'+dev_name+'_'+id+'').prop("checked",false);
    //     $.each(subtypes,function(key,value) {
    //         console.log(value)
    //         $('#types_subtype_'+dev_name+'_'+id+'_'+value+'').remove();
    //     })
    // }
    





//
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

               // $('.crt-table').scrollTop( current_element.offset().top - ($('.crt-table').height()/2) );

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
       // $('.crt-table').scrollTop( $(this).offset().top - ($('.crt-table').height()/2) );

        // console.log('types_subtype-'+ids+'')
    }
    else{
        $('.other_subtype-'+clusterid+'-'+type+'-'+discipline_id+'-'+data_id+'').prop('checked',false);
    }
    
})

})




//well activity select all
$(document.body).on('change','input[name="check_all_welltypes"]',function() {
    var data_id=$(this).attr('data-id');
    if ($(this).is(':checked')){
        $('.types_subtype-'+data_id+'').prop('checked',this.checked);
       // $('.crt-table').scrollTop( $(this).offset().top - ($('.crt-table').height()/2) );
    }
    else {
        $('.types_subtype-'+data_id+'').prop('checked',false);
    }

})

$('#project_create').submit(function(){
    $(".final-cls", this).closest('li').remove();

    return true;
});


