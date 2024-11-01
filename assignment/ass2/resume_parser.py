import json
import os

def load_resume_json(json_file):
    """Load and parse the resume JSON file"""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_head(data):
    """Generate HTML head section"""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Seongeun Park</title>
    <link rel="icon" href="letter-s.ico" type="image/x-icon">

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;500;700&display=swap" rel="stylesheet">

    <!-- Local Stylesheet -->
    <link rel="stylesheet" href="style.css">

    <!-- Font Awesome CSS -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">

    <!-- Slick Carousel CSS -->
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/slick-carousel@1.8.1/slick/slick.css"/>

    <!-- jQuery (Slick Carousel Dependency) -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <!-- Slick Carousel JS -->
    <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/slick-carousel@1.8.1/slick/slick.min.js"></script>
</head>
<body style="font-family: 'Montserrat', sans-serif;">'''

def generate_navigation(data):
    """Generate navigation section"""
    return f'''
    <nav id="navbar">
        <ul>
            <li><a href="#introduction"><b>SEONGEUN PARK</b></a></li>
            <li><a href="#education">EDUCATION</a></li>
            <li><a href="#honors">HONORS</a></li>
            <li><a href="#publication">PUBLICATIONS</a></li>
            <li><a href="#skills">SKILLS</a></li>
            <li><a href="#projects">PROJECTS</a></li>
            <li><a href="#experience">EXPERIENCES</a></li>
            <li class="cv-item"><a href="{data['basics']['cvLink']}" target="_blank">CV</a></li>
        </ul>
    </nav>'''

def generate_introduction(data):
    """Generate introduction section"""
    html = '''
    <section id="introduction">
        <div class="profile-container">
            <div class="profile-image">
                <br>
                <img src="''' + data['basics']['image'] + '''" alt="''' + data['basics']['name'] + '''" class="profile-image" id="currentImage">
            </div>

            <div class="profile-info">
                <h2>''' + data['basics']['name'] + '''</h2>
                <p>'''
    
    for profile in data['basics']['profiles']:
        html += f'''<a href="{profile['url']}" {'target="_blank"' if profile['network'] != "Email" else ''} title="{profile['network']}" style="margin-right: 10px;"><i class="{profile['icon']} fa-2x"></i></a>'''
    
    html += f'''
                </p>
                <p class="email-info"><b>Email</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{data['basics']['email']}</p>
                <p><b>Tel</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{data['basics']['phone']}</p>
                <p><b>Research Interests</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{data['basics']['interest']}</p>
                <p><a href="{data['basics']['cvLink']}" target="_blank"><b><span style="color:#B11226;">Resume</span></b></a></p>
                <br>
            </div>
        </div>'''
    
    # Mobile Alert
    html += '''
        <div id="mobileAlert" style="display: none; background-color: rgba(0,0,0,0.8); color: white; text-align: center; padding: 20px; position: fixed; top: 0; left: 0; width: 100%; z-index: 9999;">
            For the best experience,<br>
            Please view on a desktop.<br>
            <button onclick="document.getElementById('mobileAlert').style.display='none'">Close</button>
        </div>
    </section>'''
    return html

def generate_education(data):
    """Generate education section"""
    html = '''
    <section id="education">
        <h2>EDUCATION & EXPERIENCE</h2>'''
    
    for edu in data['education']:
        degree_field = f"{edu['degree']} in {edu['field']}" if edu['field'] else edu['degree']
        html += f'''
        <h3><i class="fas fa-check"></i>{degree_field}</h3>
        <p>{edu['startDate']} – {edu['endDate']}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{edu['school']}'''
        if 'link' in edu:
            html += f''', <a href="{edu['link']['url']}" target="_blank">{edu['link']['text']}</a>'''
        html += '</p>'
    
    html += '''
    </section>'''
    return html

def generate_honors(data):
    """Generate honors section"""
    html = '''
    <section id="honors">
        <h2>HONORS</h2>'''
    
    for honor in data['honors']:
        html += f'''
        <p><b>{honor['title']}</b>, {honor['awarder']}, {honor['year']}</p>'''
    
    html += '''
    </section>'''
    return html

def generate_publications(data):
    """Generate publications section"""
    html = '''
    <section id="publication">
        <h2>PUBLICATIONS</h2>'''
    
    for pub in data['publications']:
        authors = []
        for author in pub['authors']:
            if author.get('isMainAuthor'):
                authors.append(f'<b>{author["name"]}</b>')
            else:
                authors.append(author['name'])
        
        html += f'''
        <p>-&nbsp;&nbsp;'''
        if 'status' in pub:
            html += f"({pub['status']}) "
        
        html += f'''{', '.join(authors)} ({pub['year']}) {pub['title']}. <i style="color:#808080;">{pub['journal']}</i>'''
        
        if 'links' in pub:
            for link in pub['links']:
                html += f''' <a href="{link['url']}" target="_blank"><i>{link['text']}</i></a>'''
        
        html += '</p>'
    
    html += '''
    </section>'''
    return html

def generate_skills(data):
    """Generate skills section"""
    html = '''
    <section id="skills">
        <h2>SKILLS</h2>
        <ul>'''
    
    for skill in data['skills']:
        html += f'''
            <li>
                <h3><i class="fas fa-check"></i>{skill['category']}</h3>
                <p>{', '.join(skill['items'])}</p>
            </li>'''
    
    html += '''
        </ul>
    </section>'''
    return html

def generate_projects(data):
    """Generate projects section"""
    html = '''
    <section id="projects">
        <h2>ACADEMIC PROJECTS</h2>
        <ul>'''
    
    for project in data['projects']:
        html += f'''
            <li>
                <h3><i class="fas fa-check"></i> {project['title']}</h3>
                <p>
                {project['description']}<br>'''
        
        if 'image' in project:
            html += f'''<img src="{project['image']['src']}" class="{project['image']['class']}" alt="{project['image']['alt']}">'''
        
        html += f'''
                <b>Duration</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{project['duration']['start']} – {project['duration']['end']}<br>'''
        
        if 'sponsor' in project:
            html += f'''<b>Sponsor</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{project['sponsor']}<br>'''
        
        html += f'''<b>Skills</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{', '.join(project['skills'])}</p>
                <br>
            </li>'''
    
    html += '''
        </ul>
    </section>'''
    return html

def generate_footer():
    """Generate footer section"""
    html = '''
        <p style="padding-left: 30px;">
            <b>Please feel free to contact me anytime.<br>
            <a href="#introduction">Seongeun Park</a></b>
        </p>

        <div id="backToTopRight" style="display: block; position: fixed; bottom: 50px; right: 30px; cursor: pointer;">
            <i class="fas fa-arrow-up fa-2x"></i>
        </div>

        <script src="script.js" defer></script>
        
        <script type="text/javascript">
            $(document).ready(function(){
                $('.image-slider').slick({
                    dots: false,
                    infinite: true,
                    speed: 300,
                    slidesToShow: 1,
                    adaptiveHeight: true,
                    nextArrow: '<button type="button" class="slick-next">❯</button>',
                    prevArrow: false
                });
            });
        </script>
    </body>
    </html>'''
    
    return html

def generate_teaching_experience(data):
    """Generate teaching experience section HTML with check icon"""
    html = '''
    <section id="teaching_experience">
        <h2>TEACHING EXPERIENCE</h2>
        <ul>'''
    
    for teaching in data['teaching_experience']:
        html += f'''
            <li>
                <h3><i class="fas fa-check"></i> {teaching['course_name']}</h3>
                <p class="experience-period">{teaching['duration']['start']} – {teaching['duration']['end']}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{teaching['institution']}</p>
                <p class="experience-description">{teaching['description']}</p>
            </li>
            <br>'''
    
    html += '''
        </ul>
    </section>'''
    return html

def generate_additional_experience(data):
    """Generate additional experience section HTML"""
    html = '''
    <section id="experience">
        <ul>
        <h2>ADDITIONAL EXPERIENCE</h2>'''
    
    for exp in data['additional_experience']:
        html += f'''
        <li>
            <i class="fas fa-chevron-down toggle-icon"></i>
            <h3 class="project-title">{exp['category']}</h3>
            <div class="project-detail">'''

        if exp['category'] == "Diverse Programming Coursework":
            html += f'''
                <p>{exp['duration']['start']} – {exp['duration']['end']}</p>
                <p>{exp['description']}<br>'''
            for edu in exp['education']:
                html += f'''
                <strong>{edu['level']} ({len(edu['items'])} courses)</strong>: {', '.join(edu['items'])}<br>'''
            html += '</p>'

        elif exp['category'] == "Programming Study Group":
            html += f'''
                <p>{exp['duration']['start']} – {exp['duration']['end']}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{exp['institution']}, <a href="{exp['group']['url']}" target="_blank"><b>{exp['group']['name']}</b></a></p>
                <p>{exp['description']}</p>'''

        elif exp['category'] == "Volunteer Experience":
            html += f'''
                <p>{exp['duration']['start']} – {exp['duration']['end']}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{exp['totalHours']} hours</p>'''
            for activity in exp['activities']:
                html += f'''
                <p><b>{activity['organization']} ({activity['duration']['start']} - {activity['duration']['end']})</b>: {activity['description']}</p>'''

        html += '''
            </div>
        </li>
        <br>'''
    
    html += '''
        </ul>
    </section>'''
    return html

def generate_html(data):
    """Generate complete HTML"""
    html = generate_head(data)
    html += generate_navigation(data)
    html += generate_introduction(data)
    html += generate_education(data)
    html += generate_honors(data)
    html += generate_publications(data)
    html += generate_skills(data)
    html += generate_projects(data)
    html += generate_teaching_experience(data)
    html += generate_additional_experience(data)
    html += generate_footer()
    return html

def main():
    if not os.path.exists('resume.json'):
        print("Error: resume.json not found!")
        return
    
    try:
        resume_data = load_resume_json('resume.json')
        html_content = generate_html(resume_data)
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("Successfully generated index.html")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()