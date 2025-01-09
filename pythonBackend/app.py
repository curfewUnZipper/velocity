from flask import Flask, request, jsonify, send_file
from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.video.fx.all import scroll
from moviepy.video.fx.all import speedx
from moviepy.editor import concatenate_videoclips
from flask_cors import CORS  # Import CORS


"""
DOCUMENTATION:
cutEdit - the velocity edit function
"""

######################################   EDIT FUNCTIONS    ###################################

def cutEdit(videoAddress,audioAddress,audioTimings,clipSpeed=1,effectTime=0.5,vidBegin=25):
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
    return final_clip
    
    
##########################################      FLASK   ###################################
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return "Flask server is running. Use the /merge endpoint to merge video and audio."

@app.route('/merge', methods=['POST'])
def merge_video_audio():
    try:
        # Get uploaded files
        video = request.files['video']
        audio = request.files['audio']

        # Save the uploaded files locally
        video.save("uploaded_video.mp4")
        audio.save("uploaded_audio.mp3")

        # # Process the files - "uploaded_video.mp4"   and   "uploaded_audio.mp3

        editedVid = cutEdit("uploaded_video.mp4","uploaded_audio.mp3",[24,30.0, 30.5, 31.0, 31.5, 32.0, 32.5, 33.0, 33.5, 34.0, 34.5, 35.0, 35.5,38],clipSpeed=0.45,effectTime=1.2,vidBegin=25)

        # # Save the output
        output_file = "velocity_edit.mp4"
        editedVid.write_videofile(output_file, codec="libx264", audio_codec="aac")

        return send_file(output_file, as_attachment=True)
    
    except Exception as e:
        # Log the error for better debugging
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
