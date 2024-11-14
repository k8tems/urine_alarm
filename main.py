import time
import keyboard
import threading
import winsound
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials


NEXT_URINE_CELL = 'K6'
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
ss = client.open('尿/飲水周期管理(腎臓移植)')


def txt_to_dt(txt):
    return datetime.strptime(txt, '%m/%d %H:%M').replace(year=2024)


def get_next_urination_dt(sheet):
    return txt_to_dt(sheet.acell(NEXT_URINE_CELL).value)


def play_alarm():
    def f():
        winsound.PlaySound("alarm.wav", winsound.SND_FILENAME)
    thread = threading.Thread(target=f)
    thread.start()


class NullAlarm:
    def __ne__(self, other):
        return True

    def __lt__(self, other):
        return True

    def stop(self):
        pass


class Alarm:
    def __init__(self, dt):
        # only play once for now(maybe a counter in the future?)
        self.num_played = 0
        self.dt = dt
        self.stopped = False

    def play(self):
        if not self.stopped and self.num_played < 10:
            print('playing alarm', self.num_played)
            play_alarm()
            self.num_played += 1

    def __ne__(self, other):
        return self.dt != other.dt

    def __lt__(self, now):
        return self.dt < now

    def __repr__(self):
        return str(self.dt)

    def stop(self):
        self.stopped = True


def cancel_alarm():
    print('stopping alarm')
    alarm.stop()


alarm = NullAlarm()


def main():
    global alarm
    keyboard.add_hotkey('esc', cancel_alarm)
    while 1:
        worksheet_title = datetime.now().strftime('%m/%d')
        try:
            sheet = ss.worksheet(worksheet_title)
            new_alarm = Alarm(get_next_urination_dt(sheet))
            if alarm != new_alarm:
                print('setting new alarm', new_alarm)
                alarm = new_alarm
            if alarm < datetime.now():
                alarm.play()
        # エラーを限定してる余裕ないので全部キャッチして表示する
        except Exception as e:
            print(str(e))
        time.sleep(10)


if __name__ == "__main__":
    main()
