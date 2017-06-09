from scoreMyApp import *


def getScoreMsgsComponents(score,type):
    if type == 3:
        comp_score_info1 = 'To reach this score you have used these <strong>high </strong>level components:'
        # Create the list with the components used
        comp_score_info2 = [] # Initialize
        complevel = score['ComponentLevels']['L3_components']['Sensors']
        if sum(complevel) > 0:
            list = [i for i, e in enumerate(complevel) if e != 0]
            list2 = [Sensors_L3[i] for i in list]
            info = '<strong>Sensors:</strong> ' + ",".join(list2)
            comp_score_info2.append(info)
            
        complevel = score['ComponentLevels']['L3_components']['Storage']
        if sum(complevel) > 0:
            list = [i for i, e in enumerate(complevel) if e != 0]
            list2 = [Storage_L3[i] for i in list]
            info = '<strong>Storage:</strong> ' + ",".join(list2)
            comp_score_info2.append(info)
            
        complevel = score['ComponentLevels']['L3_components']['Connectivity']
        if sum(complevel) > 0:
            list = [i for i, e in enumerate(complevel) if e != 0]
            list2 = [Connectivity_L3[i] for i in list]
            info = '<strong>Connectivity:</strong> ' + ",".join(list2)
            comp_score_info2.append(info)
            
        complevel = score['ComponentLevels']['L3_components']['Lego']
        if sum(complevel) > 0:
            list = [i for i, e in enumerate(complevel) if e != 0]
            list2 = [Lego_L3[i] for i in list]
            info = '<strong>Lego:</strong> ' + ",".join(list2)
            comp_score_info2.append(info)      
                      
        complevel = score['ComponentLevels']['L3_components']['Experimental']
        if sum(complevel) > 0:
            list = [i for i, e in enumerate(complevel) if e != 0]
            list2 = [Experimental_L3[i] for i in list]
            info = '<strong>Experimental:</strong> ' + ",".join(list2)
            comp_score_info2.append(info)     
        comp_score_info3 = 'Unless you have the highest score, you can improve your app including components with medium or low level'
    
    elif type == 2:

        comp_score_info1 = 'To reach this score you have used these <strong>medium</strong> level components:'
           # Create the list with the components used
        comp_score_info2 = [] # Initialize
        complevel = score['ComponentLevels']['L2_components']['UserInterface']
        if sum(complevel) > 0:
            list = [i for i, e in enumerate(complevel) if e != 0]
            list2 = [UserInterface_L2[i] for i in list]
            info = '<strong>UserInterface:</strong> ' + ",".join(list2)
            comp_score_info2.append(info)
            
        complevel = score['ComponentLevels']['L2_components']['Media']
        if sum(complevel) > 0:
            list = [i for i, e in enumerate(complevel) if e != 0]
            list2 = [Media_L2[i] for i in list]
            info = '<strong>Media:</strong> ' + ",".join(list2)
            comp_score_info2.append(info)
            
        complevel = score['ComponentLevels']['L2_components']['Sensors']
        if sum(complevel) > 0:
            list = [i for i, e in enumerate(complevel) if e != 0]
            list2 = [Sensors_L2[i] for i in list]
            info = '<strong>Sensors: </strong>' + ",".join(list2)
            comp_score_info2.append(info)
            
        complevel = score['ComponentLevels']['L2_components']['Social']
        if sum(complevel) > 0:
            list = [i for i, e in enumerate(complevel) if e != 0]
            list2 = [Social_L2[i] for i in list]
            info = '<strong>Social:</strong> ' + ",".join(list2)
            comp_score_info2.append(info)      
                      
        complevel = score['ComponentLevels']['L2_components']['Storage']
        if sum(complevel) > 0:
            list = [i for i, e in enumerate(complevel) if e != 0]
            list2 = [Storage_L2[i] for i in list]
            info = '<strong>Storage:</strong> ' + ",".join(list2)
            comp_score_info2.append(info)   
            
        complevel = score['ComponentLevels']['L2_components']['Connectivity']
        if sum(complevel) > 0:
            list = [i for i, e in enumerate(complevel) if e != 0]
            list2 = [Connectivity_L2[i] for i in list]
            info = '<strong>Connectivity:</strong> ' + ",".join(list2)
            comp_score_info2.append(info)             
              
        comp_score_info3 = ' Try to include highest level blocks to improve your mark.'

    else: #type = 1
        comp_score_info1 = 'To reach this score you have used these <strong>low</strong> level components:'
        # Create the list with the components used
        comp_score_info2 = [] # Initialize
        complevel = score['ComponentLevels']['L1_components']['UserInterface']
        if sum(complevel) > 0:
            list = [i for i, e in enumerate(complevel) if e != 0]
            list2 = [UserInterface_L1[i] for i in list]
            info = '<strong>UserInterface:</strong> ' + ",".join(list2)
            comp_score_info2.append(info)
            
        complevel = score['ComponentLevels']['L1_components']['Layout']
        if sum(complevel) > 0:
            list = [i for i, e in enumerate(complevel) if e != 0]
            list2 = [Layout_L1[i] for i in list]
            info = '<strong>Layout:</strong> ' + ",".join(list2)
            comp_score_info2.append(info)
            
        complevel = score['ComponentLevels']['L1_components']['Media']
        if sum(complevel) > 0:
            list = [i for i, e in enumerate(complevel) if e != 0]
            list2 = [Media_L1[i] for i in list]
            info = '<strong>Media: <strong>' + ",".join(list2)
            comp_score_info2.append(info)
            
        complevel = score['ComponentLevels']['L1_components']['Drawing']
        if sum(complevel) > 0:
            list = [i for i, e in enumerate(complevel) if e != 0]
            list2 = [Drawing_L1[i] for i in list]
            info = '<strong>Drawing:</strong> ' + ",".join(list2)
            comp_score_info2.append(info)      
                      
        complevel = score['ComponentLevels']['L1_components']['Sensors']
        if sum(complevel) > 0:
            list = [i for i, e in enumerate(complevel) if e != 0]
            list2 = [Sensors_L1[i] for i in list]
            info = '<strong>Sensors:</strong> ' + ",".join(list2)
            comp_score_info2.append(info)   
        comp_score_info3 = 'Try to include high and medium level blocks to improve your mark.'
    
     
    comp_score_info = [comp_score_info1,comp_score_info2,comp_score_info3]
    
    return comp_score_info
    
