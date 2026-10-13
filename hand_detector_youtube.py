#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import mediapipe as mp
import yt_dlp
import os

# =========================================
# 📺 유튜브 영상 다운로드 및 포맷 설정 함수
# =========================================
def download_youtube_video(url):
    output_filename = "temp_youtube.mp4"
    
    # 기존에 받아둔 임시 파일이 있다면 삭제
    if os.path.exists(output_filename):
        os.remove(output_filename)
        
    # 💡 유튜브 포맷 에러 및 JS 런타임 경고 해결을 위한 안정적인 옵션 설정
    ydl_opts = {
        # 'bestvideo+bestaudio/best' 또는 'bv*+ba/b' 설정 (ffmpeg가 없어도 다운로드 가능한 포맷 우선 선택)
        'format': 'best[ext=mp4]/best', 
        'noplaylist': True,
        'outtmpl': output_filename,
        'geo_bypass': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
    }
    
    print("🔄 유튜브 영상 다운로드 중...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("✅ 다운로드 완료")
    except Exception as e:
        print(f"❌ 다운로드 실패: {e}")
        exit(1)
        
    return output_filename

# =========================================
# 🔗 유튜브 링크 설정
# =========================================
youtube_url = 'https://www.youtube.com/shorts/r_RQE230ky4'  # 원하는 유튜브 영상 링크

# 유튜브 영상 다운로드 및 로컬 파일 경로 획득
video_path = download_youtube_video(youtube_url)

# =========================================
# 🧩 Mediapipe 손 감지(Hands) 초기화
# =========================================
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

# Context Manager(with 구문)를 사용하여 리소스 관리 최적화
with mp_hands.Hands(
    static_image_mode=False,         # 동영상 입력
    max_num_hands=2,                 # 최대 손 개수
    min_detection_confidence=0.5,    # 탐지 신뢰도
    min_tracking_confidence=0.5      # 추적 신뢰도
) as hands:

    # =========================================
    # 🎥 다운로드된 비디오 파일 연결
    # =========================================
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("❌ 비디오 파일을 열 수 없습니다.")
        exit()

    print("🎥 유튜브 손 감지 스트림 시작 — ESC를 눌러 종료합니다.")

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("⚠️ 영상이 끝났거나 프레임을 읽지 못했습니다.")
            break

        # BGR → RGB 변환
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 손 검출 수행
        result = hands.process(image_rgb)

        # 🖐️ 손 랜드마크 표시
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_styles.get_default_hand_landmarks_style(),
                    mp_styles.get_default_hand_connections_style()
                )

        # 화면에 맞게 크기 조정 (세로 영상이 화면보다 커서 창이 잘리는 것 방지)
        h, w = image.shape[:2]
        if h > 720:
            image = cv2.resize(image, (int(w * 720 / h), 720))

        # 화면 표시
        cv2.imshow('🖐️ MediaPipe YouTube Hand Detector', image)

        # ESC 키로 종료 (대기 시간 30ms)
        if cv2.waitKey(30) & 0xFF == 27:
            print("👋 종료합니다.")
            break

    # 캡처 객체 해제
    cap.release()
    cv2.destroyAllWindows()

# =========================================
# 🔚 프로그램 종료 시 임시 파일 정리
# =========================================
if os.path.exists(video_path):
    os.remove(video_path)
    print("🧹 임시 파일 정리 완료.")