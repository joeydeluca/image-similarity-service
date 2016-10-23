from flask import Flask, Response, request, jsonify
from scipy.spatial import distance as dist
import sys
import numpy as np
import urllib
import cv2

app = Flask(__name__)

@app.route('/')
def hello_world():

  # Get input data
  url1 = request.args.get('url1')
  url2 = request.args.get('url2')

  # Validate input data
  if not url1 or not url2:
    resp = jsonify({
      'status'  : 'error',
      'errorMessage': 'Parameters must include url1 and url2'
    })
    resp.status_code = 400
    return resp;

  # Compare images. The lower the number, the closer the match
  try:
    compareResult = dist.euclidean(get_histogram_from_url(url1), get_histogram_from_url(url2))
  except:
    errorMessage = json.dumps(sys.exc_info()[0])
    print("Unexpected error:", errorMessage)
    resp = jsonify({
      'status'  : 'error',
      'errorMessage': errorMessage
    })
    resp.status_code = 500
    return resp;

  resp = jsonify({
    'status'  : 'success',
    'result' : str(compareResult),
  })
  resp.status_code = 200
  return resp;


def url_to_image(url):
  print "downloading %s" % (url)
  # download the image, convert it to a NumPy array, and then read
  # it into OpenCV format
  resp = urllib.urlopen(url)
  image = np.asarray(bytearray(resp.read()), dtype="uint8")
  image = cv2.imdecode(image, cv2.IMREAD_COLOR)

  # return the image
  return image

def get_histogram_from_url(url):
  image = url_to_image(url)
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

  hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
  hist = cv2.normalize(hist).flatten()

  return hist;

if __name__ == '__main__':
    app.run()