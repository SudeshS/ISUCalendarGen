from CalendarModel import *

# test 1


def test_parse_no_events():   # guest test parse calendar with no events
    f_path = 'data/input_isu_cal_i.ics'
    test_cal = CalendarModel.parse_cal(f_path)

    if CalendarModel.checkCalendarFormat(test_cal):
        test_var = CalendarModel.generateICSFile(test_cal)
        print(
            "Expected: \nVCALENDAR({'PRODID': vText('b'-//Calendar Event Generator//''), 'VERSION': vText('b'2.0'')})")
        print("Actual: ")
        print(test_var)
    else:
        print("Format Error")


# test 2
def test_guest_with_events():  # guest test parse calendar with four events
    f_path = 'UI/static/uploads/test_calendar.ics'
    test_cal = CalendarModel.parse_cal(f_path)

    if CalendarModel.checkCalendarFormat(test_cal):
        test_var = CalendarModel.generateICSFile(test_cal)
        print("\nExpected: ")
        print("Actual: ")
        print(test_var)
    else:
        print("Format Error")


def test_add_events():
    messages = [
    {'Summary': 'asdf', 'StartDate': '11/12/2022', 'StartTime': '11:00AM', 'Duration': '1H00M', 'UNTIL': '12/12/2022', 'BYDAY': 'FR', 'Description': 'ewofn132n', 'Location': '12r3'}, {'Summary': 'asdfg', 'StartDate': '09/12/2022', 'StartTime': '12:00PM', 'Duration': '1H15M', 'UNTIL': '12/15/2022', 'BYDAY': 'MO', 'Description': '21on241', 'Location': '12241'}
    ]

    event = CalendarModel.addEvents(list(messages))

def test_remove_events():
    messages = [
    {'Summary': 'COM 223', 'StartDate': '11/12/2022', 'StartTime': '11:00AM', 'Duration': '1H00M', 'UNTIL': '12/12/2022', 'BYDAY': 'FR', 'Description': 'ewofn132n', 'Location': '12r3'}, {'Summary': 'asdfg', 'StartDate': '09/12/2022', 'StartTime': '12:00PM', 'Duration': '1H15M', 'UNTIL': '12/15/2022', 'BYDAY': 'MO', 'Description': '21on241', 'Location': '12241'}
    ]
    filename = 'UI/static/uploads/test_calendar.ics'

    CalendarModel.removeEvents(filename, list(messages[0].values()))


# test 3
def test_guest_add_events():   # guest test add events
    f_path = 'data/input_isu_cal_ii.ics'
    test_cal = CalendarModel.parse_cal(f_path)

    if CalendarModel.checkCalendarFormat(test_cal):
        test_cal = CalendarModel.generateICSFile(test_cal)
    else:
        print("Format Error")

    CalendarModel.addEvents(test_cal)


if __name__ == "__main__":
    # test_parse_no_events()
    # test_guest_with_events()
    # test_add_events()
    test_remove_events()
    # add testing for accounts (sending to DB)
