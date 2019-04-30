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
        self.destination_folder = constants.ORIGINAL_FOLDER_PATH
        if debug:
            self.destination_folder = constants.DEBUG_FOLDER_PATH
        self.campaign_name = campaign_name
        self.campaign_path = self.destination_folder+"/QA - BookingPath_{}".format(self.campaign_name)
        self.requirment_folder = "{}/Requirement".format(self.campaign_path)
        self.source_folder = "{}/Source File".format(self.campaign_path)
        self.test_suite_folder = "{}/Dev test suite".format(self.campaign_path)
        self.campaign_script_folder = "{}/campaign scripts".format(self.source_folder)
        self.variant_script_folder = "{}/variant script".format(self.source_folder)
        self.qualification_script = "{}/qualification.js".format(self.campaign_script_folder)
        self.common_script = "{}/common.js".format(self.campaign_script_folder)
        self.variant_script_file = "{}/variant$.js".format(self.variant_script_folder)
        
        self.is_folder_setup = False
        self.e_handler = ExceptionHander()
        self.number_of_variants = variants
    
    #Creates required folders
    def setup_folder(self):
        try:
            path_list = [
            self.campaign_path,
            self.requirment_folder,
            self.source_folder,
            self.campaign_script_folder,
            self.variant_script_folder,
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
        files_to_create = [
                self.qualification_script,
                self.common_script
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
        files = [
            self.qualification_script,
            self.common_script
        ]

        predefined_code = [
            code.QUALIFICATION_CODE,
            code.COMMON_CODE
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
        file_mapping = self.get_condition_mapping()
        checked_conditions = {}
        conditions_to_check = []
        condition_to_inject = ""
        try:
            with open(self.qualification_script,'a+') as script:
                
                for criteria in criterias:
                    if criteria in file_mapping:
                        script.writelines(file_mapping[criteria]['code'])
                        conditions_to_check.append(file_mapping[criteria]['requirement'])
                
                    
                condition_to_inject = merge_conditions(conditions_to_check)
            filedata = ""
            with open(self.qualification_script,'r') as script:
                filedata = script.read()
                filedata = filedata.replace("$condition",condition_to_inject)
            
            with open(self.qualification_script,'w') as script:
                script.writelines(filedata)


        except Exception as e:
            self.e_handler.handle_exception(e)
    
    def get_condition_mapping(self):
        return {
            "roundtrip":conditions.IS_ROUND_TRIP,
            "singlepax":conditions.IS_SINGLE_PAX,
            "userlogin":conditions.IS_USER_LOGIN
        }
        