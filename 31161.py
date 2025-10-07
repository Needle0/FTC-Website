from flask import Flask, render_template_string, request, redirect, url_for
import calendar
from datetime import datetime

app = Flask(__name__)

# CSS for futuristic yet professional look
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Exo:ital,wght@0,100..900;1,100..900&display=swap');

body {
    background-color: #0a0a0a;
    background-image: url('https://wallpapers.com/images/high/4k-futuristic-city-3840-x-2160-4b0z0z0z0z0z0z.jpg');
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
    color: #e0e0e0;
    font-family: 'Exo', sans-serif;
    margin: 0;
    padding: 0;
    overflow-x: hidden;
    scrollbar-width: thin; /* For Firefox */
    scrollbar-color: #007acc #0a0a0a;
}

::-webkit-scrollbar {
    width: 12px;
}

::-webkit-scrollbar-track {
    background: #0a0a0a;
}

::-webkit-scrollbar-thumb {
    background-color: #007acc;
    border-radius: 20px;
    border: 3px solid #0a0a0a;
}

header {
    background: linear-gradient(to right, #00bfff, #007acc);
    padding: 30px;
    text-align: center;
    box-shadow: 0 0 15px rgba(0, 191, 255, 0.5);
    animation: subtlePulse 3s infinite;
}

@keyframes subtlePulse {
    0% { box-shadow: 0 0 15px rgba(0, 191, 255, 0.5); }
    50% { box-shadow: 0 0 20px rgba(0, 191, 255, 0.7); }
    100% { box-shadow: 0 0 15px rgba(0, 191, 255, 0.5); }
}

header h1 {
    margin: 0;
    font-size: 3em;
    text-shadow: 0 0 10px #00bfff;
    letter-spacing: 1.5px;
}

nav {
    background-color: rgba(10, 10, 10, 0.9);
    padding: 15px 0;
    text-align: center;
    box-shadow: 0 4px 8px rgba(0, 191, 255, 0.2);
}

nav a {
    color: #ccf2ff;
    text-decoration: none;
    margin: 0 20px;
    font-size: 1.3em;
    transition: color 0.3s, text-shadow 0.3s, transform 0.3s;
    letter-spacing: 1px;
    font-weight: 500;
}

nav a:hover {
    color: #00bfff;
    text-shadow: 0 0 8px #00bfff;
    transform: scale(1.05);
}

nav a.active {
    font-weight: bold;
    color: #00bfff;
    text-shadow: 0 0 5px #00bfff;
}

main {
    max-width: 1400px;
    margin: 30px auto;
    padding: 30px;
    background-color: rgba(30, 30, 30, 0.8);
    border-radius: 12px;
    box-shadow: 0 0 20px rgba(0, 191, 255, 0.4);
    animation: fadeIn 1.5s ease-in-out;
    transition: opacity 0.5s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

footer {
    text-align: center;
    padding: 8px;
    background-color: rgba(10, 10, 10, 0.9);
    color: #a0a0a0;
    position: fixed;
    width: 100%;
    bottom: 0;
    box-shadow: 0 -2px 4px rgba(0, 191, 255, 0.2);
    border-top: 1px solid #007acc;
}

h2 {
    color: #00bfff;
    text-shadow: 0 0 8px #00bfff;
    font-size: 2em;
    letter-spacing: 1px;
}

ul {
    list-style-type: none;
    padding: 0;
}

li {
    margin: 15px 0;
    padding: 10px;
    background: rgba(0, 191, 255, 0.05);
    border-radius: 5px;
    transition: background 0.3s;
}

li:hover {
    background: rgba(0, 191, 255, 0.15);
}

/* Futuristic calendar styles */
.whats-happening {
    display: flex;
    justify-content: space-between;
    gap: 30px;
}

.calendar-container {
    flex: 1;
    max-width: 60%;
}

.events-container {
    flex: 1;
    max-width: 35%;
    background: rgba(30, 30, 30, 0.9);
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 0 15px rgba(0, 191, 255, 0.3);
}

.events-container li {
    cursor: pointer;
}

.calendar {
    background: rgba(30, 30, 30, 0.9);
    padding: 25px;
    border-radius: 12px;
    color: #e0e0e0;
    box-shadow: 0 0 15px rgba(0, 191, 255, 0.4);
    transition: opacity 0.5s ease;
}

.calendar header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
    background: none;
    box-shadow: none;
    padding: 0;
}

.calendar .nav-arrow {
    color: #ccf2ff;
    font-size: 28px;
    text-decoration: none;
    padding: 5px 10px;
    border: 1px solid #007acc;
    border-radius: 5px;
    transition: background 0.3s, color 0.3s;
}

.calendar .nav-arrow:hover {
    background: #007acc;
    color: #ffffff;
}

.calendar h2 {
    font-size: 28px;
    color: #00bfff;
    text-shadow: 0 0 10px #00bfff;
}

.days, .dates {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 8px;
}

.days span {
    text-align: center;
    padding: 12px;
    color: #a0a0a0;
    font-weight: 500;
}

.dates span {
    text-align: center;
    padding: 18px;
    background: rgba(42, 42, 42, 0.9);
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.4s ease;
    color: #e0e0e0;
    font-weight: 500;
}

.dates span:hover {
    background: #00bfff;
    color: #0a0a0a;
    box-shadow: 0 0 12px #00bfff;
    transform: scale(1.05);
}

.dates span.event {
    background: linear-gradient(#00bfff, #007acc);
    color: #0a0a0a;
    box-shadow: 0 0 12px #00bfff, 0 0 24px #007acc;
    text-shadow: 0 0 6px #ffffff;
}

.dates span.current {
    border: 2px solid #00bfff;
    box-shadow: 0 0 10px #00bfff;
}

.dates span.empty {
    background: none;
    cursor: default;
}

.hero-image {
    width: 100%;
    max-height: 400px;
    object-fit: cover;
    border-radius: 12px;
    box-shadow: 0 0 15px rgba(0, 191, 255, 0.4);
    margin-bottom: 20px;
    animation: fadeIn 2s ease-in-out;
}

a {
    color: #ccf2ff;
    transition: color 0.3s;
}

a:hover {
    color: #00bfff;
}
"""

# Header HTML
HEADER = """
<header>
    <h1>Hoco Robo - FTC Team 31161</h1>
</header>
"""

# Footer HTML
FOOTER = """
<footer>
    <p>&copy; 2025 Hoco Robo. All rights reserved. Website: 31161.org (simulated locally)</p>
</footer>
"""

# NAV function
def get_nav(current_page):
    pages = {
        'home': 'Home',
        'whats-happening': "What's Happening",
        'about-us': 'About Us',
        'sponsors': 'Sponsors',
        'resources': 'Resources'
    }
    nav_html = '<nav>'
    for route, name in pages.items():
        path = '/' if route == 'home' else f'/{route}'
        active = 'class="active"' if route == current_page else ''
        nav_html += f'<a href="{path}" {active}>{name}</a>'
    nav_html += '</nav>'
    return nav_html

# Base template function
def base_template(content, current_page='home'):
    nav = get_nav(current_page)
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hoco Robo - FTC Team 31161</title>
    <style>{CSS}</style>
</head>
<body>
    {HEADER}
    {nav}
    <main id="main-content">
        {content}
    </main>
    {FOOTER}
    <script>
    function updateContent(url) {{
        const main = document.querySelector('#main-content');
        main.style.opacity = 0;
        setTimeout(() => {{
            fetch(url)
            .then(res => res.text())
            .then(html => {{
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newMain = doc.querySelector('main').innerHTML;
                main.innerHTML = newMain;
                document.title = doc.title;
                // update nav active
                const links = document.querySelectorAll('nav a');
                const targetPath = new URL(url, window.location.origin).pathname;
                links.forEach(link => {{
                    link.classList.remove('active');
                    if (new URL(link.href).pathname === targetPath) {{
                        link.classList.add('active');
                    }}
                }});
                main.style.opacity = 1;
            }})
            .catch(err => {{
                console.error(err);
                main.style.opacity = 1;
            }});
        }}, 500);
    }}

    document.addEventListener('DOMContentLoaded', () => {{
        const links = document.querySelectorAll('nav a');
        links.forEach(link => {{
            link.addEventListener('click', e => {{
                e.preventDefault();
                const url = link.getAttribute('href');
                history.pushState({{}}, '', url);
                updateContent(url);
            }});
        }});
    }});

    window.addEventListener('popstate', () => {{
        updateContent(location.pathname + location.search);
    }});
    </script>
</body>
</html>
"""

# Function to generate calendar HTML
def generate_calendar(year, month, now, events, is_ajax=False):
    month_name = calendar.month_name[month]
    cal = calendar.monthcalendar(year, month)

    # Generate dates HTML
    dates_html = ''
    for week in cal:
        for day in week:
            if day == 0:
                dates_html += '<span class="empty"></span>'
            else:
                class_str = ''
                date_obj = datetime(year, month, day)
                if date_obj in events:
                    class_str = 'event'
                if day == now.day and month == now.month and year == now.year:
                    class_str += ' current' if class_str else 'current'
                dates_html += f'<span class="{class_str}">{day}</span>'

    # Compute prev and next
    min_year, min_month = 2025, 1
    max_year, max_month = 2028, 12

    prev_month = month - 1
    prev_year = year
    if prev_month == 0:
        prev_month = 12
        prev_year -= 1
    show_prev = (prev_year > min_year) or (prev_year == min_year and prev_month >= min_month)

    next_month = month + 1
    next_year = year
    if next_month == 13:
        next_month = 1
        next_year += 1
    show_next = (next_year < max_year) or (next_year == max_year and next_month <= max_month)

    base_url = '/calendar' if is_ajax else '/whats-happening'
    prev_link = f'<a href="{base_url}?year={prev_year}&month={prev_month}" class="nav-arrow">&#9664;</a>' if show_prev else '<span></span>'
    next_link = f'<a href="{base_url}?year={next_year}&month={next_month}" class="nav-arrow">&#9654;</a>' if show_next else '<span></span>'

    calendar_html = f"""
        <header>
            {prev_link}
            <h2>{month_name} {year}</h2>
            {next_link}
        </header>
        <div class="days">
            <span>Sun</span>
            <span>Mon</span>
            <span>Tue</span>
            <span>Wed</span>
            <span>Thu</span>
            <span>Fri</span>
            <span>Sat</span>
        </div>
        <div class="dates">
            {dates_html}
        </div>
    """
    return calendar_html

# Routes
@app.route('/')
def home():
    content = """
    <h2>Welcome to Hoco Robo</h2>
    <p>We are FTC Team 31161, dedicated to innovation in robotics. Explore our site to learn more about our journey and achievements in a futuristic world of technology.</p>
    """
    return render_template_string(base_template(content, 'home'))

@app.route('/whats-happening')
def whats_happening():
    now = datetime(2025, 10, 7)
    year = int(request.args.get('year', now.year))
    month = int(request.args.get('month', now.month))

    # Normalize month
    while month > 12:
        month -= 12
        year += 1
    while month < 1:
        month += 12
        year -= 1

    # Clamp
    min_date = datetime(2025, 1, 1)
    max_date = datetime(2028, 12, 1)
    current_date = datetime(year, month, 1)
    if current_date < min_date:
        year = 2025
        month = 1
    elif current_date > max_date:
        year = 2028
        month = 12

    # Events
    events = {
        datetime(2026, 1, 10): "January 10, 2026, 7:00 AM – 5:00 PM<br>Moorefield High School, 401 N Main St, Moorefield, WV 26836, USA",
        datetime(2026, 1, 25): "January 25, 2026, 7:00 AM – 5:00 PM<br>Francis Scott Key High School, 3825 Bark Hill Rd, Union Bridge, MD 21791, USA"
    }

    calendar_html = generate_calendar(year, month, now, events, is_ajax=True)

    # Upcoming events
    upcoming_events = sorted((date, desc) for date, desc in events.items() if date >= now)
    events_html = '<ul>' + ''.join(f'<li data-year="{date.year}" data-month="{date.month}">{desc}</li>' for date, desc in upcoming_events) + '</ul>' if upcoming_events else '<p>No upcoming events.</p>'

    content = f"""
    <h2>What's Happening</h2>
    <div class="whats-happening">
        <div class="calendar-container">
            <p>Calendar (Current date: {now.strftime('%B %d, %Y')})</p>
            <div class="calendar">
                {calendar_html}
            </div>
        </div>
        <div class="events-container">
            <h3>Upcoming Event Details</h3>
            {events_html}
        </div>
    </div>
    <script>
    function updateCalendar(url) {{
        const calendar = document.querySelector('.calendar');
        calendar.style.opacity = 0;
        fetch(url, {{headers: {{'X-Requested-With': 'XMLHttpRequest'}}}})
        .then(res => res.text())
        .then(html => {{
            setTimeout(() => {{
                calendar.innerHTML = html;
                calendar.style.opacity = 1;
                const newUrl = url.replace('/calendar', '/whats-happening');
                history.pushState({{}}, '', newUrl);
            }}, 500);
        }})
        .catch(err => {{
            console.error(err);
            calendar.style.opacity = 1;
        }});
    }}

    document.querySelectorAll('.nav-arrow').forEach(arrow => {{
        arrow.addEventListener('click', e => {{
            e.preventDefault();
            updateCalendar(arrow.href);
        }});
    }});

    document.querySelectorAll('.events-container li').forEach(li => {{
        li.addEventListener('click', () => {{
            const year = li.dataset.year;
            const month = li.dataset.month;
            const url = `/calendar?year=${{year}}&month=${{month}}`;
            updateCalendar(url);
        }});
    }});
    </script>
    """
    return render_template_string(base_template(content, 'whats-happening'))

@app.route('/calendar')
def get_calendar():
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        year = int(request.args.get('year', 2025))
        month = int(request.args.get('month', 10))
        return redirect(url_for('whats_happening', year=year, month=month))

    now = datetime(2025, 10, 7)
    year = int(request.args.get('year', now.year))
    month = int(request.args.get('month', now.month))

    # Normalize month
    while month > 12:
        month -= 12
        year += 1
    while month < 1:
        month += 12
        year -= 1

    # Clamp
    min_date = datetime(2025, 1, 1)
    max_date = datetime(2028, 12, 1)
    current_date = datetime(year, month, 1)
    if current_date < min_date:
        year = 2025
        month = 1
    elif current_date > max_date:
        year = 2028
        month = 12

    events = {
        datetime(2026, 1, 10): "January 10, 2026, 7:00 AM – 5:00 PM<br>Moorefield High School, 401 N Main St, Moorefield, WV 26836, USA",
        datetime(2026, 1, 25): "January 25, 2026, 7:00 AM – 5:00 PM<br>Francis Scott Key High School, 3825 Bark Hill Rd, Union Bridge, MD 21791, USA"
    }

    calendar_html = generate_calendar(year, month, now, events, is_ajax=True)
    return calendar_html

@app.route('/about-us')
def about_us():
    content = """
    <h2>About Us</h2>
    <img src="static/kids.jpg" alt="FTC Team" class="hero-image">
    <p>We are FTC Team 31161 Hoco Robo, a dedicated group of students passionate about robotics, engineering, and teamwork. Guided by the values of FIRST, we strive to innovate, collaborate, and inspire our community through STEM.</p>
    <h3>Contact Us</h3>
    <p>Email: <a href="mailto:Hocorobo31161@gmail.com">Hocorobo31161@gmail.com</a></p>
    """
    return render_template_string(base_template(content, 'about-us'))

@app.route('/sponsors')
def sponsors():
    content = """
    <h2>Sponsors</h2>
    <p>We gratefully acknowledge our sponsors for their invaluable support:</p>
    <ul>
        <li>AiRy Consulting LLC</li>
        <li>Guanyi Fencing Academy</li>
        <li>Local Community Fund - Equipment donations</li>
    </ul>
    """
    return render_template_string(base_template(content, 'sponsors'))

@app.route('/resources')
def resources():
    content = """
    <h2>Resources</h2>
    <p>Useful links and documents for robotics enthusiasts:</p>
    <ul>
        <li><a href="https://www.firstinspires.org/robotics/ftc">FTC Official Website</a></li>
        <li>Team Handbook (PDF download placeholder)</li>
        <li>Robotics Tutorials</li>
    </ul>
    """
    return render_template_string(base_template(content, 'resources'))

if __name__ == '__main__':
    app.run(debug=True)