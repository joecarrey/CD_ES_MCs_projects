Instructions
1. Run the following command on your console:
pip install -r requirements.txt
2. Run the next command to start the game:
python ping-pong.py

Information about other files:
label_map --> folder which contains trained model of format tensorflow 	frozen inference graph.There is also hand_label_map.pbtx to give 	which label we need;
label_map_util and string_int_label_map_pb2.py --> for label mappinga and 	them from graph;
detector.py --> gets frozen graph and session. It initializes webcam and 	creates videocapture. It also get hand position (center); 	
utils.py --> loads frozen graph and session, detects hand (palm) and 	draws a rectangle around;
requirements.txt --> list of libraries that should be installed to start 	the game.