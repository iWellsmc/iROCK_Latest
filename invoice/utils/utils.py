from finance.models import CompanyBank,UserBankMaster
from invoice.models import PaymentInstruction
from custom_auth.models import *
import re
from PIL import Image
from io import BytesIO
import base64
# seperate unique list values from a list
def unique_list(a: list):
    d = {}

    # Group the values by creating a dictionary where each key is a unique value in the list
    # and the value is a list of indices where that value occurs
    for i, x in enumerate(a):
        if x not in d:
            d[x] = [i]
        else:
            d[x].append(i)

    # Create a list of lists, where each sublist contains the repeated values
    result = []
    for k, v in d.items():
        if len(v) > 1:
            result.append([a[i] for i in v])
        else:
            result.append([a[v[0]]])

    return result


def convert_to_int(amount):
    convert_to = float(re.sub(r'[^\w\s.]|[a-zA-Z]+', '', amount))
    val = int(convert_to) if convert_to.is_integer() else float(convert_to)
    return val

def payment_instruction_number(company_id,bank_id , bank_user_status) :
    if bank_user_status == 1 or bank_user_status == 2 or bank_user_status== None:
        bank = CompanyBank.objects.get(id=bank_id)
        extract_bank_sequence = str(bank.bank_name.bank_name)[:3].zfill(3)
    else :
        bank = UserBankMaster.objects.get(id=bank_id)
        extract_bank_sequence = str(bank.bank_name)[:3].zfill(3)
    bank_sequence = str(extract_bank_sequence).upper()
    company = Companies.objects.get(id=company_id).cin_number
    company_sequence = str(company)[:3]
    last_sequence = '001'
    if PaymentInstruction.objects.filter(company_id=company_id,status=True).exists():
        sequence = PaymentInstruction.objects.filter(company_id=company_id, status=True, pi_number__isnull=False).values_list('pi_number', flat=True).last()
        if sequence is not None:
            match = re.search(r"(\d+)$", sequence)
            if match:
                numeric_part = match.group(1)
                incremented_numeric_part = int(numeric_part) + 1
                last_sequence = str(incremented_numeric_part).zfill(len(numeric_part))
        else:
            last_sequence = '001'
    else:
        last_sequence = '001'

    return f'{company_sequence}-PI-{bank_sequence}-{last_sequence}'



def update_payment_instruction_number(sequence_number, bank_id , bank_user_status):
    if bank_user_status ==1 or bank_user_status ==2 or bank_user_status==None:
        bank = CompanyBank.objects.get(id=bank_id)
        bank_sequence = str(bank.bank_name.bank_name)[:3]
    else :
        bank = UserBankMaster.objects.get(id=bank_id)
        bank_sequence = str(bank.bank_name)[:3]

    fill_number = bank_sequence.zfill(3)
    bank_sequence = fill_number.upper()
    indicies = (8,10)
    out_sequence_number = bank_sequence.join([sequence_number[:indicies[0]-1], sequence_number[indicies[1]:]])
    return out_sequence_number


def payment_instruction_pdfstyle(encoded_image):
    pdf_style = '''
    @page {
        margin-bottom:150px !important;
        margin-top:110px !important;
    @top-left {
        margin-top:30px !important;
        padding-top: 50px;
        content: element(header);
        margin-bottom:30px !important;
        width: 100%;
        margin: auto;
    } 
    @top-center {
        content: element(footer);
        width:100%;
        margin: auto;
        text-align: center;
        margin-bottom: 38px;
    }
    }

    header {
        position: running(header);
        /*height: 150px;*/
    }
    footer{
        position: running(footer);
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

    .head-inv-pre {
        font-size: 20px; 
        color: #AF2B50; 
        font-weight: 600;
        word-break: break-word;
        margin-top: 10px;
    }

    .logo-image {
        margin: 10px 10px !important;
        background-image: url("data:image/png;base64,'''+encoded_image+'''");');
        background-repeat: no-repeat !important;
        width: 125px !important;
        height: 75px !important;
        object-fit: cover;
        text-align: left !important;
        background-size:contain;
    }

    .display_val{
        white-space: nowrap;
    }
    .company-details {
        margin: auto;
        text-align: center;
        width: 85% !important;
    }

    .company-details h4 {
        margin-bottom: 5px;
        font-size: 16px;
    }

    .company-details p {
        color: #000;
        font-size: 13px;
        font-weight: 500;
        margin-top: 0px;
        display: inline-block;
    } 
    .captions {
        font-weight: 600;
    }
        
        '''
    return pdf_style


