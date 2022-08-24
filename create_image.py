# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import locale
from PIL import Image, ImageDraw, ImageFont
import connect_calender as calender

font_files = dict(
    notosan='./Fonts/NotoSansJP-Regular.otf',
    title='./Fonts/BebasNeue-Regular.ttf',
    zenmaru='./Fonts/ZenMaruGothic-Regular.ttf',
)

def get_font(name: str, size: int):
    return ImageFont.truetype(font_files[name], size)

def get_weeklist(date: date):
    date_list = [datetime(date.year, date.month, date.day) + timedelta(days=i) for i in range(7)]
    # 文字列に変換
    date_str_list = [d for d in date_list]
    return date_str_list

def create():
    # 描画用カラーセット
    black = (0, 0, 0),
    white = (255, 255, 255)

    # 画像を480*800で新規作成
    SIZE = (480, 800)
    img = Image.new('RGB', SIZE, white)

    today = date.today()
    one_month_after = today + relativedelta(months=1)

    # スケジュールの取得
    events = calender.get_calender_events(start=today, end=one_month_after, count=6)
    draw = ImageDraw.Draw(img)
    # タイトル
    draw.multiline_text((10, 6), "スケジュール", fill=black, font=get_font('notosan', 30))

    # データ更新日の記載
    dt = datetime.now().isoformat(sep=' ')[:16].replace('-', '.')
    draw.multiline_text((SIZE[0] / 2, 22), f'最終更新: {dt}',
                        font=get_font('notosan', 16), fill=black)
    draw.line(((0, 46), (SIZE[0] - 10, 46)), fill=black, width=2)
    draw.line(((0, 50), (SIZE[0] - 10, 50)), fill=black, width=2)

    # ロケールを日本語にセット
    locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
    h = 0
    for event in events[0]:
        event_date_list = event[1][0].split("-")
        event_date = date(int(event_date_list[0]), int(event_date_list[1]), int(event_date_list[2]))
        weekday = event_date.strftime('%a')
        dt = "{:0>2}/{:0>2}({:1s})".format(event_date.month, event_date.day, weekday)

        text = dt \
            + f'{f"[{event[1][1][:5]}]" if len(event[1]) != 1 else "[ 終日 ]"}' \
            + f'　　{event[0] if len(event[0]) < 13 else event[0][:10] + "…"}'
        # 予定情報の書き込み
        draw.multiline_text((10,  (6 + 30 * h) + 50),
                            text, font=get_font('notosan', 22), fill=black)
        h += 1

    # 今週の予定リスト
    weeklist_top = 300
    list_space = 70
    weekday = ['月', '火', '水', '木', '金', '土', '日']
    one_week_after = today + timedelta(days=7)
    week_events = calender.get_calender_events(start=today, end=one_week_after, count=10)
    draw.multiline_text((10, 265), f'1週間の予定',
                        font=get_font('zenmaru', 30), fill=black)

    week_list = get_weeklist(today)
    for i, day in enumerate(week_list):
        draw.multiline_text((10, (list_space * i + 10) + weeklist_top),
                            f'{day.strftime("%d")} {weekday[day.weekday()]}', font=get_font('zenmaru', 25), fill=black)
        if len(week_events) != 0:
            task_count = 0
            for event in week_events[0]:
                event_date = event[1][0]
                if event_date == day.strftime("%Y-%m-%d") and task_count < 2:
                    text = f'{f"{event[1][1][:5]}〜{event[2][1][:5]}" if len(event[1]) != 1 else "[終日]"} ' + event[0]
                    draw.multiline_text((100, (list_space * i + 10) + weeklist_top + (task_count * 27)),
                                        text, font=get_font('zenmaru', 20),
                                        fill=black)
                    task_count += 1


        draw.line(((10, (list_space * i + 10) + weeklist_top), (SIZE[0] - 10, (list_space * i + 10) + weeklist_top)),
                  fill=black, width=2)

    img.save('image.bmp', 'bmp')
    return img


if __name__ == '__main__':
    create()