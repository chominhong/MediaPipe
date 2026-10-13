#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
print("🔍 파이썬 실행 및 라이브러리 로딩 시작...")

try:
    import cv2
    import mediapipe as mp
    print("✅ OpenCV 및 MediaPipe 임포트 성공")
except Exception as e:
    print(f"❌ 라이브러리 임포트 에러: {e}")
    sys.exit()

# =========================================
# 🧩 Mediapipe 얼굴 검출 초기화
# =========================================
try:
    mp_face_detection = mp.solutions.face_detection
    mp_drawing = mp.solutions.drawing_utils

    face_detection = mp_face_detection.FaceDetection(
        model_selection=0,               
        min_detection_confidence=0.5
    )
    print("✅ Mediapipe FaceDetection 객체 생성 성공")
except Exception as e:
    print(f"❌ Mediapipe 초기화 에러: {e}")
    sys.exit()

# =========================================
# 📸 카메라 연결
# =========================================
# cap = cv2.VideoCapture(0)            # 기본 카메라 사용 시
cap = cv2.VideoCapture("face.mp4")   # 동영상 파일 사용 시 (필요시 파일명 변경)

if not cap.isOpened():
    print("❌ 오류: 'hand.mp4' 파일을 찾을 수 없거나 열 수 없습니다. 파일을 파이썬 파일과 같은 폴더에 넣어주세요.")
    sys.exit()
else:
    print("✅ 비디오 파일 열기 성공")

print("📷 카메라 스트림 시작 — ESC를 눌러 종료합니다.")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("⚠️ 영상이 끝났거나 프레임을 읽지 못했습니다.")
        break

    # 좌우 반전 (셀카 뷰)
    image = cv2.flip(image, 1)

    # BGR → RGB 변환
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 얼굴 검출 수행
    result = face_detection.process(image_rgb)

    # 👤 얼굴 랜드마크 및 바운딩 박스 표시
    if result.detections:
        for detection in result.detections:
            mp_drawing.draw_detection(image, detection)

    # 화면에 맞게 크기 조정
    h, w = image.shape[:2]
    if h > 720:
        image = cv2.resize(image, (int(w * 720 / h), 720))

    # 화면 표시
    cv2.imshow('🤖 MediaPipe Face Detection', image)

    # ESC 키로 종료
    if cv2.waitKey(30) & 0xFF == 27:
        print("👋 종료합니다.")
        break

# =========================================
# 🔚 종료 처리
# =========================================
cap.release()
cv2.destroyAllWindows()