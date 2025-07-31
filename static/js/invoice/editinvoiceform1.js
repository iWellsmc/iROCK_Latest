
$(window).keydown(function(event){
    if(event.keyCode == 13) {
    event.preventDefault();
    return false;
    }
});


$(document).ready(function(){
    var blockoption='';
    var hdnblock=$('#hdnblock').val()
    var hdnfield=$('#hdnfield').val()
    var hdnwell=$('#hdnwell').val()
    var hdn_block_not=$('#id_block_not').val()
    var hdn_field_not=$('#id_field_not').val()
    var hdn_well_not=$('#id_well_not').val()
    var hdncontractid=$('#id_hdncontractid').val()
    // console.log(hdnblock)
    
        if (hdncontractid != ''){
            // alert('')
        $.ajax({
            type:"GET",
            url:'/invoice/getprojectblock',
            data:{'projectid':projectid},
            async:false,
            success: function(data){
                blockoption +='<option value="" dataid="">--Select Block--</option>'
                blockoption +='<option value="" dataid="Not Applicable">Not Applicable</option>'
                $.each(data.data,function(key,val){
                    blockoption +='<option dataid='+val.id+' value="'+val.id+'">'+val.blockname+'</option>'
                })
                $('#id_block').html(blockoption)
                if (hdn_block_not != ''){

                    if (hdnblock == ""){
                        $('#id_block option[value=""]').attr("selected", "selected");
                    }
                    else{
                        // $('#id_block').html(blockoption)

                        $('#id_block option[value='+hdnblock+']').attr("selected", "selected");  
                    }
                    // $("<input>").attr({name:"block",type: "hidden",value: hdnblock}).appendTo("form");

                }
                if (hdn_block_not != ''){
                    $.ajax({
                    type:"GET",
                    data:{'projectid':projectid,'blockid':hdnblock},
                    url:'/projects/projectcreationfield',
                    async:false,
                    success: function(data){
                        // console.log('1',data)
                        var fieldata='<option value="" dataid="">--Select Field--</option>'
                        fieldata +='<option value="" dataid="Not Applicable">Not Applicable</option>'
                        $.each(data.field,function(key,val){
                            if (val.field != 'Not Applicable'){
                                fieldata +='<option value="'+val.id+'" dataid="'+val.id+'">'+val.field+'</option> '
                            }
                        })
                        // console.log('a',data)
                        // console.log(fieldata)
                        $('#id_field').html(fieldata)
                        if (hdn_field_not != ''){
                            if (hdnfield == ""){
                                
                                $('#id_field option[value=""]').attr("selected", "selected");
                            }
                            else{
                                // $('#id_field').html(fieldata)
                                $('#id_field option[value='+hdnfield+']').attr("selected", "selected");  
                            }
                            // $("<input>").attr({name:"field",type: "hidden",value: hdnfield}).appendTo("form");
                        }  
                        }
                    })
                }
                // var block="";
                    // block +='<option value="" dataid="Not Applicable">Not Applicable</option>'
                    // $('#id_field').html(block)
                    // $('#id_field option[value=""]').attr("selected", "selected");
                    //ar blockid=$("#id_block").find(':selected').attr('dataid')
                    if (hdn_field_not != ''){
                        if (hdnblock == ""){
                            block="Not Applicable"
                        }
                        else{
                            block=hdnblock
                        }
                        if (hdnfield == ""){
                            field="Not Applicable"
                        }
                        else{
                            field=hdnfield
                        }
                        $.ajax({
                            type:"GET",
                            data:{'projectid':projectid,'fieldid':field,"blockid":block},
                            url:'/invoice/getallwell',
                            async:false,
                            success: function(data){
                            //   console.log('av',data)
                            var well ='<option value="" dataid="">--Select Well--</option>'
                            well +='<option value="" dataid="Not Applicable">Not Applicable</option>'
                            $.each(data.data,function(key,val){
                                    well +='<option value="'+val.id+'" dataid="'+val.id+'">'+val.wellname+'</option> '
                                })
                            $('#id_well').html(well)
                                if (hdn_well_not != ''){
                                    if (hdnwell == ""){
            
                                        // $('#id_well').html(well)
                                        $('#id_well option[value=""]').attr("selected", "selected");
                                    }
                                    else{
                                        // $('#id_well').html(well)
                                        $('#id_well option[value='+hdnwell+']').attr("selected", "selected");
                                    }
                                    // $("<input>").attr({name:"well",type: "hidden",value: hdnwell}).appendTo("form");
                                }
                            }
                        })  
                    }
            }
        })

    }  

})

