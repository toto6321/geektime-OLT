import os
import shutil

BACKUP = "backup"


# ### step 1: move everything into folder backup
def back_up():
    # in case of the folder "backup" has already existed
    items = os.listdir()
    items = list(filter(lambda i: os.path.isdir(i) and not i.startswith('.') and i != BACKUP, items))

    if not os.path.isdir(BACKUP):
        os.mkdir(BACKUP)
        print("CREATED:")  # INFO
        print(BACKUP)  # INFO

    # move everything to folder backup

    for f in items:
        new_path = os.path.join(BACKUP, f)
        os.rename(f, new_path)
        print("MOVED:")
        print(f)
        print(new_path)


# format file names
# Windows doesn't allow the following characters appear in filename/dirname
# /, \, ?, %, *, :, |, ", <, >, .
def format_path(p):
    return (p
            .replace("?", "")
            .replace("\"", "`")
            .replace("|", "_")
            .replace(":", "--")
            .replace("，", ",")
            )


# ### step 2: copy the original tree into project root folder
def make_a_copy():
    # example with os.walk()
    # root: ./backup/餐(1讲)
    # dirs: []
    # files: ['加餐|在社交网络上刷粉刷量，技术上是如何实现的?.html']
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), BACKUP)):
        for d in dirs:
            abs_d = os.path.join(root, d)
            copy_d = abs_d.replace(f"{BACKUP}/", "")
            new_d = format_path(copy_d)
            if not os.path.isdir(new_d):
                os.mkdir(new_d)
                print("CREATED: ")  # INFO
                print(abs_d)
                print(new_d)

        for f in files:
            abs_f = os.path.join(root, f)
            copy_f = abs_f.replace(f"/{BACKUP}", "")
            new_f = format_path(copy_f)
            shutil.copy(abs_f, new_f)
            print("COPIED: ")  # INFO
            print(abs_f)
            print(new_f)


# ## step 3: Make up common codes
# ### step 3.1. Get the chapter tree
def get_hierarchy_dict():
    root = os.getcwd().rsplit('/', 1)[-1]  # this one is much faster
    # hierarchy tree
    tree = dict()

    # traverse the root directory limiting to our target directories
    items = os.listdir()

    def my_filter(p):
        return (not p.startswith('.')
                and p != BACKUP
                and os.path.isdir(p)
                )

    chapters = list(filter(lambda i: my_filter(i), items))
    for c in chapters:
        file_list = os.listdir(c)
        # just in case
        files = list(filter(lambda f: f.endswith('.html'), file_list))
        tree[c] = files

    return tree


# ### step 3.2. make up top-level styles
def write_common_style(style_file="index.css"):
    """
        write the common styles to a file
        :arg style_file: filename of the style file
    """
    style = """
        #app {
            font: 300 1em/1.8 PingFang SC, Lantinghei SC, Microsoft Yahei, Hiragino Sans GB, Microsoft Sans Serif, WenQuanYi Micro Hei, Helvetica, sans-serif;
        }
        
        #content {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            overflow: hidden;
            overflow-y: scroll;
            font-weight: 400;
        }
        
        aside {
            position: absolute;
            top: 0;
            left: 0;
            width: 380px;
            bottom: 0;
            background: #fefdfc;
            border-right: 1px solid #e4e4e4;
            z-index: 10;
            -webkit-transition: left 0.6s ease;
            transition: left 0.6s ease;
        }
        
        .simplebar_content {
            overflow: hidden scroll;
        }
        
        .hierarchy {
            padding: 0px 22px 10px 38px;
            font-size: 24px;
            height: 40px;
            line-height: 40px;
            color: #404040;
            font-weight: 600;
        }
        
        .c_item {
            border-bottom: 1px solid #e9e9e9;
        }
        
        .chapter_wrapper {
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            padding-top: 20px;
            transition: all 0.3s ease;
        }
        
        .chapter_wrapper > h4 {
            transition: all 0.3s ease;
            font-size: 17px;
            color: #404040;
            font-weight: 600;
        }
        
        .chapter_wrapper > i {
            display: block;
            color: #404040;
            font-size: 20px;
            line-height: 20px;
            transition: transform 0.3s ease;
        }
        
        .article_list {
            overflow: hidden;
        }
        
        .article_item_wrapper {
        
        }
        
        .article_item {
            line-height: 17px;
            padding-top: 20px;
            padding-bottom: 20px;
            position: relative;
            cursor: pointer;
            color: #4c4c4c;
        }
        
        .article_item > a {
            display: block;
            text-decoration: none;
            width: 235px;
            margin-left: 14px;
            font-size: 14px;
            line-height: 20px;
            font-weight: 400;
        }
        
        .article_item:hover {
            color: orange;
        }
        
        main {
            position: absolute;
            /*top: 0;*/
            left: 380px;
            /*right: 0;*/
            /*bottom: 0;*/
            transition: left 0.6s ease;
        
        }
    """
    style = style.strip()
    with open(style_file, 'w') as style_writter:
        style_writter.write(style)


