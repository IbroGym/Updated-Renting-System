#test.py

from calculator import *

my_list = [1, 2, 3, 4]

even_instance = Even()
double_instance = Double()

double_result = list(map(double_instance.twox, my_list))

even_result = list(filter(even_instance.isEven, my_list))

print("Results from Double class:")
print(double_result)

print("\nResults from Even class:")
print(even_result)
