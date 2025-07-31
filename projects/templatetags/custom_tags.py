from textwrap import wrap
import time
import json
from time import strftime
from django import template
import re
import datetime
import ast
from functools import reduce
from datetime import date, timedelta
from datetime import datetime
import pytz
from django.utils import timezone

import operator
from django.db.models import Q

# import urllib, cStringIO, base64
from chat.models import *
from django.http import request
from django.http.response import JsonResponse
from chat.views import message
from custom_auth.models import *
from projects.models import *
from invoice.models import *
from InvoiceGuard.models import *
from credit_note.models import *
from cost_code.models import *
from wcc.models import *
from finance.models import *
from projectflow.models import *
from credit_note.templatetags.credit_custom_tags import calculate ,newcalculate ,creaditenote_gross_amount
register = template.Library()

# @register.filter
# def get64(url):
#     """
#     Method returning base64 image data instead of URL
#     """
#     if url.startswith("http"):
#         image = cStringIO.StringIO(urllib.urlopen(url).read())
#         return 'data:image/jpg;base64,' + base64.b64encode(image.read())

#     return url


def get_process(value, arg):
    if arg == 'flow':
        get_process = Process.objects.filter(process_name=value)
        return get_process


def get_project(value, arg):
    if arg == "projects":
        get_projects = Projects.objects.filter(country_id=value)
        return get_projects


def get_block(value, arg):
    if arg == "block":
        get_blockname = BlockName.objects.filter(project_id=value, status=0)
        #   ("pro",get_block)
        return get_blockname


def get_field(blockid, block):

    get_fieldname = FieldName.objects.filter(block_id=blockid, status=1)
    return get_fieldname


def get_environment(fieldid, field):
    get_environments = FieldEnvironment.objects.filter(
        field_id=fieldid, status=1)
    return get_environments


def get_clusters(environment_id, fielddata):
    clustername = Clusters.objects.filter(
        field_environment_id=environment_id, status=1)
    return clustername


def get_clustersub(value, arg):
    get_clustersubname = ClusterSubnames.objects.filter(
        cluster_id=value, status=1)
    return get_clustersubname


def get_subwell(value, arg):
    if arg == "subwell":
        #   ("pro",value)
        get_wellsubname = WellSub.objects.filter(well_id=value)
        return get_wellsubname


def checkstatuscluster(field_id, cluster_type):
    cluster_details = Clusters.objects.filter(
        field_id=field_id, cluster_name=cluster_type).first()
    return cluster_details.status


def getclustersub(cluster_id, cluster_subname):
    clustersub_details = ClusterSubnames.objects.filter(cluster_id=cluster_id)
    return clustersub_details


def checkbolckhasfield(block_id, blockdata):
    fieldname = FieldName.objects.filter(block_id=block_id, status=1)
    return fieldname.count()


def checkfieldhascluster(environmentid, field):
    if Clusters.objects.filter(field_environment_id=environmentid, status=1).exists():
        cluster = Clusters.objects.filter(
            field_environment_id=environmentid, status=1)
    else:
        cluster = ClusterSubnames.objects.filter(
            cluster_id__field_environment_id=environmentid, status=1)
    return cluster.count()


def checkclusterhasclustername(environmentid, cluster_type):
    cluster = Clusters.objects.filter(
        field_environment_id=environmentid, cluster_name=cluster_type, status=1).first()
    if (cluster != None):
        cluster_name = ClusterSubnames.objects.filter(
            cluster_id=cluster.id, status=1)
        return cluster_name
    else:
        cluster_name = []
        return cluster_name


def checkclustercount(environment, cluster_type):
    cluster = Clusters.objects.filter(
        field_environment_id=environment, cluster_name=cluster_type, status=1).first()
    if (cluster != None):
        cluster_name = ClusterSubnames.objects.filter(
            cluster_id=cluster.id, status=1)
        return cluster_name.count()
    else:
        cluster_name = 0
        return cluster_name


def checkclusterhasdevelopmenttype(cluster_id, clusterdata):
    development_type = MasterDevelopmentType.objects.filter(
        clustersubname_id=cluster_id, status=1)
    return development_type.count()


def checkdevelopmenthaswell(development_id, development):
    well = Well.objects.filter(development_type_id=development_id, status=1)
    return well.count()


def get_development_type(clustersubid, dev_type):
    development = MasterDevelopmentType.objects.filter(
        clustersubname_id=clustersubid, development_type=dev_type, status=1).first()
    id = ''
    if development:
        id = development.id
    else:
        id = ''
    return id


def replace_development(Development_type):
    get_development_type = Development_type.replace("_", " ")
    return get_development_type


def checkdevelopmenttype(cluster, development):
    development_type = MasterDevelopmentType.objects.filter(
        clustersubname_id=cluster, development_type=development, status=1)
    return development_type.count()


def cap_wells(well):
    wells = well.title()
    return wells


def wellname(well_name):
    wells = well_name.lower().split(" ")[0]
    if (wells == "workovers/well"):
        welldata = wells.replace("/well", "")
        return welldata
    else:

        return wells
    
def convert_to_int(amount):
    convert_to = float(re.sub(r'[^\w\s.]|[a-zA-Z]+', '', amount))
    val = int(convert_to) if convert_to.is_integer() else float(convert_to)
    return val


def getwellnamecount(development_id, well_type):
    well = Well.objects.filter(
        development_type_id=development_id, well_name=well_type, status=1).first()
    if (well_type == 'Workovers/Well Intervention'):
        if (well != None):
            well_name = WellSub.objects.filter(well_id=well.id, status=1)
            return well_name.count()
    else:
        well_name = 0
        return well_name


@register.simple_tag
def getwellmaindata(development_type_id, well_type):
    if development_type_id != '':
        well = Well.objects.filter(
            development_type_id=development_type_id, well_name=well_type, status=1).first()
        if (well != None):
            well_name = WellSub.objects.filter(well_id=well.id, status=1)
            return 1, well_name
        else:
            return 0, []


def getwellname(development_type_id, well_type):

    if development_type_id != '':
        well = Well.objects.filter(
            development_type_id=development_type_id, well_name=well_type, status=1).first()
        if (well != None):
            well_name = WellSub.objects.filter(well_id=well.id, status=1)
            print(well_name, development_type_id, 'asd', well_type, well.id)
            return well_name

        else:
            well_name = []
            return well_name


def get_projecttype(project_id, project_types):
    projecttypes = ProjectTypeCompany.objects.filter(project_id=project_id)
    return projecttypes


def get_projectblock(project_id, project_block):
    projectblock = ProjectBlock.objects.filter(project_id=project_id)
    return projectblock


def get_projectfield(block_id, project_field):
    projectfield = ProjectField.objects.filter(block_id=block_id)
    return projectfield


def get_development(project_id, develop):
    developmenttypes = ProjectDevelopmentType.objects.filter(
        project_id=project_id)
    return developmenttypes


def get_developmentcount(project_id, development_types):
    developmenttypes = ProjectDevelopmentType.objects.filter(
        project_id=project_id)
    column_count = 0
    if developmenttypes.count() == 1:
        column_count = 12
    elif developmenttypes.count() == 2:
        column_count = 6
    elif developmenttypes.count() == 3:
        column_count = 4
    elif developmenttypes.count() == 4:
        column_count = 3
    return column_count


def get_deveploment_subtype(development_id, dev_subtype):
    dev_subtypes = ProjectDevelopmentSubType.objects.filter(
        development_type_id=development_id)
    return dev_subtypes


def get_deveplomentsub_subtype(developmentsub_id, dev_subtype):
    devsub_subtypes = DevelopmentSubSubType.objects.filter(
        discipline_subtype_id=developmentsub_id)
    return devsub_subtypes


def get_subtypes_sub(subtypes_subid, devsub_subdivision):
    sub_subtypes = DevelopmentSubTypeSub.objects.filter(
        disciplinesub_subtype_id=subtypes_subid)
    return sub_subtypes


def replace_dev(dev_name, dev):
    get_dev = dev_name.replace("_", " ")
    return get_dev


def modify_name(value, arg):
    get_value = value.replace("_", " ")
    return get_value


def getfieldenvironment(fieldid, arg):
    getfieldid = ProjectEnvironment.objects.filter(field_id=fieldid, status=1)
    return getfieldid


def checkfieldenvironment(field_id, environment):
    fieldenvironment = ''
    if re.findall("-", environment):
        spiltenvironment = environment.split("-")
        field_environment = spiltenvironment[0]
        field_environmentsubtype = spiltenvironment[1]
        fieldenvironment = FieldEnvironment.objects.filter(
            field_id=field_id, project_environment=field_environment, project_environment_subtype=field_environmentsubtype, status=1)
    else:
        fieldenvironment = FieldEnvironment.objects.filter(
            field_id=field_id, project_environment=environment, status=1)
    fieldenvironment_count = fieldenvironment.count()
    return fieldenvironment_count


def fieldenvironment(field_id, field_envid):
    fieldenvironment = ''
    if re.findall("-", field_envid):
        split_field_env = field_envid.split("-")
        project_env = split_field_env[0]
        subtype_env = split_field_env[1]
        fieldenvironment = FieldEnvironment.objects.filter(
            field_id=field_id, project_environment=project_env, project_environment_subtype=subtype_env, status=1).values()
        if len(fieldenvironment) > 0:
            return fieldenvironment[0]['id']
    else:
        fieldenvironment = FieldEnvironment.objects.filter(
            field_id=field_id, project_environment=field_envid, status=1).values()
        if len(fieldenvironment) > 0:

            return fieldenvironment[0]['id']


def getenvironmentcluster(environmentid, cluster):
    cluster = ProjectCluster.objects.filter(
        environment_id=environmentid, status=1)
    return cluster


def Otherenvironment(field_id, environment):
    environments = FieldEnvironment.objects.filter(
        field_id=field_id, project_environment=environment, status=1)
    return environments


# edit project creation

def checkentitytype(companyid, category):
    categories = Companies.objects.filter(
        id=companyid, status=1, category_entity=category)
    return categories.count()


def category_replace(category):
    if (category != None):
        category_name = category.replace("_", " ")
        return category_name
    else:
        return ''


def disciplines_replace_cap(discipline):
    try:
        if discipline == 'QHSE_&_community_development' or discipline == 'ICT':
            category_name = discipline.replace("_", " ")
            return category_name
        else:
            category_name = discipline.replace("_", " ")
            name = category_name.title()
            return name
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

        
def new_round_of_two_values(number):
    number_val=float(number)
    number_str = f"{number_val:.3f}"  
    integer_part, decimal_part = number_str.split('.') 
    if int(decimal_part[2]) >= 5:
        rounded_decimal = str(int(decimal_part[:2]) + 1).zfill(2)
        if rounded_decimal == "100":
            integer_part = str(int(integer_part) + 1)
            rounded_decimal = "00"
    else:
        rounded_decimal = decimal_part[:2]
    result = f"{integer_part}.{rounded_decimal}"
    newResult=float(result)
    return "{:,.2f}".format(newResult)


