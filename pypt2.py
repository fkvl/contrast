import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from zoneinfo import ZoneInfo

st.set_page_config(page_title="Big Boiii Countdown", page_icon="🔒")

st.title("🔒 Countdown")
st.write("Count Down until **Big Boiii Big Dawg Danger D operates Jello**.")

target = datetime(2026, 7, 1, 8, 0, 0, tzinfo=ZoneInfo("America/New_York"))
target_ms = int(target.timestamp() * 1000)

html = r"""
<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;700&display=swap" rel="stylesheet">
<style>
  .cd-wrap { font-family: 'Rubik', system-ui, sans-serif; text-align: center; }
  .cd-bar  { height: 4px; border-radius: 0; margin: 0 auto 28px; width: 100%; max-width: 520px;
             background: linear-gradient(90deg, #1a1a1a, #8B0000, #1a1a1a); }
  .cd-grid { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }
  .cd-cell { background: #1c1c1c; border-radius: 6px; padding: 18px 22px; min-width: 92px;
             border: 1px solid #333; box-shadow: 0 4px 16px rgba(0,0,0,0.5); }
  .cd-num  { font-size: 44px; font-weight: 700; color: #cc0000; line-height: 1;
             font-variant-numeric: tabular-nums; }
  .cd-lab  { margin-top: 8px; font-size: 11px; font-weight: 500; letter-spacing: 0.15em;
             text-transform: uppercase; color: #666; }
  .cd-done { font-family: 'Rubik', system-ui, sans-serif; font-size: 28px; font-weight: 700; color: #cc0000; }
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
      body.innerHTML = '<div class="cd-done">BIG BOIII IS OPERATING.</div>';
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
