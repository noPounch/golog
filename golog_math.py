from numpy import dot, array, cross, transpose, matmul
from numpy.linalg import inv


#Transforms an arbitrary tetrahedron into a simple one
#Transforms a point P along with it
#checks if it's in the simplex tetra
def tetra_interior(b,v_1,v_2,C,P):
    b = array(b)
    v_1 = array(v_1)
    v_2 = array(v_2)
    C = array(C)
    P = array(P)
    #transform everything to x,y basis with C on the z axis
    N = cross(v_1,v_2)
    if list(N) == [0,0,0]:
        return False
    if dot(b-C,N) == 0:
        return false

    #transform into x,y,z coordinates
    M = inv(transpose(array([v_1,v_2,C-b])))

    #recenter to b, make into normal tetrahedron
    P = matmul(M,P-b)

    #check if it's in the simple tetrahedron
    #0<x<1-z and 0<y<1-z
    if 0 <= P[0] and P[0] <=1-P[2] and 0 <= P[1] and P[1] <=1-P[2]:
        return True
    else:
        return False

if __name__ == "__main__":
    v_1 = array([1,0,0])
    v_2 = array([0,1,0])
    C = array([0,0,10])
    P = array([0,0,5])
    b = array([-0.5,-0.5,0])
    for t in range(-10,10):
        P = array([t/10,0,0])
        print(t/100, tetra_interior(b,v_1,v_2,C,P))
