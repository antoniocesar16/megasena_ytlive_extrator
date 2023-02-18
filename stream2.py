import cv2, pafy

url   = "https://www.youtube.com/watch?v=86YLFOog4GM"
video = pafy.new(url)
best  = video.getbest(preftype="webm")
#documentation: https://pypi.org/project/pafy/

capture = cv2.VideoCapture(best.url)
check, frame = capture.read()
print (check, frame)

cv2.imshow('frame',frame)
cv2.waitKey(10)

capture.release()
cv2.destroyAllWindows()