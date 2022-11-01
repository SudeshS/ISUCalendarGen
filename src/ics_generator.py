from icalendar import Calendar, Event, vText
from datetime import datetime
import pytz
import uuid


def parse_cal(filename):
    with open(filename, 'r') as file:
        cal = Calendar.from_ical(file.read())
    for component in cal.walk():
        if component.name == "VEVENT":
            print(component.get('summary'))
            print(component.get('dtstart').dt)
            print(component.get('dtend').dt)
            print(component.get('dtstamp').dt)


def create_cal():
    cal = Calendar()
    cal.add('prodid', '-//Test Calendar//')
    cal.add('version', '2.0')

    event = Event()
    event.add('summary', 'Test event using icalendar package.')
    event.add('description', 'Professor: Rishi S')
    event.add('dtstart', datetime(2022, 9, 6, 9, 0, 0, tzinfo=pytz.timezone('US/Central')))
    event.add('dtend', datetime(2022, 9, 6, 10, 0, 0, tzinfo=pytz.timezone('US/Central')))
    event.add('dtstamp', datetime.now(tz=pytz.timezone('US/Central')))
    rrule_dict = {
        'freq': 'weekly',
        'byday': ['tu', 'th'],
        'until': datetime(2022, 9, 9)
    }
    event.add('rrule', rrule_dict)
    event['location'] = vText('Stevenson 104')
    event['uid'] = str(uuid.uuid4())
    cal.add_component(event)
    
    with open('data/test_cal.ics', 'wb') as file:
        file.write(cal.to_ical())


def main():
    create_cal()
    

if __name__ == '__main__':
    main()