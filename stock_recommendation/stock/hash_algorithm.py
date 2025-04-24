from random import randint

class Hash:
    
   def __init__(self, value):
      self.value = value
      self.salt = "TA613MitT"
      self.a = 0.033128132  #these numbers are assigned values for the hashing
      self.b = 4541308606
      self.m = 706915480705422413531358259993
      self.p = 820671062463788161947946672849
      self.binary_numbers = [01100101, 11011010 10001101, 10101111]
      
   def convert_to_string(self):
      self.value = str(self.value)
      
   def remove_white_space(self):
      for i in self.value:
         if i == " ":
            self.value.strip(i)
            
   def salting(self): # adds a salt value to prevent rainbow table attacks
      self.value.append(self.salt)
      
   def lowercase(self):
      self.value = self.value.lower()
      
   def convert_to_numbers(self): # allows for numerical hash methods (below)
      for i in self.value:
         i = ord(i)
         self.value.strip(i)
         self.value.append(i)
   
   # Five different hashing functions for high security
   def division_hash(self):
      self.value = self.value / self.m
   
   def multiplication_hash(self):
      self.value  = self.m*((self.value*self.a)%1)
   
   def mid_square_hash(self):
      self.value = self.value ** 2
      
      length = len(self.value) # len of hash value
      
      if length%2 == 0: #avoids hashes with an even number of characters
         self.value.strip(self.value[0])
      
      if length > 11:
         spare = length - 11  #amount of characters (more than 11)
         half_of_spare = spare/2  #to get the middle numbers
         self.value = self.value[half_of_spare:-half_of_spare]
   
   def folding_hash(self):
      value_one = 0
      value_two = 0
      value_three = 0
      
      mid_values = int(len(self.value)/3)  #divide value into three parts
      value_one = self.value[0:mid_values]
      value_one = self.value[mid_values:(mid_values*2)]
      value_three = self.value[(mid_values*2):]
         
      total = value_one + value_two + value_three
      self.value = total % self.m
   
   def universal_hash(self): #reduces chance of a value clash
      self.value = ((self.a * self.value + self.b) % self.p) % self.m
      
   def get_unicode(self):
      self.value = sum(ord(i) for i in self.value)
      
   def unicode_to_binary(self):
      self.value = bin(self.value)[2:]
      
   def random_binary(self):
      num = randint(1,4)
      return self.binary_numbers[num]
      
   def OR_operation(self):
      binary = self.random_binary()
      self.value = bin(self.value | binary)
      
   def XOR_operation(self):
      binary = self.random_binary()
      self.value = bin(self.value ^ binary)
      
   def AND_operation(self):
      binary = self.random_binary()
      self.value = bin(self.value & binary)
      
   def NOT_operation(self):
      self.value = bin(~self.value)
      
   def left_shift_operation(self):
      self.value = bin(self.value << 2)
      
   def right_shift_operation(self):
      self.value = bin(self.value >> 2) 
      
   def hash(self):  # This is the main method which will create a final hash value based on the above methods
      pass

'''
Note to self: Do ideas 6,7,8 (below) [not all necessarily have to be done],
and then make the code for the main 'hash' method


Ideas for the algorithm

1. **Input Normalization**:
   - Ensure uniformity by normalizing the input data, such as converting strings to lowercase, trimming whitespace, or handling character encoding.

2. **Salting the Input**:
   - Add a unique random value (salt) to the input before hashing to prevent pre-computed attacks like rainbow table attacks.

3. **Layered Hashing**:
   - Pass the input through multiple hash functions sequentially (e.g., SHA-256 followed by MD5) to increase complexity.

4. **Bitwise Operations**:
   - Integrate bitwise operations (e.g., XOR, AND, OR) between intermediate hashing steps to further mix the data.

5. **Keyed Hashing**:
   - Use an HMAC (Hash-Based Message Authentication Code) for added security by incorporating a secret key in the hashing process.

6. **Permutation/Transformation**:
   - Apply a transformation (e.g., substitution or reordering) on the intermediate hash output for added unpredictability.

7. **Dynamic Iterations**:
   - Base the number of hashing rounds on some characteristic of the input (e.g., input length) for a dynamic touch.

8. **Truncation or Padding**:
   - Ensure fixed-length output by truncating or padding the final hash to meet the desired size.

9. **Entropy Enhancement**:
   - Integrate external entropy (e.g., system timestamps or random numbers) into the hashing process for added randomness.

10. **Validation and Verification**:
    - Include a step for verifying the integrity of the hashed data by reapplying the algorithm on known inputs.

Remember to consider your use case—whether the goal is cryptographic security, fast indexing, or something else—as it will influence the algorithm's design.
'''