def round_of_two_values(number):
    number_val=float(number)
    number_str = f"{number_val:.3f}"
    integer_part, decimal_part = number_str.split('.') 
    if int(decimal_part[2]) >= 5:
        rounded_decimal = str(int(decimal_part[:2]) + 1).zfill(2)
        if rounded_decimal == "100":
            integer_part = str(int(integer_part) + 1)
            rounded_decimal = "00"
    else:
        rounded_decimal = decimal_part[:2]
    result = f"{integer_part}.{rounded_decimal}"
    newResult=float(result)
    return "{:.2f}".format(newResult)

def checkprojectcountry(projectid, countryid):
    country = Projectcreation.objects.filter(
        id=projectid, country_id=countryid, status=0)
    return country.count()


def checkmasterproject(projectid, masterprojectid):
    projectdata = Projectcreation.objects.filter(
        id=projectid, projectname_id=masterprojectid, status=0)
    return projectdata.count()


def checkprojectblock(projectid, blockid):
    projectblock = ProjectBlock.objects.filter(
        project_id=projectid, block_id=blockid, status=1)
    return projectblock.count()


def project_block(projectid, block):
    blockid = ProjectBlock.objects.filter(
        project_id=projectid, block_id=block).first()
    return blockid


def checkprojectfield(projectid, fieldid):
    projectfield = ProjectField.objects.filter(
        project_id=projectid, field_id=fieldid, status=1)
    return projectfield.count()

# count


@register.simple_tag
def checkprojectfieldid(blockid, fieldid, projectid):
    blockids = ProjectBlock.objects.filter(
        block_id=blockid, project_id=projectid, status=1).first()
    projectfield = ProjectField.objects.filter(
        block_id=blockids.id, project_id=projectid, field_id=fieldid, status=1)
    return projectfield.count()


def checkprojectenvironment(projectid, fieldenv):
    projectenv = ProjectEnvironment.objects.filter(
        project_id=projectid, field_environment_id=fieldenv, status=1)
    return projectenv.count()


@register.simple_tag
def checkprojectenvironmentid(fieldid, fieldenv, projectid):
    projectfieldid = ProjectField.objects.filter(
        field_id=fieldid, project_id=projectid, status=1).first()
    projectenv = ProjectEnvironment.objects.filter(
        field_id=projectfieldid.id, project_id=projectid, field_environment_id=fieldenv, status=1)
    return projectenv.count()


def getprojectcluster(filedenvid, fieldenv):
    projectcluster = Clusters.objects.filter(
        field_environment_id=filedenvid, status=1)
    data = []
    for cluster in projectcluster:
        get_clustersub = ClusterSubnames.objects.filter(
            cluster_id=cluster.id, status=1)
        clusters_list = []
        for cluster_sub in get_clustersub:
            clusters_list.append(
                {'id': cluster_sub.id, 'cluster_subname': cluster_sub.cluster_subname})
        data.append({cluster.cluster_name: clusters_list})
    return data


@register.simple_tag
def checkprojectcluster(fieldenvid, clusterid, projectid):
    project_environment = ProjectEnvironment.objects.filter(
        field_environment_id=fieldenvid, project_id=projectid, status=1).first()
    if (project_environment != None):
        project_cluster = ProjectCluster.objects.filter(
            environment_id=project_environment.id, project_id=projectid, clustersubname_id=clusterid, status=1).first()
        if (project_cluster != None):
            return project_cluster.id
        else:
            return 0
    else:
        return 0


def getprojectdevelopment(clusterid, devtype):
    dev_type = MasterDevelopmentType.objects.filter(
        clustersubname_id=clusterid, status=1)
    return dev_type


def developcount(clusterid, cluster):
    developmenttypes = MasterDevelopmentType.objects.filter(
        clustersubname_id=clusterid, status=1)
    column_count = 0
    if developmenttypes.count() == 1:
        column_count = 12
    elif developmenttypes.count() == 2:
        column_count = 6
    elif developmenttypes.count() == 3:
        column_count = 4
    elif developmenttypes.count() == 4:
        column_count = 3
    return column_count


@register.simple_tag
def checkprojectdevelopment(p_cid, clustersubid, developmentid, projectid):
    clustersubid = ProjectCluster.objects.filter(
        id=p_cid, project_id=projectid, clustersubname_id=clustersubid, status=1).first()
    if (clustersubid != None):
        project_development = ProjectDevelopmentType.objects.filter(
            cluster_id=clustersubid, project_id=projectid, development_id=developmentid, status=1).first()
        if (project_development != None):
            return project_development.id
        else:
            return 0
    else:
        return 0


@register.simple_tag
def checkprojectdiscipline(p_dpid, developmentid, projectdisciplineid, projectid):
    projectdevelopmentid = ProjectDevelopmentType.objects.filter(
        id=p_dpid, development_id=developmentid, project_id=projectid, status=1).first()
    if (projectdevelopmentid != None):
        project_discipline = ProjectDevelopmentDiscipline.objects.filter(
            development_type_id=projectdevelopmentid.id, project_id=projectid, project_discipline=projectdisciplineid, status=1).first()
        if (project_discipline != None):
            return project_discipline.id
        else:
            return 0
    else:
        return 0


def projectdisciplinetype(disciplineid, discipline):
    disciplinetype = DisciplineSubtype.objects.filter(
        project_discipline_id=disciplineid)
    return disciplinetype


@register.simple_tag
def checkprojectdisciplinetype(pdisciplineid, disciplineid, disciplinetypeid, projectid):
    disciplineid = ProjectDevelopmentDiscipline.objects.filter(
        id=pdisciplineid, project_id=projectid, project_discipline=disciplineid, status=1).first()
    if (disciplineid != None):
        project_disciplinetype = ProjectDevelopmentSubType.objects.filter(
            project_id=projectid, project_discipline_id=disciplineid.id, discipline_subtype_id=disciplinetypeid, status=1).first()
        if (project_disciplinetype != None):
            return project_disciplinetype.id
        else:
            return 0
    else:
        return 0


@register.simple_tag
def Disciplinesubtypecount(disciplinetypeid):
    disciplinetype = DisciplineSubSubTypes.objects.filter(
        discipline_subtype_id=disciplinetypeid)
    return disciplinetype.count()


@register.simple_tag
def CheckedDisciplinesubtypecount(disciplinetypeid, projectid):
    disciplinetypeid = ProjectDevelopmentSubType.objects.filter(
        project_id=projectid, id=disciplinetypeid, status=1).first()
    if disciplinetypeid != None:
        disciplinetype_activities = DevelopmentSubSubType.objects.filter(
            project_id=projectid, discipline_subtype_id=disciplinetypeid.id, status=1)
        return disciplinetype_activities.count()
    else:
        return 0


def getdisciplineactivity(disciplinetypeid, disciplinetype):
    disciplinetype = DisciplineSubSubTypes.objects.filter(
        discipline_subtype_id=disciplinetypeid)
    return disciplinetype


@register.simple_tag
def checkprojectdisciplineactivity(disciplinetypeid, disciplinetypeactid, projectid):
    disciplinetypeid = ProjectDevelopmentSubType.objects.filter(
        project_id=projectid, id=disciplinetypeid, status=1).first()
    if disciplinetypeid != None:
        disciplinetype_activities = DevelopmentSubSubType.objects.filter(
            project_id=projectid, discipline_subtype_id=disciplinetypeid.id, disciplinesub_subtype_id=disciplinetypeactid, status=1).first()
        if disciplinetype_activities != None:
            return disciplinetype_activities.id
        else:
            return 0
    else:
        return 0


def getdisciplinesubactivity(disciplinetypeid, disciplinetypeact):
    disciplinetype = Subtypes.objects.filter(
        discipline_subtype_id=disciplinetypeid)
    return disciplinetype


# all other act
@register.simple_tag
def disciplinesubactivitescount(disciplinetypeid):
    disciplinetype = Subtypes.objects.filter(
        discipline_subtype_id=disciplinetypeid)
    return disciplinetype.count()


@register.simple_tag
def checkotherallsubactivites(disciplinetypeid, projectid):
    disciplinetype = ProjectDevelopmentSubType.objects.filter(
        project_id=projectid, discipline_subtype_id=disciplinetypeid, status=1).first()
    disciplinesubact = DevelopmentSubTypeSub.objects.filter(
        project_id=projectid, other_type_id=disciplinetype.id, status=1)
    return disciplinesubact.count()


# discipline sub act
@register.simple_tag
def checkdisciplinesubactivites(disciplinetypeactid, subactivityid, projectid):
    disciplineact = DevelopmentSubSubType.objects.filter(
        project_id=projectid, disciplinesub_subtype_id=disciplinetypeactid, status=1).first()
    disciplinesubact = DevelopmentSubTypeSub.objects.filter(
        project_id=projectid, disciplinesub_subtype_id=disciplineact.id, sub_subtype_sub_id=subactivityid, status=1)
    return disciplinesubact.count()


@register.simple_tag
def Disciplinesubactcount(disciplinetypeid):
    disciplinetype = Subtypes.objects.filter(
        discipline_subtype_id=disciplinetypeid)
    return disciplinetype.count()


@register.simple_tag
def checkdisciplinesubacttotalcount(disciplinesubactid, projectid):
    disciplinesubact = DevelopmentSubSubType.objects.filter(
        project_id=projectid, id=disciplinesubactid, status=1).first()
    if disciplinesubact != None:
        dissubactdata = DevelopmentSubTypeSub.objects.filter(
            project_id=projectid, disciplinesub_subtype_id=disciplinesubact, status=1)
        return dissubactdata.count()
    else:
        return 0


# other sub act
@register.simple_tag
def checkothersubactivites(disciplinetypeid, subactivityid, projectid):
    disciplinetype = ProjectDevelopmentSubType.objects.filter(
        project_id=projectid, id=disciplinetypeid, status=1).first()
    if disciplinetype != None:
        disciplinesubact = DevelopmentSubTypeSub.objects.filter(
            project_id=projectid, other_type_id=disciplinetype.id, sub_subtype_sub_id=subactivityid, status=1)
        return disciplinesubact.count()
    else:
        return 0


def datacount(othercount):
    count = 0
    if othercount > 0:
        count = othercount
    else:
        count = 0
    return count


def get_well(developmenttype_id, arg):
    wells = Well.objects.filter(
        development_type_id=developmenttype_id, status=1)
    wellsub = wells.filter(well_name__iexact="Pilot Holes").values() | wells.filter(well_name__iexact="Development Wells").values(
    ) | wells.filter(well_name__iexact="Appraisal Wells").values() | wells.filter(well_name__iexact="Exploration Wells").values()
    return wellsub


# green field drill well
@register.simple_tag
def checkprojectwell(disciplinetypeid, wellid, projectid):
    disciplinetypeid = ProjectDevelopmentSubType.objects.filter(
        project_id=projectid, id=disciplinetypeid, status=1).first()
    if disciplinetypeid != None:
        projectwell = ProjectWellType.objects.filter(
            discipline_type_id=disciplinetypeid.id, welltype_id=wellid, status=1, project_id=projectid).first()
        if projectwell != None:
            return projectwell.id
        return 0
    else:
        return 0


