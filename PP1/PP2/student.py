import random

"""
File: student.py
Resources to manage a student's name and test scores.
"""

class Student:
    def __init__(self, name, scores):
        self.name = name
        self.scores = scores

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
        return f"Name: {self.name}\nScores: {' '.join(map(str, self.scores))}"

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def __ge__(self, other):
        return self.name >= other.name


def main():
    students = [
        Student("Charlie", [90, 94, 100]),
        Student("Alice", [95, 85, 90]),
        Student("Eve", [88, 92, 96]),
        Student("Bob", [85, 87, 89]),
        Student("David", [91, 93, 97])
    ]

    print("Original list of students:")
    for student in students:
        print(student)

    # Shuffle the list
    random.shuffle(students)
    print("\nShuffled list of students:")
    for student in students:
        print(student)

    # Sort the list
    students.sort()
    print("\nSorted list of students:")
    for student in students:
        print(student)


if __name__ == "__main__":
    main()
