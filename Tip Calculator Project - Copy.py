Tip Calculator Project

print("Welcome to the tip calculator")

tot_bill= float(input("what was the total bill? $"))

percentage_bill= float(input("what percentage tip would you like to give? "))

num_people= int(input("how many people to split the bill? "))
each_person_pay= tot_bill / num_people

final_value= round(((tot_bill/num_people)* percentage_bill/100 + each_person_pay), 2)

print(f"Each person should pay: ${final_value}")