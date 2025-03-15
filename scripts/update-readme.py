import os, sys
import re
import datetime


def get_file_names(folder_path):
    file_names = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_names.append(file)
    
    return file_names

def fetch_recent_project_list(file_names):
    recent_project_list = []
    recent_project_list = sorted(file_names, reverse=False)[:5]
    
    return recent_project_list

def fetch_recent_blog_list(file_names):
    recent_blog_list = []
    recent_blog_list = sorted(file_names, reverse=True)[:5]
    
    return recent_blog_list

def replace_chunk(content, marker, chunk, inline=False):
    pattern = re.compile(r"<!\-\- {}:Start \-\-!>.*?<!\-\- {}:End \-\-!>".format(marker, marker), re.DOTALL)
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {}:Start -->{}<!-- {}:End -->".format(marker, chunk, marker)
    
    return pattern.sub(chunk, content)


if __name__ == '__main__':
    print("---------- Update readme for JadeCong ----------")
    
    # Get recent project list from target repository
    project_path = "JadeCong.github.io/_projects"
    recent_projects = fetch_recent_project_list(get_file_names(project_path))
    print(recent_projects)
    
    # Get recent blog list from target repository
    blog_path = "JadeCong.github.io/contents/blogs/_posts"
    recent_blogs = fetch_recent_blog_list(get_file_names(blog_path))
    print(recent_blogs)
    
    # Update recent project and blog list in README.md
    with open("README.md", 'r', encoding='utf-8') as file:
        readme_content = file.read()
    print("Readme Content:\n", readme_content)
    ## Update recent project list
    recent_projects_chunk = "".join(
        [
            "- [{}](https://jadecong.github.io/contents/projects/{}/)".format(project.split('.')[0].replace("-", " "), project.split('.')[0])
            for project in recent_projects
        ]
    )
    readme_content = replace_chunk(readme_content, "Recent-Project-List", recent_projects_chunk)
    ## Update recent blog list
    recent_blogs_chunk = "".join(
        [
            "- [{}](https://jadecong.github.io/contents/blogs/{}/)".format(blog.split('.')[0][11:].replace("-", " "), blog.split('.')[0])
            for blog in recent_blogs
        ]
    )
    readme_content = replace_chunk(readme_content, "Recent-Blog-List", recent_blogs_chunk)
    print("Updated Readme Content:\n", readme_content)
    ## Update readme contents
    with open("README.md", 'w', encoding='utf-8') as file:
        file.write(readme_content)
    
    print("---------- Update readme for JadeCong ----------")
