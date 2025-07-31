


def credit_note_pdfstyle(encoded_image):
    pdf_style = '''
                    table
            {
                width: 100%;
                border-collapse: collapse;

            }
        .head-inv-pre {
            color: #AF2B50 !important;
            font-weight: 600 !important;
            font-size: 20px; !important;
        }
            .display_val{
                display:flex;
            }
             .header_text{
                font-size:10px !important;
                display: inline-block; 
                width:110px;
                font-weight:600 !important;
            }
            .header_val{
                font-size:10px !important;
                font-family: system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans","Liberation Sans",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
                width: 300px;
                margin-bottom: 0px !important;
            }
                @page {
                    size: A4 portrait; /* can use also 'landscape' for orientation */
                    margin-right:1cm !important;
                    margin-left:1cm !important;
                    margin-bottom:150px !important;
                    margin-top:110px !important;
            }

            @page {
                @bottom-right {
                    content: "Page " counter(page) " of " counter(pages);
                    font-size: 10px;
                    font-family: system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans","Liberation Sans",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"; 
                }
                @top-center{
                    content: element(header);
                    margin-left:30px !important;
                    align-items: center;
                    line-height: 1.3;
                    font-size: 20px;  
                    font-family: system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans","Liberation Sans",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"; 
                    color: #AF2B50; 
                    font-weight: 600;
                }
                @top-left {
                margin-top:100px !important;
                content: url("data:image/png;base64,'''+encoded_image+'''");    
                margin-bottom:50px !important;           
                }


                @bottom-left{
                    margin-top:35px !important;
                    content: element(footer);
                }

            }

        footer {
            position: running(footer);
            /*height: 150px;*/
        }
        header{
                position: running(header);
                font-size:10px !important;
            }
         #creditfile-td-left
            {
                width:15% !important;
                text-align: left !important;
                padding-left: 5px !important;
            }

            .inv-file {
                    /* width: 20%; */
                    color: #96183a;
                    word-wrap: break-word !important;
                    word-break: break-all !important;
                }
                .inv-file a{
                    font-weight: 400 !important;
                }
            .end-total-credit-note td {
                    color: #000;
                    font-size: 12px;
                    font-family: system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans","Liberation Sans",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
                    font-weight: 500;
                    padding-right: 4px !important;
                    padding-left: 4px !important;
                }
                /* .payment-symbol-style
                {
                    color:red !important;
                } */

            .inv-pretbl th {
                    color: #007480;
                    font-size: 12px;
                    font-family: system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans","Liberation Sans",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"; 
                    font-weight: 600;
                }
            .nme-lis {
                    font-size: 10px !important;
                    font-family: system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans","Liberation Sans",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
                    font-weight: 400;
                }
            
            .credit-note-link a {
                    font-size: 14px !important;
                    font-family: system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans","Liberation Sans",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
                }
            .Credit-Note-Summary tbody tr td:last-child
                {
                text-align: left !important;
                padding-left: 5px;
                }
                .Credit-Note-Summary thead tr th
                {
                    font-size: 10px !important;
                    font-family: system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans","Liberation Sans",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
                }
                .Credit-Note-Summary tbody tr td
                {
                    font-size: 10px !important;
                    font-family: system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans","Liberation Sans",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
                }
                .invoice-info tbody tr th
                {
                    font-size: 10px !important;
                }
                
                        /* company name */
                        .companyname-text{ 
                        text-align: center!important;    
                        font-size: 20px;  
                        font-family: system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans","Liberation Sans",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
                        color: #AF2B50; 
                        font-weight: 600;
                        margin-right: 150px;
                        } 

                        /* credit note summery and details heading*/

                .from-head {
                color: #AF2B50;
                font-weight: 600 !important;
                font-size:18px;
                font-family: system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans","Liberation Sans",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
                display: block !important;
                margin-right: 150px !important;
                margin-bottom: 0px !important;
                text-align: center !important;
                width: 100% !important;
                }
                .pdf-total-vv{
                font-weight: 900 !important;
                }

                .total-pdf-doll{
                    font-weight: 900 !important;
                }
                table{
                    page-break-inside: avoid;
                }
                .pdf-heading-section{
                text-align: center !important;
                width:85%;
                }

                    .from-sub-head{
                    color: #006e80;
                    display: block !important;
                    font-weight: 600 !important;
                    font-size:18px;
                    font-family: system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans","Liberation Sans",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
                    margin-top: 20px !important;
                    text-align: center !important;
                    margin-bottom: 15px !important;
                }

                    /* contract number */
                    .credit-con-no {
                        color: maroon;
                        font-size: 14px !important;
                        font-family: system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans","Liberation Sans",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
                        font-weight: 600 !important;
                    }

                    .credit-con-no span {
                        color: #000 !important;
                        font-size:12px !important;
                        font-family: system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans","Liberation Sans",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
                    }
                   
                
                    /* table border  */
                    .inv-pretbl {
                        border: 1px solid #c7c7c7;
                        width: 100%;
                        margin-top: 13px;

                    }

                    .inv-pretbl th,
                    .inv-pretbl td {
                        border: 1px solid #c7c7c7 !important;
                        padding: 4px 0px 0px 0px;
                        text-align: center;
                    }

                    /* second table */
                    .invoice-info {
                        width: 100%;
                        margin: 0 auto;
                        border: 1px solid #c7c7c7;
                    }

                    .invoice-info th,
                    .invoice-info td {
                        border-bottom: 1px solid #c7c7c7 !important;
                        padding: 4px 0px 0px 4px;
                        font-size: 14px !important;
                        font-family: system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans","Liberation Sans",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
                    }

                    .invoice-info th{
                        width: 50%;
                        border-right: 1px solid #c7c7c7 !important;
                        font-weight: 400 !important;
                    }
                    /* second table heading */
                    
                .credit-note-doc {
                        color: #006e80;
                        font-weight: 600 !important;
                        font-size:18px;
                        font-family: system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans","Liberation Sans",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
                        text-align: center;
                        margin-bottom: 15px !important;
                        margin-top: 30px !important;
                    }
                

                    .invoice-info a {
                        color: #96183a;
                    }
                    .inv-file a {
                        color: #96183a;
                    }

                    .invoice-info th {
                        width: 50%;
                        border-right: 1px solid #c7c7c7 !important;
                        text-align: left !important;
                    }
                    /* .wid-sn {
                        width: 5% !important;
                    } */
                    .inv_name
                    {
                        /* width: 15%; */
                        word-wrap: break-word !important;
                        word-break: break-all !important;
                        padding-right:2px !important;
                        padding-left:2px !important;
                        width:20% !important;
                    
                    }

                    .img-pdf{
                    width: 90px;
                    height: 90px;
                    }
                    .credit-font-td p{
                        font-weight: 400 !important;
                    }

                    /* table all table heading width css */
                    .Credit-Note-Summary thead tr th
                    {
                    padding-left: 2px;
                    padding-right: 2px;
                    }
                    .credit-font-td td{
                    padding-left: 2px;
                    padding-right: 2px;   
                    }
                    .table-sn-wid
                    {
                        width: 5%;
                    }
                    .credit-date-wid
                    {
                        width: 10%;
                    }
                        .company-details {
                           margin: auto;
                           text-align: center;
                           width: 100% !important;
                        }
                        .company-details h4 {
                            margin-bottom: 5px;
                            font-size: 18px;
                            font-weight: 600 !important;
                            font-family: system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans","Liberation Sans",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
                        }
                        .company-details p {
                           color: #000;
                           font-size: 10px;
                           font-weight: 500;
                          font-family: system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans","Liberation Sans",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
                           margin-top: 0px;
                           display: inline-block !important;
                                }
                
                        '''
    return pdf_style