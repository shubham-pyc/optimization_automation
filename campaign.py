import sys
import os
import constants
from utils import make_abbreviation, merge_conditions
from lib import criteria as conditions
from lib import configurations_code as code
import traceback

class ExceptionHander:
    def __init__(self):
        pass
    def handle_exception(self,exception):
        exc_type, exc_value, exc_tb = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_tb)
        #traceback.print_exception(file=sys.stdout)
        print(exception)



class Campaign:
    def __init__(self,campaign_name, debug = False, variants = 1):
        '''
            Constructor Function
            :Param campagin_name: name of the campagin
            :Param debug: debug flag
            :Param variants: number of variants
        '''
        self.destination_folder = constants.ORIGINAL_FOLDER_PATH
        if debug:
            self.destination_folder = constants.DEBUG_FOLDER_PATH
        self.campaign_name = campaign_name
        self.campaign_path = os.path.join(self.destination_folder,"QA - BookingPath_{}".format(self.campaign_name))
        self.requirment_folder = os.path.join(self.campaign_path,"Requirement")
        self.source_folder = os.path.join(self.campaign_path,"Source File")
        self.test_suite_folder = os.path.join(self.campaign_path,"Dev test suite")
        self.campaign_scripts_folder = os.path.join(self.source_folder,"campaign scripts")
        self.variant_scripts_folder = os.path.join(self.source_folder,"variant script")
        self.common_script = os.path.join(self.campaign_scripts_folder,"common.js")
        self.qualification_script = os.path.join(self.campaign_scripts_folder,"qualification.js")
        self.analytics_script = os.path.join(self.campaign_scripts_folder,"analytics.js")
        self.variant_script_file = os.path.join(self.variant_scripts_folder,"variant$.js")

        self.is_folder_setup = False
        self.e_handler = ExceptionHander()
        self.number_of_variants = variants
    
    #Creates required folders
    def setup_folder(self):
        '''
            Method to setup all the required folders
        '''
        try:
            path_list = [
            self.campaign_path,
            self.requirment_folder,
            self.source_folder,
            self.campaign_scripts_folder,
            self.variant_scripts_folder,
            self.test_suite_folder
            ]

            if not os.path.exists(self.campaign_path):
                for folders in path_list:
                    os.mkdir(folders)
                self.is_folder_setup = True
                print("Created Directory at : {}".format(self.campaign_path))
        except Exception as e:
		    self.e_handler.handle_exception(e)
    
    #Creates all the initials files
    def inject_files(self):
        '''
            Method to create all the required files
            1) Common Script
            2) Qualification Script
            3) All Variant Scripts
        '''
        files_to_create = [
                self.qualification_script,
                self.common_script,
                self.analytics_script
            ]
        try:
            if os.path.exists(self.campaign_path) and self.is_folder_setup:
                for script in files_to_create:
                    open(script,'a').close()
                for i in range(1,self.number_of_variants+1):
                    open(self.variant_script_file.replace("$",str(i)),'a').close()
        except Exception as e:
            self.e_handler.handle_exception(e)
    
    # Method to insert boilerplate code into all the files
    def populate_file(self):
        '''
            Method to inject code into
            1) Common script
            2) Qualification Script
            3) Variant Scripts
        '''
        files = [
            self.qualification_script,
            self.common_script,
            self.analytics_script
        ]

        predefined_code = [
            code.QUALIFICATION_CODE,
            code.COMMON_CODE,
            code.ANALYTICS_CODE
        ]
        
        try:
            #appending all the variant files into files object
            for i in range(1,self.number_of_variants+1):
                files.append(self.variant_script_file.replace("$",str(i)))
                predefined_code.append(code.VARIANT_CODE)

            #created an abbreviation for the campaign for data layer object
            abbreviation = make_abbreviation(self.campaign_name)
            
            if os.path.exists(self.campaign_path) and self.is_folder_setup:
                for content, path in zip(predefined_code,files):
                    with open(path,'a') as f:
                        final_text = content.replace("$replace",abbreviation)
                        f.writelines(final_text.replace("$campaign",self.campaign_name))
        except Exception as e:
            print(e)
            self.e_handler.handle_exception(e)


    def inject_eligibility_criteria(self,criterias):
        '''
            Method to inject Eligibility Creterial into Qualification Scripts
            :Param criterias: list of elibigility criterias
        '''
        file_mapping = self.get_condition_mapping()
        checked_conditions = {}
        conditions_to_check = []
        function_to_call = []
        condition_to_inject = ""
        try:
            with open(self.qualification_script,'a+') as script:
                
                for criteria in criterias:
                    if criteria in file_mapping:
                        condition_object =file_mapping[criteria] 
                        script.writelines(condition_object['code'])
                        conditions_to_check.append(condition_object['requirement'])
                        function_to_call.append(condition_object['call'])
                
                    
                condition_to_inject = merge_conditions(conditions_to_check)
            filedata = ""
            with open(self.qualification_script,'r') as script:
                filedata = script.read()
                filedata = filedata.replace("$condition",condition_to_inject)
                filedata = filedata.replace("CONDITION"," && ".join(function_to_call))

            with open(self.qualification_script,'w') as script:
                script.writelines(filedata)


        except Exception as e:
            self.e_handler.handle_exception(e)
    
    def get_condition_mapping(self):
        '''
            Method to return elibigility criteria and it's code mapping
            :returns: Dic["elibigility criteria":"Code:]
        '''
        return conditions.CRITERIA_CODE_MAPPING
        