def getScoreMsgsProgramming(score):
    
    flow_info = {}
    data_info= {}
    variable_info= {}
    general_info= {}
    
    # Flow Control and Logic
    flow_info['type'] = '<strong>Flow Control</strong>'
    if score['ProgrammingLevels']['Flow']['Score'] == 3:
        flow_info['intro'] = 'You have a <strong>high</strong> level in Flow Control due to the use of these blocks:'
        flow_info['tip'] = 'You can add more of them in order to improve your skills'
    elif score['ProgrammingLevels']['Flow']['Score'] == 2:
        flow_info['intro'] = 'You have a <strong>medium level</strong> in Flow Control due to the use of these blocks:'
        flow_info['tip'] = 'Try to include both categories to improve your level'
    else:
        flow_info['intro'] = 'You have a <strong>low</strong> level in Flow Control due to the use of these blocks:'
        flow_info['tip'] = 'Try to include at least one of the categories to improve your level'    
    flow_info['components'] = {'Component_Events':score['ProgrammingLevels']['Flow']['Component_Events'], 
                               'Control': score['ProgrammingLevels']['Flow']['Control']}
    
    
    # Data Management
    data_info['type'] = '<strong>Data Management</strong>'
    if score['ProgrammingLevels']['Data']['Score'] == 3:
        data_info['intro'] = 'You have a <strong>high</strong> level in Data Management due to the use of these blocks:'
        data_info['tip'] = 'You can add more of them in order to improve your skills'
    elif score['ProgrammingLevels']['Data']['Score'] == 2:
        data_info['intro'] = 'You have a <strong>medium</strong> level in Data management due to the use of these blocks:'
        data_info['tip'] = 'Try to include both categories to improve your level'
    else:
        data_info['intro'] = 'You have a <strong>low</strong> level in Data management due to the use of these blocks:'
        data_info['tip'] = 'Try to include at least one of the categories to improve your level'    
    data_info['components'] = {'Lists': score['ProgrammingLevels']['Data']['Lists'], 
                               'Component Set': score['ProgrammingLevels']['Data']['ComponenSet']}
    
    # Variable Control 
    variable_info['type'] = '<strong>Variable Control</strong>'
    if score['ProgrammingLevels']['Variable']['Score'] == 3:
        variable_info['intro'] = 'You have a <strong>high</strong> level in Variable Control due to the use of these blocks:'
        variable_info['tip'] = 'You can add more of them in order to improve your skills'
    elif score['ProgrammingLevels']['Variable']['Score'] == 2:
        variable_info['intro'] = 'You have a <strong>medium</strong> level in Variable Control due to the use of these blocks:'
        variable_info['tip'] = 'Try to include more categories to improve your level'
    else:
        variable_info['intro'] = 'You have a <strong>low</strong> level in Variable Control due to the use of these blocks:'
        variable_info['tip'] = 'Try to include at least one of the categories to improve your level'    
    variable_info['components'] = {'Variable':score['ProgrammingLevels']['Variable']['Variable'], 
                               'Math':score['ProgrammingLevels']['Variable']['Math'],
                               'Text':score['ProgrammingLevels']['Variable']['Text']}

    # Generalization
    general_info['type'] = '<strong>Generalization</strong>'
    if score['ProgrammingLevels']['Generalization']['Score'] == 3:
        general_info['intro'] = 'You have a <strong>high</strong> level in Generalization due to the use of these blocks:'
        general_info['tip'] = 'You can add more of them in order to improve your skills'
    elif score['ProgrammingLevels']['Generalization']['Score'] == 2:
        general_info['intro'] = 'You have a <strong>medium</strong> level in Generalization due to the use of these blocks:'
        general_info['tip'] = 'Try to include both categories to improve your level'
    else:
        general_info['intro'] = 'You have a <strong>low</strong> level in Generalization due to the use of these blocks:'
        general_info['tip'] = 'Try to include at least one of the categories to improve your level'    
    general_info['components'] = {'Procedures':score['ProgrammingLevels']['Generalization']['Procs'],
                                  'Generalization':score['ProgrammingLevels']['Generalization']['Generic']}
    
    progr_score_info = {'flow_info':flow_info,
                           'data_info':data_info,
                           'variable_info':variable_info,
                           'general_info':general_info}
    return progr_score_info
    
    
    
