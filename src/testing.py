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
    f_path = 'data/input_isu_cal_ii.ics'
    test_cal = CalendarModel.parse_cal(f_path)

    if CalendarModel.checkCalendarFormat(test_cal):
        test_var = CalendarModel.generateICSFile(test_cal)
        print("\nExpected: ")
        print("Actual: ")
        print(test_var)
    else:
        print("Format Error")


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
    test_parse_no_events()
    test_guest_with_events()
    # add testing for accounts (sending to DB)
