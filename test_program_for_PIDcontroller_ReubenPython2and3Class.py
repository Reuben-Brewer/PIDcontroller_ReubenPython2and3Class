# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision E, 08/29/2022

Verified working on: Python 2.7, 3.8 for Windows 8.1, 10 64-bit and Raspberry Pi Buster (no Mac testing yet).
'''

__author__ = 'reuben.brewer'

#########################################################
from PIDcontroller_ReubenPython2and3Class import *
from MyPrint_ReubenPython2and3Class import *
#########################################################

#########################################################
import os
import sys
import platform
import time
import datetime
import threading
import collections
#########################################################

#########################################################
if sys.version_info[0] < 3:
    from Tkinter import * #Python 2
    import tkFont
    import ttk
else:
    from tkinter import * #Python 3
    import tkinter.font as tkFont #Python 3
    from tkinter import ttk
#########################################################

#########################################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
#########################################################

###########################################################################################################
##########################################################################################################
def getPreciseSecondsTimeStampString():
    ts = time.time()

    return ts
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def TellWhichFileWereIn():

    #We used to use this method, but it gave us the root calling file, not the class calling file
    #absolute_file_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    #filename = absolute_file_path[absolute_file_path.rfind("\\") + 1:]

    frame = inspect.stack()[1]
    filename = frame[1][frame[1].rfind("\\") + 1:]
    filename = filename.replace(".py","")

    return filename
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def IsInputList(input, print_result_flag = 0):

    result = isinstance(input, list)

    if print_result_flag == 1:
        print("IsInputList: " + str(result))

    return result
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

    number_of_decimal_places = max(1, number_of_decimal_places) #Make sure we're above 1

    ListOfStringsToJoin = []

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if isinstance(input, str) == 1:
        ListOfStringsToJoin.append(input)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, int) == 1 or isinstance(input, float) == 1:
        element = float(input)
        prefix_string = "{:." + str(number_of_decimal_places) + "f}"
        element_as_string = prefix_string.format(element)

        ##########################################################################################################
        ##########################################################################################################
        if element >= 0:
            element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place
            element_as_string = "+" + element_as_string  # So that our strings always have either + or - signs to maintain the same string length
        else:
            element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1 + 1)  # +1 for sign, +1 for decimal place
        ##########################################################################################################
        ##########################################################################################################

        ListOfStringsToJoin.append(element_as_string)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, list) == 1:

        if len(input) > 0:
            for element in input: #RECURSION
                ListOfStringsToJoin.append(ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

        else: #Situation when we get a list() or []
            ListOfStringsToJoin.append(str(input))

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, tuple) == 1:

        if len(input) > 0:
            for element in input: #RECURSION
                ListOfStringsToJoin.append("TUPLE" + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

        else: #Situation when we get a list() or []
            ListOfStringsToJoin.append(str(input))

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, dict) == 1:

        if len(input) > 0:
            for Key in input: #RECURSION
                ListOfStringsToJoin.append(str(Key) + ": " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

        else: #Situation when we get a dict()
            ListOfStringsToJoin.append(str(input))

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    else:
        ListOfStringsToJoin.append(str(input))
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if len(ListOfStringsToJoin) > 1:

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        StringToReturn = ""
        for Index, StringToProcess in enumerate(ListOfStringsToJoin):

            ################################################
            if Index == 0: #The first element
                if StringToProcess.find(":") != -1 and StringToProcess[0] != "{": #meaning that we're processing a dict()
                    StringToReturn = "{"
                elif StringToProcess.find("TUPLE") != -1 and StringToProcess[0] != "(":  # meaning that we're processing a tuple
                    StringToReturn = "("
                else:
                    StringToReturn = "["

                StringToReturn = StringToReturn + StringToProcess.replace("TUPLE","") + ", "
            ################################################

            ################################################
            elif Index < len(ListOfStringsToJoin) - 1: #The middle elements
                StringToReturn = StringToReturn + StringToProcess + ", "
            ################################################

            ################################################
            else: #The last element
                StringToReturn = StringToReturn + StringToProcess

                if StringToProcess.find(":") != -1 and StringToProcess[-1] != "}":  # meaning that we're processing a dict()
                    StringToReturn = StringToReturn + "}"
                elif StringToProcess.find("TUPLE") != -1 and StringToProcess[-1] != ")":  # meaning that we're processing a tuple
                    StringToReturn = StringToReturn + ")"
                else:
                    StringToReturn = StringToReturn + "]"

            ################################################

        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    elif len(ListOfStringsToJoin) == 1:
        StringToReturn = ListOfStringsToJoin[0]

    else:
        StringToReturn = ListOfStringsToJoin

    return StringToReturn
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ConvertDictToProperlyFormattedStringForPrinting(DictToPrint, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3):

    ProperlyFormattedStringForPrinting = ""
    ItemsPerLineCounter = 0

    for Key in DictToPrint:

        if isinstance(DictToPrint[Key], dict): #RECURSION
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                 Key + ":\n" + \
                                                 ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key], NumberOfDecimalsPlaceToUse, NumberOfEntriesPerLine, NumberOfTabsBetweenItems)

        else:
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                 Key + ": " + \
                                                 ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key], 0, NumberOfDecimalsPlaceToUse)

        if ItemsPerLineCounter < NumberOfEntriesPerLine - 1:
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\t"*NumberOfTabsBetweenItems
            ItemsPerLineCounter = ItemsPerLineCounter + 1
        else:
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\n"
            ItemsPerLineCounter = 0

    return ProperlyFormattedStringForPrinting
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def TestButtonResponse():
    global MyPrint_ReubenPython2and3ClassObject
    global USE_MYPRINT_FLAG

    if USE_MYPRINT_FLAG == 1:
        MyPrint_ReubenPython2and3ClassObject.my_print("Test Button was Pressed!")
    else:
        print("Test Button was Pressed!")
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_update_clock():
    global root
    global EXIT_PROGRAM_FLAG
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_GUI_FLAG
    global DebuggingInfo_Label

    global PIDcontroller_ReubenPython2and3ClassObject
    global PIDcontroller_OPEN_FLAG
    global SHOW_IN_GUI_PIDcontroller_FLAG

    global MyPrint_ReubenPython2and3ClassObject
    global MYPRINT_OPEN_FLAG
    global SHOW_IN_GUI_MYPRINT_FLAG

    global PIDcontroller_MostRecentDict

    if USE_GUI_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
        #########################################################
        #########################################################

            #########################################################
            DebuggingInfo_Label["text"] = ConvertDictToProperlyFormattedStringForPrinting(PIDcontroller_MostRecentDict, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3)
            #########################################################

            #########################################################
            if PIDcontroller_OPEN_FLAG == 1 and SHOW_IN_GUI_PIDcontroller_FLAG == 1:
                PIDcontroller_ReubenPython2and3ClassObject.GUI_update_clock()
            #########################################################

            #########################################################
            if MYPRINT_OPEN_FLAG == 1 and SHOW_IN_GUI_MYPRINT_FLAG == 1:
                MyPrint_ReubenPython2and3ClassObject.GUI_update_clock()
            #########################################################

            root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
        #########################################################
        #########################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ExitProgram_Callback():
    global EXIT_PROGRAM_FLAG

    print("ExitProgram_Callback event fired!")

    EXIT_PROGRAM_FLAG = 1
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_Thread():
    global root
    global root_Xpos
    global root_Ypos
    global root_width
    global root_height
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_TABS_IN_GUI_FLAG
    global DebuggingInfo_Label
    global TestButton

    ################################################# KEY GUI LINE
    #################################################
    root = Tk()
    #################################################
    #################################################

    #################################################
    #################################################
    global TabControlObject
    global Tab_MainControls
    global Tab_PIDcontroller
    global Tab_MyPrint

    if USE_TABS_IN_GUI_FLAG == 1:
        #################################################
        TabControlObject = ttk.Notebook(root)

        Tab_PIDcontroller = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_PIDcontroller, text='   PIDcontroller   ')

        Tab_MainControls = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MainControls, text='   Main Controls   ')

        Tab_MyPrint = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MyPrint, text='   MyPrint Terminal   ')

        TabControlObject.pack(expand=1, fill="both")  # CANNOT MIX PACK AND GRID IN THE SAME FRAME/TAB, SO ALL .GRID'S MUST BE CONTAINED WITHIN THEIR OWN FRAME/TAB.

        ############# #Set the tab header font
        TabStyle = ttk.Style()
        TabStyle.configure('TNotebook.Tab', font=('Helvetica', '12', 'bold'))
        #############
        #################################################
    else:
        #################################################
        Tab_MainControls = root
        Tab_PIDcontroller = root
        Tab_MyPrint = root
        #################################################

    #################################################
    #################################################

    #################################################
    TestButton = Button(Tab_MainControls, text='Test Button', state="normal", width=20, command=lambda i=1: TestButtonResponse())
    TestButton.grid(row=0, column=0, padx=5, pady=1)
    #################################################

    #################################################
    DebuggingInfo_Label = Label(Tab_MainControls, text="Device Info", width=120, font=("Helvetica", 10))
    DebuggingInfo_Label.grid(row=1, column=0, padx=1, pady=1, columnspan=10, rowspan=1)
    #################################################

    ################################################# THIS BLOCK MUST COME 2ND-TO-LAST IN def GUI_Thread() IF USING TABS.
    root.protocol("WM_DELETE_WINDOW", ExitProgram_Callback)  # Set the callback function for when the window's closed.
    root.title("test_program_for_PIDcontroller_ReubenPython2and3Class")
    root.geometry('%dx%d+%d+%d' % (root_width, root_height, root_Xpos, root_Ypos)) # set the dimensions of the screen and where it is placed
    root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
    root.mainloop()
    #################################################

    #################################################  THIS BLOCK MUST COME LAST IN def GUI_Thread() REGARDLESS OF CODE.
    root.quit() #Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
    root.destroy() #Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
    #################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    #################################################
    #################################################
    global my_platform

    if platform.system() == "Linux":

        if "raspberrypi" in platform.uname():  # os.uname() doesn't work in windows
            my_platform = "pi"
        else:
            my_platform = "linux"

    elif platform.system() == "Windows":
        my_platform = "windows"

    elif platform.system() == "Darwin":
        my_platform = "mac"

    else:
        my_platform = "other"

    print("The OS platform is: " + my_platform)
    #################################################
    #################################################

    #################################################
    #################################################
    global USE_GUI_FLAG
    USE_GUI_FLAG = 1

    global USE_TABS_IN_GUI_FLAG
    USE_TABS_IN_GUI_FLAG = 1

    global USE_PIDcontroller_FLAG
    USE_PIDcontroller_FLAG = 1

    global USE_MYPRINT_FLAG
    USE_MYPRINT_FLAG = 1

    global USE_PrintMostRecentDictForDebuggingFlag
    USE_PrintMostRecentDictForDebuggingFlag = 0
    #################################################
    #################################################

    #################################################
    #################################################
    global SHOW_IN_GUI_PIDcontroller_FLAG
    SHOW_IN_GUI_PIDcontroller_FLAG = 1

    global SHOW_IN_GUI_MYPRINT_FLAG
    SHOW_IN_GUI_MYPRINT_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global GUI_ROW_PIDcontroller
    global GUI_COLUMN_PIDcontroller
    global GUI_PADX_PIDcontroller
    global GUI_PADY_PIDcontroller
    global GUI_ROWSPAN_PIDcontroller
    global GUI_COLUMNSPAN_PIDcontroller
    GUI_ROW_PIDcontroller = 1

    GUI_COLUMN_PIDcontroller = 0
    GUI_PADX_PIDcontroller = 1
    GUI_PADY_PIDcontroller = 1
    GUI_ROWSPAN_PIDcontroller = 1
    GUI_COLUMNSPAN_PIDcontroller = 1

    global GUI_ROW_MYPRINT
    global GUI_COLUMN_MYPRINT
    global GUI_PADX_MYPRINT
    global GUI_PADY_MYPRINT
    global GUI_ROWSPAN_MYPRINT
    global GUI_COLUMNSPAN_MYPRINT
    GUI_ROW_MYPRINT = 2

    GUI_COLUMN_MYPRINT = 0
    GUI_PADX_MYPRINT = 1
    GUI_PADY_MYPRINT = 1
    GUI_ROWSPAN_MYPRINT = 1
    GUI_COLUMNSPAN_MYPRINT = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0

    global CurrentTime_MainLoopThread
    CurrentTime_MainLoopThread = -11111.0

    global StartingTime_MainLoopThread
    StartingTime_MainLoopThread = -11111.0

    global root

    global root_Xpos
    root_Xpos = 900

    global root_Ypos
    root_Ypos = 0

    global root_width
    root_width = 1920 - root_Xpos

    global root_height
    root_height = 1020 - root_Ypos

    global TabControlObject
    global Tab_MainControls
    global Tab_PIDcontroller
    global Tab_MyPrint

    global GUI_RootAfterCallbackInterval_Milliseconds
    GUI_RootAfterCallbackInterval_Milliseconds = 30
    #################################################
    #################################################

    #################################################
    #################################################
    global PIDcontroller_ReubenPython2and3ClassObject

    global PIDcontroller_OPEN_FLAG
    PIDcontroller_OPEN_FLAG = -1

    global PIDcontroller_MostRecentDict
    PIDcontroller_MostRecentDict = dict()
    
    global PIDcontroller_MostRecentDict_Kp
    PIDcontroller_MostRecentDict_Kp = 0.0

    global PIDcontroller_MostRecentDict_Ki
    PIDcontroller_MostRecentDict_Ki = 0.0

    global PIDcontroller_MostRecentDict_Kd
    PIDcontroller_MostRecentDict_Kd = 0.0

    global PIDcontroller_MostRecentDict_ErrorSumMax
    PIDcontroller_MostRecentDict_ErrorSumMax = 0.0

    global PIDcontroller_MostRecentDict_ActualValueDot_ExponentialFilterLambda
    PIDcontroller_MostRecentDict_ActualValueDot_ExponentialFilterLambda = 1.0

    global PIDcontroller_MostRecentDict_LoopFrequencyHz
    PIDcontroller_MostRecentDict_LoopFrequencyHz = -11111.0

    global PIDcontroller_MostRecentDict_ActualValueDot_ActualValue
    PIDcontroller_MostRecentDict_ActualValueDot_ActualValue = 0.0

    global PIDcontroller_MostRecentDict_ActualValueDot_DesiredValue
    PIDcontroller_MostRecentDict_ActualValueDot_DesiredValue = 0.0

    global PIDcontroller_MostRecentDict_ActualValueDot_ActualValueDot_Raw
    PIDcontroller_MostRecentDict_ActualValueDot_ActualValueDot_Raw = 0.0

    global PIDcontroller_MostRecentDict_ActualValueDot_ActualValueDot_Filtered
    PIDcontroller_MostRecentDict_ActualValueDot_ActualValueDot_Filtered = 0.0

    global PIDcontroller_MostRecentDict_ActualValueDot_DesiredValueDot
    PIDcontroller_MostRecentDict_ActualValueDot_DesiredValueDot = 0.0

    global PIDcontroller_MostRecentDict_Error
    PIDcontroller_MostRecentDict_Error = 0.0

    global PIDcontroller_MostRecentDict_ErrorSum
    PIDcontroller_MostRecentDict_ErrorSum = 0.0

    global PIDcontroller_MostRecentDict_ErrorDot
    PIDcontroller_MostRecentDict_ErrorDot = 0.0

    global PIDcontroller_MostRecentDict_CorrectiveCommandToIssue
    PIDcontroller_MostRecentDict_CorrectiveCommandToIssue = 0.0
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPrint_ReubenPython2and3ClassObject

    global MYPRINT_OPEN_FLAG
    MYPRINT_OPEN_FLAG = -1
    #################################################
    #################################################

    #################################################  KEY GUI LINE
    #################################################
    if USE_GUI_FLAG == 1:
        print("Starting GUI thread...")
        GUI_Thread_ThreadingObject = threading.Thread(target=GUI_Thread)
        GUI_Thread_ThreadingObject.setDaemon(True) #Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        GUI_Thread_ThreadingObject.start()
        time.sleep(0.5)  #Allow enough time for 'root' to be created that we can then pass it into other classes.
    else:
        root = None
        Tab_MainControls = None
        Tab_PIDcontroller = None
        Tab_MyPrint = None
    #################################################
    #################################################

    #################################################
    #################################################
    global PIDcontroller_ReubenPython2and3ClassObject_GUIparametersDict
    PIDcontroller_ReubenPython2and3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_PIDcontroller_FLAG),
                                    ("root", Tab_PIDcontroller),
                                    ("EnableInternal_MyPrint_Flag", 1),
                                    ("NumberOfPrintLines", 10),
                                    ("UseBorderAroundThisGuiObjectFlag", 1),
                                    ("GUI_ROW", GUI_ROW_PIDcontroller),
                                    ("GUI_COLUMN", GUI_COLUMN_PIDcontroller),
                                    ("GUI_PADX", GUI_PADX_PIDcontroller),
                                    ("GUI_PADY", GUI_PADY_PIDcontroller),
                                    ("GUI_ROWSPAN", GUI_ROWSPAN_PIDcontroller),
                                    ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_PIDcontroller)])

    global PIDcontroller_ReubenPython2and3ClassObject_setup_dict
    PIDcontroller_ReubenPython2and3ClassObject_setup_dict = dict([("GUIparametersDict", PIDcontroller_ReubenPython2and3ClassObject_GUIparametersDict),
                                                                ("NameToDisplay_UserSet", "Reuben's Test PIDcontroller"),
                                                                ("MainThread_TimeToSleepEachLoop", 0.001),
                                                                ("Kp", 0.001),
                                                                ("Ki", 0.002),
                                                                ("Kd", 0.003),
                                                                ("ErrorSumMax", 0.004),
                                                                ("ActualValueDot_ExponentialFilterLambda", 0.1)])
    if USE_PIDcontroller_FLAG == 1:
        try:
            PIDcontroller_ReubenPython2and3ClassObject = PIDcontroller_ReubenPython2and3Class(PIDcontroller_ReubenPython2and3ClassObject_setup_dict)
            PIDcontroller_OPEN_FLAG = PIDcontroller_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("PIDcontroller_ReubenPython2and3ClassObject __init__: Exceptions: %s" % exceptions, 0)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MYPRINT_FLAG == 1:

        MyPrint_ReubenPython2and3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_MYPRINT_FLAG),
                                                                        ("root", Tab_MyPrint),
                                                                        ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                        ("GUI_ROW", GUI_ROW_MYPRINT),
                                                                        ("GUI_COLUMN", GUI_COLUMN_MYPRINT),
                                                                        ("GUI_PADX", GUI_PADX_MYPRINT),
                                                                        ("GUI_PADY", GUI_PADY_MYPRINT),
                                                                        ("GUI_ROWSPAN", GUI_ROWSPAN_MYPRINT),
                                                                        ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_MYPRINT)])

        MyPrint_ReubenPython2and3ClassObject_setup_dict = dict([("NumberOfPrintLines", 10),
                                                                ("WidthOfPrintingLabel", 200),
                                                                ("PrintToConsoleFlag", 1),
                                                                ("LogFileNameFullPath", os.getcwd() + "//TestLog.txt"),
                                                                ("GUIparametersDict", MyPrint_ReubenPython2and3ClassObject_GUIparametersDict)])

        try:
            MyPrint_ReubenPython2and3ClassObject = MyPrint_ReubenPython2and3Class(MyPrint_ReubenPython2and3ClassObject_setup_dict)
            MYPRINT_OPEN_FLAG = MyPrint_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPrint_ReubenPython2and3ClassObject __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_PIDcontroller_FLAG == 1 and PIDcontroller_OPEN_FLAG != 1:
        print("Failed to open PIDcontroller_ReubenPython2and3Class.")
        ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MYPRINT_FLAG == 1 and MYPRINT_OPEN_FLAG != 1:
        print("Failed to open MyPrint_ReubenPython2and3ClassObject.")
        ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    print("Starting main loop 'test_program_for_PIDcontroller_ReubenPython2and3Class.")
    StartingTime_MainLoopThread = getPreciseSecondsTimeStampString()

    while(EXIT_PROGRAM_FLAG == 0):

        ###################################################
        CurrentTime_MainLoopThread = getPreciseSecondsTimeStampString() - StartingTime_MainLoopThread
        ###################################################

        ################################################### GET's
        ###################################################
        if PIDcontroller_OPEN_FLAG == 1:

            PIDcontroller_MostRecentDict = PIDcontroller_ReubenPython2and3ClassObject.GetMostRecentDataDict()

            if "LoopFrequencyHz" in PIDcontroller_MostRecentDict:
                PIDcontroller_MostRecentDict_Kp = PIDcontroller_MostRecentDict["Kp"]
                PIDcontroller_MostRecentDict_Ki = PIDcontroller_MostRecentDict["Ki"]
                PIDcontroller_MostRecentDict_Kd = PIDcontroller_MostRecentDict["Kd"]
                PIDcontroller_MostRecentDict_ErrorSumMax = PIDcontroller_MostRecentDict["ErrorSumMax"]
                PIDcontroller_MostRecentDict_ActualValueDot_ExponentialFilterLambda = PIDcontroller_MostRecentDict["ActualValueDot_ExponentialFilterLambda"]
                PIDcontroller_MostRecentDict_LoopFrequencyHz = PIDcontroller_MostRecentDict["LoopFrequencyHz"]
                PIDcontroller_MostRecentDict_ActualValueDot_ActualValue = PIDcontroller_MostRecentDict["ActualValue"]
                PIDcontroller_MostRecentDict_ActualValueDot_DesiredValue = PIDcontroller_MostRecentDict["DesiredValue"]
                PIDcontroller_MostRecentDict_ActualValueDot_ActualValueDot_Raw = PIDcontroller_MostRecentDict["ActualValueDot_Raw"]
                PIDcontroller_MostRecentDict_ActualValueDot_ActualValueDot_Filtered = PIDcontroller_MostRecentDict["ActualValueDot_Filtered"]
                PIDcontroller_MostRecentDict_ActualValueDot_DesiredValueDot = PIDcontroller_MostRecentDict["DesiredValueDot"]
                PIDcontroller_MostRecentDict_Error = PIDcontroller_MostRecentDict["Error"]
                PIDcontroller_MostRecentDict_ErrorSum = PIDcontroller_MostRecentDict["ErrorSum"]
                PIDcontroller_MostRecentDict_ErrorDot = PIDcontroller_MostRecentDict["ErrorDot"]
                PIDcontroller_MostRecentDict_CorrectiveCommandToIssue = PIDcontroller_MostRecentDict["CorrectiveCommandToIssue"]

                if USE_PrintMostRecentDictForDebuggingFlag == 1:
                    print("PIDcontroller_MostRecentDict: " + ConvertDictToProperlyFormattedStringForPrinting(PIDcontroller_MostRecentDict, NumberOfDecimalsPlaceToUse=5))

        ###################################################
        ###################################################

        ################################################### SET's
        ###################################################
        if PIDcontroller_OPEN_FLAG == 1:
            PIDcontroller_ReubenPython2and3ClassObject.UpdatePIDloopError(CurrentTime_MainLoopThread,
                                                                          0.0,
                                                                          ActualValueDot = -11111.0,
                                                                          DesiredValueDot = 0.0)
        ###################################################
        ###################################################

        time.sleep(0.002)
    #################################################
    #################################################

    ################################################# THIS IS THE EXIT ROUTINE!
    #################################################
    print("Exiting main program 'test_program_for_PIDcontroller_ReubenPython2and3Class.")

    #################################################
    if PIDcontroller_OPEN_FLAG == 1:
        PIDcontroller_ReubenPython2and3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    if MYPRINT_OPEN_FLAG == 1:
        MyPrint_ReubenPython2and3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    #################################################

##########################################################################################################
##########################################################################################################