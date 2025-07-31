$(document).ready(function(){
    var projectwise_chart
    $('#countries').select2({
        placeholder: "Countries",
    })
    $('#projects').select2({
        placeholder: "Projects",
    })
    $('#services').select2({
        placeholder: "Servics",
    })
    $('#currencies').select2({
        placeholder: "Currencies",
    })
    $('#tax').select2({
        placeholder: "Tax",
    })
    $.ajax({
        type:"GET",
        url:'/dashboard/getcountry_wise_project',
        data:{'vendor_id':vendor_id},
        success: function(data){
            projectwise_chart=Highcharts.chart('country_wise_projects', {
                chart: {
                    height: '100%'
                },
                series: [{
                    type: 'sunburst',
                    data: data,
                    allowDrillToNode: true
                }],
                title: {
                    text: 'Projects per Country'
                }
            });
          
        }
    })
    $.ajax({
        type:"GET",
        url:'/dashboard/getinvoicesummarychart_byvendor',
        data:{'vendor_id':vendor_id},
        success: function(data){
            Highcharts.chart('invoice_summary_bar_chart', {
                chart: {
                    type: 'column'
                },
                title: {
                    text: 'Overview of All Submitted Invoices till Date',
                    align: 'left'
                },
                xAxis: {
                    categories: data.allprojects,
                    crosshair: true,
                    accessibility: {
                        description: 'Countries'
                    }
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Invoice Value'
                    },
                    labels: {
                        formatter: function () {
                            return data.currency + Highcharts.numberFormat(this.value, 0);
                        }
                    }
                },
                tooltip: {
                    pointFormat: 'Invoice Value: <b>${point.y:.2f}</b>'
                },
                plotOptions: {
                    column: {
                        pointPadding: 0.2,
                        borderWidth: 0
                    }
                },
                series: [
                    {
                        name: 'Approved Invoices (Paid)',
                        data: data.paid_invoice_amount,
                        color:'#b71d41'
                    },
                    {
                        name: 'Approved Invoices (Unpaid)',
                        data: data.unpaid_invoice_amount,
                        color:'#de478e'

                    },
                    {
                        name: 'Invoices Awaiting Approval',
                        data:data.allawaiting_invoices,
                        color:'#bc72f0'

                    }, 
                    {
                        name: 'Disputed Invoices',
                        data: data.alldisputed_invoices,
                        color:'#795eaf'

                    },

                ]
            });
        }
    })

    $.ajax({
        type:"GET",
        url:'/dashboard/getunpaid_overdueinvoices',
        data:{'vendor_id':vendor_id},
        success: function(data){
            Highcharts.chart('unpaid_overdue_box_chart', {
                chart: {
                    type: 'boxplot'
                },
                title: {
                    text: 'All Unpaid Invoices Vs Days Overdue'
                },
                legend: {
                    enabled: false
                },
                xAxis: {
                    categories: ['Tubu', 'Ebitu', 'Okoro', 'Abasi', 'Eka', 'Bhadia', 'Dholera', 'Gujarat'],
                    title: {
                        text: 'Country / Project'
                    }
                },
                yAxis: {
                    title: {
                        text: 'Invoice Value (Gross Amount, Excl. Taxes)'
                    },
                    plotLines: [{
                        value: 93229, // Sample median of all data
                        color: 'red',
                        width: 1,
                        label: {
                            text: 'Overall median',
                            align: 'center',
                            style: {
                                color: 'gray'
                            }
                        }
                    }]
                },
                series: [{
                    name: 'Observations',
                    data: [
                        [76000, 81000, 85000, 88500, 90000], 
                        [72000, 75000, 79500, 82250, 85000], 
                        [72000, 75000, 79500, 82250, 85000], 
                        [72000, 75000, 79500, 82250, 85000], 
                        [72000, 75000, 79500, 82250, 85000], 

                    ],
                    tooltip: {
                        headerFormat: '<em>Project {point.key}</em><br/>'
                    }
                }]
            });
            
          
        }
    })
    $(document).on('change','#countries,#currencies,#tax,#currencies,#services,#projects',function(){
        var country_id=$('#countries').val()
        var project_id=$('#projects').val()
        var services=$('#services').val()
        var currencies=$('#currencies').val()
        var tax=$('#tax').val()
        filter_dashboard(country_id,project_id,services,currencies,tax)
    })

    function filter_dashboard(country_id,project_id,services,currencies,tax){
        console.log("country_id "+typeof(country_id))
        $.ajax({
            type:"GET",
            url:'/dashboard/filtervendor_dashboard',
            data:{'country_id':country_id,'project_id':project_id,'services':services,'currencies':currencies,'tax':tax},
            success: function(data){
                $('.total_projects').html(data.project_summary_details.total_project)
                $('.active_projects').html(data.project_summary_details.active_project)
                $('.inactive_projects').html(data.project_summary_details.inactive_project)
                var invoice_summary=''
                for(var i=0;i<data.invoice_summary_details.length;i++){
                    invoice_summary +='<tr>'
                        invoice_summary +='<td>'+data.invoice_summary_details[i].currency+' '+data.invoice_summary_details[i].paid_amount+'</td>'
                        invoice_summary +='<td>'+data.invoice_summary_details[i].currency+' '+data.invoice_summary_details[i].unpaid_amount+'</td>'
                        invoice_summary +='<td>'+data.invoice_summary_details[i].currency+' '+data.invoice_summary_details[i].awaiting_amount+'</td>'
                        invoice_summary +='<td>'+data.invoice_summary_details[i].currency+' '+data.invoice_summary_details[i].disputed_amount+'</td>'
                    invoice_summary +='</tr>'
                }
                $('.invoice_summary_table tbody').html(invoice_summary)
    
                projectwise_chart.series[0].setData(data.allproject);
            }
        })
    }

});
