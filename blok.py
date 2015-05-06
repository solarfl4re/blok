#coding: utf-8

# Python imports
from datetime import datetime
from sys import argv
import io
import os
import shutil

# Pythonista modules
import webbrowser
import clipboard

# Blok modules
import template

STATIC_DIR = 'static/'
POSTS_DIR = 'posts/'
OUTPUT_DIR = 'output/'

class blog_post():
  def __init__(self, title, slug, content, date=None):
    self.title = title
    self.content = content
    self.slug = slug
    
    self.has_hour = False
    if date:
      self.date = self._parse_date(date)
    else:
      self.date = datetime.today()

  def _parse_date(self, date):
    # test for when we have an hour and minute: '30/04/2015 15:22'
    if len(date.split(' ')) > 1:
      date = datetime.strptime(date, '%d-%m-%Y %H:%M')
      self.has_hour = True
    else:
      date = datetime.strptime(date, '%d-%m-%Y')
    return date

  def get_filename(self):
    date = self.date.strftime('%d-%m-%Y')
    filename = u'{date}-{slug}.{ext}'.format(date=date, slug=self.slug, ext='markdown')
    return filename
    
  def get_date(self):
    if self.has_hour is True:
      date = self.date.strftime('%d-%m-%Y %H:%M')
    # If the post had no time, don't use the default '00:00'
    else:
      date = self.date.strftime('%d-%m-%Y')
    return date
    
    
  def prepare_post(self):
    date = self.get_date()
  
    post = u"""title: {0}
date: {1}
slug: {2}
====
{3}
""".format(self.title, date, self.slug, self.content)
    return post
    
def read(path):
  with io.open('{}'.format(path), mode='r', encoding='utf_8') as f:
    return f.read().decode('utf8')

def write(path, filename, content):
  make_dirs(path)
  with io.open(os.path.join(path, filename), mode='w', encoding='utf_8') as f:
    f.write(content)
      
def make_dirs(path):
  # If the destination dir(s) don't already exist, create them
  if os.path.isdir(path):
    return True
  else:
    os.makedirs(path)
    return True
  
def get_all_files(path):
  files = []
  for filename in os.listdir(path):
    # Without this check, we try to 'read' directories
    if os.path.isfile(os.path.join(path, filename)):
      file = read(os.path.join(path, filename))
      files.append(file)
  return files

def get_metadata(line, prefix):
  
  if line.startswith(prefix):
    
    # title: Long title here! -> ['Long', 'title', ... ] -> 'Long title ...'
    line = line.split(' ')[1:]
    line = ' '.join(line)
    
    # We don't want an empty string
    if line:
      return line 
  return False
    
def get_post_dict(post):
  """Reads an existing post and returns a dictionary.
  { title, date, slug, post }"""
  post_dict = dict()
  prefixes = ['title', 'date', 'slug']
  
  for line in post.split('\n'):
    for prefix in prefixes:
      data = get_metadata(line, prefix)
      
      if data:
        post_dict[prefix] = data
        
        # We got what we came for
        break
        
    if line.startswith('===='):
      post_start = post.index('====') + 5
      post_dict['content'] = post[post_start:]
      break

  # We need at least a title, slug, and post. We can make the date.
  if post_dict.get('title') and post_dict.get('slug') and post_dict.get('content'):
    return post_dict
  else:
    return False

def get_post(post_text):
  p = get_post_dict(post_text)
  if p:
    post = blog_post(title=p['title'], content=p['content'], date=p['date'], slug=p['slug'])
    return post
  else:
    return False

def create_post(post_text):
  """Takes a post from Editorial and writes it to the posts dir as a .md file.
  Format:
    tite:
    date:
    slug:
    ====
    (content here)
  """
  post = get_post(post_text)
  if post:
    filename = post.get_filename()
    prepared_post = post.prepare_post()
    write(POSTS_DIR, filename, prepared_post)
    return True  
  else:
    print('Failed to parse the post.')
    return False
  
def build_site():
  # Load and write each post to the output dir
  files = get_all_files(POSTS_DIR)
  posts = []
  for file in files:
    post = get_post(file)
    post_html = template.make_post(post)
    path = os.path.join(OUTPUT_DIR, '{}/'.format(post.slug))
    filename = u'index.html'
    write(path, filename, post_html)
    # We need to pass the post objects to get_index
    posts.append(post)
  
  # Get and write index.html
  index = template.get_index(posts)
  index = index.decode('utf8')
  # print repr(index)
  # print 'in build site, type of index: {}'.format(type(index))
  write(OUTPUT_DIR, u'index.html', index)
  
  # Copy static resources
  css_dir = os.path.join(STATIC_DIR, 'css/')
  css_files = os.listdir(css_dir)
  dest = os.path.join(OUTPUT_DIR, 'css/')
  for file in css_files:
    source = os.path.join(css_dir, file)
    # Make sure we're working on a file
    if os.path.isfile(source):
      # Make all the dirs up to '/output/css' if needed
      if os.path.isdir(dest) is False:
        os.makedirs(dest)
      shutil.copy(source, dest)
  
  
def clean_site():
  print 'TODO'
    
def main(filename, command, *args):
  if command == 'build':
    build_site()
  if command == 'clean':
    clean_site()
  if command == 'add':
    post = clipboard.get()
    if post:
      # It's already unicode, so no need to decode
      success = create_post(post)
      webbrowser.open('editorial://workflow-callback/?success={}'.format(success))
    else:
      print 'Nothing on clipboard'
      webbrowser.open('editorial://workflow-callback/?success=False')
  if command == 'help':
    print """Blok is a small static site generator.
    
    Arguments:
      help    - this help.
      add     - add a blog post. Input is the text of a blog post in markdown on the clipboard
      build   - write all posts in posts/ dir to site/ as html files, and create index.html
      clean   - deletes all files and directories from the output dir"""
    
if __name__ == '__main__':
  # if we have at least a command
  if len(argv) > 1:
    main(*argv)
  else:
    main(command='help', *argv)
  
  

post = u'title: Test\nslug: test-post\n\n====\nПроверка'
post_dict = get_post_dict(post)
# filename = get_filename(post_dict)

# create_post(post)