def getwellsub(wellid, well):
    wellsub = WellSub.objects.filter(well_id=wellid, status=1)
    return wellsub


@register.simple_tag
def checkprojectwellsub(wellid, wellsubid, projectid):
    projectwell = ProjectWellType.objects.filter(
        id=wellid, project_id=projectid, status=1).first()
    if projectwell != None:
        projectwellsub = ProjectWellName.objects.filter(
            welltype_id=projectwell.id, wellname_id=wellsubid, status=1, project_id=projectid).first()
        if projectwellsub != None:
            return projectwellsub.id
        else:
            return 0
    else:
        return 0


@register.simple_tag
def checkwellsubactcount(wellsubid, projectid):
    wellsubid = ProjectWellName.objects.filter(id=wellsubid, status=1).first()
    if wellsubid != None:
        wellsubact = DevelopmentSubTypeSub.objects.filter(
            wellname_id=wellsubid.id, status=1, project_id=projectid)
        return wellsubact.count()
    else:
        return 0


@register.simple_tag
def checkwellactivities(wellsubid, wellactid, projectid):
    projectwellsubid = ProjectWellName.objects.filter(
        wellname_id=wellsubid, status=1, project_id=projectid).first()
    projectwellact = DevelopmentSubTypeSub.objects.filter(
        wellname_id=projectwellsubid.id, sub_subtype_sub_id=wellactid, status=1, project_id=projectid)
    return projectwellact.count()


# project discipline
def getprojectdiscipline(devlopementid, projectid):
    projectdiscipline = ProjectDiscipline.objects.all()
    return projectdiscipline


@register.simple_tag
def checkbrownfullfield(disciplinetypeid, id, projectid):
    disciplinetypeid = ProjectDevelopmentSubType.objects.filter(
        id=disciplinetypeid, project_id=projectid, status=1).first()
    if disciplinetypeid != None:
        fullfieldid = DevelopmentSubSubType.objects.filter(
            discipline_subtype_id=disciplinetypeid.id, disciplinesub_subtype_id=id, project_id=projectid, status=1).first()
        if fullfieldid != None:
            return fullfieldid.id
        else:
            return 0
    else:
        return 0


def get_browninfillwell(developmentid, development):
    wells = Well.objects.filter(development_type_id=developmentid, status=1)
    infillwell = wells.filter(well_name__iexact="Infill Wells")
    return infillwell


@register.simple_tag
def checkprojectbrowninfill(disciplinetypeid, wellid, projectid):
    disciplinetype_id = ProjectDevelopmentSubType.objects.filter(
        id=disciplinetypeid, project_id=projectid, status=1).first()
    if disciplinetype_id != None:
        infillwellcount = ProjectWellType.objects.filter(
            discipline_type_id=disciplinetype_id.id, welltype_id=wellid, project_id=projectid, status=1).first()
        if infillwellcount != None:
            return infillwellcount.id
        else:
            return 0
    else:
        return 0


@register.simple_tag
def checkbrownsubactivites(disciplinesubtypeid, subactid, projectid):
    disciplinetypeactid = DevelopmentSubSubType.objects.filter(
        project_id=projectid, disciplinesub_subtype_id=disciplinesubtypeid, status=1).first()
    disciplinesubact = DevelopmentSubTypeSub.objects.filter(
        project_id=projectid, disciplinesub_subtype_id=disciplinetypeactid.id, sub_subtype_sub_id=subactid, status=1)
    return disciplinesubact.count()


def get_browndrillwell(developmentid, development):
    wells = Well.objects.filter(development_type_id=developmentid, status=1)
    wellsub = wells.filter(well_name__iexact="Pilot Holes") | wells.filter(
        well_name__iexact="Development Wells") | wells.filter(well_name__iexact="Workovers/Well Intervention")
    return wellsub


def vendortaxdetails(vendorid, taxtype):
    if (taxtype == "owntax"):
        vendortax = VendorTaxDetails.objects.filter(
            vendor_id=vendorid, status=1)
        return vendortax
    else:
        vendortax = VendorCompanyTaxDetails.objects.filter(
            vendor_id=vendorid, Tax_Type=taxtype, status=1)
        return vendortax


def vendorbankdetails(vendorid, id):
    vendorbankdetails = BankDetails.objects.filter(
        vendor_id=vendorid, status=1)
    return vendorbankdetails

# @register.simple_tag


def checktypesserivcecount(vendorid, types):
    vendorservices = Vendorcompanyserviceinfo.objects.filter(
        vendor_id=vendorid, type_services__iexact=types, status=1)
    return vendorservices.count()


def vendorservicedetails(vendorid, type):
    vendorservices = Vendorcompanyserviceinfo.objects.filter(
        vendor_id=vendorid, type_services__iexact=type)
    return vendorservices


def vendorcontractfile(contractid, vendorid):
    vendorcontractfile = VendorFileUpload.objects.filter(
        contract_id=contractid, vendor_id=vendorid)
    return vendorcontractfile
# vendor tag


def checktime(time, companyid):
    if (time == None):
        return ''
    else:
        company_generalsetting = Settings.objects.filter(
            company_id=companyid).first()
        all_dateformat = {'dd-M-yy': "%d-%b-%Y", 'dd-mm-yy': "%d-%m-%Y", 'dd/mm/yy': "%d/%m/%Y",
                          'mm-dd-yy': '%m-%d-%Y', 'mm/dd/yy': '%m/%d/%Y', 'yy-mm-dd': '%Y-%m-%d', 'yy/mm/dd': '%Y/%m/%d'}

        for key, value in all_dateformat.items():
            if (key == company_generalsetting.dateformat):
                return time.strftime(value)
        # else:
        #     return time.strftime("%d-%b-%Y")
        #
        # else:
        #     return time.strftime("%d-%b-%Y")
    # if (company_generalsetting.dateformat ==)
    # time_string =
    # strftime("%Y-%m-%d %H:%M:%S")
    # return time


def currentdate(companyid, data):
    company_generalsetting = Settings.objects.filter(
        company_id=companyid).first()
    date_today = datetime.today()
    all_dateformat = {'dd-M-yy': "%d-%b-%Y", 'dd-mm-yy': "%d-%m-%Y", 'dd/mm/yy': "%d/%m/%Y",
                      'mm-dd-yy': '%m-%d-%Y', 'mm/dd/yy': '%m/%d/%Y', 'yy-mm-dd': '%Y-%m-%d', 'yy/mm/dd': '%Y/%m/%d'}
    for key, value in all_dateformat.items():
        if (key == company_generalsetting.dateformat):
            if (data == 'value'):
                return date_today.strftime(value)
            else:
                return value


def covert_datetime(vendorid, companyid):

    if (vendorid != None):
        company_generalsetting = Settings.objects.filter(
            company_id=companyid).first()
        all_dateformat = {'dd-M-yy': "%d-%b-%Y", 'dd-mm-yy': "%d-%m-%Y", 'dd/mm/yy': "%d/%m/%Y",
                          'mm-dd-yy': '%m-%d-%Y', 'mm/dd/yy': '%m/%d/%Y', 'yy-mm-dd': '%Y-%m-%d', 'yy/mm/dd': '%Y/%m/%d'}
        invite_vendor = VendorInvitationModel.objects.get(id=vendorid)
        a = invite_vendor.created_at
        return datetime.now().date()

@register.simple_tag
def checkcreate(userid, moduleid):
    module = Modules.objects.filter(module_name=moduleid).first()
    if module is None:
        return 0
        
    created = UserRights.objects.filter(user_id=userid, module_id=module.id).first()
    if created is not None and created.create is not None:
        return 1
    else:
        return 0

@register.simple_tag
def checkview(userid, moduleid):
    module = Modules.objects.filter(module_name=moduleid).first()
    if module is None:
        return 0  # Return 0 if the module doesn't exist

    created = UserRights.objects.filter(user_id=userid, module_id=module.id).first()
    if created is not None and created.view is not None:
        return 1
    else:
        return 0


@register.simple_tag
def checkedit(userid, moduleid):
    module = Modules.objects.filter(module_name=moduleid).first()
    if module is None:
        return 0  # Return 0 if the module doesn't exist

    created = UserRights.objects.filter(user_id=userid, module_id=module.id).first()
    if created is not None and created.edit is not None:
        return 1
    else:
        return 0


@register.simple_tag
def checkdelete(userid, moduleid):
    module = Modules.objects.filter(module_name=moduleid).first()
    if module is None:
        return 0  # Return 0 if the module doesn't exist

    created = UserRights.objects.filter(user_id=userid, module_id=module.id).first()
    if created is not None and created.delete is not None:
        return 1  # User has delete permission for the module
    else:
        return 0  # User doesn't have delete permission for the module



@register.simple_tag
def checkvendorapprove(userid, moduleid):
    module = Modules.objects.filter(module_name=moduleid).first()
    created = UserRights.objects.filter(
        user_id=userid, module_id=module.id).first()
    if created != None:
        if created.vendor_approve != None:
            return 1
        else:
            return 0
    else:
        return 0


@register.simple_tag
def checklock(userid, moduleid):
    module = Modules.objects.filter(module_name=moduleid).first()
    created = UserRights.objects.filter(
        user_id=userid, module_id=module.id).first()
    if created != None:
        if created.lock != None:
            return 1
        else:
            return 0
    else:
        return 0


@register.simple_tag
def checkunlock(userid, moduleid):
    module = Modules.objects.filter(module_name=moduleid).first()
    created = UserRights.objects.filter(
        user_id=userid, module_id=module.id).first()
    if created != None:
        if created.unlock != None:
            return 1
        else:
            return 0
    else:
        return 0


@register.simple_tag
def Checkprojectmastersallrights(userid, module):
    if UserRights.objects.filter(user_id=userid, module_id=module).filter(Q(create=1) | Q(view=1) | Q(delete=1) | Q(edit=1)):
        return 1
    else:
        return 0


@register.simple_tag
def Checkvendormastersallrights(userid, module):
    if UserRights.objects.filter(user_id=userid, module_id=module).filter(Q(create=1) | Q(view=1) | Q(delete=1) | Q(edit=1)):
        return 1
    else:
        return 0


@register.simple_tag
def Checkcontractmastersallrights(userid, module):
    if UserRights.objects.filter(user_id=userid, module_id=module).filter(Q(create=1) | Q(view=1) | Q(delete=1) | Q(edit=1)):
        return 1
    else:
        return 0


@register.simple_tag
def Checkcontractmastersallrightscreateoredit(userid, module):
    if UserRights.objects.filter(user_id=userid, module_id=module).filter(Q(create=1) | Q(edit=1)):
        return 1
    else:
        return 0


@register.simple_tag
def Checktaxmastersallrights(userid, module):
    if UserRights.objects.filter(user_id=userid, module_id=module).filter(Q(create=1) | Q(view=1) | Q(delete=1) | Q(edit=1)):
        return 1
    else:
        return 0


