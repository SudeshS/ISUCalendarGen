# author: Kaleb Liang

# courseModel class contains everything that is related to courses (extends events)
class courseModel:
    def __init__(self, instructor, location, section, department, courseID):
        self.instructor = instructor
        self.location = location
        self.section = section
        self.department = department
        self.courseID = courseID
