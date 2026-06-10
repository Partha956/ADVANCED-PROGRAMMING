from abc import ABC, abstractmethod

class LibraryItem(ABC):
    total_items = 0

    def __init__(self, title, year):
        self.title = title
        self.year = year
        LibraryItem.total_items += 1

    @abstractmethod
    def displayInfo(self):
        pass

class Book(LibraryItem):
    def __init__(self, title, year, author="Unknown Author"):
        super().__init__(title, year)
        self.author = author

    def displayInfo(self):
        print(f"Book: '{self.title}' ({self.year}) by {self.author}")

class DVD(LibraryItem):
    def __init__(self, title, year, duration, genre):
        super().__init__(title, year)
        self.duration = duration
        self.genre = genre

    def displayInfo(self):
        print(f"DVD: '{self.title}' ({self.year}) - Genre: {self.genre}, Duration: {self.duration} mins")

library_collection = [
    Book("Dune", 1965, "Frank Herbert"),
    Book("1984", 1949),
    DVD("The Matrix", 1999, 136, "Sci-Fi"),
    DVD("Spirited Away", 2001, 125, "Animation")
]

for item in library_collection:
    item.displayInfo()

print(f"\nTotal items in library: {LibraryItem.total_items}")