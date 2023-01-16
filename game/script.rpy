init python:
    import pygame

    class ParallaxLayer(renpy.Displayable):

        def __init__(self, child, xmotion, ymotion, **kwargs):

            super(ParallaxLayer, self).__init__(**kwargs)

            self.child = renpy.displayable(child)
            self.xmotion, self.ymotion = xmotion, ymotion

            if FreeCameraEnabled == True:
                self.x, self.y = renpy.display.draw.get_mouse_pos()
            else:
                self.x, self.y = (838, 574)
            self.x *= -self.xmotion
            self.y *= -self.ymotion
            self.target_x, self.target_y = self.x, self.y
            self.st = 0

        def render(self, width, height, st, at):

            if self.xmotion and FreeCameraEnabled == True:
                xspeed_mod = 2 * (st - self.st) / self.xmotion
                self.x += (self.target_x - self.x) * xspeed_mod
                if self.x < -self.xmotion * width:
                    self.x = -self.xmotion * width
                if self.x > 0:
                    self.x = 0

            if self.ymotion and FreeCameraEnabled == True:
                yspeed_mod = 2 * (st - self.st) / self.ymotion
                self.y += (self.target_y - self.y) * yspeed_mod
                if self.y < -self.ymotion * height:
                    self.y = -self.ymotion * height
                if self.y > 0:
                    self.y = 0

            self.st = st

            rv = renpy.Render(width, height)
            child = renpy.render(self.child, width, height, st, at)
            rv.subpixel_blit(child, (self.x, self.y))

            if self.target_x != self.x or self.target_y != self.y:
                renpy.redraw(self, 0)

            return rv

        def event(self, ev, x, y, st):
            if ev.type == pygame.MOUSEMOTION:
                if x * self.xmotion != self.target_x or y * self.xmotion != self.target_y:
                    self.target_x = -x * self.xmotion
                    self.target_y = -y * self.ymotion
                    renpy.redraw(self, 0)

        def visit(self):
            return [ self.child ]

    class ParallaxSprite(renpy.Displayable):

        def __init__(self, child, xmotion, ymotion, xpos=.5, xanchor=.5, ypos=.5, yanchor=.5, **kwargs):

            super(ParallaxSprite, self).__init__(**kwargs)

            self.child = renpy.displayable(child)
            self.xmotion = xmotion
            self.ymotion = ymotion

            self.x = 0
            self.target_x = 0
            self.y = 0
            self.target_y = 0
            self.st = 0

            self.xpos = xpos
            self.xanchor = xanchor
            self.ypos = ypos

        def render(self, width, height, st, at):

            x = renpy.display.draw.get_mouse_pos()[0]
            x *= -self.xmotion

            if FreeCameraEnabled != True:
                self.y = -25
                self.target_y = self.y
                self.x = -138
                self.target_y = self.x
            
            if self.xmotion and FreeCameraEnabled == True:
                xspeed_mod = 2 * (st - self.st) / self.xmotion
                self.x += (self.target_x - self.x) * xspeed_mod

            if self.ymotion and FreeCameraEnabled == True:
                yspeed_mod = 2 * (st - self.st) / self.ymotion
                self.y += (self.target_y - self.y) * yspeed_mod

            self.st = st

            if type(self.xpos) == float:
                xpos = width * self.xpos
            else:
                xpos = self.xpos
                
            if type(self.ypos) == float:
                ypos = width * self.ypos
            else:
                ypos = self.ypos

            child = renpy.render(self.child, width, height, st, at)
            cw, ch = child.get_size()
            rv = renpy.Render(width, height)
            rv.subpixel_blit(child, (xpos - cw * self.xanchor + self.x + width * self.xmotion / 2, self.y - height + cw * 1.75))

            if self.target_x != self.x and FreeCameraEnabled == True:
                renpy.redraw(self, 0)

            if self.target_y != self.y and FreeCameraEnabled == True:
                renpy.redraw(self, 0)

            return rv

        def event(self, ev, x, y, st):
            if ev.type == pygame.MOUSEMOTION:
                if x * self.xmotion != self.target_x or y * self.xmotion != self.target_y:
                    self.target_x = -x * self.xmotion
                    self.target_y = -y * self.ymotion
                    renpy.redraw(self, 0)

        def visit(self):
            return [ self.child ]
    
    def FreeCameraToggle():
        global CantUseFreeCamera, FreeCameraEnabled

        if CantUseFreeCamera == False:
            # there's a better way to do this
            if FreeCameraEnabled == False:
                FreeCameraEnabled = True
            else:
                FreeCameraEnabled = False 
        else:
            return


## Example of the code in use ##################################################

# chars
image asuka neutral = ParallaxSprite("images/asuka neutral.png", .10, .26)
image eileen1 happy = ParallaxSprite("images/jade happy.png", .10, .26)
image sydney worried = ParallaxSprite("images/sydney worried.png", .10, .26)

# bgs
image apartment = "images/apartment_day.png"

define e = Character('Eileen')

screen parallax:
    layer 'master'
    key '`' action Function(FreeCameraToggle)
    add ParallaxLayer("images/apartment_day.png", .10, .20)

label start:
    show screen parallax
    show asuka neutral at left_1
    show sydney worried at center_1
    show eileen1 happy at right_1
    $ CantUseFreeCamera = False 
    'You can use the free camera.'
    $ CantUseFreeCamera = True 
    $ FreeCameraEnabled = False
    'You cannot use the free camera.'
    return