// var hdn_dateformat=$('#companydateformat').val()
// var currentdate;
// if(hdn_dateformat == ''){
//     defaultdateFormat='dd-M-yy',
//     currentdate=$.datepicker.formatDate(defaultdateFormat, new Date());

// }
// else{
//     console.log('hdn_dateformat',hdn_dateformat)
//     currentdate=$.datepicker.formatDate(hdn_dateformat, new Date());
//     console.log('currentdate',currentdate)
// }
/*
if (hdn_dateformat ==''){
    $(document).on('focus',".dateformat-cls", function(){
        $(this).datepicker({
            dateFormat: 'dd-M-yy',
            maxDate:new Date(),
            changeMonth:true,
            changeYear:true,
            yearRange: '1900:+0',
        });
      });
      
}
else{
    $(document).on('focus',".dateformat-cls", function(){
        $(this).datepicker({
            dateFormat: hdn_dateformat,
            maxDate:new Date(),
            changeMonth:true,
            changeYear:true,
            yearRange: '1900:+0',
        });
      });

}
*/

$(document).ready(function(){
    
    var hdncontractid=$('#id_hdncontractid').val()
    var vend_id=$('#ven_id').val();
    var val=$('.contractcls').val()
    var contracttypes=$('#costContracttype').val();
    var contractids=$('#costContractid').val();
    // console.log(hdnblock)
        if (hdncontractid != ''){
            
            $.ajax({
                type:"GET",
                data:{'contract_id':contractids,'vendor_id':vend_id,'contracttype':contracttypes},
                url:'/invoice/getcostcodeval',
                async:false,
                success: function(data){
                    // console.log('1',data)
                    var fieldata='<option value="">--Select Code--</option>'
                    $.each(data.data, function(key,val) {
                        if (val.field != 'Not Applicable'){
                            fieldata +='<option value="'+val.id+'">'+val.costcode_preview+'-'+val.costcode_string+'</option> '
                        }
                    })
                    $('#id_costcode2').html(fieldata);
                     
                },
                error: function(xhr, status, error) {
                    console.error('Error fetching cost codes:', error);
                    // Handle error condition if needed
                }
            })
        }

    })

