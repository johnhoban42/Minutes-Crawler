import re
from os import listdir


# Get the difference of two times written in XX:XX format
def time_diff(start, end):
    start = list(map(int, start.split(':')))
    end = list(map(int, end.split(':')))
    if start[0] > end[0]:
        end[0] += 12
    diff = 60 * (end[0] - start[0]) + (end[1] - start[1])
    return diff


# Build roster
f = open("roster.txt", "r")
roster = f.readlines()
roster = [roster[x][:-1] for x in range(len(roster))]
f.close()

# Get directory containing minutes
minutes = None
try:
    minutes = listdir("./minutes")
except FileNotFoundError:
    print("Could not find the \"minutes\" directory. Aborting the crawler.\n")

for file_name in minutes:
    f = open("./minutes/{}".format(file_name), "r", encoding="utf8")
    contents = "".join(f.readlines())
    f.close()
    print("Data from minutes recorded in {}\n".format(file_name))

    # Find meeting length
    # Assumes all meetings are less than 12 hours, which is very reasonable
    pattern = r'Called to [Oo]rder at [0-9]{1,2}:[0-9]{2}'
    start_time = re.search(pattern, contents).group(0)[19:].strip()
    pattern = r'Adjournment \([0-9]{1,2}:[0-9]{2}'
    end_time = re.search(pattern, contents).group(0)[13:].strip()
    meeting_length = time_diff(start_time, end_time)
    print("MEETING LENGTH: {} minutes".format(meeting_length))

    # Find the length of each section of the meeting
    # These do not necessarily appear in the same order every meeting (Committee Business, Unfinished Business,
    # New Business, Special Orders, Announcement, Adjournment
    miscellaneous = 0
    committee_business = 0
    unfinished_business = 0
    new_business = 0
    special_orders = 0
    announcements = 0

    pattern = r'[^\n]+\([0-9]{1,2}:[0-9]{2}'
    times = re.findall(pattern, contents)
    start = start_time
    next_section = 'M'
    for section in times:
        end = section[section.index('(')+1:]
        section_length = time_diff(start, end)
        if next_section == 'M':
            miscellaneous = section_length
        elif next_section == 'C':
            committee_business = section_length
        elif next_section == 'U':
            unfinished_business = section_length
        elif next_section == 'N':
            new_business = section_length
        elif next_section == 'S':
            special_orders = section_length
        elif next_section == 'A':
            announcements = section_length
        start = end
        next_section = section[0]

    print("Committee Business: {} minutes".format(committee_business))
    print("Unfinished Business: {} minutes".format(unfinished_business))
    print("New Business: {} minutes".format(new_business))
    print("Special Orders: {} minutes".format(special_orders))
    print("Announcements: {} minutes".format(announcements))
    print("Miscellaneous: {} minutes\n".format(miscellaneous))

    total_speeches = 0
    total_motions = 0

    for name in roster:
        # Count speeches
        pattern = r'{}:'.format(name)
        speeches = len(re.findall(pattern, contents))
        total_speeches += speeches

        # Count motions
        pattern = r'{}:[^\n]+\([Ss]econded and passed\)'.format(name)
        motions = len(re.findall(pattern, contents))
        total_motions += motions

        print("{}: {} speeches, {} motions".format(name.upper(), speeches, motions))

    print("\nTOTAL: {} speeches, {} motions".format(total_speeches, total_motions))

    print("***\n")
