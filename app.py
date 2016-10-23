from flask import Flask, Response, request
from scipy.spatial import distance as dist
import numpy as np
import urllib
import cv2

app = Flask(__name__)

@app.route('/')
def hello_world():
  url1 = request.args.get('url1')
  url2 = request.args.get('url2')

  if not url1 or not url2:
    return Response(response='Parameters must include url1 and url2',
                    status=400, \
                    mimetype="application/json")


  image1 = url_to_image(url1)
  image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)

  hist1 = cv2.calcHist([image1], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
  hist1 = cv2.normalize(hist1).flatten()

  image2 = url_to_image(url2)
  image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)

  hist2 = cv2.calcHist([image2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
  hist2 = cv2.normalize(hist1).flatten()

  SCIPY_METHODS = (
    ("Euclidean", dist.euclidean),
    ("Manhattan", dist.cityblock),
    ("Chebysev", dist.chebyshev))


  d = dist.euclidean(hist1, hist2)


  return Response(response=str(d),
                  status=200, \
                  mimetype="application/json")

def url_to_image(url):
  print "downloading %s" % (url)
  # download the image, convert it to a NumPy array, and then read
  # it into OpenCV format
  resp = urllib.urlopen(url)
  image = np.asarray(bytearray(resp.read()), dtype="uint8")
  image = cv2.imdecode(image, cv2.IMREAD_COLOR)

  # return the image
  return image

if __name__ == '__main__':
    app.run()