$(document).on('click',".periodformdate-cls",function(){
    var val=$('.contractcls').val()
    console.log('asd',val)
    $(".periodtodate-cls").datepicker("destroy");
    $('.periodtodate-cls').removeClass('hasDatepicker')
    if($('.contractcls').val()=='' ){
        swal.fire('Select Contract')
    }
   })

   $(document).on('focus',".periodformdate-cls", function(){
    var current = $(this)
    var val=$('.contractcls').val()
    var dataid=$('.contractcls').find(':selected').attr('data_id')
    var vend_id=$('#ven_id').val();
    if(val != ''){
      $.ajax({
        type:"GET",
        url:'/invoice/contractdetails',
        data:{'contractid':val,'type':dataid,'vendor_id':vend_id},
        async:false,
        success: function(data){
          
            var date = new Date(data.data.contract_date);
            var cdate = date.getDate();
            var cmonth = date.getMonth() ;
            var cyear = date.getFullYear();
            $('.periodtodate-cls').val('')
            console.log('getdate--1',$('#from_date').val())
            if($('.contractcls').val()!='' ){
               current.datepicker({
                   changeMonth: true, 
                   changeYear: true,
                   showButtonPanel: true,
                   dateFormat:'dd-M-yy',
                   yearRange: '1900:' + new Date().getFullYear(),
                //    minDate: new Date(1999, 10 - 1, 25),
                   minDate: new Date(cyear,cmonth,cdate),
                   maxDate: new Date(),
                   // beforeShow: function(input,inst) {
                   //     $(input).datepicker("widget").addClass('hide-calendar');
                   // },
       
               onChangeMonthYear: function (year,month) {
                   var minusmonth = month-1
                   console.log('ak',year,month)
                  //    console.log('getdate--',$('#from_date').val())
                   $(".periodtodate-cls" ).datepicker( "destroy" );
       
                //    $('.periodtodate-cls').datepicker({
                //        // defaultDate: "+1w",
                //        dateFormat: 'dd-M-yy',
                //        showButtonPanel: true,
                //        changeMonth: true,
                //        changeYear: true,
                //        minDate: new Date(year, month-1, 01),
                //        maxDate: new Date(),
                //        // onClose: function(dateText, inst) {
                //        //     $(this).datepicker('setDate', new Date(inst.selectedYear, inst.selectedMonth, 1));
                //        //   }
                //    });
               },
               
               onClose: function(dateText, inst) {
                $(this).datepicker('widget').removeClass('hide-calendar');
            },
           })
}

}
})
}
});
$(document).on('change', '.periodformdate-cls',function() {
    var fromDateValue = $(this).val();
    var selectedDate = new Date(fromDateValue);
    // Reinitialize the second datepicker with the new selected date
    initializeDatepicker(selectedDate);
});
function initializeDatepicker(selectedDate) {
    $('.periodtodate-cls').datepicker({
        dateFormat: 'dd-M-yy',
        showButtonPanel: true,
        changeMonth: true,
        changeYear: true,
        minDate: selectedDate, // Set minDate to the selected date
        maxDate: new Date(),  // Set maxDate to today
        // Add other options if needed
    });
}

$(document).on('focus',".periodtodate-cls", function(){
    var getdata=$('.periodformdate-cls').val()
    var splitdata=getdata.split('-')
    fromdate=splitdata[0]
    current_date=fromdate.replace(/^0+/, '')
    console.log('current_date',current_date)
    var formmonth=splitdata[1]
    console.log({'formmonth':formmonth})
    var formyear=splitdata[2]
    console.log({'formyear':formyear})
    var months=new Date().getMonth()+1
    console.log({'months':months})
    var days=months+':' + new Date().getFullYear()
    // console.log(formyear)
    // console.log({'days':days})
    var minusmonth = formyear
    if($('.contractcls').val()!=' ' ){
      $(".periodtodate-cls").datepicker( {
          // defaultDate: "+1w",
          changeMonth: true,
          changeYear: true,
          showButtonPanel: true,
          dateFormat: 'dd-M-yy',
          // monthrange:formyear,
          // yearRange: '1900:' + new Date().getFullYear(),
          // monthRange:months,
          minDate: new Date(formyear, months-1,current_date),
          maxDate: new Date(),
          onChangeMonthYear: function (year,month) {
            var minusmonth = month-1
           //    console.log('getdate--',$('#from_date').val())
            $(".periodtodate-cls" ).datepicker( "destroy" );

            $('.periodtodate-cls').datepicker({
                // defaultDate: "+1w",
                dateFormat: 'dd-M-yy',
                showButtonPanel: true,
                changeMonth: true,
                changeYear: true,
                minDate: new Date(year, month-1, current_date),
                maxDate: new Date(),
                // onClose: function(dateText, inst) {
                //     $(this).datepicker('setDate', new Date(inst.selectedYear, inst.selectedMonth, 1));
                //   }
            });
        },
          beforeShow: function(input) {
            // $(input).datepicker("widget").addClass('hide-calendar');
          },
         
      })
    }
    else{
        swal.fire('Select Contract')
    }
}); 
$(document).on('change','.periodtodate-cls',function(){
  console.log('todate',$(this).val())
  console.log('fromdate',$('.periodformdate-cls').val())
   if(new Date($(this).val()) < new Date($('.periodformdate-cls').val())){
    $("#validationMessage").text('Selected date is not within the valid range')
    $(this).val('')
   }
   else{
    $("#validationMessage").text('');
   }
})

