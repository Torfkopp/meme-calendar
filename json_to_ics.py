import json
from datetime import datetime

with open ("memes.json", "r") as f: entries = json.load(f)

filtered = []
id = 0

# In case only having DTSTART doesn't work
# def convert_to_ics_date(month, day):
#     date = f"{datetime.datetime.now().year()}{month.zfill(2)}{day.zfill(2)}"
#     return "DTSTART:" + date + "T000000Z", "DTEND:" + date + "T235959Z"

def convert_to_ics_date(month, day):
    return f"{datetime.now().year}{str(month).zfill(2)}{str(day).zfill(2)}"

def is_filtered(origin):
    return origin in filtered if type(origin) is not list else any(x in filtered for x in origin)

def create_entry(entry):
    if is_filtered(entry["origin"]): return ""
    global id
    uid = "UID:" + f"MEMECALENDAR-Entry-{day}.{month}-{id}"
    id += 1
    summary = "SUMMARY:" + entry["name"]
    description = "DESCRIPTION:" + entry["description"]
    dt_start = "DTSTART:" + convert_to_ics_date(month, day)
    dt_stamp = "DTSTAMP:" + datetime.now().strftime("%Y%m%dT%H%M%S")
    return "\n".join(["BEGIN:VEVENT", uid, summary, description, dt_start, dt_stamp, "END:VEVENT", ""]) 

ics = ""

for month in entries:
    for day in entries[month]:
        if type(entry := entries[month][day]) is list: 
            for i in entry: ics += create_entry(i)
        else: ics += create_entry(entry)

ics = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:1\n" + ics + "END:VCALENDAR"

with open("memes.ics", "w") as f: f.write(ics)