from CalendarModel import *

# test 1


def test_guest_no_events():   # guest test generation with no events
    f_path = 'data/input_isu_cal_i.ics'
    test_cal = CalendarModel.parse_cal(f_path)
    if CalendarModel.checkCalendarFormat(test_cal):
        CalendarModel.generateICSFile(test_cal)
        print("Test 1 Successful")
    else:
        print("Format Error")


# test 2
def test_guest_with_events():  # guest test generation with four events
    f_path = 'data/input_isu_cal_i.ics'
    test_cal = CalendarModel.parse_cal(f_path)
    if CalendarModel.checkCalendarFormat(test_cal):
        CalendarModel.generateICSFile(test_cal)
        print("Test 2 Successful")
    else:
        print("Format Error")


if __name__ == "__main__":
    test_guest_no_events()
    test_guest_with_events()
    # add testing for accounts (sending to DB)
