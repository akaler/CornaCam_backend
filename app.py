# flask and other web required frameworks
from flask import Flask, jsonify, request, Response, make_response
from flask_cors import CORS
import json
import numpy as np
import analytics
#import argparse

# from app import violations
import server_social_distance_detector 
import server_detect_mask 
import twillio_test
#from server_social_distance_detector import current_violations_sd

#from server_social_distance_detector import average_violations_sd
app = Flask(__name__)
CORS(app)


#phone_number = +19253231499
phone_number = +19494620
# # #
# # # # ROUTES        
# # # # # # # # #
def serialize_sets(obj):
    if isinstance(obj, set):
        return list(obj)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/getViolations", methods=['GET'])
def getViolations():
    # filee = request.files['file'] # get file from request body
    jsonData = []
    sentenceJSON = {
        "current_violations_sd": analytics.current_violations_sd,
        "average_violations_sd": analytics.average_violations_sd,
        "current_violations_masks": analytics.current_violations_masks,
        "average_violations_masks": analytics.average_violations_masks,
    }
    sentenceJSON = json.dumps(sentenceJSON, default=serialize_sets)
    jsonData.append(sentenceJSON)
    print("getViolation is called")

    if twillio_test.text_sent_sd == True: 
        if analytics.current_violations_sd < 9:
            twillio_test.text_sent_sd = False

    if analytics.average_violations_sd >= 9 and twillio_test.text_sent_sd == False:
        message = "Corona Cam warning: Number of social distance violation is too high. Current average is: {}".format(.analytics.average_violations_sd)
        twillio_test.send_message(message, phone_number)
        twillio_test.text_sent_sd = True

    if analytics.current_violations_masks >= 1:
        message = "Corona Cam warning: Number of mask violation is too high. Current average is: {}".format(analytics.average_violations_masks)
        twillio_test.send_message(message, phone_number) 
    return jsonify({
        "data": jsonData,
    })
@app.route('/video_sd1')
def video_sd1():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(server_social_distance_detector.gen_social_distancing(0),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_sd2')
def video_sd2():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(server_social_distance_detector.gen_social_distancing(1),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_sd3')
def video_sd3():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(server_social_distance_detector.gen_social_distancing(2),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_mask1')
def video_mask1():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(server_detect_mask.gen_mask(0),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_mask2')
def video_mask2():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(server_detect_mask.gen_mask(1),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_mask3')
def video_mask3():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(server_detect_mask.gen_mask(2),mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route("/savePhoneNumber", methods=['POST'])
def savePhoneNumber():
    phone_number = request.json['data']
    print(phone_number) # Save this phone number somewhere
    return jsonify({
        "data": "SUCCESS",
    })

if __name__ == "__main__":
    analytics.init()
    app.run(host='127.0.0.1', port=5000, debug=True)
