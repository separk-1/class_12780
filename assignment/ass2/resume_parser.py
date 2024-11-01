import json
import os

def load_resume_json(json_file):
    """Load and parse the resume JSON file"""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_html(data):
    """Generate HTML from resume data"""
    html = '''<!DOCTYPE html>
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

    # Navigation
    html += '''
    <nav id="navbar">
        <ul>
            <li><a href="#introduction"><b>SEONGEUN PARK</b></a></li>
            <li><a href="#education">EDUCATION</a></li>
            <li><a href="#honors">HONORS</a></li>
            <li><a href="#publication">PUBLICATIONS</a></li>
            <li><a href="#skills">SKILLS</a></li>
            <li><a href="#projects">PROJECTS</a></li>
            <li><a href="#experience">EXPERIENCES</a></li>
            <li class="cv-item"><a href="''' + data['basics']['cvLink'] + '''" target="_blank">CV</a></li>
        </ul>
    </nav>'''

    # Introduction section
    html += '''
    <section id="introduction">
        <div class="profile-container">
            <div class="profile-image">
                <br>
                <img src="''' + data['basics']['image'] + '''" alt="''' + data['basics']['name'] + '''" class="profile-image" id="currentImage">
            </div>

            <div class="profile-info">
                <h2>''' + data['basics']['name'] + '''</h2>
                <p>'''
    
    # Social profiles
    for profile in data['basics']['profiles']:
        html += f'''<a href="{profile['url']}" {'target="_blank"' if profile['network'] != "Email" else ''} title="{profile['network']}" style="margin-right: 10px;"><i class="{profile['icon']} fa-2x"></i></a>'''
    
    html += '''
                </p>
                <p class="email-info"><b>Email</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;''' + data['basics']['email'] + '''</p>
                <p><b>Tel</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;''' + data['basics']['phone'] + '''</p>
                <p><b>Research Interests</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;''' + data['basics']['interest'] + '''</p>
                <p><a href="''' + data['basics']['cvLink'] + '''" target="_blank"><b><span style="color:#B11226;">Resume</span></b></a></p>
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

    # Education section
    html += '''
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

    # Honors section
    html += '''
    <section id="honors">
        <h2>HONORS</h2>'''
    
    for honor in data['honors']:
        html += f'''
        <p><b>{honor['title']}</b>, {honor['awarder']}, {honor['year']}</p>'''
    
    html += '''
    </section>'''

    # Publications section
    html += '''
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

    # Skills section
    html += '''
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

    # Project section
    html += '''
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

    # Footer and scripts
    html += '''
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

def main():
    if not os.path.exists('resume.json'):
        print("Error: resume.json not found!")
        return
    
    try:
        # Load JSON data
        resume_data = load_resume_json('resume.json')
        
        # Generate HTML
        html_content = generate_html(resume_data)
        
        # Write to file
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("Successfully generated index.html")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()