@register.simple_tag
def Checkbankinformationallrights(userid, module):
    if UserRights.objects.filter(user_id=userid, module_id=module).filter(Q(create=1) | Q(view=1) | Q(delete=1) | Q(edit=1)):
        return 1
    else:
        return 0


@register.simple_tag
def Checkcompanysignatorysettingsallrights(userid, module):
    if UserRights.objects.filter(user_id=userid, module_id=module).filter(Q(create=1) | Q(view=1) | Q(delete=1) | Q(edit=1)):
        return 1
    else:
        return 0


@register.simple_tag
def Checkprojectsallrights(userid, module):
    if UserRights.objects.filter(user_id=userid, module_id=module).filter(Q(create=1) | Q(view=1) | Q(delete=1) | Q(edit=1) | Q(lock=1) | Q(unlock=1)):
        return 1
    else:
        return 0


@register.simple_tag
def Checkvendorallrights(userid, module):
    if UserRights.objects.filter(user_id=userid, module_id=module).filter(Q(create=1) | Q(view=1) | Q(delete=1) | Q(edit=1) | Q(edit=1)):
        # | Q(vendor_approve=1)
        return 1
    else:
        return 0


@register.simple_tag
def Checkcostcodeallrights(userid, module):
    if UserRights.objects.filter(user_id=userid, module_id=module).filter(Q(create=1) | Q(view=1) | Q(delete=1) | Q(edit=1)):
        return 1
    else:
        return 0


@register.simple_tag
def Checkassigncostcoderights(userid, module):
    if UserRights.objects.filter(user_id=userid, module_id=module).filter(Q(create=1) | Q(view=1) | Q(delete=1) | Q(edit=1)):
        return 1
    else:
        return 0

@register.simple_tag
def getselectedcount(userid, module):
    moduleid = Modules.objects.filter(module_name=module).first()
    if UserRights.objects.filter(user_id=userid, module_id=moduleid.id).exclude(status__isnull=True):
        print('yes')
    else:
        print('no')
    return 0


def convertnum(data):
    if data:
        code = Basecountries.objects.get(id=data)
        num = code.phonecode
        x = re.findall("\+", num)
        if x:
            return num
        else:
            return '+'+num
    else:
        return ''


def Capwords(name):
    if (name):
        if "-" in name:
            c = name.title()
            names = c.replace("-", " & ")
            return names
        elif "_" in name:
            c = name.title()
            names = c.replace("_", " & ")
            return names
        else:
            return name.title()


def Userdesignation(designation):
    if (designation):
        return designation.title()
    else:
        return ''


@register.simple_tag
def convert_json(value):
    data = ''
    if (value != ''):
        data = ast.literal_eval(value)
        return data
    else:
        data


@register.simple_tag
def convert_jsonformat(value):
    data = ''
    if (value != ''):
        data = ast.literal_eval(value)
        return data
    else:
        data


@register.simple_tag
def convert_jsonformatforuser(value):
    data = ''
    if (value != ''):
        data = CompanyBankUser.objects.filter(companybank_id=value)
        return data, list(data.values_list('user_id', flat=True))

    else:
        data

# @register.simple_tag


def get_currencies(value, empty):
    if (value == '' or value == None):
        return empty
    else :
        currency = ast.literal_eval(value)
        currency = Basecountries.objects.filter(
            reduce(operator.or_, (Q(id__iexact=x) for x in currency)))
        return currency
   


def Dateformat(date):
    all_dateformat = {'dd-M-yy': 'DD-MMM-YYYY', 'dd-mm-yy': 'DD-MM-YYYY', 'dd/mm/yy': 'DD/MM/YYYY',
                      'mm-dd-yy': 'MM-DD-YYYY', 'mm/dd/yy': 'MM/DD/YYYY', 'yy-mm-dd': 'YYYY-MM-DD', 'yy/mm/dd': 'YYYY/MM/DD'}
    for key, value in all_dateformat.items():
        if (date == key):
            return value


def removeunderscore(value):
    data = value.replace('_', ' ')
    return data


@register.simple_tag
def getusers(id):
    users = User.objects.filter(id__in=(CompanyBankUser.objects.filter(
        companybank_id=id)).values_list('user', flat=True))
    return users
# user rights

# end user rights

# contract service masters


def servicecontract(vendorid, type):
    service = ContractMaster.objects.filter(
        contractvendor_id=vendorid, types_service=type, status=1)
    return service

@register.simple_tag
def get_contract(contract_id, type):
    service = ContractMaster.objects.filter(
        id=contract_id, types_service=type, status=1)
    return service


# contract service masters count
@register.simple_tag
def cheack_serviceademdmentcontract(contract_id , user_id):
    service= Amendment.objects.filter(service_id=contract_id, status=1).count()
    contract = ContractMaster.objects.filter(id=contract_id, status=1).first()
    contract_name=contract.name_service
    projects=contract.projects
    try:
        Project_discipline=convert_projectdiscipline(contract.projectdiscipline) 
    except:
        Project_discipline=''
    try:
        projectdiscipline_type=contract.projectdisciplinetype.discipline_subtype
    except:
        projectdiscipline_type=''
    Reference_Number=contract.reference_number
    Executed_Date=checktime(contract.executed_date ,user_id)
    
    try:
        Maximum_Value=f"{contract.currency.currency_symbol} {contract.amount}"
    except:
        Maximum_Value=''
    tax_id=contract.id
    type='original'
    wcc =contract.wcc
    if service !=0:
        
            latest_amendment = Amendment.objects.filter(service_id=contract_id,status=1).latest('id')
            try:
                discipline_type=contract.projectdisciplinetype.discipline_subtype
            except:
                discipline_type=''
            print(f'contract.name_service {latest_amendment.amendment_executed_date}, ')
            try:
                currency_symbol=f"{latest_amendment.amendment_currency.currency_symbol} {amount_convertion_to_separtors(latest_amendment.amendment_amount) }"
            except:
                currency_symbol=''
           
            data={
                    
                    'contract_name' :contract.name_service,
                    'projects' : contract.projects,
                    'Project_discipline' :convert_projectdiscipline(contract.projectdiscipline) ,
                    'projectdiscipline_type' :discipline_type,
                    'Reference_Number' : latest_amendment.amendment_reference_number,
                    'Executed_Date' : checktime(latest_amendment.amendment_executed_date, user_id ),
                    'Maximum_Value' : currency_symbol,
                    'tax_id': latest_amendment.id,
                    'type': 'amendment',
                    'wcc' :latest_amendment.wcc
                    
                }
            print(data["Executed_Date"])
            print('data',convert_projectdiscipline(contract.projectdiscipline) )
            return data
          
    else:
        try:
            Maximum_Value=f"{contract.currency.currency_symbol} {amount_convertion_to_separtors(contract.amount) }"
        except:
            Maximum_Value=''
        try:
            discipline_type=contract.projectdisciplinetype.discipline_subtype
        except:
            discipline_type=''
        data={
            
            'contract_name' :contract.name_service,
            'projects' : contract.projects,
            'Project_discipline' :convert_projectdiscipline(contract.projectdiscipline) ,
            'projectdiscipline_type' :discipline_type,
            'Reference_Number' : contract.reference_number,
            'Executed_Date' : checktime(contract.executed_date, user_id ),
            'Maximum_Value' : Maximum_Value,
            'tax_id': contract.id,
            'type': 'original',
            'wcc' :contract.wcc
        }
        

    
        return data
    
    
@register.simple_tag
def supply_amendments(contract_id):
    amendments = Amendment.objects.filter(service_id=contract_id)
    return amendments   

@register.simple_tag
def supply_amendments_count(contract_id):
    amendments = Amendment.objects.filter(service_id=contract_id).count()
    return amendments


def servicecontractcount(vendorid, type):
    service = ContractMaster.objects.filter(
        contractvendor_id=vendorid, types_service=type, status=1)
    return service.count()

def servicesubmitcontractcount(vendorid, type):
    service = ContractMaster.objects.filter(
        contractvendor_id=vendorid, types_service=type, status=1,save_type=2)
    return service.count()

@register.simple_tag
def serviceademdmentcontract(serviceid):
    serviceademdment = Amendment.objects.filter(service_id=serviceid, status=1)
    return serviceademdment


def serviceademdmentcontractpdf(serviceid):
    serviceademdment = Amendment.objects.filter(service_id=serviceid, status=1).exclude(Q(amendment_reference_number__exact='') | Q(amendment_executed_date__isnull=True) | Q(amendment_amount__exact='') | Q(amendment_amount__isnull=True) | Q(
        amendment_upload_contract__exact='') | Q(amendment_upload_contract__isnull=True) | Q(amendment_upload_pricetable__exact='') | Q(amendment_upload_pricetable__isnull=True) | Q(amendment_currency_id__isnull=True))
    return serviceademdment


def serviceademdmentcontractcount(serviceid):
    serviceademdment = Amendment.objects.filter(service_id=serviceid, status=0)
    return serviceademdment.count()

# contract supply masters


def supplycontract(vendorid, type):
    supply = ContractMaster.objects.filter(
        contractvendor_id=vendorid, types_service=type, status=1)
    return supply
# contract service masters count


def supplycontractcount(vendorid, type):
    supply = ContractMaster.objects.filter(
        contractvendor_id=vendorid, types_service=type, status=1)
    return supply.count()

def supplysubmitcontractcount(vendorid, type):
    supply = ContractMaster.objects.filter(
        contractvendor_id=vendorid, types_service=type, status=1,save_type=2)
    return supply.count()


def supplyademdmentcontract(serviceid):
    serviceademdment = Amendment.objects.filter(service_id=serviceid, status=1)
    return serviceademdment


def supplyademdmentcontractcount(serviceid):
    serviceademdment = Amendment.objects.filter(service_id=serviceid, status=1)
    return serviceademdment.count()

# contract servicesupply masters


def servicesupplycontract(vendorid, type):

    servicesupply = ContractMaster.objects.filter(
        contractvendor_id=vendorid, types_service=type, status=1)
    return servicesupply
# contract service masters count


def servicesupplycontractcount(vendorid, type):
    servicesupply = ContractMaster.objects.filter(
        contractvendor_id=vendorid, types_service=type, status=1)
    return servicesupply.count()

def servicesupplysubmitcontractcount(vendorid, type):
    servicesupply = ContractMaster.objects.filter(
        contractvendor_id=vendorid, types_service=type, status=1,save_type=2)
    return servicesupply.count()

def servicesupplyademdmentcontract(serviceid):
    serviceademdment = Amendment.objects.filter(service_id=serviceid, status=1)
    return serviceademdment


def servicesupplyademdmentcontractcount(serviceid):
    serviceademdment = Amendment.objects.filter(service_id=serviceid, status=1)
    return serviceademdment.count()


@register.simple_tag
def checkcontracts_vendor(vendor_id):
    vendor_contracts = ContractMaster.objects.filter(
        contractvendor_id=vendor_id, status=1).count()
    return vendor_contracts


