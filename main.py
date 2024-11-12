import time
import threading
import winsound
from pathlib import Path
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials


scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
ss = client.open('尿/飲水周期管理(腎臓移植)')
sheet = ss.get_worksheet(0)


def dt_to_txt(dt):
    return dt.strftime('%m/%d %H:%M')


def txt_to_dt(txt):
    return datetime.strptime(txt, '%m/%d %H:%M').replace(year=2024)


def get_next_urination_dt():
    return txt_to_dt(sheet.acell('C4').value)


prev_date = None


def save_alarm(dt):
    str_dt = dt_to_txt(dt)
    with open('alarm.txt', 'w') as f:
        f.write(str_dt)


def get_past_date_indices(dt_ary):
    now = datetime.now()
    return [i for i, d in enumerate(dt_ary) if now > d]


def read_txt_file(f_name):
    return Path(f_name).read_text()


def write_txt_file(f_name, txt):
    Path(f_name).write_text(txt)


def play_alarm():
    def f():
        winsound.PlaySound("alarm.wav", winsound.SND_FILENAME)
    thread = threading.Thread(target=f)
    thread.start()


def digest_alarm():
    alarm_dts = [txt_to_dt(a) for a in read_txt_file('alarm.txt').split('\n') if a]
    past_indices = get_past_date_indices(alarm_dts)
    if past_indices:
        print('past indices', past_indices)
        play_alarm()
        alarm_dts = [x for i, x in enumerate(alarm_dts) if i not in past_indices]
        write_txt_file('alarm.txt', '\n'.join(dt_to_txt(a) for a in alarm_dts))


def main():
    global prev_date
    while 1:
        digest_alarm()
        dt = get_next_urination_dt()
        if dt != prev_date:
            print('saving', dt)
            save_alarm(dt)
            prev_date = dt
        time.sleep(1)


if __name__ == "__main__":
    main()
