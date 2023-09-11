import os
import csv

class Descriptor:
    def __init__(self, value: str) -> None:
        self.name = value
    def __set_name__(self, owner, name):
        self.name = name
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]
    
    def __set__(self, instance, value: str) -> None:
        if not value.istitle():
            raise TypeError(f"Ошибка. Строка: {value} Первая буква должна быть заглавной")        
        if not value.isalpha():
            raise TypeError("Имеются недопустимые символы")
        instance.__dict__[self.name] = value

class student:
    surname = Descriptor("surname")
    name = Descriptor("name")
    patronymic = Descriptor("patronymic")
    def __init__(self, file: str, surname: str, name: str, patronymic: str) -> None:
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.result = self.readCSVFile(file)
        

    
    def verificationFile(self, file: str) -> bool:
        if os.path.exists(file):
            return True
        else:
            return False
    
    def readCSVFile(self, file: str) -> dict:
        result = {}
        if self.verificationFile(file):
            with open(file, "r", encoding="utf8") as f:
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    theme = row['Предмет']
                    evaluation = int(row['Оценка'])
                    test = int(row['Тест'])
                    mark = int(row['Балл'])
                    if theme in result.keys():
                        size = len(result[theme])
                        result[theme][size] = {"evaluation": evaluation, "test": test, "mark": mark}
                    else:
                        result[theme] = {}
                        result[theme][0] = {"evaluation": evaluation, "test": test, "mark": mark}
            return result
        else:
            return None
    
    def getAverageTestScore(self) -> None:
        for item in self.result:
            sumBall = 0
            for i in self.result[item]:
                sumBall += self.result[item][i]["mark"]
            sumBall /= len(self.result[item])
            print(f'По предмету {item} по тестам средний балл: {sumBall}')

    def getAverageGradeInSubjects(self) -> None:
        d = 0
        summa = 0
        for item in self.result:
            for i in self.result[item]:
                summa += self.result[item][i]["evaluation"]
                d += 1
        print(f'Средняя оценка по предметам {summa / d}')
    
    def getSurname(self) -> str:
        return self.surname
    
    def getName(self) -> str:
        return self.name
    
    def getPatronymic(self) -> str:
        return self.patronymic

if __name__ == "__main__":
    file = "grade.csv"
    snp = input("Введите ФИО: ")
    temp = snp.split(" ")
    obj = student(file, temp[0], temp[1], temp[2])
    print(obj.getSurname())
    print(obj.getName())
    obj.getAverageTestScore()
    obj.getAverageGradeInSubjects()