@register.simple_tag
def checkvendorexistscompany(vendorname, companyid):
    if (vendorname != None):
        if ContractMasterVendor.objects.filter(vendor_name__exact=vendorname, company_id=companyid, status=1).exists():
            return 1
        else:
            return 0
    else:
        return 0


@register.simple_tag
def CheckVendoremail(email, companyid):
    if (email != None):
        if User.objects.filter(email__exact=email, company_id=companyid, status=1).exists():
            return 1
        else:
            return 0
    else:
        return 0


def amountseperator(amount):
    if amount:
        if re.search(r'(?i)no max limit', str(amount)):
            return "No Max Limit"
        else:
            return "{:,}".format(amount)
    else:
        return ''


@register.simple_tag
def GetUserImage(userid):
    if User.objects.filter(id=userid).filter(Q(image__isnull=True) | Q(image='')):
        imageurl = ''
    else:
        userdata = User.objects.filter(id=userid).first()
        imageurl = userdata.image.url
    return imageurl


@register.simple_tag
def GetCompanyImage(companyid):
    if Companies.objects.filter(id=companyid).filter(Q(image__isnull=True) | Q(image='')):
        imageurl = ''
    else:
        userdata = Companies.objects.filter(id=companyid).first()
        imageurl = userdata.image.url
    return imageurl


def convertcompanytimezone(time, companyid):
    if (time != None):
        company_generalsetting = Settings.objects.filter(
            company_id=companyid).first()
        dt_object = datetime.fromtimestamp(float(time))
        dateonly = dt_object.date()
        all_dateformat = {'dd-M-yy': "%d-%b-%Y", 'dd-mm-yy': "%d-%m-%Y", 'dd/mm/yy': "%d/%m/%Y",
                          'mm-dd-yy': '%m-%d-%Y', 'mm/dd/yy': '%m/%d/%Y', 'yy-mm-dd': '%Y-%m-%d', 'yy/mm/dd': '%Y/%m/%d'}
        if company_generalsetting.dateformat in all_dateformat:
            get_value = all_dateformat[company_generalsetting.dateformat]
            change_dateformat = datetime.strftime(dateonly, get_value)
            return change_dateformat
        else:
            get_value = "%d-%b-%Y"
            change_dateformat = datetime.strftime(dateonly, get_value)
            return change_dateformat


def convert_contract_date(time, companyid):
    if (time != None):
        change_time = json.loads(time)
        remove_t = change_time.replace('T', ' ')
        company_generalsetting = Settings.objects.filter(
            company_id=companyid).first()
        date_string = change_time
        possible_formats = ["%d-%b-%Y", "%d-%m-%Y", "%d/%m/%Y", '%m-%d-%Y', '%m/%d/%Y', '%Y-%m-%d', '%Y/%m/%d', "%d-%b-%Y %H:%M:%S",
                            "%d-%m-%Y %H:%M:%S", "%d/%m/%Y %H:%M:%S", '%m-%d-%Y %H:%M:%S', '%m/%d/%Y %H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S']
        for fmt in possible_formats:
            try:
                date_obj = datetime.strptime(date_string, fmt)
                break
            except ValueError:
                pass
        else:
            print("Could not determine date format")
        dt_object = datetime.strptime(str(change_time), fmt)
        dateonly = dt_object.date()
        all_dateformat = {'dd-M-yy': "%d-%b-%Y", 'dd-mm-yy': "%d-%m-%Y", 'dd/mm/yy': "%d/%m/%Y",
                          'mm-dd-yy': '%m-%d-%Y', 'mm/dd/yy': '%m/%d/%Y', 'yy-mm-dd': '%Y-%m-%d', 'yy/mm/dd': '%Y/%m/%d'}
        if company_generalsetting.dateformat in all_dateformat:
            get_value = all_dateformat[company_generalsetting.dateformat]
            change_dateformat = datetime.strftime(dateonly, get_value)
            return change_dateformat
        else:
            get_value = "%d-%b-%Y"
            change_dateformat = datetime.strftime(dateonly, get_value)
            return change_dateformat
    else:
        return ''


@register.simple_tag
def checkvendorcontractexistscompany(contractname, company):
    if (ContractMaster.objects.filter(company_id=company, reference_number__exact=contractname, status=1).exists()):
        return 1
    else:
        return 0


@register.simple_tag
def checkfile(file):
    if (file != '' and file != None):
        return 1
    else:
        return 0


def getcontractamendment(contractid):
    amendments = Amendment.objects.filter(service_id=contractid, status=1)
    get_files = amendments.filter(
        Q(amendment_upload_contract='') | Q(amendment_upload_pricetable=''))
    return get_files


def getvendornamebyamenment(amenment_id):
    vendor_name = Amendment.objects.filter(id=amenment_id, status=1).values_list(
        'contractvendor__vendor_name', flat=True).first()
    return vendor_name


@register.filter
def SignatoryUser(signatory_id):
    return SignatoriesUsers.objects.filter(signatory_id=signatory_id)


@register.filter
def no_of_users(signatory_id):
    return SignatoriesUsers.objects.filter(signatory_id=signatory_id).count()


def split_addspace(value):
    try:
        split_word = wrap(value, 14)
        addspace = " ".join(split_word)
        return addspace
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def split_addspaces(value):
    split_word = wrap(str(value), 14)
    addspace = " ".join(split_word)
    return addspace