// $(document).on('focus',".periodformdate-cls", function(){
//     $('.periodtodate-cls').val('')
//     $(this).datepicker({
//         dateFormat: 'M-yyyy',
//         language: 'en',
//         range : true,
//         //minDate : mindate,
//         //maxDate : maxdate,
//         multipleDates: true,
//         multipleDatesSeparator: " - ",
//         view: 'months',
//         minView: 'months'
//         })
    /*
    $(this).datepicker( {
        changeMonth: true,
        changeYear: true,
        showButtonPanel: true,
        dateFormat: 'M-yy',
        yearRange: '1900:' + new Date().getFullYear(),
        maxDate: new Date(),
        beforeShow: function(input,inst) {
            $(input).datepicker("widget").addClass('hide-calendar');
          },
*/
        /*  onChangeMonthYear: function (year,month) {
            var minusmonth = month-1
            console.log(minusmonth)
            $(".periodtodate-cls" ).datepicker( "destroy" );

            $('.periodtodate-cls').datepicker({
                dateFormat: 'M-yy',
                showButtonPanel: true,
                changeMonth: true,
                changeYear: true,
                minDate: new Date(year, minusmonth, 01),
                maxDate: new Date(),
                onClose: function(dateText, inst) {
                    $(this).datepicker('setDate', new Date(inst.selectedYear, inst.selectedMonth, 1));
                    
                  }
            });
        }, */
        
        /*  onClose: function(dateText, inst) {
            $(this).datepicker('setDate', new Date(inst.selectedYear, inst.selectedMonth, 1));
            //$(input).datepicker('widget').removeClass('hide-calendar');
          }
    })
*/
//   });
  


//   $(document).on('focus',".periodtodate-cls", function(){

      
     /* var getdata=$('.periodformdate-cls').val()
      console.log(getdata)
      var splitdata=getdata.split('-')
      var formmonth=splitdata[0]
      var formyear=splitdata[1]
      var days=formyear+':' + new Date().getFullYear()
      console.log(formyear)
      var fromdateminDate = moment(getdata, "MMM-YYYY");
        $(this).datepicker({
            changeMonth: true,
            changeYear: true,
            showButtonPanel: true,
            dateFormat: 'M-yy',
            monthrange:0,
            yearRange:days,
            ///maxDate: new Date(),
            minDate: new Date(formyear, fromdateminDate.month(), 01),
            beforeShow: function(input){
                $(input).datepicker("widget").addClass('hide-calendar');
            },
            onClose: function(dateText, inst) {
                $(this).datepicker('setDate', new Date(inst.selectedYear, inst.selectedMonth, 1));
                $(this).datepicker('widget').removeClass('hide-calendar');
            }
        }) */
//   });
  

// old 
// $(document).on('change','.contractcls',function(){
//    /* Swal.fire({
//         text: 'Data Auto Fill?',
//         showDenyButton: true,
//         confirmButtonText: 'Yes',
//         allowOutsideClick:false,
//         denyButtonText: 'No',
//         confirmButtonColor: '#AF2B50',
//         denyButtonColor:'#AF2B50',
//         customClass: {
//         actions: 'my-actions',
//         confirmButton: 'order-2',
//         denyButton: 'order-3',
//         }
//       }).then((result) => {
//         if (result.isConfirmed) {*/

