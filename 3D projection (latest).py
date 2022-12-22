import pygame
from math import *
pygame.init()
#colors
red = (255, 0, 0); lime = (50, 205, 50); black = (20, 20, 20); blue = (100, 100, 255); white = (220, 220, 220); darkblack = (0, 0, 0)
WIDTH, HEIGHT = 1000, 600; window = pygame.display.set_mode((WIDTH, HEIGHT))

window.fill(darkblack)
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("calibri", 15)


class camera():
    def __init__(self, pos = (0, 0, 400), rot = (0, 0), FOV = 70, focal_length = 150, speed = 3):
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.rotx = rot[0]
        self.roty = rot[1]
        self.focal_length = focal_length
        self.speed = speed
        self.FOV = FOV

    def changeFOV(self):
        self.width = tan(radians(self.FOV / 2)) * self.focal_length * 2

    def move(self, key):
        if key[pygame.K_SPACE]: self.y += self.speed
        if key[pygame.K_LSHIFT]: self.y -= self.speed

        moveX = lambda rot: sin(radians(rot)) * self.speed
        moveZ = lambda rot: cos(radians(rot)) * self.speed

        if key[pygame.K_w]: self.x += moveX(self.rotx); self.z -= moveZ(self.rotx)
        if key[pygame.K_s]: self.x -= moveX(self.rotx); self.z += moveZ(self.rotx)
        if key[pygame.K_a]: self.x -= moveX(self.rotx - 90); self.z += moveZ(self.rotx - 90)
        if key[pygame.K_d]: self.x -= moveX(self.rotx + 90); self.z += moveZ(self.rotx + 90)

        if key[pygame.K_LEFT]: self.rotx += self.speed
        if key[pygame.K_RIGHT]: self.rotx -= self.speed
        if key[pygame.K_UP]: self.roty += 0.5
        if key[pygame.K_DOWN]: self.roty -= 0.5

cam = camera((0, 0, 400))
cam.changeFOV()



class cube():
    def __init__(self, size):
        self.vertices = [[-1,-1,-1],[1,-1,-1],[-1,1,-1],[1,1,-1],[-1,-1,1],[1,-1,1],[-1,1,1],[1,1,1]]
        for idx in range(len(self.vertices)):
            for i in range(3):
                self.vertices[idx][i] *= size
        self.edges = [[0,1],[0,2],[1,3],[2,3],[1,5],[0,4],[2,6],[3,7],[4,5],[5,7],[6,7],[4,6]]

cube1 = cube(40)
cube2 = cube(20)


def xprojected(pointXYZ):
    rot = radians(cam.rotx)
    px, py, pz = pointXYZ
    angle = atan2((px - cam.x), (pz - cam.z))
    x = cam.focal_length * (tan(angle + rot))
    x = (x * (WIDTH / (cam.width*2))) + WIDTH/2
    return x

def yprojected(pointXYZ):
    # turn degrees to radians
    rot = radians(cam.roty)
    # get x y z of the point
    px, py, pz = pointXYZ
    # calculate angle between the cam and point
    angle = atan2((py - cam.y), sqrt((px - cam.x)**2 + (pz - cam.z)**2))
    #calculate y based on the angle calculated before
    y = cam.focal_length * (tan(rot - angle))

    #scale the point
    y = (y * (WIDTH / (cam.width*2))) + HEIGHT/2
    return y

def project(pointXYZ):
    x, y = xprojected(pointXYZ), yprojected(pointXYZ)
    return x, y

def drawDebugMenu():

    #rots
    camrotxText = FONT.render(f"rot x: {cam.rotx} deg", False, white)
    camrotyText = FONT.render(f"rot y: {cam.roty} deg", False, white)
    window.blit(camrotxText, (WIDTH - (camrotxText.get_width()+10), 20))
    window.blit(camrotyText, (WIDTH - (camrotyText.get_width()+10), 40))

    # XYZ
    camxText = FONT.render(f"x: {int(cam.x)}", False, white)
    camyText = FONT.render(f"y: {int(cam.y)}", False, white)
    camzText = FONT.render(f"z: {int(cam.z)}", False, white)
    window.blit(camxText, (WIDTH - (camxText.get_width()+10), 70))
    window.blit(camyText, (WIDTH - (camyText.get_width()+10), 90))
    window.blit(camzText, (WIDTH - (camzText.get_width()+10), 110))

    #FOV and focal length
    FOVText = FONT.render(f"FOV: {cam.FOV} deg", False, white)
    FocalLengthText = FONT.render(f"Focal length: {cam.focal_length}", False, white)
    window.blit(FOVText, (WIDTH - (FOVText.get_width() + 10), 140))
    window.blit(FocalLengthText, (WIDTH - (FocalLengthText.get_width() + 10), 160))


def drawCubes(cubes):
    # drawing points
    # for point in cube.vertices:
    #     x, y = project(point)
    #     pygame.draw.circle(window, (255, 0, 0), (x, y), 2)
    for mycube in cubes:
        for edge in mycube.edges:
            p1 = project(mycube.vertices[edge[0]])
            p2 = project(mycube.vertices[edge[1]])
            pygame.draw.line(window, white, p1, p2, 1)

running = True
while running:
    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]: running = False
    if key[pygame.K_i]: cam.focal_length += 1
    if key[pygame.K_k]: cam.focal_length -= 1
    if key[pygame.K_u]: cam.FOV += 1; cam.changeFOV()
    if key[pygame.K_j]: cam.FOV -= 1; cam.changeFOV()

    cam.move(key)
    #deviding by 0 error
    # try:
    window.fill(darkblack)
    drawCubes([cube1, cube2])
    drawDebugMenu()
    # except:
        # print("Error probably division by zero")
    pygame.display.update()
    clock.tick(60)
    print(cam.FOV)
pygame.quit()
quit()