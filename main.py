import time
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials


scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
ss = client.open('尿/飲水周期管理(腎臓移植)')
sheet = ss.get_worksheet(0)


def get_next_urination_dt():
    dt = sheet.acell('B4').value
    return datetime.strptime(dt, '%m/%d %H:%M').replace(year=2024)


prev_date = None


def main():
    global prev_date
    while 1:
        time.sleep(1)
        dt = get_next_urination_dt()
        if dt != prev_date:
            print(dt)
            prev_date = dt


if __name__ == "__main__":
    main()