@register.simple_tag
def vendoremailvalidation(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (re.fullmatch(regex, email)):
        return 0
    else:
        return 1


@register.filter
def split_by_space(number):
    add_space = str(number)
    new_space = add_space.split(',')
    new_number = ',\n'.join(map(str, new_space))
    return new_number


def convert_projectdiscipline(value):
    if (value != None):
        convert_title = value.development_type.cluster.environment.field.field.field_name.title()
        types = value.development_type.cluster.clustersubname.cluster_subname.title()
        if (value.project_discipline == '1'):
            return 'Green Field Development-'+convert_title + '-' + types
        elif (value.project_discipline == '2'):
            return 'Brown Field Development-'+convert_title + '-' + types
        elif (value.project_discipline == '3'):
            return 'Others-'+convert_title + '-' + types
    else:
        return ''
    
      


@register.simple_tag
def checknotapplicable(contractid, companyid, taxtype):
    taxcount = VendorCompanyTaxDetails.objects.filter(
        Tax_Type=taxtype, contract_id=contractid, company_id=companyid, status=1, tax_id=None).first()
    if (taxcount != None):
        name = "not_applicable"
    else:
        name = ""
    return name


@register.simple_tag
def checknotamendmentapplicable(contractid, companyid, taxtype):
    taxcount = VendorCompanyTaxDetails.objects.filter(
        Tax_Type=taxtype, amendment_id=contractid, company_id=companyid, status=1, tax_id=None).first()
    if (taxcount != None):
        name = "not_applicable"
    else:
        name = ""
    return name


def taxwithpercentage(taxid):
    taxes = VendorCompanyTaxPercentage.objects.filter(
        vendortax_id=taxid, status=1)
    return taxes


def converttime(value):
    conv = datetime.fromtimestamp(int(value))
    fmt = '%d/%m/%Y %H:%M'
    utc = conv.replace(tzinfo=pytz.UTC)
    localtz = utc.astimezone(timezone.get_current_timezone())
    System_time = datetime.now()
    return localtz.strftime(fmt)


def filecomma(value):
    getvalue = json.loads(value)
    list_com = [i for i in getvalue if i != ""]
    if (len(list_com) > 0):
        getfile = Fileupload.objects.filter(id__in=list_com)
        return getfile
    else:
        return '12'


def showsendername(value):
    username = User.objects.get(id=value)
    return username.name+' '+username.lastname


@register.simple_tag
def vendor_detail(vin_number):
    get_vendor = ContractMasterVendor.objects.filter(
        vin=vin_number, status=1).first()
    if get_vendor != None:
        return get_vendor
    else:
        return ''


def check_contract_invoice(contract_id, type):
    if (type == 'vendor'):
        get_invoice = Invoice.objects.filter(
            vendor_id=contract_id, status=1).count()
    else:
        get_invoice = Invoice.objects.filter(
            contractid=contract_id, contracttype=type, status=1).count()
    return get_invoice


def check_contract_tax(contract_id, type):
    if (type == 'original'):
        get_contract_tax = VendorCompanyTaxDetails.objects.filter(
            contract_id=contract_id, status=1).count()
    else:
        get_contract_tax = VendorCompanyTaxDetails.objects.filter(
            amendment_id=contract_id, status=1).count()
    return get_contract_tax


def checkeditcontractinvoice(contract_id, contract_type):
    try:
        get_invoice = Invoice.objects.filter(
            contractid=contract_id, contracttype=contract_type, status=1).count()
        contract_type = contract_type.lower()
        if (contract_type == 'original'):
            get_amendment_ids = list(Amendment.objects.filter(
                service_id=contract_id, status=1).values_list('id', flat=True))
            get_amendment_invoice = Invoice.objects.filter(
                contractid__in=get_amendment_ids, contracttype__startswith='a', status=1).count()
            if (get_invoice > 0):
                data = get_invoice
            elif (get_amendment_invoice > 0):
                data = get_invoice
            else:
                data = 0
        else:
            data = get_invoice
        return data
    except:
        data=0
        return data


@register.simple_tag
def geturlname(value):

    # if (value != None):
    # data=value.get('data')
    # geturl=ast.literal_eval(data)
    # return geturl.get('url')
    return ""


def get_history_file(history_id):
    payment_files = PaymentHistoryFile.objects.filter(
        payment_history=history_id, status=1)
    return payment_files


def get_count(count):
    return count


register.filter('get_count', get_count)


@register.simple_tag
def show_date_format(date, hours, minutes):
    convert_date = date.strftime('%d-%b-%Y')
    convert_time = (date + timedelta(hours=int(hours),
                    minutes=int(minutes))).strftime('%I:%M %p')
    return f'{convert_date} {convert_time}'


def checkprojectexists(project_masterid, company):
    project_count = Projectcreation.objects.filter(
        company=company, projectname_id=project_masterid, status=0).count()
    return project_count


@register.filter(name='checkInvoiceExists')
def checkInvoiceExists(contract_id, contract_type):
    if contract_type == 'original':
        invoice_status = Invoice.objects.filter(
            contractid=contract_id, contracttype__startswith='o', status=1).count()
    else:

        invoice_status = Invoice.objects.filter(
            contractid=contract_id, contracttype__startswith='a', status=1).count()
    return invoice_status


@register.simple_tag
def get_phone_number(phone_number):
    if phone_number == None:
        return
    else:
        phone = Basecountries.objects.filter(id=phone_number).values_list('phonecode', flat=True).first()
        if '+' not in phone:
            phone = f'+{phone}'
        return phone if phone else ''


def replacecommaid(id):
    if (id != ''):
        con_str = str(id)
        return con_str.replace(',', '')
    else:
        return ''


@register.filter(name='get_dept_name')
def get_dept_name(id):
    if id != None:
        value = UserDepartment.objects.get(id=id)
        return value
    else:
        return None


@register.filter(name='increment')
def increment(value):
    return value + 1

def check_for_condition(value1, value2):
    print('******************************')
    if value1 =="":
        print("yes")
    
    print("value1 ",value1)
    print("value2 ",value2)
    print('******************************')
    if (value1 != None and value2 != None ) and (value1 != "" and value2 != ""):
        if value1 == value2 :
            return_status = True
        elif int(value1) == int(value2) :
            return_status = True
        else :
            return_status = False
    else :
        return_status = False

    return return_status


@register.filter(name='users_in_project')
def users_in_project(project_id, request):
    get_user = ProjectUser.objects.filter(project_id=project_id, status='True').values_list(
        'user_id', flat=True).exclude(user_id=request.user.id)
    list_data = []
    for i in list(get_user):
        get_users_in_project = User.objects.get(id=i)
        list_data.append(get_users_in_project)
    return list_data


@register.simple_tag
def filter_by_project(project_id, request, user):
    # get_project=ProjectUser.objects.filter(project_id=project_id,status=True).values_list('user_id',flat=True)
    # filter_user = User.objects.filter(roles_id__in=[2,3],status=1,company=request.company).exclude(id__in=get_project)
    filter_user = User.objects.filter(
        roles_id__in=[2, 3], status=1, company=request.company).exclude(id=user)
    return filter_user


@register.simple_tag
def getAllCostCodeType(company):
    get_cost_type_list = LevelMaster.objects.filter_company(company.id, 1)
    return get_cost_type_list


@register.simple_tag
def getvendordata(vin):
    vendorid = ContractMasterVendor.objects.filter(vin=vin).first()
    return vendorid


@register.simple_tag
def replace_func(value, old, new):
    return value.replace(old, new)


@register.simple_tag
def checkwccapproval(user_id, status):
    return WccStationUsers.objects.filter_by_user(user_id, status).count()


@register.simple_tag
def getcountwccflow(id):
    countwcc = WccPerStation.objects.filter(project=id, status=1)
    return countwcc.count()


@register.simple_tag
def getcountinvoiceflow(id):
    countinvoice = Projectcreation.objects.filter(id=id).exclude(flow=None)
    return countinvoice.count()


@register.simple_tag
def checkpendingwcc(request, status):
    wcc_ids = list(WorkCompletionCost.objects.get_wcc_approval_check(
        status,0,request.company,).values_list('id', flat=True))
    return wcc_ids


@register.simple_tag
def get_bankcount(id):
    variables = CompanyBank.objects.filter(bank_name_id=id, status=1).exists()
    return variables


@register.simple_tag
def getusers(id):
    userlist = CompanyBankUser.objects.filter(companybank_id=id, status=True)
    return userlist


@register.simple_tag
def getstarredreport(companyid):
    starredlist = starredreport.objects.filter(company_id=companyid)
    return starredlist


register.filter('replacecommaid', replacecommaid)
# invoice
register.filter('checkprojectexists', checkprojectexists)
# register.filter('show_date_format',show_date_format)
register.filter('showsendername', showsendername)
register.filter('check_contract_invoice', check_contract_invoice)
register.filter('check_contract_tax', check_contract_tax)
register.filter('checkeditcontractinvoice', checkeditcontractinvoice)
register.filter('get_history_file', get_history_file)

register.filter('currentdate', currentdate)
register.filter('converttime', converttime)
register.filter('filecomma', filecomma)
register.filter('taxwithpercentage', taxwithpercentage)
# contract master
register.filter('convert_projectdiscipline', convert_projectdiscipline)
register.filter('split_addspace', split_addspace)
register.filter('split_addspaces', split_addspaces)
register.filter('disciplines_replace_cap', disciplines_replace_cap)
register.filter('supplycontract', supplycontract)
register.filter('supplycontractcount', supplycontractcount)
register.filter('supplysubmitcontractcount', supplysubmitcontractcount)
register.filter('supplyademdmentcontract', supplyademdmentcontract)
register.filter('supplyademdmentcontractcount', supplyademdmentcontractcount)
register.filter('amountseperator', amountseperator)
register.filter('convert_contract_date', convert_contract_date)
register.filter('getcontractamendment', getcontractamendment)
register.filter('getvendornamebyamenment', getvendornamebyamenment)

register.filter('servicecontract', servicecontract)
register.filter('servicecontractcount', servicecontractcount)
register.filter('servicesubmitcontractcount', servicesubmitcontractcount)
register.filter('serviceademdmentcontract', serviceademdmentcontract)
register.filter('serviceademdmentcontractpdf', serviceademdmentcontractpdf)
register.filter('serviceademdmentcontractcount', serviceademdmentcontractcount)

register.filter('servicesupplycontract', servicesupplycontract)
register.filter('servicesupplycontractcount', servicesupplycontractcount)
register.filter('servicesupplysubmitcontractcount', servicesupplysubmitcontractcount)
register.filter('servicesupplyademdmentcontract',
                servicesupplyademdmentcontract)
register.filter('servicesupplyademdmentcontractcount',
                servicesupplyademdmentcontractcount)


# vendor view
register.filter('vendortaxdetails', vendortaxdetails)
register.filter('vendorbankdetails', vendorbankdetails)
register.filter('vendorservicedetails', vendorservicedetails)
register.filter('vendorcontractfile', vendorcontractfile)
register.filter('checktime', checktime)
register.filter('convertnum', convertnum)
register.filter('Capwords', Capwords)
register.filter('Userdesignation', Userdesignation)
register.filter('get_currencies', get_currencies)
register.filter('Dateformat', Dateformat)
register.filter('removeunderscore', removeunderscore)
register.filter('checktypesserivcecount', checktypesserivcecount)
register.filter('covert_datetime', covert_datetime)
register.filter('convertcompanytimezone', convertcompanytimezone)
# end vendor view

# project creation
register.filter('getprojectdiscipline', getprojectdiscipline)

register.filter('checkentitytype', checkentitytype)
register.filter('category_replace', category_replace)
register.filter("getenvironmentcluster", getenvironmentcluster)
register.filter('checkprojectcountry', checkprojectcountry)
register.filter('checkmasterproject', checkmasterproject)
register.filter('checkprojectblock', checkprojectblock)
register.filter('project_block', project_block)
register.filter('checkprojectfield', checkprojectfield)
register.filter('checkprojectfieldid', checkprojectfieldid)
register.filter('checkprojectenvironment', checkprojectenvironment)
register.filter('checkprojectenvironmentid', checkprojectenvironmentid)
register.filter('getprojectcluster', getprojectcluster)
register.filter('checkprojectcluster', checkprojectcluster)
register.filter('getprojectdevelopment', getprojectdevelopment)
register.filter('developcount', developcount)
register.filter('checkprojectdevelopment', checkprojectdevelopment)
register.filter('checkprojectdiscipline', checkprojectdiscipline)
register.filter('projectdisciplinetype', projectdisciplinetype)
register.filter('checkprojectdisciplinetype', checkprojectdisciplinetype)
register.filter('getdisciplineactivity', getdisciplineactivity)
register.filter('checkprojectdisciplineactivity',
                checkprojectdisciplineactivity)
register.filter('getdisciplinesubactivity', getdisciplinesubactivity)
# register.filter('checkdisciplinesubactivites',checkdisciplinesubactivites)
register.filter('checkothersubactivites', checkothersubactivites)
register.filter('datacount', datacount)
register.filter('getwellsub', getwellsub)
register.filter('get_browninfillwell', get_browninfillwell)
register.filter('get_browndrillwell', get_browndrillwell)

# end project creation edit

# master project
register.filter('cap_wells', cap_wells)
register.filter('wellname', wellname)
register.filter('get_project', get_project)
register.filter('get_block', get_block)
register.filter('get_field', get_field)
register.filter('get_clusters', get_clusters)
register.filter('get_clustersub', get_clustersub)
register.filter('get_well', get_well)
register.filter('get_subwell', get_subwell)
register.filter('checkstatuscluster', checkstatuscluster)
register.filter('getclustersub', getclustersub)
register.filter('checkbolckhasfield', checkbolckhasfield)
register.filter('checkfieldhascluster', checkfieldhascluster)
register.filter('checkclusterhasclustername', checkclusterhasclustername)
register.filter('checkclustercount', checkclustercount)
register.filter('checkclusterhasdevelopmenttype',
                checkclusterhasdevelopmenttype)
register.filter('replace_development', replace_development)
register.filter('checkdevelopmenttype', checkdevelopmenttype)
register.filter('getwellnamecount', getwellnamecount)
register.filter('getwellname', getwellname)
register.filter('get_projecttype', get_projecttype)
register.filter('get_projectblock', get_projectblock)
register.filter('get_projectfield', get_projectfield)
register.filter('get_development', get_development)
register.filter('get_development_type', get_development_type)
register.filter('get_developmentcount', get_developmentcount)
register.filter('checkdevelopmenthaswell', checkdevelopmenthaswell)
register.filter('get_deveploment_subtype', get_deveploment_subtype)
register.filter('get_deveplomentsub_subtype', get_deveplomentsub_subtype)
register.filter('get_subtypes_sub', get_subtypes_sub)
# register.filter('get_projectclusters', get_projectclusters)
# register.filter('get_projectwells', get_projectwells)
register.filter('replace_dev', replace_dev)
register.filter('get_environment', get_environment)
register.filter('checkfieldenvironment', checkfieldenvironment)
register.filter('fieldenvironment', fieldenvironment)
register.filter('Otherenvironment', Otherenvironment)
register.filter('modify_name', modify_name)
register.filter('getfieldenvironment', getfieldenvironment)
register.filter('check_for_condition', check_for_condition)
# end master project


@register.simple_tag
def checkCostCodePdf(request):
    print('count', CostCodeType.objects.filter_by_company(
        1, request.company).count())
    return CostCodeType.objects.filter_by_company(1, request.company).count()


@register.filter
def get_file_name(file_name):
    get_file = DisputedQueryFiles.objects.filter(
        disputedquery_id=file_name).first()
    print(f'get_file {get_file}')
    document_name = ''
    if get_file != None:
        document_name = get_file.document_name
        if document_name == None:
            document_name = ''
    print(f'{document_name} document_name')
    return document_name


@register.simple_tag
def get_files(id, request):
    get_files = DisputedQueryFiles.objects.filter(disputedquery_id=id)
    return get_files


@register.simple_tag
def get_total_credit_val(invoice_cost, request, invoice_id, usage_status):
    print(f'invoice_id {invoice_id}')
    if usage_status == 1:
        usage_status = [1]
    elif usage_status == 2:
        usage_status = [1, 2]
    else:
        usage_status = []
    get_invoice = Invoice.objects.get_by_id(invoice_id)
    # CreditNoteInvoice.objects.filter(credit__contract_id=get_invoice.contractid,status=1,credit__usage_status__in=[1,2])
    # print(f'get_invoice {get_invoice}')
    get_credit = CreditNoteInvoice.objects.filter(
        invoice_id=invoice_id, status=1, credit__credit_status=2, credit__usage_status__in=usage_status, credit__approval_status=4)
    get_credit_note = CreditNoteContractInvoice.objects.filter(credit_id__in=list(get_credit.values_list(
        'credit_id', flat=True)), vendor_split_invoice__currency_id=invoice_cost.currency_id, credit_id__credit_status=2)
    credit_val = 0
    for credit in get_credit_note:
        if credit.new_netpayable != None:
            print(f'credit {credit.new_netpayable}')
            get_invoice = convert_val_to_float(credit.new_netpayable)
            credit_val += float(get_invoice)
        else:
            credit_val += 0
    # print(f'vendor_split_invoice__currency_id {credit_val}')
    return round_of_two_values(credit_val)


def convert_val_to_float(string_val):
    match = ''.join(filter(lambda x: x.isdigit() or x == '.', string_val))
    get_invoice = round_of_two_values(float(match))
    return get_invoice


@register.simple_tag
def get_net_payableamount(inv_amount, cr_amount):
    inv_amount=str(inv_amount)
    invoice = float(
        ''.join(filter(lambda x: x.isdigit() or x == '.', inv_amount)))
    credit_note = float(
        ''.join(filter(lambda x: x.isdigit() or x == '.', cr_amount)))
    if (credit_note > invoice):
        final_value = 0
    else:
        final_value = invoice-credit_note
        # print(f'final_value {final_value}')
    # print(f'invoice {invoice}, credit_note {credit_note}')
    return new_round_of_two_values(float(final_value))


def convert_to_digit(string_val):
    match = ''.join(filter(str.isdigit, string_val))
    get_invoice = "{:.2f}".format(float(match))
    return get_invoice


@register.simple_tag
def get_credit_investment(invoice_cost, request):
    # print(f' invoice_cost {invoice_cost}')
    get_credit = CreditNoteMappingBase.objects.filter(
        invoice_id=invoice_cost.invoice_id, status=True, invoice_split_id=invoice_cost.vendor_invoice_id)
    amount_used = 0
    for used_credits in get_credit:
        amount_used += float(used_credits.credit_payable)
    # credit_datas=list(get_credit.values_list('credit_note_id',flat=True).distinct())
    get_org_credit = list(CreditNoteInvoice.objects.filter(invoice_id=invoice_cost.invoice_id, credit__usage_status=1,
                          credit__credit_status=2, credit__approval_status=4).values_list('credit_id', flat=True))
    # credit_datas.extend(get_org_credit)
    contract_credit = CreditNoteContractInvoice.objects.filter(
        credit_id__in=get_org_credit, vendor_split_invoice_id=invoice_cost.vendor_invoice_id, credit_id__credit_status=2, status=True, credit__usage_status=1)
    if contract_credit.count() > 0:
        for current_credit in contract_credit:
            used_val = 0
            if (CreditNoteMappingBase.objects.filter(credit_note_split_id=current_credit.id).exists()):
                get_pending_val = CreditNoteMappingBase.objects.filter(
                    credit_note_split_id=current_credit.id, credit_note_id=current_credit.credit_id)
                for used_amount in get_pending_val:
                    used_val += float(used_amount.credit_payable)
                amount_used += float(convert_val_to_float(
                    current_credit.new_netpayable))-used_val
            else:
                amount_used += float(convert_val_to_float(
                    current_credit.new_netpayable))

    # total_amount=0
    # for i in contract_credit:
    #     pending_val=CreditNoteMappingBase.objects.filter(credit_note_split_id=i.id,status=True,invoice_split_id=invoice_cost.vendor_invoice_id)
    #     # print(f'pending_val {pending_val}')
    #     for v in pending_val:
    #         if v:
    #             total_amount+=int(float(v.credit_payable))
    #         # else:
    #         #     total_amount+=int(convert_to_float(i.payment_currency_amount))
    #     total_amount=int(convert_to_float(i.payment_currency_amount))-total_amount
    #     currently_used=get_credit.filter(credit_note_split_id=i.id,invoice_split_id=invoice_cost.vendor_invoice_id)
    #     # print(f'currently_used {currently_used}')
    #     # total_amount-=int(convert_to_float(i.payment_currency_amount))
    # print(f'total_amount {total_amount}')

    return "{:,}".format(int(amount_used))


@register.simple_tag
def get_balance_credit_val(invoice_amount, credit_note):
    invoice_amount=str(invoice_amount)
    invoice = float(convert_val_to_float(invoice_amount))
    credit_note = float(convert_val_to_float(credit_note))
    if (credit_note > invoice):
        final_value = credit_note-invoice
    else:
        final_value = 0
    print(f'invoice {invoice}, credit_note {credit_note}')
    return '{:,}'.format(float(final_value))

# @register.simple_tag
# def get_initial_credit_balance(invoice_amount,credit_amount):
#     return 0


def convert_to_float(string_val):
    string_val=str(string_val)
    match = ''.join(filter(str.isdigit, string_val))
    # get_invoice="{:.2f}".format(float(match))
    return float(match)


@register.simple_tag
def Checkdynamicrights(userid, module, *args):
    count = 0
    for arg in args:
        query = Q(**{arg: 1})
        if UserRights.objects.filter(user_id=userid, module_id=module).filter(query):
            count += 1
    return count


@register.simple_tag
def checkwcccontract(user):
    vendor_data = vendor_detail(user.cin_number)
    contractlist = ContractMaster.objects.getcontractmaster(vendor_data.id).filter(wcc=1)
    if contractlist.count() == 0:
        contractlist=Amendment.objects.filter(contractvendor_id=vendor_data.id,status=1 ,wcc=1 ,save_type=2)
    
    return contractlist.count()


@register.simple_tag
def checkforbankuser(company):
    bank_user = 0
    if company:
        try:
            check_for_user = Settings.objects.get(company_id=company.id)
            bank_user = check_for_user.bank_user
        except:
            bank_user = 0
    return bank_user

def add_months(date_string, add_month):
    # Try parsing the input date string with various common date formats
    common_formats = ['%d-%b-%Y', '%d-%m-%Y', '%d/%m/%Y', '%m-%d-%Y', '%m/%d/%Y', '%Y/%m/%d' ,'%Y-%m-%d']
    parsed_date = None
    original_format = None
    for fmt in common_formats:
        try:
            parsed_date = datetime.strptime(date_string, fmt)
            original_format = fmt
            break
        except ValueError:
            continue
    
    if parsed_date is None:
        raise ValueError("Could not parse the date string")

    # Add the specified number of months to the parsed date
    new_date = parsed_date + timedelta(days=30.44 * add_month)
    # Convert the new date to the original format
    formatted_new_date = new_date.strftime(original_format)
    return formatted_new_date


@register.filter
def renival_date(num, data):
    try:
        if data:
            date= date=data.user.company.invoicedate 
            company_id=data.user.company.id
            settin=Settings.objects.filter(company_id=company_id).first()
            date_format=settin.dateformat
            print("date",date_format)
        else:
            pass
    
        if num:
            if num == 1 or num == '1':
                if data:
                    add_month=1
                    date=data.user.company.invoicedate 
                    new_datetime = add_months(date, add_month)
                    return new_datetime
                else:
                    return ''
            else:
                if date:
                    add_month=12
                    date=data.user.company.invoicedate 
                    new_datetime = add_months(date, add_month)
                    return new_datetime
                else:
                    pass
        else:
            return ''
    except:
        return ''
    
@register.filter
def get_country_by_pro(request):
    company_id = request.company.id

    # Retrieve distinct country IDs associated with active projects for the company
    country_ids = list(Projectcreation.objects.filter(
        company_id=company_id, status=0
    ).values_list("country_id", flat=True).distinct())

    # Retrieve country objects based on the IDs obtained
    country_objects = Countries.objects.filter(id__in=country_ids)

    # Return a dictionary containing country names and IDs
    return {"country_names": country_objects, 'country_ids': country_ids}


@register.filter
def get_project_by_pro(request):
    company_id = request.company.id

    # Retrieve distinct country IDs associated with active projects for the company
    total_project = list(Projectcreation.objects.filter(
        company_id=company_id, status=0
    ).values_list("id", flat=True).distinct())
    active_project = list(Projectcreation.objects.filter(
        company_id=company_id, status=0, active_status=True
    ).values_list("id", flat=True).distinct())

    inactive_project = list(Projectcreation.objects.filter(
        company_id=company_id, status=0, active_status=False
    ).values_list("id", flat=True).distinct())

    return {"total_project": len(total_project), 'active_project': len(active_project), 'inactive_project': len(inactive_project)}


@register.filter
def get_vendors(request):
    company_id = request.company.id

    total_vendor = list(User.objects.filter(
        company_id=company_id, designation_role='Vendor').values_list("id", flat=True).distinct())
    active_vendor = list(User.objects.filter(
        company_id=company_id, designation_role='Vendor', is_active=True).values_list("id", flat=True).distinct())
    Inactive_vendor = list(User.objects.filter(
        company_id=company_id, designation_role='Vendor', is_active=False).values_list("id", flat=True).distinct())

    return {"total_vendor": len(total_vendor), 'active_vendor': len(active_vendor), 'Inactive_vendor': len(Inactive_vendor)}


@register.filter
def awar_contracts(request):
    company_id = request.company.id

    total_contract = list(ContractMaster.objects.filter(
        company_id=company_id).values_list("id", flat=True).distinct())

    active_contract = list(ContractMaster.objects.filter(
        company_id=company_id, status=True).values_list("id", flat=True).distinct())
    Inactive_contract = list(ContractMaster.objects.filter(
        company_id=company_id, status=False).values_list("id", flat=True).distinct())

    print(total_contract)
    return {"total_contract": len(total_contract), 'active_contract': len(active_contract), 'Inactive_contract': len(Inactive_contract)}
    
@register.simple_tag
def Checkprojectuser(request):
    projectuser=ProjectUser.objects.filter(company=request.company,user_id=request.user.id,project__status=0).count()
    return projectuser


@register.simple_tag
def getActionContract(contractid):
    get_contract=ContractMaster.objects.filter(id=contractid).first()
    contract_edit=0
    edit_ammendment=0
    amendment_id=None
    try:
        editcontract_possiblities=get_contract.save_type
        if editcontract_possiblities == 1:
            contract_edit=1
        else:
            contract_edit=0
    except:
        contract_edit=0
    if contract_edit == 0:
        try:
            amendment_check=Amendment.objects.filter(service_id=contractid).latest('id')
            if amendment_check.save_type == 1:
                edit_ammendment=1
                amendment_id=amendment_check.id
            elif amendment_check.save_type == 2:
                edit_ammendment=2
            else:
                edit_ammendment=0
        except:
            return
    print(f'edit_ammendment {edit_ammendment}, contract_edit {contract_edit}, amendment_id {amendment_id}')
    return {'contract_edit': contract_edit, 'edit_ammendment': edit_ammendment,'amendment_id':amendment_id}

@register.simple_tag
def get_contract_file(id,contracttype,filetype):
    if contracttype== 'Amendment' or contracttype== 'Addendum':
        files=VendorContractPriceTable.objects.filter(amendment_addendum_id=id,file_type=filetype,status=1)
        file_count=files.count()
        
        return files,file_count
    else:
        files=VendorContractPriceTable.objects.filter(contract_id=id,file_type=filetype,status=1)
        file_count=files.count()
        print('file_count',file_count)
        return files,file_count
    
    
@register.filter
def amount_convertion_to_separtors(amount):
    try:
        if amount.strip() != '' and amount != "No Max Limit":
            base_amount=convert_to_int(amount)
            formatted_amount = new_round_of_two_values(base_amount)

            formatted_amount = formatted_amount.replace(",", ",,").replace(",", ",,")

            return new_round_of_two_values(base_amount)
        elif amount == "No Max Limit":
            return "No Max Limit"
        else:
            return 0
    except:
        return ''
        

@register.simple_tag
def check_for_amendment(contract_id,request):
    try:
        total_amendments=Amendment.objects.filter(service_id=contract_id,company_id=request.company.id).count()
        return total_amendments
    except:
        total_amendments=0
        return total_amendments

@register.filter(name='convert_date_format')
def convert_date_format(value):
    try:
        # Define possible date formats
        possible_formats = ["%d-%b-%y", "%d-%m-%y", "%d/%m/%y", "%m-%d-%y", "%m/%d/%y", "%Y-%m-%d", "%y/%m/%d"]

        # Attempt to parse the date using each format
        for fmt in possible_formats:
            try:
                date_obj = datetime.strptime(value, fmt)
                return date_obj.strftime("%m-%d-%Y")
            except ValueError:
                continue 
        return '' 
    except Exception as e:
        return ''  


@register.simple_tag
def new_contract_file(contract,contracttype,filetype):
    if contracttype== 'Amendment' or contracttype== 'Addendum' or contracttype== 'amendment' or contracttype== 'addendum' :
        # files=VendorContractPriceTable.objects.filter(amendment_addendum_id=id,file_type=filetype,status=1)
        files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.service_id,filetype).values()
        file_count=files.count()
        return files,file_count
    else:
        # files=VendorContractPriceTable.objects.filter(contract_id=id,file_type=filetype,status=1)
        files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.id,filetype).values()
        file_count=files.count()
        return files,file_count
    
    
    
