# MediaPipe & OpenCV Video Processing Project

파이썬(Python), OpenCV, Google MediaPipe 라이브러리를 활용하여 웹캠, 영상 파일, 유튜브 스트림을 실시간으로 분석하고 처리하는 프로젝트입니다.

## 파일 구성 및 소개

1. 손 감지 (hand_detector.py)
- 설명: 동영상 파일(hand.mp4) 또는 웹캠을 입력받아 손의 관절 위치를 실시간으로 검출하고 연결선을 그려주는 프로그램입니다.
- 주요 기술: mediapipe.solutions.hands, cv2.VideoCapture

2. 유튜브 손 감지 (hand_youtube.py)
- 설명: 유튜브 영상 링크를 입력받아 스트림 주소를 추출한 뒤, 영상 속 손의 움직임을 감지하는 프로그램입니다.
- 주요 기술: yt-dlp, mediapipe.solutions.hands

3. 얼굴 감지 (face_detector.py)
- 설명: 영상 속 인물의 얼굴 영역(Bounding Box)과 주요 특징점을 감지하여 표시해 주는 프로그램입니다.
- 주요 기술: mediapipe.solutions.face_detection

4. 인물 배경 분리 및 블러 (selfie_segmentation.py)
- 설명: Selfie Segmentation 모델을 사용하여 인물과 배경을 실시간으로 분리하고, 인물만 남긴 채 배경에 가우시안 블러(Gaussian Blur)를 적용하는 프로그램입니다.
- 주요 기술: mediapipe.solutions.selfie_segmentation, cv2.GaussianBlur, numpy

## 사전 설치 요구사항

코드를 실행하기 전에 터미널에 아래 명령어를 입력하여 필요한 라이브러리를 설치하세요.

pip install opencv-python mediapipe numpy yt-dlp

## 실행 방법

원하는 파이썬 파일을 터미널에서 실행합니다. (예시: 손 감지 실행)

python hand_detector.py

- 공통 조작법: 실행 중인 창에서 키보드의 ESC 키를 누르면 프로그램이 종료됩니다.