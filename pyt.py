import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from zoneinfo import ZoneInfo

st.set_page_config(page_title="Countdown", page_icon="⏳")

st.title("⏳ Countdown")
st.write("Counting down to **July 1, 2026 at 8:00 AM** (US Eastern Time).")

# Anchor the target to a specific timezone so the countdown is correct no
# matter where it's viewed, and so it stays right through daylight saving.
# Change the zone here if you want a different one (e.g. "UTC", "Europe/London").
target = datetime(2026, 7, 1, 8, 0, 0, tzinfo=ZoneInfo("America/New_York"))
target_ms = int(target.timestamp() * 1000)

html = r"""
<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;700&display=swap" rel="stylesheet">
<style>
  .cd-wrap { font-family: 'Rubik', system-ui, sans-serif; text-align: center; }
  .cd-bar  { height: 6px; border-radius: 6px; margin: 0 auto 24px; width: 100%; max-width: 520px;
             background: linear-gradient(90deg, #ff00c1, #FEDA00, #67dedf); }
  .cd-grid { display: flex; gap: 14px; justify-content: center; flex-wrap: wrap; }
  .cd-cell { background: #F9F8F8; border-radius: 16px; padding: 18px 22px; min-width: 92px;
             box-shadow: 0 2px 10px rgba(143,0,107,0.08); }
  .cd-num  { font-size: 44px; font-weight: 700; color: #8f006b; line-height: 1;
             font-variant-numeric: tabular-nums; }
  .cd-lab  { margin-top: 8px; font-size: 13px; font-weight: 500; letter-spacing: 0.08em;
             text-transform: uppercase; color: #1d8587; }
  .cd-done { font-family: 'Rubik', system-ui, sans-serif; font-size: 34px; font-weight: 700; color: #ff00c1; }
</style>

<div class="cd-wrap">
  <div class="cd-bar"></div>
  <div id="cd-body" class="cd-grid"></div>
</div>

<script>
  const target = __TARGET__;
  const body = document.getElementById('cd-body');
  function cell(n, l) {
    return '<div class="cd-cell"><div class="cd-num">' + n + '</div>'
         + '<div class="cd-lab">' + l + '</div></div>';
  }
  function pad(n) { return String(n).padStart(2, '0'); }
  function tick() {
    const diff = target - Date.now();
    if (diff <= 0) {
      body.className = '';
      body.innerHTML = '<div class="cd-done">🎉 It\'s here!</div>';
      clearInterval(timer);
      return;
    }
    const d = Math.floor(diff / 86400000);
    const h = Math.floor((diff % 86400000) / 3600000);
    const m = Math.floor((diff % 3600000) / 60000);
    const s = Math.floor((diff % 60000) / 1000);
    body.innerHTML = cell(d, 'Days') + cell(pad(h), 'Hours')
                   + cell(pad(m), 'Minutes') + cell(pad(s), 'Seconds');
  }
  tick();
  const timer = setInterval(tick, 1000);
</script>
"""

components.html(html.replace("__TARGET__", str(target_ms)), height=200)
