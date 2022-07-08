"""
import class from core

game.run()
"""

# from core import IsommtricGame
import subprocess
import sys

import core


def main():
    # cmdstring = ('ffmpeg', # put it in the same dir
    #         '-y',         # overwrite the file w/o warning
    #         '-r', '%f' % 30.0, # frame rate of encoded video
    #         '-an',       # no audio
    #         '-analyzeduration', '0',  # skip auto codec analysis
    #         # input params
    #         '-s', '800x600', # default panda window size
    #         '-f', 'rawvideo',   # RamImage buffer is raw buffer
    #         '-pix_fmt', 'rgba', # format of panda texure RamImage buffer
    #         '-i', '-',  # this means a pipe
    #         # output params
    #         # '-vtag', 'xvid', 
    #         '-vcodec', 'mpeg4',
    #         'screen.mp4')
        
    # p = subprocess.Popen(
    #         cmdstring, 
    #         stdin=subprocess.PIPE,
    #         bufsize=-1, 
    #         shell=False,
    #         )
    
    game = core.GameScene()

    if len(sys.argv) > 1:
        game.record()
    # game.proc = p
    try:
        game.run()
    finally:
        if len(sys.argv) > 1:
            subprocess.run('ffmpeg -r 30 -f image2 -s 2880x1800 -i frame_%04d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p screen.mp4 -y', shell=True)
        subprocess.run('rm frame_*', shell=True)
    


if __name__ == '__main__':
    main()
