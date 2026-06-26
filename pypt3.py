import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from zoneinfo import ZoneInfo
import calendar

st.set_page_config(page_title="Big Boiii Countdown", page_icon="🔒")

st.title("🔒 Countdown")
st.write("Count Down until **Big Boiii Big Dawg Danger D operates Jello**.")

tz = ZoneInfo("America/New_York")
target = datetime(2026, 8, 1, 8, 0, 0, tzinfo=tz)
target_ms = int(target.timestamp() * 1000)

today = datetime.now(tz).date()
cal = calendar.Calendar(firstweekday=6)  # Sunday start
weeks = cal.monthdatescalendar(today.year, today.month)

calendar_rows = ""
for week in weeks:
    calendar_rows += "<tr>"
    for day in week:
        classes = ["cal-day"]

        if day.month != today.month:
            classes.append("muted")

        if day == today:
            classes.append("today")

        if day == target.date():
            classes.append("target")

        calendar_rows += f'<td class="{" ".join(classes)}">{day.day}</td>'
    calendar_rows += "</tr>"

html = f"""
<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;700&display=swap" rel="stylesheet">

<style>
  .cd-wrap {{
    font-family: 'Rubik', system-ui, sans-serif;
    text-align: center;
  }}

  .cd-bar {{
    height: 4px;
    margin: 0 auto 28px;
    width: 100%;
    max-width: 520px;
    background: linear-gradient(90deg, #1a1a1a, #8B0000, #1a1a1a);
  }}

  .cd-grid {{
    display: flex;
    gap: 12px;
    justify-content: center;
    flex-wrap: wrap;
  }}

  .cd-cell {{
    background: #1c1c1c;
    border-radius: 6px;
    padding: 18px 22px;
    min-width: 92px;
    border: 1px solid #333;
    box-shadow: 0 4px 16px rgba(0,0,0,0.5);
  }}

  .cd-num {{
    font-size: 44px;
    font-weight: 700;
    color: #cc0000;
    line-height: 1;
    font-variant-numeric: tabular-nums;
  }}

  .cd-lab {{
    margin-top: 8px;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #666;
  }}

  .cd-done {{
    font-size: 28px;
    font-weight: 700;
    color: #cc0000;
  }}

  .calendar {{
    margin: 34px auto 0;
    max-width: 420px;
    background: #111;
    border: 1px solid #333;
    border-radius: 10px;
    padding: 18px;
    color: #eee;
  }}

  .cal-title {{
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 12px;
    color: #cc0000;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
  }}

  th {{
    color: #777;
    font-size: 12px;
    padding-bottom: 10px;
  }}

  td {{
    width: 14.28%;
    height: 42px;
    text-align: center;
    font-weight: 500;
  }}

  .cal-day {{
    border-radius: 50%;
  }}

  .muted {{
    color: #333;
  }}

  .today {{
    outline: 3px solid #cc0000;
    outline-offset: -5px;
    color: white;
    font-weight: 700;
  }}

  .target {{
    background: #8B0000;
    color: white;
    font-weight: 700;
  }}
</style>

<div class="cd-wrap">
  <div class="cd-bar"></div>
  <div id="cd-body" class="cd-grid"></div>

  <div class="calendar">
    <div class="cal-title">{today.strftime("%B %Y")}</div>
    <table>
      <thead>
        <tr>
          <th>Sun</th><th>Mon</th><th>Tue</th><th>Wed</th>
          <th>Thu</th><th>Fri</th><th>Sat</th>
        </tr>
      </thead>
      <tbody>
        {calendar_rows}
      </tbody>
    </table>
  </div>
</div>

<script>
  const target = {target_ms};
  const body = document.getElementById('cd-body');

  function cell(n, l) {{
    return '<div class="cd-cell"><div class="cd-num">' + n + '</div>'
         + '<div class="cd-lab">' + l + '</div></div>';
  }}

  function pad(n) {{
    return String(n).padStart(2, '0');
  }}

  function tick() {{
    const diff = target - Date.now();

    if (diff <= 0) {{
      body.className = '';
      body.innerHTML = '<div class="cd-done">BIG BOIII IS OPERATING.</div>';
      clearInterval(timer);
      return;
    }}

    const d = Math.floor(diff / 86400000);
    const h = Math.floor((diff % 86400000) / 3600000);
    const m = Math.floor((diff % 3600000) / 60000);
    const s = Math.floor((diff % 60000) / 1000);

    body.innerHTML = cell(d, 'Days') + cell(pad(h), 'Hours')
                   + cell(pad(m), 'Minutes') + cell(pad(s), 'Seconds');
  }}

  tick();
  const timer = setInterval(tick, 1000);
</script>
"""

components.html(html, height=640)