//             var val=$(this).val()
//             var data_id=$(this).find(':selected').attr('data_id')
//             var projectid=$(this).find(':selected').attr('projectid')
//             var formname = $('.formname').val()
//             if (val != ''){
//                 $('#id_block').html('<option value="" selected>--Select Block--</option>')
//                 $('#id_field').html('<option value="" selected>--Select Field--</option>')
//                 $('#id_well').html('<option value="" selected>--Select Well--</option>')
//                 $('#id_block_not').val('')
//                 $('#id_field_not').val('')
//                 $('#id_well_not').val('')
//                 $.ajax({
//                     type:"GET",
//                     url:'/invoice/contractdetails',
//                     data:{'contractid':val,'type':data_id},
//                     async:false,
//                     success: function(data){
//                         $('.nameservicecls').val(data.data.contractname)
//                         $('.types_service').val(data.data.contractservice)
//                         $('#id_hdncontractid').val(data.data.contractid+'-'+data_id)
//                     }
//                 })
//                 var hdncontractvalue=$('#id_hdncontractid').val()
//                 var splitval=hdncontractvalue.split("-")
//                 var contractid=splitval[0]
//                 $.ajax({
//                     type:"GET",
//                     url:'/invoice/getproject',
//                     data:{'contractid':contractid},
//                     async:false,
//                     success: function(data){
//                         console.log(data)
//                         $('#id_project').val(data.data.projectname)
//                         $('#id_project').attr('dataid',projectid)
//                     }
//                 })
//                 var projectid=$('#id_project').attr('dataid')
//                 var blockoption='';
//                 $.ajax({
//                     type:"GET",
//                     url:'/invoice/getprojectblock',
//                     data:{'projectid':projectid},
//                     success: function(data){
//                         console.log(data)
//                         blockoption +='<option value="" dataid="" selected>--Select Block--</option>'
//                         $.each(data.data,function(key,val){
//                             blockoption +='<option dataid='+val.id+' value="'+val.id+'">'+val.blockname+'</option>'
//                         })
//                         $('#id_block').html(blockoption)
//                     }
//                 })
    
//             }

// })

// end old code

var invoice;
var draftcount;
$(document).on('change','.contractcls',function(){
    var formname = $('.formname').val()
    var val=$(this).val()
    var current = $(this)
    var active_class_check=$(this).find('option:selected').attr('check_type')
    console.log('contractcls',val)
    var dataid=$(this).find(':selected').attr('data_id')
    var vend_id=$('#ven_id').val();
    if (val != ''){
        $('#id_block').html('<option value="" selected>--Select Block--</option>')
        $('#id_field').html('<option value="" selected>--Select Field--</option>')
        $('#id_well').html('<option value="" selected>--Select Well--</option>')
        $('#id_block_not').val('')
        $('#id_field_not').val('')
        $('#id_well_not').val('')
        $.ajax({
            type:"GET",
            url:'/invoice/contractdetails',
            data:{'contractid':val,'type':dataid,'vendor_id':vend_id,'formname':formname},
            async:false,
            success: function(data){
               var invoices_count=data.data.invoices_count
               var date = new Date(data.data.contract_date);
                let Flowdisciplinecluster=data.data.Flowdisciplinecluster
                var month = date.getMonth() + 1; 
                var year = date.getFullYear();
                invoice = parseInt(data.data.invoices_count)
                draftcount=parseInt(data.data.draft_count)
                if(Flowdisciplinecluster == false){
                    swal.fire('Approval Flow Required. Please Contact Client Administrator ')
                    current.val(' ')
                }
                else{
                if (parseInt(data.data.draft_count) > 0 ){
                    if(active_class_check == 'True'){
                    $('.nameservicecls').val(data.data.contractname)
                    $('.types_service').val(data.data.contractservice)
                    }
                    $('#id_hdncontractid').val(data.data.contractid+'-'+dataid)
                    $('#draft_id').prop('disabled',false)
                    $('#save_id').prop('disabled',false)
                    

                }
                else{
                    swal.fire('There are no Taxes,Currency Split and Payment Terms for Contract. Please contact Client or Raise a Query')
                    $('.nameservicecls').val('')
                    $('.types_service').val('')
                    $('#id_hdncontractid').val('')
                    $('#id_block').html('<option value=" " selected>--Select Block--</option>')
                    $('#id_field').html('<option value=" " selected>--Select Field--</option>')
                    $('#id_well').html('<option value=" " selected>--Select Well--</option>')
                    $('#draft_id').prop('disabled',true)
                    $('#save_id').prop('disabled',true)
                }
            }
        }
        })
        if (draftcount > 0){
            
        var hdncontractvalue=$('#id_hdncontractid').val()
        var splitval=hdncontractvalue.split("-")
        var contractid=splitval[0]
        $.ajax({
            type:"GET",
            url:'/invoice/getproject',
            data:{'contractid':contractid,'type':dataid},
            async:false,
            success: function(data){
                console.log(data)
                var get_project_name=data.data.projectname
                if(active_class_check == 'False'){
                    swal.fire(''+get_project_name+' Inactive. Please contact Client Admin')
                    current.val(' ')
                    
                }
                else{
                console.log(data)
                $('#id_project').val(data.data.projectname)
                $('#id_project').attr('dataid',data.data.id)
                $('#id_project_hdn').val(data.data.id)
                }
            }
        })
        if(active_class_check == 'True'){
        var projectid=$('#id_project').attr('dataid')
        var blockoption='';
        $.ajax({
            type:"GET",
            url:'/invoice/getprojectblock',
            data:{'projectid':projectid},
            success: function(data){
                console.log(data)
                blockoption +='<option value=" " dataid="" selected>--Select Block--</option>'
                blockoption +='<option dataid="Not Applicable" value="">Not Applicable</option>'
                $.each(data.data,function(key,val){
                    blockoption +='<option dataid='+val.id+' value="'+val.id+'">'+val.blockname+'</option>'
                })
                $('#id_block').html(blockoption)
            }
        })
    }
                                
        }
    
}

})


