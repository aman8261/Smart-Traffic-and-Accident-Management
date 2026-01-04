import cv2
import time
from ultralytics import YOLO
import numpy as np

# ======================================================================
#                          1) AMBULANCE DETECTION
# ======================================================================

def run_ambulance(video_source=0):
    print("\n🚑 Running Ambulance Detection... Press 'q' to exit.\n")

    model = YOLO("/Users/amangupta/Downloads/best.pt")
    cap = cv2.VideoCapture(video_source)

    ambulance_start_time = None
    ambulance_detected = False
    alert_triggered = False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, verbose=False)

        ambulance_found = False
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                label = model.names[cls_id]

                if "ambulance" in label.lower() and conf > 0.5:
                    ambulance_found = True

        # timing logic
        if ambulance_found:
            if not ambulance_detected:
                ambulance_detected = True
                ambulance_start_time = time.time()
            else:
                if time.time() - ambulance_start_time > 2 and not alert_triggered:
                    print("🚨 Ambulance detected continuously for 2 seconds!")
                    alert_triggered = True
        else:
            ambulance_detected = False
            ambulance_start_time = None
            alert_triggered = False

        cv2.imshow("Ambulance Detection", results[0].plot())
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


# ======================================================================
#                    2) ACCIDENT DETECTION (YOLO ACCIDENT MODEL)
# ======================================================================

def run_accident(video_source=0):
    print("\n💥 Running Accident Detection... Press 'q' to exit.\n")

    model = YOLO("/Users/amangupta/Downloads/latestAccident (1).pt")
    cap = cv2.VideoCapture(video_source)

    if not cap.isOpened():
        print("❌ Cannot open camera/video")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, verbose=False)
        accident_detected = False

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                label = model.names[cls]

                x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1-5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

                if "accident" in label.lower() and conf > 0.5:
                    accident_detected = True

        if accident_detected:
            cv2.putText(frame, "🔥 ACCIDENT DETECTED!", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

        cv2.imshow("Accident Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


# ======================================================================
#                    3) SMART TRAFFIC MANAGEMENT
# ======================================================================

def run_smart_traffic(video_source=0):
    print("\n🚦 Running Smart Traffic Light System... Press 'q' to exit.\n")

    model = YOLO("yolov8n.pt")
    cap = cv2.VideoCapture(video_source)

    CONF_THRESHOLD = 0.25
    DECISION_INTERVAL = 6
    MIN_GREEN = 5
    MAX_GREEN = 25

    def get_green_time(count):
        add = min(MAX_GREEN - MIN_GREEN, int(count * 1.5))
        return MIN_GREEN + add

    current_green = "TOP"
    green_remaining = 5
    last_switch = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        h, w = frame.shape[:2]

        LANES = {
            "TOP":    (0, 0, w, h//3),
            "LEFT":   (0, h//3, w//3, 2*h//3),
            "RIGHT":  (2*w//3, h//3, w, 2*h//3),
            "BOTTOM": (0, 2*h//3, w, h)
        }

        lane_counts = {k: 0 for k in LANES}

        # YOLO detection
        results = model(frame, verbose=False)
        r = results[0]

        if r.boxes is not None:
            for box in r.boxes:
                conf = float(box.conf[0])
                if conf < CONF_THRESHOLD:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                cx, cy = (x1 + x2)//2, (y1 + y2)//2

                # count in lanes
                for name, (lx1, ly1, lx2, ly2) in LANES.items():
                    if lx1 <= cx <= lx2 and ly1 <= cy <= ly2:
                        lane_counts[name] += 1
                        break

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 200, 0), 2)
                cv2.circle(frame, (cx, cy), 5, (0,255,255), -1)

        # decision logic
        now = time.time()
        if now - last_switch >= DECISION_INTERVAL:
            current_green = max(lane_counts, key=lane_counts.get)
            green_remaining = get_green_time(lane_counts[current_green])
            last_switch = now

        green_remaining -= 1/30  # approx FPS

        # Draw lanes
        for name, (x1, y1, x2, y2) in LANES.items():
            color = (0,255,0) if name == current_green else (0,0,255)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
            cv2.putText(frame, f"{name} ({lane_counts[name]})",
                        (x1+10, y1+40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        cv2.putText(frame, f"GREEN: {current_green} | {int(green_remaining)} sec",
                    (20, h-20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

        cv2.imshow("Smart Traffic Light", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


# ======================================================================
#                        MAIN MENU (Selection)
# ======================================================================

if __name__ == "__main__":
    print("""
==========================================
      SMART TRAFFIC UNIFIED SYSTEM
==========================================
1. Ambulance Detection
2. Accident Detection (YOLO Model)
3. Smart Traffic Light System
==========================================
""")

    choice = input("Select option (1/2/3): ")

    video_input = input("Enter video path (or 0 for webcam): ").strip()
    if video_input == "0":
        video_input = 0

    if choice == "1":
        run_ambulance(video_input)
    elif choice == "2":
        run_accident(video_input)
    elif choice == "3":
        run_smart_traffic(video_input)
    else:
        print("❌ Invalid selection")
