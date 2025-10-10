class Hash:
    
   def __init__(self, value):
      self.value = value
      self.salt = "TA613MitT"
      self.a = 0.033128132  #these numbers are assigned values for the hashing, and reflect the algabraic formulas which are used in the hashing algorithms
      self.b = 4541308606
      self.m = 706915480705422413531358259993
      self.p = 820671062463788161947946672849
      self.binary_numbers = [11011010, 10001101, 10101111]
      
   def convert_to_string(self):
      self.value = str(self.value)
      
   def remove_white_space(self):
      for i in self.value:
         if i == " ":
            self.value.strip(i)
            
   def salting(self): # adds a salt value to prevent rainbow table attacks
      self.value = self.value + self.salt
      
   def lowercase(self):
      self.value = self.value.lower()
      
   def convert_to_numbers(self): # allows for numerical hash methods (below)
      self.value = sum([ord(i) for i in self.value]) * (self.b**3)
   
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
      value = str(self.value)
      mid_values = int(len(value)/3)  #divide value into three parts
      
      value_one = float(value[0:mid_values])
      value_two = float(value[mid_values:(mid_values*2)])
      value_three = float(value[(mid_values*2):])
         
      total = value_one + value_two + value_three
      self.value = int(total % self.m)
   
   def universal_hash(self): #reduces chance of a value clash
      self.value = ((self.a * self.value + self.b) % self.p) % self.m
      
   
   # Methods for binary values
   def get_unicode(self):
      self.value = sum(ord(i) for i in str(self.value))
      
   def unicode_to_binary(self):
      self.value = bin(self.value)[2:]
      
   def OR_operation(self):
      self.value = bin(int(self.value) | self.binary_numbers[0])
      
   def XOR_operation(self):
      self.value = bin(int(self.value) ^ self.binary_numbers[1])
      
   def AND_operation(self):
      self.value = bin(int(self.value) & self.binary_numbers[2])
      
   def NOT_operation(self):
      self.value = bin(~int(self.value, 2)) # the number 2 turns it into base 2
      
   def left_shift_operation(self):
      self.value = bin(int(self.value, 2) << 2)
      
   def right_shift_operation(self):
      self.value = bin(int(self.value, 2) >> 2)
      
   def transformation(self):
      hold_var = self.value[2]
      self.var[2] = self.var[6]
      self.var[6] = hold_var
      
      
   def hash(self):  # This is the main method which will create a final hash value based on the above methods
      
      # Methods for every value before hashing begins
      self.convert_to_string()
      self.remove_white_space()
      self.remove_white_space()
      self.salting()
      self.lowercase()
      self.convert_to_numbers()
      
      # Get the first numbers of the value to decide which hashing methods are used
      values = str(self.value)
      
      first_value = int(values[0])
      second_value = int(values[1])
      third_value = int(values[2])
      fourth_value = int(values[3])
      
      # Hashing methods are decided by its value
      if first_value < 5:
         self.division_hash()
      else:
         self.multiplication_hash()
         
      if second_value < 5:
         self.mid_square_hash()
      else:
         self.folding_hash()
         
      if third_value < 5:
         self.universal_hash()
      
      elif third_value > 8:
         self.get_unicode()
         self.unicode_to_binary()
         
         if first_value == 0:
            self.OR_operation()
         else:
            self.XOR_operation()
         
         if second_value == 0:
            self.AND_operation()
         else:
            self.NOT_operation()
         
         if third_value == 0:
            self.left_shift_operation()
         else:
            self.right_shift_operation()
            
         if fourth_value == 0:
            self.transformation()
            
      return int(self.value, 2)