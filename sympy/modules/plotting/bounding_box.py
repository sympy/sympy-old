from pyglet.gl import *
from plot_object import PlotObject
from plot_function import PlotFunction
"""from pyglet import font
from util import billboard_matrix"""

class BoundingBox(PlotObject):
    
    def __init__(self,
                 line_color=(0.7,0.75,0.8),
                 fill_color=(0.97,0.97,0.98),
                 cull_front=True,
                 show_labels=True):
        self.x_min, self.x_max = 0.0, 0.0
        self.y_min, self.y_max = 0.0, 0.0
        self.z_min, self.z_max = 0.0, 0.0

        if not cull_front and fill_color != None:
            raise Exception("Bounding Box: cull_front must = True if fill_color != None.")

        self.line_color = line_color
        self.fill_color = fill_color
        self.cull_front = cull_front

        """self.show_labels = show_labels
        self.label_font = None"""

    def consider_function(self, f):
        self.x_min = min([self.x_min, f.x_min])
        self.x_max = max([self.x_max, f.x_max])
        self.y_min = min([self.y_min, f.y_min])
        self.y_max = max([self.y_max, f.y_max])
        self.z_min = min([self.z_min, f.z_min])
        self.z_max = max([self.z_max, f.z_max])

    def render(self):
        if self.x_min == self.x_max and self.y_min == self.y_max and self.z_min == self.z_max:
            return

        """
        self.start_render(True)
        if self.show_labels:
            self.render_labels()
        self.end_render()
        """

        self.start_render(False)
        if self.fill_color != None:
            self.render_box(line=False)
        if self.line_color != None:
            self.render_box(line=True)
        self.end_render()

    def start_render(self, drawing_text):
        glPushAttrib(GL_ENABLE_BIT | GL_POLYGON_BIT | GL_DEPTH_BUFFER_BIT)

        if self.cull_front:
            if not drawing_text:
                glCullFace(GL_FRONT)
                glEnable(GL_CULL_FACE)
            glDisable(GL_DEPTH_TEST)

    def end_render(self):
        glPopAttrib()

    """
    def render_labels(self):
        self.render_basis_labels('x', (self.x_min, self.y_min, self.z_max), (self.x_max, self.y_min, self.z_max))
        self.render_basis_labels('y', (self.x_min, self.y_min, self.z_max), (self.x_min, self.y_max, self.z_max))
        self.render_basis_labels('z', (self.x_min, self.y_min, self.z_min), (self.x_min, self.y_min, self.z_max))

    def scale_vec(self, v, r):
        return (v[0]*r, v[1]*r, v[2]*r)

    def render_basis_labels(self, label, start, end, stride=0.25):
        self.draw_text(str(start), self.scale_vec(start, 1.2))
        self.draw_text(str(end), self.scale_vec(end, 1.2))

    def draw_text(self, text, position):
        if self.label_font == None:
            self.label_font = font.load('Arial', 18, bold=True, italic=False)
        label = font.Text(self.label_font, text, color=(0,0,0,1), halign=font.Text.CENTER)

        glPushMatrix()
        glTranslatef(*position)
        billboard_matrix()
        glScalef(0.01,0.01,0.01)
        glColor4f(0,0,0,0)
        label.draw()
        glPopMatrix()
    """

    def render_box(self, line=True):
        if line:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glColor3f(*self.line_color)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glColor3f(*self.fill_color)

        glBegin(GL_QUADS)

        # Top
        glVertex3f(self.x_max, self.y_max, self.z_max)
        glVertex3f(self.x_max, self.y_max, self.z_min)
        glVertex3f(self.x_min, self.y_max, self.z_min)
        glVertex3f(self.x_min, self.y_max, self.z_max)

        # Bottom
        glVertex3f(self.x_min, self.y_min, self.z_max)
        glVertex3f(self.x_min, self.y_min, self.z_min)
        glVertex3f(self.x_max, self.y_min, self.z_min)
        glVertex3f(self.x_max, self.y_min, self.z_max)

        # Left
        glVertex3f(self.x_min, self.y_max, self.z_min)
        glVertex3f(self.x_min, self.y_min, self.z_min)
        glVertex3f(self.x_min, self.y_min, self.z_max)
        glVertex3f(self.x_min, self.y_max, self.z_max)

        # Right
        glVertex3f(self.x_max, self.y_max, self.z_max)
        glVertex3f(self.x_max, self.y_min, self.z_max)
        glVertex3f(self.x_max, self.y_min, self.z_min)
        glVertex3f(self.x_max, self.y_max, self.z_min)

        # Front
        glVertex3f(self.x_min, self.y_max, self.z_max)
        glVertex3f(self.x_min, self.y_min, self.z_max)
        glVertex3f(self.x_max, self.y_min, self.z_max)
        glVertex3f(self.x_max, self.y_max, self.z_max)

        # Back
        glVertex3f(self.x_max, self.y_max, self.z_min)
        glVertex3f(self.x_max, self.y_min, self.z_min)
        glVertex3f(self.x_min, self.y_min, self.z_min)
        glVertex3f(self.x_min, self.y_max, self.z_min)

        glEnd()
