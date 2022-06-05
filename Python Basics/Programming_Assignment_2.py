# Programming Assignment 2
# 1. Write a Python program to convert kilometers to miles?
# 2. Write a Python program to convert Celsius to Fahrenheit?
# 3. Write a Python program to display calendar?
# 4. Write a Python program to solve quadratic equation?
# 5. Write a Python program to swap two variables without temp variable?

def convert_km_to_miles(km):
    """This function converts kilometers to miles
    :rtype: float
    :param km:
    :return miles:
    """
    miles = km * 0.621371
    return miles


def convert_celsius_to_fahrenheit(dc):
    """This function converts celsius to fahrenheit"""
    fh = dc * 1.8 + 32
    return fh


def display_calendar(yr):
    """This function displays the calendar for the year"""
    import calendar
    cals = calendar.calendar(yr)
    return cals


def quadratic_equation(a, b, c):
    """This function solves the quadratic equation"""
    import math
    p1 = (-b + math.sqrt(b**2 - 4 * a * c)) / (2 * a)
    p2 = (-b - math.sqrt(b**2 - 4 * a * c)) / (2 * a)
    return p1, p2


def swap_variables(a, b):
    """This function swaps the variables"""
    a, b = b, a
    return a, b


if __name__ == '__main__':
    print("1. Write a Python program to convert kilometers to miles?")
    print("2. Write a Python program to convert Celsius to Fahrenheit?")
    print("3. Write a Python program to display calendar?")
    print("4. Write a Python program to solve quadratic equation?")
    print("5. Write a Python program to swap two variables without temp variable?")

    km = float(input("Enter the number of kilometers: "))
    miles = convert_km_to_miles(km)
    print("The number of miles is: ", miles)

    celsius = float(input("Enter the number of celsius: "))
    fahrenheit = convert_celsius_to_fahrenheit(celsius)
    print("The number of fahrenheit is: ", fahrenheit)

    year = int(input("Enter the year: "))
    cal = display_calendar(year)
    print("The calendar for the year is: ", cal)

    a = float(input("Enter a: "))
    b = float(input("Enter b: "))
    c = float(input("Enter c: "))
    x1, x2 = quadratic_equation(a, b, c)
    print("The roots of the quadratic equation are: ", x1, x2)

    a = int(input("Enter a: "))
    b = int(input("Enter b: "))
    a, b = swap_variables(a, b)
    print("The swapped variables are: ", a, b)

