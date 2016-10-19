from flask import Flask, Response, request
from scipy.spatial import distance as dist
#import cv2

app = Flask(__name__)

@app.route('/')
def hello_world():
  url1 = request.args.get('url1')
  url2 = request.args.get('url2')

  #image = cv2.imread(url1)

  if not url1 or not url2:
    return Response(response='Parameters must include url1 and url2',
      status=400, \
      mimetype="application/json")

  return Response(response='cool',
                  status=200, \
                  mimetype="application/json")

if __name__ == '__main__':
    app.run()