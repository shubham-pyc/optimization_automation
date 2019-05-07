import sys
from campaign import Campaign
from cli import get_arguments
campagin_name_argument = 1

def main():
	try:
		arguments = get_arguments()
		campaign_name = arguments.name
		variants = arguments.variants
		debug = arguments.debug
		conditions = arguments.conditions
		campaign  = Campaign(campaign_name, debug=True, variants=variants)
	
		campaign.setup_folder()
		campaign.inject_files()
		campaign.populate_file()
		
		condition_mapping = campaign.get_condition_mapping()
		if conditions:
			for condition in conditions:
				if condition not in condition_mapping:
					raise ValueError("Invalid Condition {}".format(condition))
			campaign.inject_eligibility_criteria(conditions)
	except Exception as e:
		print(e)
main()
