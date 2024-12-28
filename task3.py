class School:

    def __init__(self):
        self.classes = []
        self.students = []

    def add_class(self, new_class):
        self.classes.append(new_class)

    def get_classes(self):
        return self.classes

    def add_student(self, new_student):
        self.students.append(new_student)

    def get_students(self):
        return self.students


class Student:

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.classes = []

    def add_class(self, new_class):
        self.classes.append(new_class)

    def get_average(self):
        sum_of_points = 0
        for some_class in self.classes:
            sum_of_points += some_class.get_score(self)
        return sum_of_points / len(self.classes)

    def count_attendance(self):
        sum_of_classes = 0
        for some_class in self.classes:
            if some_class.get_attendance(self):
                sum_of_classes += 1
        return sum_of_classes / len(self.classes)


class Class:

    def __init__(self, name):
        self.name = name
        self.students = []
        self.scores = {}
        self.attendance = {}

    def add_student(self, student):
        self.students.append(student)
        self.scores[student] = 0
        self.attendance[student] = False
        student.add_class(self)

    def set_score(self, student, score):
        if not self.attendance.get(student):
            raise Exception("Cannot set points for absent student: {} {}!".format(student.name, student.surname))
        self.scores[student] = score

    def set_attendance(self, student, attendance):
        self.attendance[student] = attendance

    def get_score(self, student):
        return self.scores.get(student)

    def get_attendance(self, student):
        return self.attendance.get(student)

    def get_students_average(self):
        sum_of_points = 0
        for score in self.scores.values():
            sum_of_points += score
        return sum_of_points / len(self.students)


if __name__ == '__main__':
    school1 = School()
    school2 = School()

    c1 = Class("OOP1-1")
    school1.add_class(c1)

    s1 = Student("Adam", "Kowalski")
    s2 = Student("Jan", "Nowak")

    school1.add_student(s1)
    school1.add_student(s2)
    c1.add_student(s1)
    c1.add_student(s2)

    c1.set_attendance(s1, True)
    c1.set_attendance(s2, True)
    c1.set_score(s1, 10)
    c1.set_score(s2, 5)

    c2 = Class("OOP1-2")
    school1.add_class(c2)

    c2.add_student(s1)
    c2.add_student(s2)

    c2.set_attendance(s1, True)
    c2.set_attendance(s2, False)
    c2.set_score(s1, 8)
    try:
        c2.set_score(s2, 6)
    except Exception as e:
        print(e)

    for school in [school1, school2]:
        for some_class in school.get_classes():
            print("Class:", some_class.name, "AVG:", some_class.get_students_average())
        for student in school.get_students():
            print("Student:", student.name, student.surname, "AVG:", student.get_average())
            print("Student:", student.name, student.surname, "attendance:", (student.count_attendance() * 100), '%')