@register.simple_tag
def get_net_payamount(netamount, total_credit):
    if isinstance(netamount, dict):
        net_payment = netamount.get('netpayment', 0)
    print(f'total_credit {total_credit}')
    net_payment = netamount.get('netpayment', 0)
    total_credit = float(total_credit.replace(',', ''))
    net_payable_amount = net_payment - total_credit
    formatted_net_payable = new_round_of_two_values(net_payable_amount)
    return formatted_net_payable



@register.simple_tag
def get_tax_withcredit(total_credit, exclusive_value):
    # Remove commas from the strings and convert to float
    total_credit = float(total_credit.replace(',', ''))
    exclusive_value = float(exclusive_value.replace(',', ''))
    total_amount = total_credit + exclusive_value
    return "{:,}".format((total_amount))

@register.simple_tag
def new_credit_investment(invoice_cost, request):
    # print(f' invoice_cost {invoice_cost}')
    get_credit = CreditNoteMappingBase.objects.filter(invoice_id=invoice_cost.invoice_id, status=True, invoice_split_id=invoice_cost.vendor_invoice_id)
    getexchangetype=check_exchage_value(invoice_cost.invoice_id)
    amount_used = 0
    exchange_rate=0
    exclusive_tax=0
    for used_credits in get_credit:

        # print('-------------------------------------------------------------------------')
        # print('-------------------------------------------------------------------------')
        if getexchangetype == 1 or getexchangetype == '1':
            exchange_rate=used_credits.credit_note_split.exchange_rate
            netpayable= float(used_credits.credit_payable)
        else :
            exchange_rate =check_exchage_percentage(used_credits.invoice_id , used_credits.invoice_split.id)
            if exchange_rate == 'N/A':
                exchange_rate=1
            netpayable = float(used_credits.credit_payable)*float(exchange_rate)
        
        
        
        if exchange_rate == 'N/A':
            exchange_rate=1
        
        # ex_calc=(float(used_credits.credit_note_split.percentage)*float(used_credits.credit_note_split.credit.exclusive_value))/100
        # exclusive_tax +=(float(ex_calc)*float(exchange_rate))
            
        ex_calc=creaditenote_gross_amount(used_credits.credit_note.total_value, used_credits.credit_note_split.percentage , used_credits.credit_note_split.exchange_rate)
        credite_exclusive_percentage=CreditNoteExclusive.objects.filter(credit_id=used_credits.credit_note.id).values_list('exclusive_percentage', flat=True)
        for exc in list(credite_exclusive_percentage):
            exc_value=round_of_two_values(float(ex_calc)*float(exc)/100)
            exclusive_tax += float(exc_value)
            print(exc_value)    
            
        amount_used += netpayable
        
        
        
        # print('percentage ', float(used_credits.credit_note_split.percentage))
        # print('exclusive ', used_credits.credit_note_split.credit.exclusive_value)
        # # print('ex_calc ',ex_calc)
        # print('credit_payable ',used_credits.credit_payable)
        # print('exclusive_tax ',exclusive_tax)
        # print('getexchangetype ',getexchangetype)
        # print('amount_used ',amount_used)


        # print('-------------------------------------------------------------------------')
        # print('-------------------------------------------------------------------------')

    # credit_datas=list(get_credit.values_list('credit_note_id',flat=True).distinct())

    total=amount_used +exclusive_tax
    get_org_credit = list(CreditNoteInvoice.objects.filter(invoice_id=invoice_cost.invoice_id, credit__usage_status=1,
                          credit__credit_status=2, credit__approval_status=4).values_list('credit_id', flat=True))
    # credit_datas.extend(get_org_credit)
    contract_credit = CreditNoteContractInvoice.objects.filter(
        credit_id__in=get_org_credit, vendor_split_invoice_id=invoice_cost.vendor_invoice_id, credit_id__credit_status=2, status=True, credit__usage_status=1)
    if contract_credit.count() > 0:
        # print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        # print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        # print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        for current_credit in contract_credit:
            used_val = 0
            if (CreditNoteMappingBase.objects.filter(credit_note_split_id=current_credit.id).exists()):
                get_pending_val = CreditNoteMappingBase.objects.filter(
                    credit_note_split_id=current_credit.id, credit_note_id=current_credit.credit_id)
                for used_amount in get_pending_val:
                    used_val += float(used_amount.credit_payable)
                amount_used += float(convert_val_to_float(
                    current_credit.new_netpayable))-used_val
            else:
                amount_used += float(convert_val_to_float(
                    current_credit.new_netpayable))

    return new_round_of_two_values(float(total))

