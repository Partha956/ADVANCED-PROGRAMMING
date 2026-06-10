class Address:
    def __init__(self, street, city, zipCode):
        self.street = street
        self.city = city
        self.zipCode = zipCode

    def __str__(self):
        return f"{self.street}, {self.city}, {self.zipCode}"


class Student:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age 
        self.address = address
        self.courses = []

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Age must be a positive integer.")
        self._age = value

    def add_course(self, course):
        self.courses.append(course)

    def display(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Address: {self.address}")
        print(f"Courses: {', '.join(self.courses) if self.courses else 'No courses enrolled'}")


class ScholarshipStudent(Student):
    def __init__(self, name, age, address, scholarshipAmount):
        super().__init__(name, age, address)
        self.scholarshipAmount = scholarshipAmount

    def display(self):
        super().display()
        print(f"Scholarship Amount: ${self.scholarshipAmount}")


if __name__ == "__main__":
    addr1 = Address("123 Maple St", "Springfield", "12345")
    student1 = Student("Alice Smith", 20, addr1)
    
    student1.add_course("Mathematics")
    student1.add_course("Computer Science")
    student1.display()
    
    print("-" * 30)
    
    addr2 = Address("456 Oak Ave", "Metropolis", "67890")
    scholar_student = ScholarshipStudent("Bob Jones", 22, addr2, 5000)
    
    scholar_student.add_course("Physics")
    scholar_student.add_course("Chemistry")
    scholar_student.display()
    
    print("-" * 30)
    
    try:
        student1.age = -5
    except ValueError as e:
        print(f"Validation Error Caught: {e}")