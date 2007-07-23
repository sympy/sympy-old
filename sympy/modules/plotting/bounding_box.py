from pyglet.gl import *
from plot_object import PlotObject
from plot_function import PlotFunction
from pyglet import font
from util import billboard_matrix

class BoundingBox(PlotObject):
    
    def __init__(self,
                 line_color=(0.7,0.75,0.8),
                 fill_color=(0.97,0.97,0.98),
                 cull_front=True,
                 show_labels=False):

        self.x_min, self.x_max = 0.0, 0.0
        self.y_min, self.y_max = 0.0, 0.0
        self.z_min, self.z_max = 0.0, 0.0

        self.line_color = line_color
        self.fill_color = fill_color
        self.cull_front = cull_front

        self.show_labels = show_labels
        self.label_font = None

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
        if self.show_labels:
            self.render_labels()
        if self.fill_color != None:
            self.render_box(line=False)
        if self.line_color != None:
            self.render_box(line=True)

    def start_render(self, drawing_text):
        glPushAttrib(GL_ENABLE_BIT | GL_POLYGON_BIT | GL_DEPTH_BUFFER_BIT)
        if self.cull_front:
            if not drawing_text:
                glCullFace(GL_FRONT)
                glEnable(GL_CULL_FACE)
            glDisable(GL_DEPTH_TEST)

    def end_render(self):
        glPopAttrib()

    def render_labels(self):
        self.start_render(True)

        p = 0.2 # padding
        px_min = self.x_min-p; px_max = self.x_max+p
        py_min = self.y_min-p; py_max = self.y_max+p
        pz_min = self.z_min-p; pz_max = self.z_max+p

        self.render_basis_labels(0, (self.x_min, py_min, pz_max), (self.x_max, py_min, pz_max))
        self.render_basis_labels(1, (px_min, self.y_min, pz_max), (px_min, self.y_max, pz_max))
        self.render_basis_labels(2, (px_max, py_min, self.z_min), (px_max, py_min, self.z_max))

        self.end_render()

    def render_basis_labels(self, axis, start, end, stride=0.25):
        color = [.25,.25,.25,1]
        color[axis] = .75
        color = tuple(color)
        self.draw_text(str(start[axis]), start, color)
        self.draw_text(str(end[axis]), end, color)

    def draw_text(self, text, position, color):
        if self.label_font == None:
            #size = 18
            size = 10
            self.label_font = font.load('Arial', size, bold=True, italic=False)
        label = font.Text(self.label_font, text, color=color, halign=font.Text.CENTER)

        glPushMatrix()
        glTranslatef(*position)
        billboard_matrix()
        glScalef(0.01,0.01,0.01)
        glColor4f(0,0,0,0)
        label.draw()
        glPopMatrix()

    def render_box(self, line=True):
        self.start_render(False)

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

        self.end_render()
