from .models import *
from .parser import parseXML
from collections import Counter,namedtuple
import re 
import xml.etree.ElementTree as ET
import operator
import math
from django.contrib.messages.storage.base import LEVEL_TAGS

# Define Component Levels
UserInterface_L1 = ['Button','CheckBox','DatePicker','Image','Label','ListPicker','ListView',
                    'Notifier','Slider','Spinner','TextBox','TimePicker']
UserInterface_L2 = ['PasswordTextBox','WebViewer']
Layout_L1 = ['HorizontalArrangement','HorizontalScrollArrangement','TableArrangement',
             'VerticalArrangement','VerticalScrollArrangement']
Media_L1 = ['ImagePicker']
Media_L2 = ['Camcorder','Camera','Player','Sound','SoundRecorder','SpeechRecognizer',
            'TextToSpeech','VideoPlayer','YandexTranslate']
Drawing_L1 = ['Ball','Canvas','ImageSprite']
Sensors_L1 =['Clock']
Sensors_L2 = ['AccelerometerSensor','BarcodeScanner','OrientationSensor','Pedometer']
Sensors_L3 = ['GyroscopeSensor','LocationSensor','NearField','ProximitySensor'] 
Social_L2 = ['ContactPicker','EmailPicker','PhoneCall','PhoneNumberPicker','Sharing','Texting,','Twitter']
Storage_L2 = ['File','TinyDB']
Storage_L3 = ['FusionTablesControl','TinyWebDB']
Connectivity_L2 = ['ActivityStarter','BluetoothClient']
Connectivity_L3 = ['BluethoothServer','Web']
Lego_L3 = ['NctDrive','NctColorSensor','NxtLightSensor','NxtSoundSensor','NxtTouchSensor',
           'NxtUltrasonicSensor','NxtDirectCommands','Ev3Motors','Ev3ColorSensor','Ev3GyroSensor',
           'Ev3TouchSensor','Ev3UltrasonicSensor','Ev3Sound','Ev3UI','Ev3Commands']
Experimental_L3 = ['FirebaseDB']


def countBlocks (root,namespace,tag,*args):
    '''
        Count the number of tag elements in the root tree

        Inputs: 
            - root (ElementTree)
            - namespace (dict)
            - tag (str)
            - args [0]: component_type/type (str)
            - args [1]: type = .... (str)
     
        Output: 
            - count_blocks (int)
    '''
    if len(args) == 0:
        expr = '{' +namespace['xmlns'] + '}'+ tag
    else:
        expr = '{' +namespace['xmlns'] + '}'+ tag +'[@'+args[0]+'="'+args[1]+'"]'
    
    count_blocks = len(root.findall('.//'+ expr))
    
    #for element in root.findall('.//{http://www.w3.org/1999/xhtml}block'):
        #count_blocks= count_blocks + 1
        #print element.tag
    
    return count_blocks

def lookForBlocks(root,namespace,tag,type,list):
    '''
        Look for blocks inside the tree using a search list

        Inputs: 
            - root (ElementTree)
            - namespace (dict)
            - tag (str): mutation/block
            - type (str): component_type
            - list (list): component types to look for
     
        Output: 
            - list_found (list): contains the number of components founded
    '''
    
    list_found = [0 for x in range(len(list))] # Empty list to save the number of components founded
    
    for l in range(len(list_found)):
        list_found[l] = countBlocks(root,namespace,tag,type,list[l])
    
    return list_found

def listOfTypes(root,namespace,tag,type):
    '''
        List of tag elements in the root tree to look for specific attributes

        Inputs: 
            - root (ElementTree)
            - namespace (dict)
            - type (str)
     
        Output: 
            - List of attributes(list)
    '''

    expr = '{' +namespace['xmlns'] + '}'+ tag + '[@'+type+']'
    myList = root.findall('.//'+ expr)
    
    myTypeList = [] # Empy List
    for l in myList:
        myTypeList.append(l.attrib[type])

    return myTypeList

