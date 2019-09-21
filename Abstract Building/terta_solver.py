from numpy import dot, array, cross, transpose, matmul
from numpy.linalg import inv


#Transforms an arbitrary tetrahedron into a simple one
#Transforms a point P along with it
#checks if it's in the simplex tetra
def tetra_interior_solution(b,v_1,v_2,C,P):
    #transform everything to x,y basis with C on the z axis
    N = cross(v_1,v_2)
    if list(N) == [0,0,0]:
        return False

    #transform into x,y,z coordinates
    M = inv(transpose(array([v_1,v_2,N])))

    #transform from v_1, v_2, N coordinates with origin b, to x,y,z cooredinate with origin 0
    T_1 = lambda v: matmul(M,v-b)
    if T_1(C)[2] == 0:
        return False

    #normalize tetrahedron peak
    T_2 = lambda v: v - v[2]/T_1(C)[2]*(T_1(C)-array([0,0,1]))

    #Transform arbitrary tetrahedron to simple tetrahedron
    T = lambda v: T_2(T_1(v))

    #transform the proposed point
    P = T(P)

    #check if it's in the simple tetrahedron
    #0<x<1-z and 0<y<1-z
    if 0 <= P[0] and P[0] <=1-P[2] and 0 <= P[1] and P[1] <=1-P[2]:
        return True
    else:
        return False

v_1 = array([1,0,0])
v_2 = array([0,1,0])
N = cross(v_1,v_2)
M = array([v_1,v_2,N])
print(M)
C = array([0,0,10])
P = array([0,0,5])
b = array([-0.5,-0.5,0])
print(tetra_interior_solution2(b,v_1,v_2,C,P))
