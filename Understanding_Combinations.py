# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 01:55:01 2023

@author: hadaw
"""
from functools import lru_cache
from math import factorial
import numpy as np
import concurrent.futures


class Combinations:
    def __init__(self):
        super().__init__()
        self.Length = None

    @lru_cache(maxsize=1024)
    def total_combinations(self, Length, MaxSize, Permutations=False):
        """
            Parameters
            ----------
            length : int32
                Length is a integer that represents the length of the combination (EX: 123==3 1234=4)
            maxSize : int32
                maxSize is a integer that represents the max ammount of numbers in the combination
            permutations : Boolean, optional
                The default is False, but if set to true will find the permutations instead.

            Returns
            -------
            Array
                Returns an array.
        """
        def _c(N, R):
            if N < R:
                R = N

            # If permutations is set to true find the permuations rather.
            if Permutations:
                return factorial(N) / factorial(N - R)
            else:
                return factorial(N) / (factorial(R) * factorial(N - R))

        # Set the length object to the self length object
        self.Length = Length
        # Generate an array of zeros
        array = np.zeros((MaxSize - Length + 1))


        """ This while loop essentially increments through the array of zeros, assigning each index
            to the function call """


        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            while self.Length <= MaxSize:
                futures.append(executor.submit(_c, MaxSize, self.Length))
                self.Length += 1


            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                array[i] = future.result()

        # set the Length var to 0
        self.Length = 0


        # return the sum of the array
        return array.sum()


    # Define a function to start the game.
    def _main_(self):
        # Start the engine.
        pass


import timeit

# Create an instance of the Combinations class
combinations_instance = Combinations()

# Define a function to wrap the execution of total_combinations
def run_total_combinations():
    combinations_instance.total_combinations(3, 7, Permutations=False)

# Measure the execution time using timeit
execution_time = timeit.timeit(run_total_combinations, number=10000000)

# Print the execution time
print(f"Execution Time: {execution_time} seconds")