def flow_control(root,namespace,typeList):
    '''
        Assign the Flow Control skill result
    
       Inputs: 
            - root (ElementTree)
            - namespace (dict)
            - typeList (list)
     
        Output: 
            - results (dict):{'Score','Component_Events','Control'}
    '''

    '''c_forRange = countBlocks(root,namespace,'block','type','controls_forRange')
    c_while = countBlocks(root,namespace,'block','type','controls_while')
    c_forEach = countBlocks(root,namespace,'block','type','controls_forEach')
    c_if = countBlocks(root,namespace,'block','type','controls_if')
    c_choose = countBlocks(root,namespace,'block','type','controls_choose')
    c_do_then_return = countBlocks(root,namespace,'block','type','controls_do_then_return')'''

    # component_event, controls_ 
    r = re.compile('^component_event$')
    FC1 = filter(r.match,typeList)
    r = re.compile('^controls_')
    FC2 = filter(r.match,typeList)

    # Count the number of occurrences for every level
    c1 = dict(Counter(FC1))
    c2 = dict(Counter(FC2))
    
    if len(c1.keys()) > 0 and len(c2.keys()) > 0 :
        score = 3
    elif  len(c1.keys()) > 0 or len(c2.keys()) > 0:
        score = 2
    else:
        score = 1
        
    results = {'Score':score,
               'Component_Events': c1,
               'Control': c2}
    
    return results

def data_control(root,namespace,typeList):
    '''
        Assign the Data representation skill result
        
        Inputs: 
            - root (ElementTree)
            - namespace (dict)
            - typeList (list)
     
        Output: 
            - results (dict): {'Score','Lists','ComponenSet'}
            
                 
    '''
    '''list_Id = ['lists_create_with','lists_add_items','lists_is_in','lists_length','lists_is_empty',
             'lists_pick_random_item','lists_remove_item','lists_lookup_in_pairs',
             'lists_position_in','lists_append_list','lists_select_item','lists_insert_item',
             'lists_copy','lists_is_list','lists_to_csv_row','lists_replace_item',
             'lists_to_csv_table','lists_from_csv_row','lists_from_csv_table']
    
    set_Id = ['lexical_variable_set']
    
    modif_Id = ['component_set_get']'''
    
     # lists_ + modification + set
    r = re.compile('^lists_')
    FC1 = filter(r.match,typeList)
    r = re.compile('^component_set_get$')
    FC2 = filter(r.match,typeList)
    
    # Count the number of occurrences for every type
    c1 = dict(Counter(FC1))
    c2 = dict(Counter(FC2))
    
    if len(c1.keys()) > 0 and len(c2.keys()) > 0 :
        score = 3
    elif len(c1.keys()) > 0 or len(c2.keys()) > 0 :
        score = 2
    else:
        score = 1
        
    results = {'Score':score,
               'Lists': c1,
               'ComponenSet':c2}
    
    return results
    
def variable_control(root,namespace,typeList):
    '''
        Assign the Variable Control skill result
    
       Inputs: 
            - root (ElementTree)
            - namespace (dict)
            - typeList (list)
     
        Output: 
            - results (dict): {'Score',Variable','Math','Text}
    '''
    
    variable_Id = ['global_declaration','lexical_variable_get','lexical_variable_set',
                   'local_declaration_statement','local_declaration_expression']
    
    # component_event, controls_ 
    FC1 = lookForBlocks(root,namespace,'block','type',variable_Id)
    r = re.compile('^math_')
    FC2 = filter(r.match,typeList)
    r = re.compile('^text_')
    FC3 = filter(r.match,typeList)

    # Count the number of occurrences for every level
    c1 = {'variable':sum(FC1)}
    c2 = dict(Counter(FC2))
    c3 = dict(Counter(FC3))
    if c1['variable']> 0 and (len(c2.keys()) > 0 or len(c3.keys()) > 0) :
        score = 3
    elif c1['variable']> 0 or (len(c2.keys()) > 0 or len(c3.keys()))> 0 :
        score = 2
    else:
        score = 1
        
    results = {'Score':score,
               'Variable': c1,
               'Math': c2,
               'Text':c3}
    
    return results

def generalization_control(root,namespace,typeList):
    '''
        Assign the Generalization Control skill result
    
       Inputs: 
            - root (ElementTree)
            - namespace (dict)
            - typeList (list)
     
        Output: 
            - results (dict): {'Score',Procedures','Generalization'}
    
    
    procedures_Id = ['procedures_defreturn','procedures_defnoreturn','procedures_callreturn]
    generalization_Id: is_generic = True inside Mutation
    '''
    
    # 
    r = re.compile('^procedures_')
    FC1 = filter(r.match,typeList)
    FC2 = lookForBlocks(root,namespace,'mutation','is_generic',['true'])

    # Count the number of occurrences for every characteristic
    c1 = dict(Counter(FC1))
    c2 = {'generic':sum(FC2)}
    
    
    if len(c1.keys())>0 and c2['generic']> 0 :
        score = 3
    elif len(c1.keys())>0:
        score = 2
    else:
        score = 1
        
    results = {'Score':score,
               'Procs': c1,
               'Generic': c2}
    
    return results    

