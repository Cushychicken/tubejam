import subprocess as sp
import re
from sys import argv

def mp3_slowdown(f_in, rate='0.5'):
    # FFMPEG binary
    FFMPEG_BIN = 'ffmpeg'
    # Destination Filehandle
    chop_ext = f_in.split('.')
    mp3_trans = open(chop_ext[0] + '-slow.mp3', 'wb')

    # Command array
    cmd = [ FFMPEG_BIN, '-i', '"%s"' % f_in,
           '-filter:a', '"atempo=%s"' % rate,
           '-f', 'mp3', '-']
    print " ".join(cmd)

    # Subprocess pipe variable
    pipe = sp.Popen(cmd,
                    stdin=sp.PIPE, 
                    stdout=sp.PIPE, 
                    stderr=sp.PIPE)

    # Write ffmpeg data to file and close
    mp3_trans.write(pipe.stdout.read())
    mp3_trans.close()
    return f_in + '-slow.mp3'

def audio_extract(f_in):
    # FFMPEG binary
    FFMPEG_BIN = 'ffmpeg'
    # Destination Filehandle
    chop_ext = f_in.split('.')
    mp3_trans = open(chop_ext[0] + '.mp3', 'wb')
    
    # Command array
    cmd = [ FFMPEG_BIN, '-i', f_in,
            '-vn', 
            '-ac', '2',
            '-ar', '44100',
            '-ab', '320k',
            '-f', 'mp3', '-']

    # Command Array
    pipe = sp.Popen(cmd,
                    stdin=sp.PIPE, 
                    stdout=sp.PIPE, 
                    stderr=sp.PIPE)
    mp3_trans.write(pipe.stdout.read())
    mp3_trans.close()
    return chop_ext[0] + '.mp3'

if __name__ == '__main__':
    codec_re = re.compile(r'(.*)\.mp([34])')
    for arg in argv[1:]:
        result = codec_re.search(arg)
        codec = ''
        if result:
            codec = result.group(2)
            if codec == '3':
                result = mp3_slowdown(arg)
            elif codec == '4':
                result = audio_extract(arg)
        else:
            print "Please provide an .mp3 or .mp4 file to transcode."
            raise SystemExit


