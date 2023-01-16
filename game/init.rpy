default FreeCameraEnabled = False 
default CantUseFreeCamera = True

init:
    transform jump_up:
        pause .15
        yoffset 0
        easein .150 yoffset -25
        easeout .150 yoffset 0
        yoffset 0

    transform right_1:
        xpos 0.25
        
    transform left_1:
        xpos -0.25

    transform center_1:
        xpos 0.00
        
    transform moveinright_1:
        xanchor 0.5 yanchor 1.0 ypos 1.02 xpos 0.5
        linear 0.22 xpos 0.65