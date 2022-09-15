# import the necessary packages
# construct the argument parser and parse the arguments

def fun(url):
      import argparse
      import cv2
      import os
      args ={'edge_detector': 'hed_model'}
      url=str(url)
      args['image']=url
      print(args)
      class CropLayer(object):
            def __init__(self, params, blobs):
                  # initialize our starting and ending (x, y)-coordinates of
		      # the crop
                  self.startX = 0
                  self.startY = 0
                  self.endX = 0 
                  self.endY = 0
            def getMemoryShapes(self, inputs):
                  # the crop layer will receive two inputs -- we need to crop
		      # the first input blob to match the shape of the second one,
		      # keeping the batch size and number of channels
                  (inputShape, targetShape) = (inputs[0], inputs[1])
                  (batchSize, numChannels) = (inputShape[0], inputShape[1])
                  (H, W) = (targetShape[2], targetShape[3])
		      # compute the starting and ending crop coordinates
                  self.startX = int((inputShape[3] - targetShape[3]) / 2) 
                  self.startY = int((inputShape[2] - targetShape[2]) / 2)
                  self.endX = self.startX + W
                  self.endY = self.startY + H
		      # return the shape of the volume (we'll perform the actual
		      # crop during the forward pass
                  return [[batchSize, numChannels, H, W]]
            def forward(self, inputs):
		# use the derived (x, y)-coordinates to perform the crop
                  return [inputs[0][:, :, self.startY:self.endY,self.startX:self.endX]]
      print("[INFO] loading edge detector...")
      protoPath = os.path.sep.join([args["edge_detector"],"deploy.prototxt.txt"])
      modelPath = os.path.sep.join([args["edge_detector"],"hed_pretrained_bsds.caffemodel"])
      protoPath ="C:\\Users\\Akshaya\\Downloads\\hned-20220911T044053Z-001\\hned\\"+protoPath
      modelPath="C:\\Users\\Akshaya\\Downloads\\hned-20220911T044053Z-001\\hned\\"+modelPath
      print(protoPath,modelPath)
      net = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
      # register our new layer with the model
      cv2.dnn_registerLayer("Crop", CropLayer)
      # load the input image and grab its dimensions
      image = cv2.imread(args["image"])
      (H, W) = image.shape[:2]
      # convert the image to grayscale, blur it, and perform Canny
      # edge detection
      print("[INFO] performing Canny edge detection...")
      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
      blurred = cv2.GaussianBlur(gray, (5, 5), 0)
      canny = cv2.Canny(blurred, 30, 150)
      # construct a blob out of the input image for the Holistically-Nested
      # Edge Detector
      blob = cv2.dnn.blobFromImage(image, scalefactor=1.0, size=(W, H),mean=(104.00698793, 116.66876762, 122.67891434),swapRB=False, crop=False)
      # set the blob as the input to the network and perform a forward pass
      # to compute the edges
      print("[INFO] performing holistically-nested edge detection...")
      net.setInput(blob)
      hed = net.forward()
      hed = cv2.resize(hed[0, 0], (W, H))
      hed = (255 * hed).astype("uint8")
      # show the output edge detection results for Canny and
      # Holistically-Nested Edge Detection
      s1=args['image']
      print(s1)
      p='C:\\Users\\Admin\\Downloads\\hned\\hned\\\static\\pics\\'+'canny_'+"output1.jpg"
      q='C:\\Users\\Admin\\Downloads\\hned\\hned\\\static\\pics\\'+'hed_'+"output2.jpg"
      r='C:\\Users\\Admin\\Downloads\\hned\\hned\\\static\\pics\\'+'input_'+"output3.jpg"
      print(p)
      cv2.imwrite(p,canny)
      cv2.imwrite(q,hed)
      cv2.imwrite(r,image)
      cv2.waitKey(0)