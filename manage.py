import sys
from campaign import Campaign
from cli import get_arguments
campagin_name_argument = 1

def main():
	try:
		arguments = get_arguments()
		campaign_name = arguments.name
		variants = arguments.variants
		campaign  = Campaign(campaign_name, debug=True, variants=variants)
		campaign.setup_folder()
		campaign.inject_files()
		campaign.populate_file()
		campaign.inject_eligibility_criteria(['roundtrip','singlepax'])
	except Exception as e:
		print(e)
main()
