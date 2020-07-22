import os
import shutil
import re

backup = "backup"


#### step 1: move everything into folder backup
def back_up():
    # in case of the folder "backup" has already existed
    items = os.listdir()
    items = list(filter(lambda i: os.path.isdir(i) and not i.startswith('.') and i != backup , items))

    if not os.path.isdir(backup):
        os.mkdir(backup)
        print("CREATED:")  ##INFO
        print(backup)  ##INFO

    # move everything to folder backup

    for f in items:
        new_path = os.path.join(backup, f)
        os.rename(f, new_path)
        print("MOVED:")  ##INFO
        print(f)  ##INFO
        print(new_path)  ##INFO


### step 2: copy the original tree into project root folder
def make_a_copy():
    import os
    import shutil
    ## example with os.walk()
    # root: ./backup/加餐(1讲)
    # dirs: []
    # files: ['加餐|在社交网络上刷粉刷量，技术上是如何实现的?.html']
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), backup)):
        for d in dirs:
            abs_d = os.path.join(root, d)
            copy_d = abs_d.replace(f"{backup}/", "")
            os.mkdir(copy_d)
            print("CREATED: ")  ##INFO
            print(copy_d)  ##INFO

        for f in files:
            abs_f = os.path.join(root, f)
            copy_f = abs_f.replace(f"/{backup}", "")
            shutil.copy(abs_f, copy_f)
            print("COPIED: ")  ##INFO
            print(abs_f)  ##INFO
            print(copy_f)  ##INFO


# format file names
# Windows doesn't allow the following characters appear in filename/dirname
# /, \, ?, %, *, :, |, ", <, >, .
def format_path(p):
    return (p
            .replace("?", "")
            .replace("\"", "`")
            .replace("|", "_")
            .replace(":", "--")
            )


### step 3: generate valid html files
def generate_valid_html():
    import os
    dirs = os.listdir()
    dirs = list(filter(lambda d: not d.startswith('.') and os.path.isdir(d), dirs))
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

            ## generate valid html with original content
            new_content = f"""
                <!doctype html>
                <html>
                <head>
                    <meta charset="utf-8"/>
                    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                    <title>{f[:-5]}</title>
                </head>
                <body>
                    {content}
                </body>
                </html>
                """

            ## override the original file
            with open(abs_f, 'w') as writer:
                writer.write(new_content)

            ## rename
            new_basename = format_path(f)
            abs_f_new = '/'.join(abs_f.rsplit('/', 1)[0:-1] + [new_basename])
            os.rename(abs_f, abs_f_new)
            print("CREATED: ")  ##INFO
            print(abs_f_new)  ##INFO


### step 4: generate index.html
def get_hierarchy_dict():
    # root=os.path.basename(os.path.abspath(os.getcwd())))
    root = os.getcwd().rsplit('/', 1)[-1]  # this one is much faster
    # hierarchy dict
    tree = dict()

    ## traverse the root directory limiting to our target directories
    items = os.listdir()

    def my_filter(p):
        import os
        return (not p.startswith('.')
                and p != backup
                and os.path.isdir(p)
                )

    chapters = list(filter(lambda i: my_filter(i), items))
    print(chapters)
    for c in chapters:
        file_list = os.listdir(c)
        # just in case
        files = list(filter(lambda f: f.endswith('.html'), file_list))
        tree[c] = files

    return tree


def generate_index_html(file):
    import os
    tree = get_hierarchy_dict()

    chapter_title_list = list(tree.keys())
    n_chapter = len(chapter_title_list)

    # the real semantic permutation of chapters, distinct from class to class
    order = [1, 2, 4, 3, 5, 0, 6]

    # HTML const value
    IFRAME_NAME = 'iframe_article'
    CHARSET = 'UTF-8'

    # chapter container list
    c_items = []
    for i, o in zip(range(n_chapter), order):
        chapter=chapter_title_list[o]
        file_list = os.listdir(chapter)
        # just in case there are other files in the chapter folders
        articles = list(filter(lambda f: f.endswith('.html'), file_list))

        # article container list
        article_lis = []
        for a in articles:
            href=a.split('.html', 1)[0]
            element = f"""
            <a  class='w3-block'
                href='{os.path.join(chapter, a)}'
                target='{IFRAME_NAME}'>
                {href}
            </a>
            """
            element=element.strip()
            article_lis.append(element)

        # a chapter node
        # output: <ul><li><a></a></li></ul>
        collapsable_node_id = 'c' + str(i)

        a_list = '\n'.join(article_lis)
        c_item = f"""
        <section class='c_item'>
            <h5 class='w3-block' onclick="collapse('{collapsable_node_id}')">{chapter_title_list[o]}</h5>
            <div id='{collapsable_node_id}' class='w3-block'>
                {a_list}
            </div>
        </section>
        """
        c_item=c_item.strip()
        c_items.append(c_item)

    # chapters
    chapter_elements='\n'.join(c_items)

    title=os.getcwd().rsplit('/', 1)[1]
    js=file.rsplit('.html', 1)[0]+'.js'
    html=f"""
    <!doctype html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>

        <title>数据分析实战45讲</title>

        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
        <link rel="stylesheet" href="index.css"/>
        <script src="{js}"></script>
    </head>
    <body>
    <div id="content" class="w3-content">
        <div class="w3-row">
            <aside class="w3-container w3-quarter">
                <h4 class="w3-text-red">{title}</h4>
                {chapter_elements}
            </aside>
            <main class="w3-container w3-rest">
                        <article class="w3-container">
                            <iframe
                                    id="iframe_article"
                                    name="iframe_article"
                                    class="w3-container"
                            >
                            </iframe>
                        </article>
                    </main>
                </div>
            </div>
        </body>
    </html>
    """
    html=html.strip()

    with open(file, 'w') as fw:
        fw.write(html)

    script="""
        function collapse(id){
            let x = document.getElementById(id)
            if (x.className.indexOf("w3-hide") === -1) {
                x.className += " w3-hide"
            } else {
                x.className = x.className.replace(" w3-hide", "w3-show")
            }
        }
    """
    script=script.strip()
    with open(js, 'w') as fw:
        fw.write(script)
    return


if "__main__" == "__main__":
    # back_up()
    # make_a_copy()
    # generate_valid_html()
    generate_index_html("index.html")
