class Class():

    def __init__(self, teacherName, courseName, days):
        # Teacher name
        self.teacherName = teacherName
        # Course name
        self.courseName = courseName
        # List of days where this class takes place
        self.days = days
    
    def getTeacherName(self):
        return self.teacherName

    def getCourseName(self):
        return self.courseName
    
    def getCourse(self):
        splittedCourseName = self.courseName.split(' ')
        name = splittedCourseName[0] + ' ' + splittedCourseName[1]
        return name

    def getDays(self):
        return self.days

class Email():

    def __init__(self, subject, body):
        self.subject = subject
        self.body = body