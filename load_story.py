from models.story import Story
from utils import format_content


page = 1
story_name = 'dpcq'

with open('qqqq.txt', 'rb') as f:
    file = f.read()
    ls = file.split(b'------------\n\n')
    print(len(ls))
    ls.pop(0)
    ls.pop(-1)
    for l in ls:
        try:
            title, content = l.split(b'\n\n', 1)
            print('title:', title.decode('gbk'))
            con = format_content(content.decode('gbk'))
            form = {
                'title': title.decode('gbk'),
                'content': con,
                'page': page,
                'story_name': story_name,
            }
            Story.new(form)
            page += 1
        except Exception as result:
            print(result)
