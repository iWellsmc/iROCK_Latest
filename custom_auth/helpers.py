from custom_auth.models import *
import re
from datetime import datetime 
from notifications.models import Notification
from PIL import Image
from io import BytesIO
import base64
from invoice.templatetags.invoice_custom_tags import check_bank_user


def companygeneratecin(companyname):
    max_id = Companies.objects.values('id').order_by('-id').first()
    if(max_id != None):
        next_id=int(max_id['id'])
        max_id_str=str((next_id+1))
    else:
        next_id=1
        max_id_str=str(next_id)
    companyname=re.sub('[^A-Za-z0-9]+', '', companyname)
    companynameshort=companyname[:3].upper()

    max_id_str=max_id_str.zfill(3)
    return companynameshort+"-"+max_id_str

def convertdate(companydateformat,date):
    if (date != ""):
        if (companydateformat == 'dd-M-yy'):
            convert_date=datetime.strptime(date,"%d-%b-%Y").date()
        elif (companydateformat == 'dd-mm-yy'):
            convert_date=datetime.strptime(date,"%d-%m-%Y").date()
            # print('2',date)
        elif (companydateformat == 'dd/mm/yy'):
            convert_date=datetime.strptime(date,"%d/%m/%Y").date()
            # print('3',date)
        elif (companydateformat == 'mm-dd-yy'):
            convert_date=datetime.strptime(date,"%m-%d-%Y").date()
            # print('4',date)
        elif (companydateformat == 'mm/dd/yy'):
            convert_date=datetime.strptime(date,"%m/%d/%Y").date()
            # print('5',date)
        elif (companydateformat == 'yy-mm-dd'):
            convert_date=datetime.strptime(date,"%Y-%m-%d").date()
            # print('6',date)
        elif (companydateformat == 'yy/mm/dd'):
            convert_date=datetime.strptime(date,"%Y/%m/%d").date()
            # print('7',date)
        else:
            convert_date=datetime.strptime(date,"%d-%b-%Y").date()
    else:
        convert_date=None
    return convert_date

def getcompany_iamge(company_id):
    encoded_image=None
    company= Companies.objects.filter(id=company_id).first()
    if company.image:
        imageurl = company.image.url
        with open(company.image.path, 'rb') as f:
            image_data = f.read()
        image = Image.open(BytesIO(image_data))
        image = image.convert('RGB')  # Convert the image to RGB mode
        image = image.resize((120, 80))  # Resize the image to 150x100 pixels
        buffered = BytesIO()
        image.save(buffered, format="JPEG")      
        encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        encoded_image = "data:image/jpeg;base64," + encoded_image
    else:
        imageurl = None
    
    return {'encoded_image':encoded_image,'imageurl':imageurl}

def check_user_sign(user_data):
    count = 0
    if check_bank_user(user_data) :
        count=0 
    elif user_data.signature_type == None:
        count = 1
       
    return count


def markas_read_status(fullurl):
    if 'msg' in fullurl:
        if fullurl.split('msg')[1]:
            print('yes')
            try:
                Notification.objects.get(pk=int(str(fullurl.split('msg')[1]).replace(',',''))).mark_as_read()
            except Exception as e:
                print('Notification Read Status Exception',e)
        else:
            print('no')