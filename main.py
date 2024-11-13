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
sheet = ss.get_worksheet(2)  # 11/14


def txt_to_dt(txt):
    return datetime.strptime(txt, '%m/%d %H:%M').replace(year=2024)


def get_next_urination_dt():
    return txt_to_dt(sheet.acell('C4').value)


def play_alarm():
    def f():
        winsound.PlaySound("alarm.wav", winsound.SND_FILENAME)
    thread = threading.Thread(target=f)
    thread.start()


class NullAlarm:
    def __init__(self):
        self.dt = datetime(1970, 1, 1)

    def __ne__(self, other):
        return True

    def __lt__(self, other):
        return True


class Alarm:
    def __init__(self, dt):
        # only play once for now(maybe a counter in the future?)
        self.num_played = 0
        self.dt = dt

    def play(self):
        if self.num_played < 10:
            print('playing alarm', self.num_played)
            play_alarm()
            self.num_played += 1

    def __ne__(self, other):
        return self.dt != other.dt

    def __lt__(self, now):
        return self.dt < now

    def __repr__(self):
        return str(self.dt)


def main():
    alarm = NullAlarm()
    while 1:
        try:
            new_alarm = Alarm(get_next_urination_dt())
            if alarm != new_alarm:
                print('setting new alarm', new_alarm)
                alarm = new_alarm
            if alarm < datetime.now():
                alarm.play()
        except gspread.exceptions.APIError as e:
            print(str(e))
        time.sleep(10)


if __name__ == "__main__":
    main()
