import math
from math import sqrt
import numbers

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I

class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
       
        det = 0
        
        if self.h == 1:
            det = self.g[0][0]
            
        else:
            a = self.g[0][0]
            b = self.g[0][1]
            c = self.g[1][0]
            d = self.g[1][1]
            det = a*d - b*c
        return det

            
    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")
        
        trace = 0
        for i in range(self.h):
            trace += self.g[i][i]
        return trace

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")
        
        det = self.determinant()
        if det == 0:
            raise ValueError('Determinant equal to zero. Hence Inverse of the matrix does not exist')
        
        if self.h == 1:
            inverse = [[1./det]]
        else:
            inverse = 1./det * (self.trace()*identity(self.h) - self)
                    
        return inverse
            
    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        matrix_transpose = zeroes(self.w,self.h)
        for i in range(self.w):
            for j in range(self.h):
                matrix_transpose[i][j]=self.g[j][i]
        return matrix_transpose

    def is_square(self):
        return self.h == self.w

    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same") 
            
        added_matrix = zeroes(self.h,self.w)
        
        for i in range(self.h):
            for j in range(self.w):
                added_matrix[i][j] = self.g[i][j] + other.g[i][j]
        return added_matrix

    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        negative = zeroes(self.h,self.w)
        
        for i in range(self.h):
            for j in range(self.w):
                negative[i][j] = -self.g[i][j]
        return negative

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        subtracted_matrix = self + (-other)
        return subtracted_matrix

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        if isinstance(other,list):
            other_h = len(other)
            other_w = len(other[0])
        else:
            other_h = other.h
            other_w = other.w
            
        if self.w != other_h:
            raise(ValueError, "Matrices can only be multiplied when the #columns of the first matrix is equal to #rows of the                                    second matrix")
            
        product = zeroes(self.h,other_w)
        
        for i in range(self.h): # Traversing the rows of the matrix - product
            for j in range(other_w): # Traversing the columns of the matrix - product
                for k in range(self.w):
                    product[i][j] += self.g[i][k] * other[k][j] #Dot Product of row vectors from 'self' matrix with column                                                                        vectors from 'other' matrix
        return product
                

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        if isinstance(other, numbers.Number):
            pass
            scalar_product = zeroes(self.h,self.w)
            for i in range(self.h):
                for j in range(self.w):
                    scalar_product[i][j] = other * self.g[i][j]
        return scalar_product
            