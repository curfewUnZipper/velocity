from moviepy.editor import VideoFileClip, AudioFileClip
# from moviepy.video.fx.all import shake
from moviepy.video.fx.all import scroll
from moviepy.video.fx.all import speedx
from moviepy.editor import concatenate_videoclips


"""
DOCUMENTATION:
cutEdit - the velocity edit function
"""

######################################   EDIT FUNCTIONS    ###################################

def cutEdit(videoAddress,audioAddress,audioTimings,outputAddress,clipSpeed=1,effectTime=0.5,vidBegin=25):
    #normal and slowed flow with cuts
    #audio timings = [timeStart,t1,t2,t3,...tn,timeEnd];

    #.fx(speedx, clipSpeed)

    audioCut = [audioTimings.pop(0),audioTimings[-2],audioTimings.pop()]
    audio_clip = AudioFileClip(audioAddress).subclip(audioCut[0],audioCut[-1])
    cutBeg,cutEnd=[],[]
    durationList = []
    for x in range(len(audioTimings)):
        audioTimings[x]= audioTimings[x]-audioCut[0]
    durationList.append(audioTimings[0])
    for x in range(len(audioTimings)-1):
        durationList.append(audioTimings[x+1]-audioTimings[x])
    durationList.append(audioCut[-1]-audioCut[-2])        
    cutBeg.append(vidBegin) #change this to adjust video beginning
    cutEnd.append(cutBeg[0]+durationList[0]*clipSpeed)
    for x in range(1,len(durationList)):
        cutBeg.append(cutEnd[x-1]+effectTime)
        cutEnd.append(cutBeg[x]+durationList[x]*clipSpeed)

    # Initial Checks
    print(len(durationList),"DURATION LIST:",sum(durationList),durationList)
    print(len(cutBeg),"CUTS STARTS:",cutBeg)
    print(len(cutEnd),"CUTS ENDS  :",cutEnd)

    output=[]
    for i in range(len(cutBeg)):       
        output.append(VideoFileClip(videoAddress).subclip(cutBeg[i],cutEnd[i]).fx(speedx, clipSpeed))
    this = [(lambda x: x.duration)(obj) for obj in output]
    # Final Check before render
    print("DURATION LIST   :",len(durationList),durationList,"\nOUTPUT DURATIONS:",len(this),this)
    print("Audio Duration =",audioCut[-1]-audioCut[0],"\nVideo Duration =",sum(this))
    final_clip = concatenate_videoclips(output, method="compose")
    
    # Add audio and Render output
    final_clip = final_clip.set_audio(audio_clip)
    
    final_clip.write_videofile(outputAddress, codec="libx264", audio_codec="aac")
    
    

######################################    main     ###################################

cutEdit("./videos/llinkin.mp4","./audios/g3ox_em - GigaChad Theme (Phonk House Version).mp3",[24,30.0, 30.5, 31.0, 31.5, 32.0, 32.5, 33.0, 33.5, 34.0, 34.5, 35.0, 35.5,38],"./outputs/cutOut.mp4",clipSpeed=0.45,effectTime=1.2,vidBegin=25)
# cutEdit("./videos/llinkin.mp4","./audios/líue - Suffer With Me.mp3",[30,35.9, 36.6, 37.3, 38.0, 38.9, 39.6, 40.3, 41.6,47],"./outputs/cutOut2.mp4",clipSpeed=0.5,effectTime=2)



"""
audios/g3ox_em - GigaChad Theme (Phonk House Version).mp3        
starts 24; data = [30.0, 30.5, 31.0, 31.5, 32.0, 32.5, 33.0, 33.5, 34.0, 34.5, 35.0, 35.5]

audios/líue - Suffer With Me.mp3     
starts 30; data = [35.9, 36.6, 37.3, 38.0, 38.9, 39.6, 40.3, 41.6]
"""