def coversheet_pdfstyle(encoded_image,approved_users):
        # @import url('https://fonts.googleapis.com/css2?family=Babylonica&family=Ballet&family=Birthstone+Bounce&family=Caveat&family=Dancing+Script:wght@500&family=Dr+Sugiyama&family=Kristi&family=La+Belle+Aurore&family=Licorice&family=Mea+Culpa&family=Meddon&family=Miss+Fajardose&family=Monsieur+La+Doulaise&family=Mr+Dafoe&family=Mrs+Saint+Delafield&family=Passions+Conflict&family=Qwigley&family=Satisfy&family=Tangerine:wght@400;700&display=swap');
        # @import url('https://fonts.googleapis.com/css2?family=Caveat&family=Dancing+Script:wght@500&family=Qwigley&family=Sacramento&family=Yellowtail&display=swap');
        # @import url('https://fonts.googleapis.com/css2?family=Babylonica&family=Ballet&family=Birthstone+Bounce&family=Caveat&family=Dancing+Script:wght@500&family=Dr+Sugiyama&family=Kristi&family=La+Belle+Aurore&family=Licorice&family=Mea+Culpa&family=Meddon&family=Miss+Fajardose&family=Monsieur+La+Doulaise&family=Mr+Dafoe&family=Mrs+Saint+Delafield&family=Passions+Conflict&family=Qwigley&family=Satisfy&family=Tangerine:wght@400;700&family=Zeyada&display=swap');
        # @import url('https://fonts.googleapis.com/css2?family=Caveat&family=Dancing+Script:wght@500&family=Homemade+Apple&family=Kristi&family=Mr+Dafoe&family=Mrs+Saint+Delafield&family=Qwigley&family=Satisfy&family=Tangerine:wght@400;700&family=Yellowtail&display=swap');
    pdf_style='''
            @import url('https://fonts.googleapis.com/css2?family=Babylonica&family=Ballet&family=Birthstone+Bounce&family=Caveat&family=Dancing+Script:wght@500&family=Dr+Sugiyama&family=Kristi&family=La+Belle+Aurore&family=Licorice&family=Mea+Culpa&family=Meddon&family=Miss+Fajardose&family=Monsieur+La+Doulaise&family=Mr+Dafoe&family=Mrs+Saint+Delafield&family=Passions+Conflict&family=Qwigley&family=Satisfy&family=Tangerine:wght@400;700&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Caveat&family=Dancing+Script:wght@500&family=Qwigley&family=Sacramento&family=Yellowtail&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Babylonica&family=Ballet&family=Birthstone+Bounce&family=Caveat&family=Dancing+Script:wght@500&family=Dr+Sugiyama&family=Kristi&family=La+Belle+Aurore&family=Licorice&family=Mea+Culpa&family=Meddon&family=Miss+Fajardose&family=Monsieur+La+Doulaise&family=Mr+Dafoe&family=Mrs+Saint+Delafield&family=Passions+Conflict&family=Qwigley&family=Satisfy&family=Tangerine:wght@400;700&family=Zeyada&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Caveat&family=Dancing+Script:wght@500&family=Homemade+Apple&family=Kristi&family=Mr+Dafoe&family=Mrs+Saint+Delafield&family=Qwigley&family=Satisfy&family=Tangerine:wght@400;700&family=Yellowtail&display=swap');
        '''
    for i in approved_users:
        user_data= User.objects.get(id=i)
        data=''
        if user_data.signature_type == "signature":
            if user_data.signature_image:
                data=user_data.signature_image.path
        elif user_data.signature_type == "file":
            if user_data.signature_image:
                data=user_data.signature_image.path
        if (data):
            # convert image to jpg  
            # with open(data, 'rb') as f:
            #     image_data = f.read()
            #     image = Image.open(BytesIO(image_data))
            #     image = image.convert('RGB')  # Convert the image to RGB mode
            #     image = image.resize((120, 80))  # Resize the image to 150x100 pixels
            #     buffered = BytesIO()
            #     image.save(buffered, format="JPEG")      
                # user_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
            with open(data, 'rb') as f:
                image_data = f.read()
                user_image = base64.b64encode(image_data).decode('utf-8')
                pdf_style += '''
                            .logo-'''+str(i)+''' {
                               margin: 10px 10px !important;
                                background-image: url("data:image/png;base64,'''+user_image+'''");
                                background-repeat: no-repeat;
                                background-position: center;
                                background-size: 100px;
                                width: 100px;
                                height: 50px; 
                                background-size:contain;
                            }
                            '''
    pdf_style += '''
        .head-inv-pre{
           color:#000 !important;
            font-weight: 600;
            font-size:16px;
            }

             .line-brk{
        word-break:break-all !important;
        width:30%;
        font-size:10px;
        }
        .font-reduce{
        font-size:12px !important;
        }
        .middle-tbl{
        margin:0px auto;
        }
        .space_cls{
        margin-bottom:50px !important;
        }
        @page  {
            size: A4 portrait; /* can use also 'landscape' for orientation */
            margin-right:1cm !important;
            margin-left:1cm !important;
        }


        @page {
            margin-bottom:100px !important;
            margin-top:235px !important;

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
        header{
            position: running(header);
            font-size:10px !important;
        }
        * {
            font-family: Arial, Helvetica, sans-serif;
        }

        .head-inv-pre {
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

        .inv_approved_cls {
            border-radius: 30px !important;
            margin-top: 15px;
            border: 2px solid #000;
            width: 30%;
            margin-bottom: 20px;
            font-size: 10px;
            color: #679B6E;
        }

        .inv_approved_cls p {
            text-align: center;
            margin: 10px 10px !important;
        }

        .logo {
            margin: 10px 10px !important;
            background-image: url("data:image/png;base64,'''+encoded_image+'''");
            background-repeat: no-repeat; 
            width: 100px !important;
            height: 75px !important;
            object-fit: cover;
            text-align: left !important;
            margin-left:15px !important;
            background-size:contain;
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
            width: 16.66666667%;
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

        /********** Approval Table **********/

        .head-inv-pre-approval {
            color: #000;
            font-size: 10px;
            font-weight: 600;
            margin-top: 10px !important;
            padding-top: 10px !important;
            margin-bottom: 0px;
        }

        .approval-head {
            color: #000;
            font-size: 10px;
            font-weight: 500;
            margin-bottom: 10px !important;
            margin-top: 5px;
        }

        .invoice-approval-ptag {
            color: #000;
            font-size: 10px;
            font-weight: 600;
            padding-bottom:10px !important;
            /* margin-bottom:10px !important; */
            
        }

        .coversheet-approval-table {
            /*width: 85%;*/
            width: 100%;
            border: 1px solid #c7c7c7;
            border-collapse: collapse;
            margin-top: -28px;
        }

        .coversheet-approval-table th {
            color: #007480;
            /* color: #AF2B50; */
            font-size: 10px !important;
            font-weight: 600;
            text-align: center;
            padding: 6px 5px !important;
            border: 1px solid #c7c7c7 !important;

        }

        .coversheet-approval-table td {
                    font-size: 10px;
                    font-weight: 500;
                    margin: 0px auto !important;
                    padding: 6px 5px !important;
                    border: 1px solid #c7c7c7 !important;
                    }
                    
        .coversheet-approval-table-bold {
                    font-weight: 600 !important;
                    }

         .td-red {
            color: red;
        }

        .td-black {
            color: #000;
            font-weight: 600;
        }            

        /********** Approval Table **********/ 

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

        .details {
            text-align: center;
            /*width: 84.8%;*/
            width: 99.8%;
            border-bottom: none;
            margin-top: 10px;
        }

        .footer-table td {
            border: none !important;
            padding: 0px;
        }

        .coversheet-users {
            width: 100%;
            border-collapse: collapse;
        }

        .coversheet-users th {
            /* color: #007480; */
            color: #fff;
            background-color: #891737;
            /* color: #AF2B50; */
            font-size: 12px;
            font-weight: 500;
            text-align: center;
        }

        .coversheet-users th, td {
            padding: 10px 10px;
            border: 1px solid #c7c7c7 !important;
            /*border: 2px solid #000 !important;*/
            # font-size: 13px;
            border-collapse: collapse;
        }

        .coversheet-users td {
            color: #000;
            font-size: 12px;
            font-weight: 500;
        }

        .coversheet-users-image {
            text-align: center;
        }

        .coversheet-users-image img {
            width: 250px;
        }

        .coversheet-users-image p {
            font-size: 30px;
            font-weight: 500;
            margin-bottom: 0px;
        }
       
        @font-face {
  font-family: 'Arial, Helvetica, sans-serif';
  font-style: normal;
  font-weight: normal;
  src: url(http://themes.googleusercontent.com/static/fonts/opensans/v8/cJZKeOuBrn4kERxqtaUH3aCWcynf_cDxXwCLxiixG1c.ttf) format('truetype');
}
        
        '''
    return pdf_style