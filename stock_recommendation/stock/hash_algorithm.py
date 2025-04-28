class Hash:
    
   def __init__(self, value):
      self.value = value
      self.salt = "TA613MitT"
      self.a = 0.033128132  #these numbers are assigned values for the hashing
      self.b = 4541308606
      self.m = 706915480705422413531358259993
      self.p = 820671062463788161947946672849
      self.binary_numbers = [11011010 10001101, 10101111]
      
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
      self.value = bin(self.value | self.binary[0])
      
   def XOR_operation(self):
      self.value = bin(self.value ^ self.binary[1])
      
   def AND_operation(self):
      self.value = bin(self.value & self.binary[2])
      
   def NOT_operation(self):
      self.value = bin(~self.value)
      
   def left_shift_operation(self):
      self.value = bin(self.value << 2)
      
   def right_shift_operation(self):
      self.value = bin(self.value >> 2)
      
   def transformation(self):
      hold_var = self.value[2]
      self.var[2] = self.var[6]
      self.var[6] = hold_var
      
   def hash(self):  # This is the main method which will create a final hash value based on the above methods
      #probably good idea to include idea 7 below in this method
      #this method should give a final value
      # ideally the value should not be binary

'''
Note to self: make the code for the main 'hash' method, and then test


Ideas for the algorithm

7. **Dynamic Iterations**:
   - Base the number of hashing rounds on some characteristic of the input (e.g., input length) for a dynamic touch.
'''