import flask
from flask import request, redirect, url_for
from datetime import timedelta
import uuid
import time


app = flask.Flask(__name__);
timers = {}



@app.route('/<clock_id>')
def get_clock(clock_id):
    if clock_id not in timers:
        return '404', 404
    start_time = int(timers[clock_id]['start_time'])
    total_time = int(timers[clock_id]['total_time'])
    current_time = time.time()
    if current_time - start_time > total_time:
        return 'expired'
    seconds_diff = int(total_time - (current_time - start_time))
    diff_text = '{seconds_diff // (60 * 60)} hours, {(seconds_diff - ((seconds_diff // (60 * 60)) * 60 * 60)) // 60} minutes, {seconds_diff - (seconds_diff // 60) * 60} seconds left'
    html = f"""
    <div style="display: flex; justify-content: center; align-items: center; font-size: 75px; width: 95vw; height: 95vh;">
        {seconds_diff // (60 * 60)} hours, {(seconds_diff - ((seconds_diff // (60 * 60)) * 60 * 60)) // 60} minutes, {seconds_diff - (seconds_diff // 60) * 60} seconds left
    </div>
    <script>
        setTimeout(() => window.location.reload(true), 1000)
    </script>
    """

    return html

@app.route('/')
def main():
    clock_id = uuid.uuid4().hex
    print(request.args.get('total_time', 600)) # 10 mins
    timers[clock_id] = {
        'start_time': time.time(),
        'total_time': request.args.get('total_time', 600)
    };
    return redirect(url_for('.get_clock', clock_id=clock_id))





app.run(host='0.0.0.0', port=8080)