$(document).on('change','#id_block',function(){
    $('#id_field').html('<option value=" " dataid="" selected>--Select Field--</option>')
    $('#id_well').html('<option value =" " dataid="" selected>--Select Well--</option>')
    var blockid=$(this).find(':selected').attr('dataid')
    var projectid=$('#id_project').attr('dataid')
    var block='';
    var well="";
    $.ajax({
        type:"GET",
        data:{'projectid':projectid,'blockid':blockid},
        url:'/projects/projectcreationfield',
        success: function(data){
          console.log(data)
            if (blockid == "Not Applicable"){
                $('#id_block_not').val('Not Applicable')
                $('#id_field_not').val('')
                $('#id_well_not').val('')
                var fieldata='<option value=" " selected dataid="">--Select Field--</option>'
                fieldata +='<option dataid="Not Applicable" value="">Not Applicable</option>'
                $.each(data.field,function(key,val){
                    if (val.field != 'Not Applicable'){
                        fieldata +='<option value="'+val.id+'" dataid="'+val.id+'">'+val.field+'</option> '
                    }
                })
                $('#id_field').html(fieldata)
                well +='<option value=" " dataid="" selected>--Select Well--</option>'
                well +='<option value="" dataid="Not Applicable">Not Applicable</option>'
                $.each(data.data,function(key,val){
                    well +='<option value="'+val.id+'" dataid="'+val.id+'">'+val.wellname+'</option> '
                })
                $('#id_well').html(well)
                }
            else{
                $('#id_block_not').val('id')
                $('#id_field_not').val('')
                $('#id_well_not').val('')
                block +='<option value=" " dataid="" selected>--Select Field--</option>'
                block +='<option value="" dataid="Not Applicable" >Not Applicable</option>'
                $.each(data.field,function(key,val){
                    if (val.field != 'Not Applicable'){
                        block +='<option value="'+val.id+'" dataid="'+val.id+'">'+val.field+'</option> '
                    }
                })
                $('#id_field').html(block)
                }
        }
      })
})

$(document).on('change','#id_field',function(){
    var projectid=$('#id_project').attr('dataid')
    $('#id_well').html('<option value="" selected>--Select Well--</option>')
    var fieldid=$(this).find(':selected').attr('dataid')
    // alert(fieldid)
    var blockid=$("#id_block").find(':selected').attr('dataid')
    var well='';
    $.ajax({
        type:"GET",
        data:{'projectid':projectid,'fieldid':fieldid,'blockid':blockid},
        url:'/invoice/getallwell',
        success: function(data){
            if (fieldid == 'Not Applicable'){
                $('#id_field_not').val('Not Applicable')
                $('#id_well_not').val('')
            }
            else{
                $('#id_field_not').val('id')
                $('#id_well_not').val('')
            }
            console.log(data)
                well +='<option value=" " dataid="" selected>--Select Well--</option>'
                well +='<option value="" dataid="Not Applicable">Not Applicable</option>'
                $.each(data.data,function(key,val){
                well +='<option value="'+val.id+'" dataid="'+val.id+'">'+val.wellname+'</option> '
                })
                $('#id_well').html(well)
        }
        })

})