# ### Step 3.3. make up top-level scripts
def write_common_js(js_file="index.js"):
    """
        write common scripts to index.js
        :arg js_file: filename of the js file
    """
    script = """
        function collapse(id) {
            let x = document.getElementById(id)
            if (x.className.indexOf("w3-hide") === -1) {
                x.className = x.className.replace(" w3-show", " w3-hide")
            } else {
                x.className = x.className.replace(" w3-hide", " w3-show")
            }
        }

        function sidebar_click() {
            let sidebar = document.getElementsByClassName('w3-sidebar')[0]
            sidebar.style.display === 'none' ? sidebar.style.display = 'block' : sidebar.style.display = 'none'
        }       
    """
    script = script.strip()
    with open(js_file, 'w') as js_writer:
        js_writer.write(script)


# ### step 3.4: generate common HTML elements
def generate_common_elements(order=None):
    """
    @params order: list Real chapter order
    """
    style_file = "index.css"
    js_file = "index.js"
    # write_common_style(style_file)
    # write_common_js(js_file)
    shutil.copy(f'../../{style_file}', f'./{style_file}')
    shutil.copy(f'../../{js_file}', f'./{js_file}')

    if order is None:
        order = [1, 2, 4, 3, 5, 0, 6]  # for the course: 数据分析实战45讲
    tree = get_hierarchy_dict()

    chapter_title_list = list(tree.keys())
    n_chapter = len(chapter_title_list)

    # HTML const value
    CHARSET = 'UTF-8'

    # chapter container list
    c_items = []
    for i, o in zip(range(n_chapter), order):
        chapter = chapter_title_list[o]
        file_list = os.listdir(chapter)
        # just in case there are other files in the chapter folders
        articles = list(filter(lambda f: f.endswith('.html'), file_list))

        # article container list
        article_lis = []
        for a in articles:
            href = a.split('.html', 1)[0]
            element = f"""
            <div class='article_item'>
                <a  class='w3-bar'
                    href='{os.path.join("..", chapter, a)}'
                    >
                    {href}
                </a>
            </div>
            """
            element = element.strip()
            article_lis.append(element)

        # a chapter node
        # output: <ul><li><a></a></li></ul>
        collapsible_node_id = 'c' + str(i)

        a_list = '\n'.join(article_lis)
        c_item = f"""
        <section class='c_item'>
            <div class='chapter_wrapper' onclick="collapse('{collapsible_node_id}')">
                <h4 class='chapter_title'>{chapter_title_list[o]}</h4>
                <i class='fas fa-angle-down'></i>
            </div>
            <div id='{collapsible_node_id}' class='article_list w3-hide'>
                {a_list}
            </div>
        </section>
        """
        c_item = c_item.strip()
        c_items.append(c_item)

    # chapters
    chapter_elements = '\n'.join(c_items)

    title = os.getcwd().rsplit('/', 1)[-1]

    before = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="{CHARSET}">
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>

        <title>{title}</title>

        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
        <link rel="stylesheet" href="../{style_file}"/>
        <script src="../{js_file}"></script>
    </head>
    <body>
    <div id="app">
        <aside id='aside' class=' w3-show'>
            <div class="course_header">
                <h3 class='w3-text-red'>{title}</h3>
                <div class='course_content'>
                    <h4><span>&gt;</span><span>课程目录</span></h4>
                     <div class='button' onclick="collapse('aside')">关闭</div>
                </div>
            </div>
            {chapter_elements}
        </aside>
        <main class="">
            <article class="">

    """

    # Between before and after is the original content
    after = """
            </article>
        </main>
    </div>
    </body>
    </html>
    """

    return before.strip(), after


# ### step 4: generate valid html files
def generate_valid_html(before="", after=""):
    dirs = os.listdir()
    dirs = list(filter(lambda d: not d.startswith('.') and os.path.isdir(d) and d != BACKUP, dirs))
    root = os.getcwd()
    for d in dirs:
        files = os.listdir(d)
        files = list(filter(lambda f: f.endswith('.html'), files))
        for f in files:
            abs_f = os.path.join(root, d, f)

            # read file content and save into memory
            content = ""
            with open(abs_f, 'r') as reader:
                content = reader.read()

            # generate valid html with original content
            new_content = before + content + after

            # override the original file
            with open(abs_f, 'w') as writer:
                writer.write(new_content)

            abs_f_new = abs_f.rsplit('/', 1)[0] + '/' + f
            os.rename(abs_f, abs_f_new)
            print("CREATED: ")  # INFO
            print(abs_f)
            print(abs_f_new)


if "__main__" == "__main__":
    back_up()
    make_a_copy()
    before, after = generate_common_elements([1, 2, 4, 3, 5, 0, 6]) # 课程：数据分析实战45讲
    generate_valid_html(before, after)
