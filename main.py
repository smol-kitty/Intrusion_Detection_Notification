import cv2
from flask import Flask
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
from datetime import datetime

app = Flask(__name__)

sender_email = "<Sender Email>"
sender_password = "<Sender Password>"
receiver_email = "<Receiver Email>"

def send_email(image_path):
    subject = "Intruder Detected"
    body = "Pls check image!"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with open(image_path, 'rb') as img_file:
        img_attachment = MIMEImage(img_file.read())
        img_attachment.add_header('Content-Disposition', f'attachment; filename={os.path.basename(image_path)}')
        msg.attach(img_attachment)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)  # Log in to the email account
        text = msg.as_string()  # Convert the message to a string
        server.sendmail(sender_email, receiver_email, text)  # Send the email
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()  # Close the connection


@app.route('/trigger_camera')
def trigger_camera():
    cap = cv2.VideoCapture(1)
    ret, frame = cap.read()
    if ret:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        image_filename = f"captured_image_{timestamp}.jpg"
        image_path = os.path.join('captured_images', image_filename)

        os.makedirs('captured_images', exist_ok=True)

        cv2.imwrite(image_path, frame)
        print(f"Image captured and saved as {image_filename}")

        send_email(image_path)

    cap.release()
    return "Image captured and sent via email!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
