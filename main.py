import time
import threading
import winsound
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials


scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
ss = client.open('尿/飲水周期管理(腎臓移植)')
sheet = ss.get_worksheet(1)  # 11/13


def txt_to_dt(txt):
    return datetime.strptime(txt, '%m/%d %H:%M').replace(year=2024)


def get_next_urination_dt():
    return txt_to_dt(sheet.acell('C4').value)


alarm_dt = None


def play_alarm():
    def f():
        winsound.PlaySound("alarm.wav", winsound.SND_FILENAME)
    thread = threading.Thread(target=f)
    thread.start()


def maybe_update_alarm():
    global alarm_dt
    try:
        dt = get_next_urination_dt()
        if dt != alarm_dt:
            alarm_dt = dt
    except gspread.exceptions.APIError as e:
        print(str(e))


def main():
    global alarm_dt
    while 1:
        maybe_update_alarm()
        if alarm_dt and datetime.now() > alarm_dt:
            play_alarm()
        time.sleep(10)


if __name__ == "__main__":
    main()