def programmingLevels_Score(root,namespace):
    
    '''
        Assign the Programmning skill result
        
        Inputs: 
            - root (ElementTree)
            - namespace (dict)
     
        Output: 
            - score (dict)
            
        Flow Control and Logic
        Data management
        Variable representation
        Generalization (procedures + generalization) 
                 
    '''
    
    typeList = listOfTypes(root,namespace,'block','type')
    
    # Flow Control levels: component_event + control_ /control_/None
    flowCtrl = flow_control(root,namespace,typeList)
    # Data Control levels: lists_ + modification /list |modification_identifier/None
    dataCtrl = data_control(root,namespace,typeList)
    # Variable Control levels: Variables+Math+Text / Math |Text / None
    variableCtrl = variable_control(root,namespace,typeList)
    # Generalization Control levels: procedures + generic_action / procedures / None
    generalizationCtrl = generalization_control(root,namespace,typeList)

    results = {'Flow': flowCtrl,
               'Data': dataCtrl,
               'Variable': variableCtrl,
               'Generalization': generalizationCtrl}
    
    return results

def componentLevels_Score (root,namespace):
    '''
        Assign the Blocks used skill result
        
        Inputs: 
            - root (ElementTree)
            - namespace (dict)
     
        Output: 
            - results (dict): {'Score','L1_components','L2_components','L3_components'}
              
        3 Points: Sensors_L3,Storage_L3,Connectivity_L3,Lego_L3, Experimental_L3
        2 Points:  UserInterface_L2, Sensors_L2, Social_L2,Storage_L2,Connectivity_L2 
        1 Point: UserInterface_L1,Layout_L1,Media_L1,Media_L2,Drawing_L1,Sensors_L1
        
    '''
    UserInterface_L1_found = lookForBlocks(root,namespace,'mutation','component_type',UserInterface_L1)
    UserInterface_L2_found = lookForBlocks(root,namespace,'mutation','component_type',UserInterface_L2)
    Layout_L1_found = lookForBlocks(root,namespace,'mutation','component_type',Layout_L1)
    Media_L1_found = lookForBlocks(root,namespace,'mutation','component_type',Media_L1)
    Media_L2_found  = lookForBlocks(root,namespace,'mutation','component_type',Media_L2)
    Drawing_L1_found = lookForBlocks(root,namespace,'mutation','component_type',Drawing_L1)
    Sensors_L1_found = lookForBlocks(root,namespace,'mutation','component_type',Sensors_L1)
    Sensors_L2_found  = lookForBlocks(root,namespace,'mutation','component_type',Sensors_L2)
    Sensors_L3_found  = lookForBlocks(root,namespace,'mutation','component_type',Sensors_L3)
    Social_L2_found = lookForBlocks(root,namespace,'mutation','component_type',Social_L2)
    Storage_L2_found  = lookForBlocks(root,namespace,'mutation','component_type',Storage_L2)
    Storage_L3_found = lookForBlocks(root,namespace,'mutation','component_type',Storage_L3)
    Connectivity_L2_found  = lookForBlocks(root,namespace,'mutation','component_type',Connectivity_L2)
    Connectivity_L3_found  = lookForBlocks(root,namespace,'mutation','component_type',Connectivity_L3)
    Lego_L3_found  = lookForBlocks(root,namespace,'mutation','component_type',Lego_L3)
    Experimental_L3_found  = lookForBlocks(root,namespace,'mutation','component_type',Experimental_L3)

    L1_found = {'UserInterface': UserInterface_L1_found,
                'Layout': Layout_L1_found,
                'Media': Media_L1_found,
                'Drawing': Drawing_L1_found,
                'Sensors': Sensors_L1_found}
    
    L2_found = {'UserInterface': UserInterface_L2_found,
                'Media': Media_L2_found,
                'Sensors': Sensors_L2_found,
                'Social': Social_L2_found,
                'Storage': Storage_L2_found,
                'Connectivity':Connectivity_L2_found}
    
    L3_found = {'Sensors': Sensors_L3_found,
                'Storage': Storage_L3_found,
                'Connectivity':Connectivity_L3_found,
                'Lego':Lego_L3_found,
                'Experimental':Experimental_L3_found}
    
    # Count the number of occurrences for every level
    c1 = 0
    for c in L1_found:
        c1 = c1 + sum(L1_found[c])
    c2 = 0
    for c in L2_found:
        c2 = c2 + sum(L2_found[c])  
    c3 = 0
    for c in L3_found:
        c3 = c3 + sum(L3_found[c]) 

    if c3 > 0 :
        score = 3
    elif c2 > 0:
        score = 2
    else: # Low score for simple programs
        score = 1
    
    results = {'Score':score,
               'L1_components':L1_found,
               'L2_components': L2_found,
               'L3_components': L3_found}
    
    return results