$(document).on('change','#id_well',function(){  
var dataid=$(this).find(':selected').attr('dataid')
if (dataid == ""){
    $('#id_well_not').val('')
}
else{
    if (dataid == 'Not Applicable'){
    $('#id_well_not').val('Not Applicable')
}
else{
    $('#id_well_not').val('id')
}
}


})  


$.validator.addMethod("checkselect", function(value, element) {
console.log(element.value)
if((element.value) == " ") {
    return false    
}
else{
    return  true
}

});


$(document).on('click','.ui-datepicker-close',function(){
$('.periodformdate-cls').nextAll('.error').remove()
var fromdate=$('.periodformdate-cls').val()
var todate=$('.periodtodate-cls').val()
if (fromdate != "" && todate == ""){
    $('.periodformdate-cls').removeClass('error')
}
else if (todate != "" && fromdate == ""){
    $('.periodtodate-cls').removeClass('error')
    $('.periodtodate-cls').nextAll('.error').remove()
}
else if (fromdate != "" && todate != "" ){
    $('.periodformdate-cls').removeClass('error')
    $('.periodtodate-cls').removeClass('error')
    $('.periodtodate-cls').nextAll('.error').remove()
}
// else{

// }
})


$('.draft-cls').click(function(e){
// alert('')
e.preventDefault()
var block=$('#id_block').find(':selected').attr('dataid')
var field=$('#id_field').find(':selected').attr('dataid')
var well=$('#id_well').find(':selected').attr('dataid')

if (block == ""){
    $('#id_block').find(':selected').val('')
}
if (field == ""){
    $('#id_field').find(':selected').val('')
    console.log($('#id_field').find(':selected').val().length)
}
if (well == ""){
    $('#id_well').find(':selected').val('')
    console.log( $('#id_well').find(':selected').val().length)
}
// $('#invoiceform1')[0].validate().currentForm = '';
$("<input>").attr({
            name: "submit_type",
            id: "hiddenId",
            type: "hidden",
            value: 0
        }).appendTo("form");

$('#editinvoiceform1')[0].submit();
// alert('a')
// console.log($(this).parents('form').submit())

})

$(document).on('click','.final-cls',function(){
$("#editinvoiceform1 ").validate({
    rules: {
        fromdate:{
            required:true,
        },
        todate:{
            required:true,
        },
        contract:{
            checkselect:true,
        },
        // contractnameservice:{
        //     required:true,
        // },
        // contractservicetype:{
        //     required:true,
        // },
        service_rendered: {
            required: true,
        },
        location_service: {
            required:true,
        },
        // project:{
        //     required:true,
        // },
        block: {
            checkselect: true,
        },
        field:{
            checkselect:true,
        },
        well:{
            checkselect:true,
        },
        costcode:{
            required:true,
        },
    },
    messages: {
        fromdate:{
            required:"This Field is Required",
        },
        todate:{
            required:"This Field is Required",
        },
        contract:{
            checkselect:"This Field is Required",
        },
        // contractservicetype:{
        //     required:"This Field is Required",
        // },
        // service_rendered: {
        //     required: "This Field is Required",
        // },
        service_rendered:{
            required:"This Field is Required",
        },
        location_service: {
            required:"This Field is Required",
        },
        // project:{
        //     required:"This Field is Required",
        // },
        block: {
            checkselect:"This Field is Required",
        },
        field:{
            checkselect:"This Field is Required",
        },
        well:{
            checkselect:"This Field is Required",
        },
        costcode:{
            required:"This Field is Required",
        },
        errorElement : 'span',
        },
    submitHandler: function(form) {
        $('#submit').attr('disabled','disabled');
        form.submit();
        $("<input>").attr({
            name: "submit_type",
            id: "hiddenId",
            type: "hidden",
            value: 1
        }).appendTo("form");
    }
})    
})
