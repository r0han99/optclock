#!~/miniconda3/bin/python

from datetime import date
import datetime
import sys
import json
import webbrowser
import pyperclip

def load_data_from_json(filename="~/.optdaysdata.json"):
    with open(filename, "r") as json_file:
        data = json.load(json_file)
    return data

def days_since_june_26():
    today = date.today()
    june_26 = date(today.year, 6, 26)
    
    if today < june_26:
        june_26 = date(today.year - 1, 6, 26)
    
    days_difference = (today - june_26).days
    
    return days_difference, today

# Function to calculate the number of days between two dates in the same year
def calculate_days_between_dates(stop_date_str):
    start_date_str = "June 26"
    year = datetime.datetime.now().year  # Assuming the current year for both dates
    start_date = datetime.datetime.strptime(f"{start_date_str} {year}", "%B %d %Y")
    stop_date = datetime.datetime.strptime(f"{stop_date_str} {year}", "%d %B %Y")
    days_difference = (stop_date - start_date).days
    return days_difference

def stop_the_clock():
    
    # result, _ = days_since_june_26()
    stopped_date = input("Enter the stop date (e.g., 8 July): ")
    result = calculate_days_between_dates(stopped_date)
    
    opt_clock_remaining = 90 - result

    # Write the values to a JSON file
    data = {
        "date-recorded": stopped_date,
        "daysfromstart": result,
        "daysremaining": opt_clock_remaining
    }

    with open("~/.optdaysdata.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
    
    print("Clockstopped!, Days recorded!.")
    print(f"- Number of days from June 26th to ({stopped_date}): {result} Days.")
    print(f"- OPT clock remaining days: {opt_clock_remaining} Days.")

print()

# ----

receipt_number = "" 

if "-s" in sys.argv or "--stop" in sys.argv:
    
    with open("~/.optflagfile", "r") as f:
        line = f.readline()

    print()

    if line.strip() != 'clock-stopped!':
        
        with open("~/.optflagfile", "w") as f:
            f.write("clock-stopped!")
            stop_the_clock()
            

    else:
        # Prompt the user for override confirmation
        override = input("Clock Already Stopped. Do you want to override and make changes? (Y/n): ")

        if override.lower() == 'y':
            # If user wants to override, perform the necessary actions
            print("Override confirmed. You can now make changes.")
            stop_the_clock()

        elif override.lower() == 'n':
            # If user does not want to override, perform the necessary actions
            print("No changes made. Keeping the current state.")
            loaded_data = load_data_from_json()
            date_stopped = loaded_data['date-recorded']
            print(f"OPT Clock Stopped!, Stopped on {date_stopped}")
            
            
            print("--" * 25)
            print(f"Number of days from June 26th to {date_stopped}: {loaded_data['daysfromstart']} Days.")
            print(f"OPT clock remaining days: {loaded_data['daysremaining']} Days.")
        
        else:
            raise "Invalid input use (y/n)!"

        
    

elif "--reset" in sys.argv:
    

    print("Clock reset!")

    with open("~/.optflagfile", "r") as f:
        line = f.readline()

    

    if line.strip() == 'clock-stopped!':
        print("Last Recorded Data! Status Clock -- Stopped!")
        loaded_data = load_data_from_json()
        date_stopped = loaded_data['date-recorded']
            
        print("--" * 25)
        print(f"Number of days from June 26th to {date_stopped}: {loaded_data['daysfromstart']} Days.")
        print(f"OPT clock remaining days: {loaded_data['daysremaining']} Days.")
    
    else:
        print("Last Recorded Data!")
        loaded_data = load_data_from_json()
        date_stopped = loaded_data['date-recorded']
            
        
        print("--" * 25)
        print(f"Number of days from June 26th to {date_stopped}: {loaded_data['daysfromstart']} Days.")
        print(f"OPT clock remaining days: {loaded_data['daysremaining']} Days.")

    with open("~/.optflagfile", "w") as f:
        f.write("running")

elif "--status" in sys.argv:
    with open("~/.optflagfile", "r") as f:
        line = f.readline()

    print(f"OPT Clock Status: {line.strip()}")
    if line.strip() == 'running':
        print("run, `optclock` to get the days!")

elif "--ead" in sys.argv:
    
    url = "https://egov.uscis.gov/"
    print(f"Receipt Number: {receipt_number}")
    print(f"Case Status Website: {url}" )

    pyperclip.copy(receipt_number)
    webbrowser.open(url)

elif "--uscis" in sys.argv:

    print("USCIS: https://www.uscis.gov/")
    webbrowser.open('https://www.uscis.gov/')

elif "--init" in sys.argv:

    with open("~/.optflagfile", "w") as f:
        pass

    print("Init Complete.")

    

elif "--help" in sys.argv:

    docs = '''
    Opt Clock Script Docs!
    
    -s or --stop: To stop the clock and record the last counted days of the clock.
    --reset: To Restart the clock and begin the count from where it left off.
    --status: Get the current status of the clock, "running" or "clock-stopped".
    --ead: Prints the case status website link and Receipt Number, 
            opens and copys the reciept number to the clipboard.
    --uscis: Opens USCIS Website to check status updates. Get your phone Ready with Authenticator.
    --help: To get help, oh shit, I guess you are here already.
    
    '''
    print(docs)
    
        
else:
    with open("~/.optflagfile", "r") as f:
        line = f.readline()

    if line.strip() == "running":
        result, today = days_since_june_26()

        
        print("OPT Clock!")
        print("--"*25)
        today_date = today.strftime('%d %B')
        print(f"- Number of days from June 26th to today ({today_date}): {result} Days.")

        opt_clock_remaining = 90 - result
        print(f"- OPT clock remaining days: {opt_clock_remaining} Days.")

        # Write the values to a JSON file
        data = {
            "date-recorded": today_date,
            "daysfromstart": result,
            "daysremaining": opt_clock_remaining
        }

        with open("~/.optdaysdata.json", "w") as json_file:
            json.dump(data, json_file, indent=4)
    
    else:
        loaded_data = load_data_from_json()
        date_stopped = loaded_data['date-recorded']
        print(f"OPT Clock Stopped!, Stopped on {date_stopped}")
        
        
        print("--" * 25)
        print(f"Number of days from June 26th to {date_stopped}: {loaded_data['daysfromstart']} Days.")
        print(f"OPT clock remaining days: {loaded_data['daysremaining']} Days.")