def returnUnion(values1,values2,option):
    '''
       Giving two lists returns the union of them 
        
        Inputs: 
            - values1 (dict)
            - values2 (dict)
            - option: 0 = dictionaries with lists, 1 = dictioaries with no list
     
        Output: 
            - unionResult (dict)   
    '''
    if option == 0:
        v_keys = values1.keys() # Both dicts have the same keys
        unionResult = {}
        for k in range(len(v_keys)):
            k1 = values1[v_keys[k]]
            k2 = values1[v_keys[k]]
            unionResult[v_keys[k]] = map(operator.add,k1,k2)
            
    elif option == 1:
       v_keys = values1.keys() # Both dicts have the same keys
       unionResult = {}
       for k in range(len(v_keys)):
            k1 = values1[v_keys[k]]
            k2 = values1[v_keys[k]]
            unionResult[v_keys[k]] = k1+k2

    return unionResult

def nScreens_control(scrN):
    '''
        Assign the Screens schedule skill result
        
        Inputs: 
            - scrN (int)
     
        Output: 
            - score (int)            
    '''
    if scrN > 1 and scrN < 3:
        score = 2 # Notes, Watch, Calc
    elif scrN >= 3 and scrN < 10:
        score = 3 # Twitter, FB, Instagram
    else:
        score = 1 # More complexity, less usability OR too simply
    
    return score

