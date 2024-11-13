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


def play_alarm():
    def f():
        winsound.PlaySound("alarm.wav", winsound.SND_FILENAME)
    thread = threading.Thread(target=f)
    thread.start()


class Alarm:
    def __init__(self, dt):
        # only play once for now(maybe a counter in the future?)
        self.played = False
        self.dt = dt

    def play(self):
        if not self.played:
            play_alarm()

    def __lt__(self, now):
        return self.dt < now


class NullAlarm:
    def play(self):
        pass


def main():
    alarm = NullAlarm()
    while 1:
        try:
            # 毎回更新するのでOK
            alarm = Alarm(get_next_urination_dt())
        except gspread.exceptions.APIError as e:
            print(str(e))
        if alarm < datetime.now():
            alarm.play()
        time.sleep(10)


if __name__ == "__main__":
    main()