@register.simple_tag
def new_total_credit_val(invoice_cost, request, invoice_id, usage_status):
    if usage_status == 1:
        usage_status = [1]
    elif usage_status == 2:
        usage_status = [1, 2]
    else:
        usage_status = []
    ex_calc=0
    exchange_rate=0
    get_invoice = Invoice.objects.get_by_id(invoice_id)
    getexchangetype=check_exchage_value(invoice_id)
    # CreditNoteInvoice.objects.filter(credit__contract_id=get_invoice.contractid,status=1,credit__usage_status__in=[1,2])
    # print(f'get_invoice {get_invoice}')
    get_credit = CreditNoteInvoice.objects.filter(
        invoice_id=invoice_id, status=1, credit__credit_status=2, credit__usage_status__in=usage_status, credit__approval_status=4)
    get_credit_note = CreditNoteContractInvoice.objects.filter(credit_id__in=list(get_credit.values_list(
        'credit_id', flat=True)), vendor_split_invoice__currency_id=invoice_cost.currency_id, credit_id__credit_status=2)
    credit_val = 0
    exclusive_tax=0
    for credit in get_credit_note:
        if credit.new_netpayable != None:
            

            if getexchangetype ==  1 or getexchangetype == '1':
                exchange_rate =credit.exchange_rate
                get_invoice = convert_val_to_float(credit.new_netpayable)
                
            else :
                exchange_rate =check_exchage_percentage(invoice_id , credit.vendor_split_invoice.id)
                if exchange_rate == 'N/A':
                    exchange_rate=1
                netamount = convert_val_to_float(credit.new_netpayable)
                get_invoice = float(round_of_two_values(netamount))*float(round_of_two_values(exchange_rate))
                
            
            if exchange_rate == 'N/A':
                exchange_rate=1
            # ex_calc=round_of_two_values((float(credit.percentage)*float(round_of_two_values(credit.credit.exclusive_value)))/100)
            # exclusive_tax +=(float(ex_calc)*float(exchange_rate))
            ex_calc=creaditenote_gross_amount(credit.credit.total_value,credit.percentage , credit.exchange_rate)
            credite_exclusive_percentage=CreditNoteExclusive.objects.filter(credit_id=credit.credit.id).values_list('exclusive_percentage', flat=True)
            for exc in list(credite_exclusive_percentage):
                exc_value=round_of_two_values(float(ex_calc)*float(exc)/100)
                exclusive_tax += float(exc_value)
            
            credit_val += float(get_invoice)    
            
               

        else:
            credit_val += 0

    
    total=float(round_of_two_values(credit_val+exclusive_tax))
    
   
    return new_round_of_two_values(total)


@register.simple_tag
def check_exchage_value(pk):
    pass
    contractid=Invoice.objects.get_by_id(pk)
    getvendordetails=ContractMasterVendor.objects.filter(id=contractid.vendor.id,status=1).first()
    if (contractid.contracttype == 'original'):
        contract=ContractMaster.objects.filter(id=contractid.contractid ,status=1).first()
        vendorinvoice=VendorInvoiceSplit.objects.filter(vendor_id=getvendordetails.id,contract_id=contract.id,status=1)
    else:
        contract=Amendment.objects.filter(id=contractid.contractid ,status=1).first()
        vendorinvoice=VendorInvoiceSplit.objects.filter(vendor_id=getvendordetails.id,amendment_id=contract.id,status=1)

    getexchangetype=vendorinvoice.first()
      # Initialize with a default value
    exchange_type = None
    if getexchangetype is not None:
        exchange_type = getexchangetype.exchange_rate
    
    return exchange_type
    
@register.simple_tag
def check_exchage_percentage(pk , vendorsplit):
    
    invoice_cost=InvoiceCostInvoice.objects.filter(invoice_id = pk ,vendor_invoice_id=vendorsplit , status=1 ).first()
    if invoice_cost is not None:
        return invoice_cost.invoice_exchange_rate
    else :
        return 'N/A'


@register.simple_tag   
def check_querylist(contract_id , contractype):
    if contractype == 'original':
        check_status=CheckVendorContract.objects.filter(contract_id=contract_id , status=1).count()
    else :
        check_status=CheckVendorContract.objects.filter(amendment_id=contract_id, status=1).count()
    
    
    return check_status

@register.simple_tag   
def getcontractdetails(pk,vendor_id):
    contract=ContractMaster.objects.filter(id=pk,contractvendor_id=vendor_id ,status=1).first()