def getScore (prjScreens):
    
    p = prjScreens.values_list('scrID',flat=True)
    
    generalScore = {}
    
    for scr in prjScreens.values_list('scrID',flat=True):

        scrXML= prjScreens.get(scrID = scr).bky
        
        root = parseXML(scrXML) # ElementTree
        namespace = {'xmlns': root.tag.split('}',1)[0][1:]} # Namespace of the xml http://www.w3.org/1999/xhtml
        
        count_blocks = countBlocks(root,namespace,'block')
        
        # Blocks used skill result (dict)
        componentLevels = componentLevels_Score(root,namespace)
        
        # Programming skills results 
        programmingLevels = programmingLevels_Score(root,namespace)
            
        if len(generalScore.keys()) > 0:
            # Screen <> 1 : Only if the score is better, we update the General Results
            
            # ComponentLevels: {'Score','L1_components','L2_components','L3_components'}
            if componentLevels['Score'] > generalScore['ComponentLevels']['Score']:
                # Update
                generalScore['ComponentLevels']['Score'] = componentLevels['Score']
            
            # In every case we update the components info
            G1 = generalScore['ComponentLevels']['L1_components']
            S1 = componentLevels['L1_components']
            generalScore['ComponentLevels']['L1_components'] = returnUnion(G1,S1,0)  
            
            G2 = generalScore['ComponentLevels']['L2_components']
            S2 = componentLevels['L2_components']
            generalScore['ComponentLevels']['L2_components'] = returnUnion(G2,S2,0)  
             
            G3 = generalScore['ComponentLevels']['L3_components']
            S3 = componentLevels['L3_components']
            generalScore['ComponentLevels']['L3_components'] = returnUnion(G3,S3,0)  
            
            # ProgrammingLevels: {'Flow','Data','Variable','Generalization'}
            if programmingLevels['Flow']['Score']> generalScore['ProgrammingLevels']['Flow']['Score']:
                # Update
                generalScore['ProgrammingLevels']['Flow']['Score'] = programmingLevels['Flow']['Score']
            # In every case we update the components info
            G1 = generalScore['ProgrammingLevels']['Flow']['Component_Events']
            S1 = programmingLevels['Flow']['Component_Events']
            generalScore['ProgrammingLevels']['Flow']['Component_Events'] = returnUnion(G1,S1,1) 
            
            G2 = generalScore['ProgrammingLevels']['Flow']['Control']
            S2 = programmingLevels['Flow']['Control']
            generalScore['ProgrammingLevels']['Flow']['Control'] = returnUnion(G2,S2,1) 
            
            if programmingLevels['Data']['Score']> generalScore['ProgrammingLevels']['Data']['Score']:
                # Update
                generalScore['ProgrammingLevels']['Data']['Score'] = programmingLevels['Data']['Score']
            # In every case we update the components info
            G1 = generalScore['ProgrammingLevels']['Data']['Lists']
            S1 = programmingLevels['Data']['Lists']
            generalScore['ProgrammingLevels']['Data']['Lists'] = returnUnion(G1,S1,1) 
            
            G2 = generalScore['ProgrammingLevels']['Data']['ComponenSet']
            S2 = programmingLevels['Data']['ComponenSet']
            generalScore['ProgrammingLevels']['Data']['ComponenSet'] = returnUnion(G2,S2,1)            
            
            if programmingLevels['Variable']['Score']> generalScore['ProgrammingLevels']['Variable']['Score']:
                # Update
                generalScore['ProgrammingLevels']['Variable']['Score'] = programmingLevels['Variable']['Score']
            # In every case we update the components info
            G1 = generalScore['ProgrammingLevels']['Variable']['Variable']
            S1 = programmingLevels['Variable']['Variable']
            generalScore['ProgrammingLevels']['Variable']['Variable'] = returnUnion(G1,S1,1) 
            
            G2 = generalScore['ProgrammingLevels']['Variable']['Math']
            S2 = programmingLevels['Variable']['Math']
            generalScore['ProgrammingLevels']['Variable']['Math'] = returnUnion(G2,S2,1)    
        
            G3 = generalScore['ProgrammingLevels']['Variable']['Text']
            S3 = programmingLevels['Variable']['Text']
            generalScore['ProgrammingLevels']['Variable']['Text'] = returnUnion(G3,S3,1)            

            if programmingLevels['Generalization']['Score']> generalScore['ProgrammingLevels']['Generalization']['Score']:
                # Update
                generalScore['ProgrammingLevels']['Generalization']['Score'] = programmingLevels['Generalization']['Score']
            # In every case we update the components info
            G1 = generalScore['ProgrammingLevels']['Generalization']['Procs']
            S1 = programmingLevels['Generalization']['Procs']
            generalScore['ProgrammingLevels']['Generalization']['Procs'] = returnUnion(G1,S1,1) 
            
            G2 = generalScore['ProgrammingLevels']['Generalization']['Generic']
            S2 = programmingLevels['Generalization']['Generic']
            generalScore['ProgrammingLevels']['Generalization']['Generic'] = returnUnion(G2,S2,1) 
  
        else:
            #Screen == 1 
            generalScore = {'ComponentLevels':componentLevels,
                            'ProgrammingLevels': programmingLevels}

    # Here we have a generalScore with almost all the info of the program  
    # ComponentLevels: {'Score','L1_components','L2_components','L3_components'}
    # ProgrammingLevels: {'Flow','Data','Variable','Generalization'} -> No Score!
    progScores = [generalScore['ProgrammingLevels']['Flow']['Score'],
                 generalScore['ProgrammingLevels']['Data']['Score'],
                 generalScore['ProgrammingLevels']['Variable']['Score'],
                 generalScore['ProgrammingLevels']['Generalization']['Score']]
    generalScore['ProgrammingLevels']['Score'] = int(round(sum(progScores)/float(len(progScores))))
    
    # Finally, we calculate the Screen Control score  
    scrN = len(p)
    generalScore['ScreensLevels']={'Screens': scrN,
                                  'Score': nScreens_control(scrN)}
    
    # And the general Score!
    # ComponentLevels 45% ProgrammingLevels 45% ScreensLevels 10%
    generalScore['Score'] = int(round(generalScore['ComponentLevels']['Score']*0.45 + 
                                      generalScore['ProgrammingLevels']['Score']*0.45 + 
                                      generalScore['ScreensLevels']['Score']*0.1))
    
        
    return generalScore

