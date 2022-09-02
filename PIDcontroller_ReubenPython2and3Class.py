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
from LowPassFilter_ReubenPython2and3Class import *
from EntryListWithBlinking_ReubenPython2and3Class import *
#########################################################

#########################################################
import os
import sys
import platform
import time
import datetime
import math
import collections
from copy import * #for deepcopy(dict)
import inspect #To enable 'TellWhichFileWereIn'
import threading
import traceback
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
if sys.version_info[0] < 3:
    import Queue  # Python 2
else:
    import queue as Queue  # Python 3
#########################################################

#########################################################
if sys.version_info[0] < 3:
    from builtins import raw_input as input
else:
    from future.builtins import input as input
######################################################### #"sudo pip3 install future" (Python 3) AND "sudo pip install future" (Python 2)

#########################################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
#########################################################

class PIDcontroller_ReubenPython2and3Class(Frame): #Subclass the Tkinter Frame

    ##########################################################################################################
    ##########################################################################################################
    def __init__(self, setup_dict): #Subclass the Tkinter Frame

        print("#################### PIDcontroller_ReubenPython2and3Class __init__ starting. ####################")

        #########################################################
        #########################################################
        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
        self.EntryListWithBlinking_OPEN_FLAG = 0

        self.EnableInternal_MyPrint_Flag = 0

        self.CurrentTime_CalculatedFromUpdateFunction = -11111.0
        self.LastTime_CalculatedFromUpdateFunction = -11111.0
        self.DataStreamingFrequency_CalculatedFromUpdateFunction = -11111.0
        self.DataStreamingDeltaT_CalculatedFromUpdateFunction = -11111.0

        self.MostRecentDataDict = dict()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if platform.system() == "Linux":

            if "raspberrypi" in platform.uname(): #os.uname() doesn't work in windows
                self.my_platform = "pi"
            else:
                self.my_platform = "linux"

        elif platform.system() == "Windows":
            self.my_platform = "windows"

        elif platform.system() == "Darwin":
            self.my_platform = "mac"

        else:
            self.my_platform = "other"

        print("PIDcontroller_ReubenPython2and3Class __init__: The OS platform is: " + self.my_platform)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "GUIparametersDict" in setup_dict:
            self.GUIparametersDict = setup_dict["GUIparametersDict"]

            #########################################################
            #########################################################
            if "USE_GUI_FLAG" in self.GUIparametersDict:
                self.USE_GUI_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", self.GUIparametersDict["USE_GUI_FLAG"])
            else:
                self.USE_GUI_FLAG = 0

            print("PIDcontroller_ReubenPython2and3Class __init__: USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "root" in self.GUIparametersDict:
                self.root = self.GUIparametersDict["root"]
            else:
                print("PIDcontroller_ReubenPython2and3Class __init__: ERROR, must pass in 'root'")
                return
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "EnableInternal_MyPrint_Flag" in self.GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", self.GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("PIDcontroller_ReubenPython2and3Class __init__: EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "PrintToConsoleFlag" in self.GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", self.GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("PIDcontroller_ReubenPython2and3Class __init__: PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "NumberOfPrintLines" in self.GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", self.GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("PIDcontroller_ReubenPython2and3Class __init__: NumberOfPrintLines: " + str(self.NumberOfPrintLines))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "UseBorderAroundThisGuiObjectFlag" in self.GUIparametersDict:
                self.UseBorderAroundThisGuiObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseBorderAroundThisGuiObjectFlag", self.GUIparametersDict["UseBorderAroundThisGuiObjectFlag"])
            else:
                self.UseBorderAroundThisGuiObjectFlag = 0

            print("PIDcontroller_ReubenPython2and3Class __init__: UseBorderAroundThisGuiObjectFlag: " + str(self.UseBorderAroundThisGuiObjectFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROW" in self.GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", self.GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("PIDcontroller_ReubenPython2and3Class __init__: GUI_ROW: " + str(self.GUI_ROW))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMN" in self.GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", self.GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("PIDcontroller_ReubenPython2and3Class __init__: GUI_COLUMN: " + str(self.GUI_COLUMN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADX" in self.GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", self.GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 0

            print("PIDcontroller_ReubenPython2and3Class __init__: GUI_PADX: " + str(self.GUI_PADX))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADY" in self.GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", self.GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 0

            print("PIDcontroller_ReubenPython2and3Class __init__: GUI_PADY: " + str(self.GUI_PADY))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROWSPAN" in self.GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", self.GUIparametersDict["GUI_ROWSPAN"], 0.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 1

            print("PIDcontroller_ReubenPython2and3Class __init__: GUI_ROWSPAN: " + str(self.GUI_ROWSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMNSPAN" in self.GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", self.GUIparametersDict["GUI_COLUMNSPAN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 1

            print("PIDcontroller_ReubenPython2and3Class __init__: GUI_COLUMNSPAN: " + str(self.GUI_COLUMNSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_STICKY" in self.GUIparametersDict:
                self.GUI_STICKY = str(self.GUIparametersDict["GUI_STICKY"])
            else:
                self.GUI_STICKY = "w"

            print("PIDcontroller_ReubenPython2and3Class __init__: GUI_STICKY: " + str(self.GUI_STICKY))
            #########################################################
            #########################################################

        else:
            self.GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("PIDcontroller_ReubenPython2and3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))

        #print("PIDcontroller_ReubenPython2and3Class __init__: GUIparametersDict: " + str(self.GUIparametersDict))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "NameToDisplay_UserSet" in setup_dict:
            self.NameToDisplay_UserSet = str(setup_dict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = ""

        print("PIDcontroller_ReubenPython2and3Class __init__: NameToDisplay_UserSet: " + str(self.NameToDisplay_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "NumberOfVariablesToTrack" in setup_dict:
            self.NumberOfVariablesToTrack = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfVariablesToTrack", setup_dict["NumberOfVariablesToTrack"], 1, 10))

        else:
            self.NumberOfVariablesToTrack = 1

        print("PIDcontroller_ReubenPython2and3Class __init__: NumberOfVariablesToTrack: " + str(self.NumberOfVariablesToTrack))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "Kp" in setup_dict:
            self.Kp = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("Kp", setup_dict["Kp"], -sys.float_info.max, sys.float_info.max)

        else:
            self.Kp = 0.0

        print("PIDcontroller_ReubenPython2and3Class __init__: Kp: " + str(self.Kp))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "Ki" in setup_dict:
            self.Ki = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("Ki", setup_dict["Ki"], -sys.float_info.max, sys.float_info.max)

        else:
            self.Ki = 0.0

        print("PIDcontroller_ReubenPython2and3Class __init__: Ki: " + str(self.Ki))
        #########################################################
        #########################################################
        
        #########################################################
        #########################################################
        if "Kd" in setup_dict:
            self.Kd = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("Kd", setup_dict["Kd"], -sys.float_info.max, sys.float_info.max)

        else:
            self.Kd = 0.0

        print("PIDcontroller_ReubenPython2and3Class __init__: Kd: " + str(self.Kd))
        #########################################################
        #########################################################
        
        #########################################################
        #########################################################
        if "ErrorSumMax" in setup_dict:
            self.ErrorSumMax = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("ErrorSumMax", setup_dict["ErrorSumMax"], -sys.float_info.max, sys.float_info.max)

        else:
            self.ErrorSumMax = 0.0

        print("PIDcontroller_ReubenPython2and3Class __init__: ErrorSumMax: " + str(self.ErrorSumMax))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "ActualValueDot_ExponentialFilterLambda" in setup_dict:
            self.ActualValueDot_ExponentialFilterLambda = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("ActualValueDot_ExponentialFilterLambda", setup_dict["ActualValueDot_ExponentialFilterLambda"], -sys.float_info.max, sys.float_info.max)

        else:
            self.ActualValueDot_ExponentialFilterLambda = 1.0 #Default to no filtering, new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value

        print("PIDcontroller_ReubenPython2and3Class __init__: ActualValueDot_ExponentialFilterLambda: " + str(self.ActualValueDot_ExponentialFilterLambda))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.ActualValueDot_LowPassFilter_ReubenPython2and3ClassObject = list()
        for index in range(0, self.NumberOfVariablesToTrack):
            self.ActualValueDot_LowPassFilter_ReubenPython2and3ClassObject.append(LowPassFilter_ReubenPython2and3Class(dict([("UseMedianFilterFlag", 0),
                                                        ("UseExponentialSmoothingFilterFlag", 1),
                                                        ("ExponentialSmoothingFilterLambda", self.ActualValueDot_ExponentialFilterLambda)])))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.PrintToGui_Label_TextInputHistory_List = [" "]*self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""
        self.GUI_ready_to_be_updated_flag = 0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.ActualValue = [0.0]*self.NumberOfVariablesToTrack
        self.ActualValue_last = [0.0]*self.NumberOfVariablesToTrack

        self.ActualValueDot_Raw = [0.0] * self.NumberOfVariablesToTrack
        self.ActualValueDot_Filtered = [0.0]*self.NumberOfVariablesToTrack

        self.Error = [0.0]*self.NumberOfVariablesToTrack
        self.ErrorSum = [0.0]*self.NumberOfVariablesToTrack
        self.ErrorDot = [0.0]*self.NumberOfVariablesToTrack
        self.CorrectiveCommandToIssue = [0.0]*self.NumberOfVariablesToTrack

        self.DataUpdateNumber = 0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.USE_GUI_FLAG == 1:
            self.StartGUI(self.root)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        time.sleep(0.5)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1
        #########################################################
        #########################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __del__(self):
        pass
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PassThrough0and1values_ExitProgramOtherwise(self, InputNameString, InputNumber):

        try:
            InputNumber_ConvertedToFloat = float(InputNumber)
        except:
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()

        try:
            if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1:
                return InputNumber_ConvertedToFloat
            else:
                input("PassThrough0and1values_ExitProgramOtherwise Error. '" +
                          InputNameString +
                          "' must be 0 or 1 (value was " +
                          str(InputNumber_ConvertedToFloat) +
                          "). Press any key (and enter) to exit.")

                sys.exit()
        except:
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PassThroughFloatValuesInRange_ExitProgramOtherwise(self, InputNameString, InputNumber, RangeMinValue, RangeMaxValue):
        try:
            InputNumber_ConvertedToFloat = float(InputNumber)
        except:
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()

        try:
            if InputNumber_ConvertedToFloat >= RangeMinValue and InputNumber_ConvertedToFloat <= RangeMaxValue:
                return InputNumber_ConvertedToFloat
            else:
                input("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
                          InputNameString +
                          "' must be in the range [" +
                          str(RangeMinValue) +
                          ", " +
                          str(RangeMaxValue) +
                          "] (value was " +
                          str(InputNumber_ConvertedToFloat) + "). Press any key (and enter) to exit.")

                sys.exit()
        except:
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TellWhichFileWereIn(self):

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
    def getPreciseSecondsTimeStampString(self):
        ts = time.time()

        return ts
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_CalculatedFromUpdateFunction(self):

        try:
            self.DataStreamingDeltaT_CalculatedFromUpdateFunction = self.CurrentTime_CalculatedFromUpdateFunction - self.LastTime_CalculatedFromUpdateFunction

            if self.DataStreamingDeltaT_CalculatedFromUpdateFunction != 0.0:
                self.DataStreamingFrequency_CalculatedFromUpdateFunction = 1.0/self.DataStreamingDeltaT_CalculatedFromUpdateFunction

            self.LastTime_CalculatedFromUpdateFunction = self.CurrentTime_CalculatedFromUpdateFunction
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_MainThread ERROR with Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdatePIDloopError(self, ActualValue, DesiredValue, ActualValueDot = -11111.0, DesiredValueDot = -11111.0):

        # print("UpdatePIDloopError event fired!")

        #########################################################
        if self.IsInputList(ActualValue) == 0:
            ActualValue = list([ActualValue])

        if len(ActualValue) != self.NumberOfVariablesToTrack:
            print("UpdatePIDloopError: ERROR, len(ActualValue) must match self.NumberOfVariablesToTrack = " +
                  str(self.NumberOfVariablesToTrack) +
                  ", bad value provided was " +
                  str(ActualValue))
            return
        #########################################################

        #########################################################
        if self.IsInputList(DesiredValue) == 0:
            DesiredValue = list([DesiredValue])

        if len(DesiredValue) != self.NumberOfVariablesToTrack:
            print("UpdatePIDloopError: ERROR, len(DesiredValue) must match self.NumberOfVariablesToTrack = " +
                  str(self.NumberOfVariablesToTrack) +
                  ", bad value provided was " +
                  str(DesiredValue))
            return
        #########################################################

        #########################################################
        if self.IsInputList(ActualValueDot) == 0:
            ActualValueDot = list([ActualValueDot])

        if ActualValueDot[0] == -11111.0:
            ActualValueDot = list([-11111.0]*self.NumberOfVariablesToTrack)

        if len(ActualValueDot) != self.NumberOfVariablesToTrack:
            print("UpdatePIDloopError: ERROR, len(ActualValueDot) must match self.NumberOfVariablesToTrack = " +
                  str(self.NumberOfVariablesToTrack) +
                  ", bad value was " +
                  str(ActualValueDot))
            return
        #########################################################

        #########################################################
        if self.IsInputList(DesiredValueDot) == 0:
            DesiredValueDot = list([DesiredValueDot])

        if DesiredValueDot[0] == -11111.0:
            DesiredValueDot = list([-11111.0]*self.NumberOfVariablesToTrack)

        if len(DesiredValueDot) != self.NumberOfVariablesToTrack:
            print("UpdatePIDloopError: ERROR, len(DesiredValueDot) must match self.NumberOfVariablesToTrack = " +
                  str(self.NumberOfVariablesToTrack) +
                  ", bad value was " +
                  str(DesiredValueDot))
            return
        #########################################################

        #########################################################
        self.CurrentTime_CalculatedFromUpdateFunction = self.getPreciseSecondsTimeStampString()
        self.UpdateFrequencyCalculation_CalculatedFromUpdateFunction()
        self.DataUpdateNumber = self.DataUpdateNumber + 1
        #########################################################

        #########################################################
        self.ActualValue = list(ActualValue)
        self.DesiredValue = list(DesiredValue)
        self.DesiredValueDot = list(DesiredValueDot)
        #########################################################

        #########################################################
        if self.USE_GUI_FLAG == 1:
            EntryListWithBlinking_MostRecentDataDict_LocalCopy = self.EntryListWithBlinking_ReubenPython2and3ClassObject.GetMostRecentDataDict() #Get latest gain values

            self.Kp = EntryListWithBlinking_MostRecentDataDict_LocalCopy["Kp"]
            self.Ki = EntryListWithBlinking_MostRecentDataDict_LocalCopy["Ki"]
            self.Kd = EntryListWithBlinking_MostRecentDataDict_LocalCopy["Kd"]
            self.ErrorSumMax = EntryListWithBlinking_MostRecentDataDict_LocalCopy["ErrorSumMax"]
            self.ActualValueDot_ExponentialFilterLambda = EntryListWithBlinking_MostRecentDataDict_LocalCopy["ActualValueDot_ExponentialFilterLambda"]
        #########################################################

        #########################################################
        #########################################################
        for Index in range(0, self.NumberOfVariablesToTrack):

            #########################################################
            self.Error[Index] = self.DesiredValue[Index] - self.ActualValue[Index]
            #########################################################

            #########################################################
            if abs(self.ErrorSum[Index] + self.Error[Index]) <= self.ErrorSumMax:
                self.ErrorSum[Index] = self.ErrorSum[Index] + self.Error[Index]
            #########################################################

            #########################################################

            ###########################
            if ActualValueDot[Index] == -11111.0: #No input
                if self.DataStreamingDeltaT_CalculatedFromUpdateFunction > 0.0:
                    self.ActualValueDot_Raw[Index] = (self.ActualValue[Index] - self.ActualValue_last[Index])/self.DataStreamingDeltaT_CalculatedFromUpdateFunction
                else:
                    print("UpdatePIDloopError, ERROR: DataStreamingDeltaT_CalculatedFromUpdateFunction = 0")
            else:
                self.ActualValueDot_Raw[Index] = ActualValueDot[Index]
            ###########################

            self.ActualValueDot_Filtered[Index] = self.ActualValueDot_LowPassFilter_ReubenPython2and3ClassObject[Index].AddDataPointFromExternalProgram(self.ActualValueDot_Raw[Index])["SignalOutSmoothed"]

            self.ErrorDot[Index] = self.DesiredValueDot[Index] - self.ActualValueDot_Filtered[Index]
            #########################################################

            #########################################################
            self.CorrectiveCommandToIssue[Index] = self.Error[Index]*self.Kp + \
                                       self.ErrorSum[Index]*self.Ki + \
                                       self.ErrorDot[Index]*self.Kd
            #########################################################

        #########################################################
        #########################################################

        #########################
        self.MostRecentDataDict = dict([("DataUpdateNumber", self.DataUpdateNumber),
                                        ("Kp", self.Kp),
                                        ("Ki", self.Ki),
                                        ("Kd", self.Kd),
                                        ("ErrorSumMax", self.ErrorSumMax),
                                        ("ActualValueDot_ExponentialFilterLambda", self.ActualValueDot_ExponentialFilterLambda),
                                        ("LoopFrequencyHz", self.DataStreamingFrequency_CalculatedFromUpdateFunction),
                                        ("ActualValue", self.ActualValue),
                                        ("DesiredValue", self.DesiredValue),
                                        ("ActualValueDot_Raw", self.ActualValueDot_Raw),
                                        ("ActualValueDot_Filtered", self.ActualValueDot_Filtered),
                                        ("DesiredValueDot", self.DesiredValueDot),
                                        ("Error", self.Error),
                                        ("ErrorSum", self.ErrorSum),
                                        ("ErrorDot", self.ErrorDot),
                                        ("CorrectiveCommandToIssue", self.CorrectiveCommandToIssue)])
        #########################

        #########################
        self.ActualValue_last = list(self.ActualValue)
        #########################

        return self.CorrectiveCommandToIssue
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        if self.EXIT_PROGRAM_FLAG == 0:

            #deepcopy IS required as MostRecentDataDict sometimes contains lists (e.g. self.MostRecentDataDict["DesiredValue"] can be a list).
            return deepcopy(self.MostRecentDataDict)

        else:
            return dict() #So that we're not returning variables during the close-down process.
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for PIDcontroller_ReubenPython2and3Class object")

        self.EXIT_PROGRAM_FLAG = 1

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StartGUI(self, GuiParent):

        self.GUI_Thread_ThreadingObject = threading.Thread(target=self.GUI_Thread, args=(GuiParent,))
        self.GUI_Thread_ThreadingObject.setDaemon(True) #Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        self.GUI_Thread_ThreadingObject.start()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_Thread(self, parent):

        print("Starting the GUI_Thread for PIDcontroller_ReubenPython2and3Class object.")

        #################################################
        self.root = parent
        self.parent = parent
        #################################################

        #################################################
        self.myFrame = Frame(self.root)

        if self.UseBorderAroundThisGuiObjectFlag == 1:
            self.myFrame["borderwidth"] = 2
            self.myFrame["relief"] = "ridge"

        self.myFrame.grid(row = self.GUI_ROW,
                          column = self.GUI_COLUMN,
                          padx = self.GUI_PADX,
                          pady = self.GUI_PADY,
                          rowspan = self.GUI_ROWSPAN,
                          columnspan= self.GUI_COLUMNSPAN,
                          sticky = self.GUI_STICKY)
        #################################################

        #################################################
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150) #RGB
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150) #RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        self.EntryWidth = 10
        self.LabelWidth = 35
        self.FontSize = 12
        #################################################

        #################################################
        self.NameLabel = Label(self.myFrame, text=self.NameToDisplay_UserSet, width=50, font=("Helvetica", int(self.FontSize)))
        self.NameLabel.grid(row=0, column=0, padx=5, pady=1, columnspan=1, rowspan=1)
        #################################################

        #################################################
        self.EntryListWithBlinking_ReubenPython2and3ClassObject_GUIparametersDict = dict([("root", self.myFrame),("UseBorderAroundThisGuiObjectFlag", 0),("GUI_ROW", 1),("GUI_COLUMN", 0)])
        
        self.EntryListWithBlinking_Variables_ListOfDicts = [dict([("Name", "Kp"),("Type", "float"), ("StartingVal", self.Kp),("EntryWidth", self.EntryWidth),("LabelWidth", self.LabelWidth),("FontSize", self.FontSize)]),
                                                       dict([("Name", "Ki"),("Type", "float"), ("StartingVal", self.Ki),("EntryWidth", self.EntryWidth),("LabelWidth", self.LabelWidth),("FontSize", self.FontSize)]),
                                                       dict([("Name", "Kd"),("Type", "float"), ("StartingVal", self.Kd),("EntryWidth", self.EntryWidth),("LabelWidth", self.LabelWidth),("FontSize", self.FontSize)]),
                                                       dict([("Name", "ErrorSumMax"),("Type", "float"), ("StartingVal", self.ErrorSumMax),("EntryWidth", self.EntryWidth),("LabelWidth", self.LabelWidth),("FontSize", self.FontSize)]),
                                                       dict([("Name", "ActualValueDot_ExponentialFilterLambda"),("Type", "float"), ("StartingVal", self.ActualValueDot_ExponentialFilterLambda),("MinVal", 0.0),("MaxVal", 1.0),("EntryWidth", self.EntryWidth),("LabelWidth", self.LabelWidth),("FontSize", self.FontSize)])]

        self.EntryListWithBlinking_ReubenPython2and3ClassObject_setup_dict = dict([("GUIparametersDict", self.EntryListWithBlinking_ReubenPython2and3ClassObject_GUIparametersDict),
                                                                              ("EntryListWithBlinking_Variables_ListOfDicts", self.EntryListWithBlinking_Variables_ListOfDicts),
                                                                              ("DebugByPrintingVariablesFlag", 0)])

        try:
            self.EntryListWithBlinking_ReubenPython2and3ClassObject = EntryListWithBlinking_ReubenPython2and3Class(self.EntryListWithBlinking_ReubenPython2and3ClassObject_setup_dict)
            time.sleep(0.010)
            self.EntryListWithBlinking_OPEN_FLAG = self.EntryListWithBlinking_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("EntryListWithBlinking_ReubenPython2and3ClassObject __init__: Exceptions: %s" % exceptions, 0)
            traceback.print_exc()
        #################################################

        #################################################
        self.Data_Label = Label(self.myFrame, text="Data_Label", width=90)
        self.Data_Label.grid(row=1, column=1, padx=5, pady=1, columnspan=1, rowspan=1)
        #################################################

        #################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=75)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=2, column=0, padx=1, pady=1, columnspan=10, rowspan=1)
        #################################################

        #################################################
        self.GUI_ready_to_be_updated_flag = 1
        #################################################

        ################################################# INITIALIZE VARIABLES
        self.UpdatePIDloopError([0.0]*self.NumberOfVariablesToTrack, [0.0]*self.NumberOfVariablesToTrack, ActualValueDot=[0.0]*self.NumberOfVariablesToTrack, DesiredValueDot=[0.0]*self.NumberOfVariablesToTrack)
        #################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_update_clock(self):

        #######################################################
        #######################################################
        #######################################################
        #######################################################
        if self.USE_GUI_FLAG == 1 and self.EXIT_PROGRAM_FLAG == 0:

            #######################################################
            #######################################################
            #######################################################
            if self.GUI_ready_to_be_updated_flag == 1:

                #######################################################
                #######################################################
                try:

                    #######################################################
                    if self.EntryListWithBlinking_OPEN_FLAG == 1:
                        self.EntryListWithBlinking_ReubenPython2and3ClassObject.GUI_update_clock()
                    #######################################################

                    #######################################################
                    Data_Label_TextToDisplay = self.ConvertDictToProperlyFormattedStringForPrinting(self.MostRecentDataDict, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3)
                    self.Data_Label["text"] = Data_Label_TextToDisplay
                    #######################################################

                    #######################################################
                    self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                    #######################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("PIDcontroller_ReubenPython2and3Class GUI_update_clock ERROR: Exceptions: %s" % exceptions)
                    traceback.print_exc()
                #######################################################
                #######################################################

            #######################################################
            #######################################################
            #######################################################

        #######################################################
        #######################################################
        #######################################################
        #######################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitNumber(self, min_val, max_val, test_val):

        if test_val > max_val:
            test_val = max_val

        elif test_val < min_val:
            test_val = min_val

        else:
            test_val = test_val

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitTextEntryInput(self, min_val, max_val, test_val, TextEntryObject):

        test_val = float(test_val)  # MUST HAVE THIS LINE TO CATCH STRINGS PASSED INTO THE FUNCTION

        if test_val > max_val:
            test_val = max_val
        elif test_val < min_val:
            test_val = min_val
        else:
            test_val = test_val

        if TextEntryObject != "":
            if isinstance(TextEntryObject, list) == 1:  # Check if the input 'TextEntryObject' is a list or not
                TextEntryObject[0].set(str(test_val))  # Reset the text, overwriting the bad value that was entered.
            else:
                TextEntryObject.set(str(test_val))  # Reset the text, overwriting the bad value that was entered.

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MyPrint_WithoutLogFile(self, input_string):

        input_string = str(input_string)

        if input_string != "":

            #input_string = input_string.replace("\n", "").replace("\r", "")

            ################################ Write to console
            # Some people said that print crashed for pyinstaller-built-applications and that sys.stdout.write fixed this.
            # http://stackoverflow.com/questions/13429924/pyinstaller-packaged-application-works-fine-in-console-mode-crashes-in-window-m
            if self.PrintToConsoleFlag == 1:
                sys.stdout.write(input_string + "\n")
            ################################

            ################################ Write to GUI
            self.PrintToGui_Label_TextInputHistory_List.append(self.PrintToGui_Label_TextInputHistory_List.pop(0)) #Shift the list
            self.PrintToGui_Label_TextInputHistory_List[-1] = str(input_string) #Add the latest value

            self.PrintToGui_Label_TextInput_Str = ""
            for Counter, Line in enumerate(self.PrintToGui_Label_TextInputHistory_List):
                self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + Line

                if Counter < len(self.PrintToGui_Label_TextInputHistory_List) - 1:
                    self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + "\n"
            ################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def IsInputList(self, InputToCheck):

        result = isinstance(InputToCheck, list)
        return result
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self, input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

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
                    ListOfStringsToJoin.append(self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

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
                    ListOfStringsToJoin.append("TUPLE" + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

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
                    ListOfStringsToJoin.append(str(Key) + ": " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

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
    def ConvertDictToProperlyFormattedStringForPrinting(self, DictToPrint, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3):

        ProperlyFormattedStringForPrinting = ""
        ItemsPerLineCounter = 0

        for Key in DictToPrint:

            ##########################################################################################################
            if isinstance(DictToPrint[Key], dict): #RECURSION
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     Key + ":\n" + \
                                                     self.ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key], NumberOfDecimalsPlaceToUse, NumberOfEntriesPerLine, NumberOfTabsBetweenItems)

            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     Key + ": " + \
                                                     self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key], 0, NumberOfDecimalsPlaceToUse)
            ##########################################################################################################

            ##########################################################################################################
            if ItemsPerLineCounter < NumberOfEntriesPerLine - 1:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\t"*NumberOfTabsBetweenItems
                ItemsPerLineCounter = ItemsPerLineCounter + 1
            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\n"
                ItemsPerLineCounter = 0
            ##########################################################################################################

        return ProperlyFormattedStringForPrinting
    ##########################################################################################################
    ##########################################################################################################

