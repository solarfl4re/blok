# blok
A simple static site generator for Pythonista + Editorial: write in Editorial and send to blok

**How it works**
In `build_site()`, each post is read, converted to html, and then added to an html template and written to the output directory.
If in `posts/` there's a post `03-05-2015-test-post.markdown`, it will be wriiten to `$OUTPUT_DIR/test-post/index.html'.
After the posts are written, for each post a link is added to the main index.html. For the test post above, the link would be `/test-post/`. This gives nice links with no '.html' on the end.

**Editorial workflows**:
* [New post](http://www.editorial-workflows.com/workflow/5812790350577664/oa40mJqmRxY) - a UI for making a new post in Editorial. If you tell it to use the existing file, the contents of the file are added to the post metadata, like so:
```
title: Example title
date: 16-04-2015
slug: example-title
====
(existing file contents here)
```

* [Post -> Blok](http://www.editorial-workflows.com/workflow/5900215483629568/b1X0ckOwSCY) - sends the current post to Blok, where it is added to the posts folder as a markdown file. Then, when the site is built, the post will be included.
