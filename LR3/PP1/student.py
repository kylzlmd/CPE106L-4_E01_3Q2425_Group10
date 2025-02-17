"""
File: student.py
Resources to manage a student's name and test scores.
"""

class Student(object):
    def __init__(self, name, number):
        self.name = name
        self.scores = []
        for count in range(number):
            self.scores.append(0)

    def getName(self):
        return self.name

    def setScore(self, i, score):
        self.scores[i - 1] = score

    def getScore(self, i):
        return self.scores[i - 1]

    def getAverage(self):
        return sum(self.scores) / len(self.scores)

    def getHighScore(self):
        return max(self.scores)

    def __str__(self):
        return "Name: " + self.name + "\nScores: " + " ".join(map(str, self.scores))

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def __ge__(self, other):
        return self.name >= other.name

def main():
    student1 = Student("Alice", 3)
    student2 = Student("Bob", 3)
    student3 = Student("Alice", 3)

    print(f"Is {student1.getName()} equal to {student2.getName()}? {student1 == student2}") # False
    print(f"Is {student1.getName()} equal to {student3.getName()}? {student1 == student3}") # True
    print(f"Is {student1.getName()} less than {student2.getName()}? {student1 < student2}") # True
    print(f"Is {student2.getName()} less than {student1.getName()}? {student2 < student1}") # False
    print(f"Is {student1.getName()} greater than or equal to {student2.getName()}? {student1 >= student2}") # False
    print(f"Is {student2.getName()} greater than or equal to {student1.getName()}? {student2 >= student1}") # True

if __name__ == "__main__":
    main()
