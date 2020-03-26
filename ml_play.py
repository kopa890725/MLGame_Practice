"""
The template of the main script of the machine learning process
"""
import pickle
from os import path

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)

def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False
    ballPreX = 93;
    ballPreY = 395;
    #filename = 'your_file_name.pickle'
    #filename = path.join(path.dirname(__file__), filename)
    #log = pickle.load(open(filename, 'rb'))

    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()

    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()

        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            ball_served = False

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information
        
        speedX = scene_info.ball[0] - ballPreX;
        ballPreX = scene_info.ball[0];
        speedY = scene_info.ball[1] - ballPreY;
        ballPreY = scene_info.ball[1];

        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_RIGHT)
            ball_served = True
        else:
            # history_log = log[scene_info.frame]
            # action = history_log.command
            if abs(speedY) > 0 and scene_info.ball[1] > 10 and scene_info.ball[0] > 20 and scene_info.ball[0] < 480:
                frameBFcollide = (395 - scene_info.ball[1])/speedY ;
                point = scene_info.ball[0];
                direct = speedX / abs(speedX);
                speedX = abs(speedX);
                print(scene_info.ball[0],"  ",frameBFcollide,"  ",point);
                while frameBFcollide >= 1:
                    if direct == -1.0:
                        point = point + speedX
                    elif direct == -1.0:
                        point = point - speedX;
                    if point >= 200:
                        point = 200 - (point - 200);
                        direct = -direct;
                    elif point < 0:
                        point = -point;
                        direct = -direct;
                    frameBFcollide = frameBFcollide - 1;
                if point > scene_info.platform[0] + 20 :
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                if point < scene_info.platform[0] + 20 :
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                print(scene_info.platform[0] + 20 ,  "  " , point);
            else:
                if scene_info.platform[0] > 80 :
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                elif scene_info.platform[0] < 80 :
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
            