def getScoreMsgsSchedule(score):
    
    if score['ScreensLevels']['Screens'] == 1:
        sched_score_info1 = 'You have included <strong>' + str(score['ScreensLevels']['Screens']) + '</strong> screen in your app'
    else:
        sched_score_info1 = 'You have included <strong>' + str(score['ScreensLevels']['Screens']) + '</strong> screens in your app'
    
    if score['ScreensLevels']['Score'] == 3:  
        sched_score_info2 = 'This schedule is perfect so ensure a good user experience'
    elif score['ScreensLevels']['Score'] == 2 or score['ScreensLevels']['Screens'] == 1:
        sched_score_info2 = 'With this schedule you have a simple app. Why not improve its design by adding one or two screens more?'
    else:
        sched_score_info2 = 'This schedule could be too complex. Why not reduce the number of screens to simplify it?'
    
    sched_score_info = [sched_score_info1,sched_score_info2]
    return sched_score_info
    
def getScoreMsgs(score):
    
    '''
        Return the messages to display in the app
        
        Inputs: 
            - score (dict)
     
        Output: 
            - messages (namedtuple)           
    '''
    #### Main Info ####
    
    # General Score message
    if score['Score'] == 3:
        general_score_msg = 'Great job! Your app has a HIGH score! Check out the different skills to improve it even more'
    elif score['Score'] == 2:
        general_score_msg = 'Great job! Your app has a MEDIUM score! Check out the different skills to reach the next level'
    else:
        general_score_msg = 'Ups! Your app has a LOW score. Check out the different skills to improve it'
    
    # Components Score message    
    if score['ComponentLevels']['Score'] == 3:
        comp_score_msg = 'Due to the components used, you have a HIGH score. We challenge you to include more high level blocks'
    elif score['ComponentLevels']['Score'] == 2:
        comp_score_msg = 'Due to the components used, you have a MEDIUM score. Try to include high level blocks to improve your mark'
    else:
        comp_score_msg = 'Due to the components used, you have a LOW score. Have you tried to include higher level blocks?'
     
    # Programming Score message    
    if score['ProgrammingLevels']['Score'] == 3:
        progr_score_msg = 'Your skills with the Built-in blocks have a HIGH score. We challenge you to improve even more the complexity of your app'
    elif score['ProgrammingLevels']['Score'] == 2:
        progr_score_msg = 'Your skills with the Built-in blocks have a  MEDIUM score. Try to improve the complexity of your blocks to upgrade your mark'
    else:
        progr_score_msg = 'Your skills with the Built-in blocks have a LOW score. Try to improve the complexity of your blocks to upgrade your mark'

    # Screens Score message    
    if score['ScreensLevels']['Score'] == 3:
        sched_score_msg = 'Your app usability has a HIGH score. Your number of screens is perfect'
    elif score['ScreensLevels']['Score'] == 2:
        sched_score_msg = 'Your app usability has a MEDIUM score. Maybe you can include some additional screens to improve the user experience'
    else:
        sched_score_msg = "Your app usability has a LOW score. Try to optimize the number of screens between 2 and 10 for a better user experience"


    #### Components info ####
    comp_score_info = getScoreMsgsComponents(score,score['ComponentLevels']['Score'])
    progr_score_info = getScoreMsgsProgramming(score)
    sched_score_info = getScoreMsgsSchedule(score)

    # https://docs.python.org/3/library/collections.html#namedtuple-factory-function-for-tuples-with-named-fields
    Messages = namedtuple('Messages',['general_score_msg','comp_score_msg','progr_score_msg','sched_score_msg',
                                      'comp_score_info','progr_score_info','sched_score_info'])
    m = Messages(general_score_msg, comp_score_msg,progr_score_msg,sched_score_msg,
                 comp_score_info,progr_score_info,sched_score_info)
    return m
    
