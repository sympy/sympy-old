from pyglet.gl import *

def get_matrix():
    """
    Returns the current modelview matrix.
    """
    m = (c_float*16)()
    glGetFloatv(GL_MODELVIEW_MATRIX, m)
    return m

def billboard_matrix():
    """
    Removes rotational components of
    current matrix so that primitives
    are always drawn facing the viewer.

    |1|0|0|x|
    |0|1|0|x|
    |0|0|1|x| (x means left unchanged)
    |x|x|x|x|
    """
    m = get_matrix()
    m[0] =1;m[1] =0;m[2] =0
    m[4] =0;m[5] =1;m[6] =0
    m[8] =0;m[9] =0;m[10]=1
    glLoadMatrixf(m)
