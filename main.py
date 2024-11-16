import time
import keyboard
import winsound
import gspread
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials


SPREAD_TITLE = '尿/飲水周期管理(腎臓移植)'
NEXT_URINE_CELL = 'K6'


def get_spread_sheet(title):
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    return client.open(title)


def txt_to_dt(txt):
    return datetime.strptime(txt, '%m/%d %H:%M').replace(year=2024)


def get_next_urination_dt(sheet):
    return txt_to_dt(sheet.acell(NEXT_URINE_CELL).value)


def play_alarm():
    winsound.PlaySound("alarm.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)


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


alarm = NullAlarm()


def stop_alarm():
    print('stopping alarm')
    global alarm
    alarm.stop()
    # Play null sound to stop the current one playing
    winsound.PlaySound(None, winsound.SND_ASYNC)


def is_urination_dt_valid(sheet):
    try:
        return sheet.acell(NEXT_URINE_CELL).value != '#N/A'
    except ValueError:
        return False


def get_worksheet(spread, now):
    """
    今回のループで使うシートを返す処理
    出来れば現在の日付に当たるシートを使いたいが、
    日付が丁度変わったタイミングで最新のシートに何もデータが無いと尿の日付に値がセットされてない
    値の取得が無理な場合は前日のスプシの「次の尿時間」を利用する為、前日のスプシを返す
    """
    def get_worksheet_title(dt):
        return dt.strftime('%m/%d')

    sheet = spread.worksheet(get_worksheet_title(now))
    if not is_urination_dt_valid(sheet):
        sheet = spread.worksheet(get_worksheet_title(now - timedelta(days=1)))
    return sheet


def main():
    global alarm
    keyboard.add_hotkey('esc', stop_alarm)
    while 1:
        try:
            # TODO: integration test
            now = datetime.now()
            new_alarm = Alarm(get_next_urination_dt(get_worksheet(get_spread_sheet(SPREAD_TITLE), now)))
            if alarm != new_alarm:
                print('setting new alarm', new_alarm)
                alarm = new_alarm
            if alarm < now:
                alarm.play()
        # エラーを限定してる余裕ないので全部キャッチして表示する
        except Exception as e:
            print(str(e))
        time.sleep(10)


if __name__ == "__main__":
    main()
