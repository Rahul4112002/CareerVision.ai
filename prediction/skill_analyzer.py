import requests
import json
import logging
from django.conf import settings
from .models import Skill, JobRoleSkill, LearningResource

logger = logging.getLogger(__name__)

class SkillGapAnalyzer:
    def __init__(self):
        self.api_key = settings.GOOGLE_API_KEY
        self.job_skills_mapping = {
            'CRM/Managerial Roles': ['Project Management', 'Leadership', 'CRM Software', 'Client Relations', 'Business Analysis', 'Communication', 'Stakeholder Management'],
            'Analyst': ['Data Analysis', 'SQL', 'Excel', 'Data Visualization', 'Statistical Analysis', 'Problem Solving', 'Business Intelligence'],
            'Mobile Applications/ Web Development': ['JavaScript', 'HTML/CSS', 'React', 'Mobile Development', 'API Integration', 'UI/UX Principles', 'Git'],
            'QA/Testing': ['Test Planning', 'Automated Testing', 'Manual Testing', 'Test Documentation', 'Bug Tracking', 'Selenium', 'Quality Assurance'],
            'UX/Design': ['User Research', 'Wireframing', 'Prototyping', 'Design Systems', 'User Testing', 'Figma', 'Interaction Design'],
            'Databases': ['SQL', 'Database Management', 'Data Modeling', 'NoSQL', 'Database Security', 'Query Optimization', 'Data Architecture'],
            'Programming/ Systems Analyst': ['Programming Logic', 'Algorithm Design', 'System Analysis', 'Documentation', 'Business Requirements', 'Troubleshooting'],
            'Networks/ Systems': ['Network Protocols', 'Security Fundamentals', 'System Administration', 'Cloud Infrastructure', 'Firewalls', 'Monitoring Tools'],
            'SE/SDE': ['Data Structures', 'Algorithms', 'Object-Oriented Programming', 'Version Control', 'Testing Methodologies', 'Framework Experience', 'API Design'],
            'Technical Support/Service': ['Troubleshooting', 'Customer Service', 'Technical Documentation', 'Support Tools', 'Ticket Management', 'Hardware Knowledge'],
            'others': ['Cloud Services', 'Solution Design', 'Architecture Principles', 'IT Governance', 'Compliance', 'Infrastructure Planning']
        }
        
        # Predefined learning resources for common skills
        self.default_resources = {
            'SQL': [
                {'title': 'SQL Basics', 'url': 'https://www.w3schools.com/sql/', 'type': 'Tutorial', 'is_free': True, 'provider': 'W3Schools'},
                {'title': 'Introduction to SQL', 'url': 'https://www.codecademy.com/learn/learn-sql', 'type': 'Course', 'is_free': True, 'provider': 'Codecademy'},
                {'title': 'SQL for Data Analysis', 'url': 'https://www.udacity.com/course/sql-for-data-analysis--ud198', 'type': 'Course', 'is_free': True, 'provider': 'Udacity'}
            ],
            'Python': [
                {'title': 'Learn Python', 'url': 'https://www.learnpython.org/', 'type': 'Tutorial', 'is_free': True, 'provider': 'LearnPython.org'},
                {'title': 'Python for Everybody', 'url': 'https://www.coursera.org/specializations/python', 'type': 'Course', 'is_free': False, 'provider': 'Coursera'},
                {'title': 'Automate the Boring Stuff with Python', 'url': 'https://automatetheboringstuff.com/', 'type': 'Book', 'is_free': True, 'provider': 'Al Sweigart'}
            ],
            # Add more predefined resources for common skills
        }
        
    def get_user_skills(self, user_data):
        """Extract user skills from form data"""
        user_skills = []
        
        # Add coding skills if rating is high enough
        coding_rating = int(user_data.get('coding_skills_rating', 0))
        if coding_rating >= 7:
            user_skills.append('Advanced Programming')
        elif coding_rating >= 4:
            user_skills.append('Intermediate Programming')
        elif coding_rating > 0:
            user_skills.append('Basic Programming')
            
        # Add public speaking if points are high
        speaking_points = int(user_data.get('public_speaking_points', 0))
        if speaking_points >= 7:
            user_skills.append('Public Speaking')
            user_skills.append('Communication')
            
        # Add certification as a skill
        certification = user_data.get('certifications')
        if certification and certification != 'Unknown':
            user_skills.append(certification.title())
            
            # Add related skills based on certifications
            cert_skill_mapping = {
                'python': ['Python', 'Programming'],
                'machine learning': ['Machine Learning', 'Data Science', 'Python'],
                'full stack': ['JavaScript', 'HTML/CSS', 'Web Development', 'Backend Development'],
                'app development': ['Mobile Development', 'UI/UX Principles'],
                'information security': ['Security Fundamentals', 'Network Security'],
                'hadoop': ['Big Data', 'Data Processing'],
                'r programming': ['R', 'Data Analysis', 'Statistics']
            }
            
            if certification.lower() in cert_skill_mapping:
                user_skills.extend(cert_skill_mapping[certification.lower()])
            
        # Add workshop knowledge as a skill
        workshop = user_data.get('workshops')
        if workshop and workshop != 'Unknown':
            user_skills.append(workshop.title())
            
            # Add related skills based on workshops
            workshop_skill_mapping = {
                'data science': ['Data Analysis', 'Statistics', 'Machine Learning'],
                'web technologies': ['HTML/CSS', 'JavaScript', 'Web Development'],
                'cloud computing': ['Cloud Infrastructure', 'Scalability', 'AWS/Azure/GCP'],
                'game development': ['Game Design', 'Graphics Programming', 'Unity/Unreal'],
                'hacking': ['Security Fundamentals', 'Penetration Testing', 'Ethical Hacking']
            }
            
            if workshop.lower() in workshop_skill_mapping:
                user_skills.extend(workshop_skill_mapping[workshop.lower()])
            
        # Add subject interest as a skill
        subject = user_data.get('interested_subjects')
        if subject and subject != 'Unknown':
            user_skills.append(subject.title())
            
        # Team experience
        if user_data.get('team') == 'yes':
            user_skills.append('Team Collaboration')
            
        # Technical vs Management orientation
        orientation = user_data.get('management_technical')
        if orientation == 'Technical':
            user_skills.append('Technical Aptitude')
        elif orientation == 'Management':
            user_skills.append('Management Skills')
            user_skills.append('Leadership')
        
        # Hackathon experience
        hackathons = int(user_data.get('hackathons', 0))
        if hackathons > 2:
            user_skills.append('Competitive Programming')
            user_skills.append('Rapid Prototyping')
        elif hackathons > 0:
            user_skills.append('Hackathon Experience')
            
        # Remove duplicates and return
        return list(set(user_skills))
    
    def get_required_skills(self, job_role):
        """Get the required skills for a specific job role"""
        return self.job_skills_mapping.get(job_role, [])
    
    def identify_skill_gaps(self, user_skills, required_skills):
        """Identify skills the user needs to develop"""
        # Simple gap analysis - skills in required_skills but not in user_skills
        user_skills_lower = [skill.lower() for skill in user_skills]
        skill_gaps = []
        
        for skill in required_skills:
            # Check if skill or a similar skill is in user_skills
            if not any(skill.lower() in s for s in user_skills_lower):
                skill_gaps.append(skill)
                
        return skill_gaps
    
    def get_skill_proficiency(self, user_data, skill):
        """Estimate user's proficiency in a given skill (1-10 scale)"""
        proficiency = 0
        
        # Check coding skills
        if "programming" in skill.lower() or "coding" in skill.lower():
            proficiency = int(user_data.get('coding_skills_rating', 0))
            
        # Check public speaking
        elif "speaking" in skill.lower() or "communication" in skill.lower():
            proficiency = int(user_data.get('public_speaking_points', 0))
            
        # Check logical reasoning
        elif "problem solving" in skill.lower() or "logical" in skill.lower():
            proficiency = int(user_data.get('logical_quotient_rating', 0))
            
        # Default proficiency for other skills
        else:
            proficiency = 3  # Assume beginner level
            
        return proficiency
    
    def fetch_learning_resources(self, skill, limit=3):
        """Fetch learning resources for a specific skill"""
        # First check if we have predefined resources
        if skill.lower() in [k.lower() for k in self.default_resources.keys()]:
            for key in self.default_resources.keys():
                if skill.lower() == key.lower():
                    return self.default_resources[key][:limit]
        
        # Then check if we have resources in our database
        try:
            db_resources = LearningResource.objects.filter(
                skill__name__icontains=skill
            )[:limit]
            
            if db_resources.exists():
                return [
                    {
                        'title': resource.title,
                        'description': resource.description,
                        'url': resource.url,
                        'type': resource.resource_type,
                        'is_free': resource.is_free,
                        'provider': resource.provider
                    }
                    for resource in db_resources
                ]
        except Exception as e:
            logger.error(f"Error fetching resources from database: {str(e)}")
        
        # If no database resources, use Google Custom Search API
        try:
            # Only make API calls if we have a valid key
            if not self.api_key or self.api_key == 'AIzaSyBOPlaUvJkpVSPsSsCI2q3j-KFbFEHn28g':
                # Return fallback resources if API key isn't properly configured
                return self._get_fallback_resources(skill)
                
            # Craft the search query
            query = f"{skill} tutorial OR course OR learning resource"
            
            # Google Custom Search API endpoint
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': self.api_key,
                'cx': '017576662512468239146:omuauf_lfve',  # This is a default search engine ID
                'q': query,
                'num': limit
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            resources = []
            for item in data.get('items', [])[:limit]:
                resource = {
                    'title': item.get('title'),
                    'description': item.get('snippet'),
                    'url': item.get('link'),
                    'type': 'Resource',  # Default type
                    'is_free': True,  # Default to free
                    'provider': self._extract_provider(item.get('displayLink', ''))
                }
                resources.append(resource)
                
            return resources
        except Exception as e:
            logger.error(f"Error fetching resources from Google API: {str(e)}")
            return self._get_fallback_resources(skill)
    
    def _extract_provider(self, display_link):
        """Extract provider name from display link"""
        if not display_link:
            return "Unknown"
        
        # Remove www. and .com/.org/etc.
        provider = display_link.replace('www.', '')
        provider = provider.split('.')[0]
        return provider.capitalize()
    
    def _get_fallback_resources(self, skill):
        """Get fallback resources when API fails"""
        # Generic resources for when API calls fail
        generic_resources = [
            {
                'title': f'Learn {skill} on Coursera',
                'description': f'Find courses related to {skill} on Coursera',
                'url': f'https://www.coursera.org/search?query={skill.replace(" ", "%20")}',
                'type': 'Course Platform',
                'is_free': False,
                'provider': 'Coursera'
            },
            {
                'title': f'{skill} Tutorials on YouTube',
                'description': f'Search for free {skill} tutorials on YouTube',
                'url': f'https://www.youtube.com/results?search_query={skill.replace(" ", "+")}+tutorial',
                'type': 'Video Tutorials',
                'is_free': True,
                'provider': 'YouTube'
            },
            {
                'title': f'{skill} Documentation and Guides',
                'description': f'Find free documentation and guides about {skill}',
                'url': f'https://www.google.com/search?q={skill.replace(" ", "+")}+documentation+guide',
                'type': 'Documentation',
                'is_free': True,
                'provider': 'Various'
            }
        ]
        return generic_resources
    
    def create_learning_plan(self, user_data, job_role):
        """Create a personalized learning plan based on skill gaps"""
        # Get user's current skills
        user_skills = self.get_user_skills(user_data)
        
        # Get required skills for the job
        required_skills = self.get_required_skills(job_role)
        
        # Identify skill gaps
        skill_gaps = self.identify_skill_gaps(user_skills, required_skills)
        
        # Create a learning plan with resources for each skill gap
        learning_plan = {
            'job_role': job_role,
            'current_skills': user_skills,
            'required_skills': required_skills,
            'skill_gaps': [],
        }
        
        for skill in skill_gaps:
            proficiency = self.get_skill_proficiency(user_data, skill)
            resources = self.fetch_learning_resources(skill)
            
            skill_info = {
                'name': skill,
                'current_proficiency': proficiency,
                'target_proficiency': 8,  # Assume 8 is target proficiency
                'resources': resources
            }
            
            learning_plan['skill_gaps'].append(skill_info)
            
        return learning_plan