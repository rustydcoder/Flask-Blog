# BLOG

This is my capstone project, it is a light-weight blog built with
flask and other packages in requirements.txt. A blog with anonymous user, users can mask
their identity and read about possible solutions to internal problems.

## Steps

1. Structure Project, use flask blueprint
2. Finding html template or code one - [template from here](https://bootstrapmade.com/zenblog-bootstrap-blog-template/)
3. Edit the template to fit your need

| Route             | Template      | Redirect to  | Methods   |
| ----------------- | ------------- |--------------| --------  |
| /                 | index.html    | None         | GET       |
| /register         | register.html | /            | GET, POST |
| /login            | login.html    | /            | GET, POST |
| /logout           | ------------- | /            | GET       |
| /about            | about.html    | None         | GET       |
| /contact          | contact.html  | None         | GET       |
| /blog/all         |               |              | GET       |
| /blog/new         | make-post.html| /            | GET, POST |
| /blog/<id>        | post.html     | /login or /# | GET, POST |
| /blog/edit/<id>   | make-post.html| /post/<id>   | GET, POST |
| /blog/delete/<id> | ------------- | /post/all    | GET       |
**NB:** # means the same route
