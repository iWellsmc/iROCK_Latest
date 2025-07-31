def wcc_pdfstyle(encoded_image):
    pdf_style = '''
        .head-inv-pre {
            color: #AF2B50;
            font-weight: 600;
            font-size:16px;
            }

        * {
            font-family:arial,helvetica,sans-serif !important;
        }    

        @page  {
            size: A4 portrait; /* can use also 'landscape' for orientation */
            margin-right:1cm !important;
            margin-left:1cm !important;
        }


        @page {
            margin-bottom:100px !important;
            margin-top:90px !important;

        @top-center {
            content: element(header);
            align-items: center;
            width: 97.8%;
        }

        @bottom-right {
            content: "Page " counter(page) " of " counter(pages);
            font-size: 10px;
            width: 20% !important;
            margin-right: 0px;
            margin-top:-30px; 
            padding:20px; 
        }

        @bottom-left {
            margin-top:35px !important;
            content: element(footer);
            font-size: 5px !important;
            margin-bottom: 30px !important;
            width: 100% !important;
        }

        }

        footer {
            position: running(footer);
            font-size:10px !important;
            /*height: 150px;*/
            margin-top:-60px !important;
        }

        header {
            position: running(header);
            font-size:10px !important;
        }
        
        * {
            font-family: Arial, Helvetica, sans-serif;
        }

        .head-inv-pre {
            color: #AF2B50 !important;
            font-size: 15px !important;
        }

        .inv_rec_cls {
            border-radius: 30px !important;
            margin-top: 10px;
            border: 2px solid #000;
            width: 30%;
            margin-left: 69.7%;
            margin-bottom: 20px;
        }

        .inv_rec_cls p {
            text-align: center;
            margin: 10px 10px !important;
        }

        .invoice-received {
            font-weight: 600;
        }

        .logo {
            margin: 10px auto !important;
            background-image: url("data:image/png;base64,'''+encoded_image+'''");
            background-repeat: no-repeat; 
            width: 100px !important;
            height: 75px !important;
            object-fit: cover;
            text-align: left !important;
        }

        .company-details {
            margin: auto;
            text-align: center;
            width: 85% !important;
        }

        .company-details h4 {
            margin-bottom: 5px;
        }

        .company-details p {
            color: #000;
            font-size: 10px;
            font-weight: 500;
            margin-top: 0px;
            display: inline-block;
        }

        .parent {
            justify-content: center;
            width: 100%;
            margin: auto;
        }

        .row-border {
            border: 1px solid #c7c7c7;
        }

        .bor-top {
            border-top: none !important;
        }

        .bor-bottom-none {
            border-bottom: none !important;
        }

        .bor-ryt {
            border-right: 1px solid #c7c7c7;
        }

        .row-content h4 {
            color: #AF2B50;
            font-size: 12px;
            font-weight: 600;
            word-break: break-word;
            /* width: 25%; */
            margin: 0px !important;
            padding: 8px 0px 0px;
        }

        .row-content p {
            color: #000;
            font-size: 10px;
            font-weight: 500;
            margin: 0px auto !important;
            padding: 8px 0px !important;
            line-height: 1.5;
        }

        .captions {
            color: #AF2B50;
            font-size: 12px;
            font-weight: 600;
            word-break: break-word;
            padding: 8px 5px;
        }

        .red {
            color: red !important;
            font-weight: 600 !important;
        }

        .lr-bor {
            border-left: 1px solid #c7c7c7 !important;
            border-right: 1px solid #c7c7c7 !important;
        }

        .d-flex {
        display: flex;
        }

        .justify-content-center {
        justify-content: center;
        }

        .align-items-center {
        align-items: center;
        }

        .justify-content-end {
            justify-content: end;
        }

        .col-2 {

        }

        .col-6 {
            width: 50%;
        }

        .col-4 {
            width: 33.33%;
        }

        .col-10 {
            width:83.33333333%;
        }

        .col-12 {
            width: 100%;
        }

         .text-center {
            text-align: center;
        }

        .side-pad {
            padding: 0px 5px;
        }

        .bottom-pad {
            padding-bottom: 10px !important;
        }

        .caption-head {
            font-size:10px !important;
            display: inline-block; 
            margin-right: 5px !important;
            font-weight: 600 !important;
        }

        .caption-value {
            font-size: 10px !important;
        }

        .split_val {
            page-break-inside: avoid;
        }
        

/******************** wcc styles ********************/
.head-inv-pre-vend {
  font-size: 16px !important;
  color: #AF2B50;
}

.from-head {
    color: #AF2B50;
    font-weight: 600;
    font-size: 15px;
    text-align: center;
    margin: 0px 0px 10px 0px;
}

.from-head-wcc {
    color: #AF2B50;
    font-weight: 600;
    font-size: 15px;
    text-align: center;
    margin: 0px 0px 10px 0px;
}

.from-sub-head {
    color: #006e80;
    font-weight: 600;
    font-size: 15px;
    text-align: center;
    margin: 10px 0px;
}

.from-sub-head-wcc {
    color: #006e80;
    font-weight: 600;
    font-size: 15px;
    text-align: center;
    margin: 10px 0px;
}

.from-sub-head-wcc-support {
    color: #006e80;
    font-weight: 600;
    font-size: 15px;
    text-align: center;
    margin: 15px auto;
}

.invoice-info {
    width: 100%;
    border: 1px solid #c7c7c7;
    border-collapse: collapse;
}

.invoice-info th {
    width: 50%;
    border-right: 1px solid #c7c7c7 !important;
    color: #000;
    font-weight: 600 !important;
    border-collapse: collapse;
    font-size: 12px !important;
}

.invoice-info th, .invoice-info td {
    border-bottom: 1px solid #c7c7c7 !important;
    padding: 8px; 
    color: #000;
    font-size: 12px;
    font-weight: 500;
     border-collapse: collapse;
}

.invoice-info a, .inv-pretbl a {
    color: #96183a;
    font-weight: 500;
    font-size: 12px !important;
}

.invoice-info span, .inv-pretbl span {
    color: #96183a;
    font-weight: 500;
    font-size: 12px !important;
}

.head-inv-pre-sum-details {
    text-align: center;
    color: #5e0000 !important;
    font-weight: 600;
    font-size: 15px !important;
    margin: 15px auto;
}

.inv-pretbl {
    border: 1px solid #9f9f9f94;
    width: 100%;
    border-collapse: collapse;
}

.inv-pretbl th {
    color: #007480;
    font-size: 12px;
    font-weight: 600;
    padding: 6px 5px 6px 5px;
    border-right: 1px solid #9f9f9f94 !important;
    border-bottom: 1px solid #9f9f9f94 !important;
    border-collapse: collapse;
    text-align: center;
}

.inv-pretbl td {
    color: #000;
    font-size: 12px;
    font-weight: 500;
    border-right: 1px solid #9f9f9f94 !important;
    border-collapse: collapse;
    padding: 6px 5px 6px 5px;
    text-align: center;
}

#file-width {
    width: 10% !important;
    word-break: break-word;
}

/******************** wcc styles ********************/

        '''
    return pdf_style