import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-variants', type=int, help= "Number of variants for the campaign", default=1)
    parser.add_argument('-name', type=str, required= True, help= "Name of the campaign")
    parser.add_argument('-removepath',type=bool, help="Removes BookingPath_ from files", default=False)
    arguments = parser.parse_args()
    return arguments
