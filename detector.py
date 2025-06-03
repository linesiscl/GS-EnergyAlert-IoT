import mediapipe as mp

class DetectorGestos:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=False,
                                    model_complexity=1,
                                    enable_segmentation=False,
                                    min_detection_confidence=0.5,
                                    min_tracking_confidence=0.5)

    #Essa função serve para detectar se os dois braços estão levantados
    def detect_raised_arms(self, frame):
        image_rgb = frame.copy()
        results = self.pose.process(image_rgb)

        if not results.pose_landmarks:
            return False

        landmarks = results.pose_landmarks.landmark

        RIGHT_WRIST = self.mp_pose.PoseLandmark.RIGHT_WRIST
        RIGHT_SHOULDER = self.mp_pose.PoseLandmark.RIGHT_SHOULDER
        LEFT_WRIST = self.mp_pose.PoseLandmark.LEFT_WRIST
        LEFT_SHOULDER = self.mp_pose.PoseLandmark.LEFT_SHOULDER

        rw_y = landmarks[RIGHT_WRIST].y
        rs_y = landmarks[RIGHT_SHOULDER].y
        lw_y = landmarks[LEFT_WRIST].y
        ls_y = landmarks[LEFT_SHOULDER].y

        right_arm_up = rw_y < rs_y
        left_arm_up = lw_y < ls_y

        return right_arm_up and left_arm_up
