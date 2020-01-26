import datetime
import os
import re
import sys
import zipfile

TEMPLATE_ZIP = os.path.join(os.path.dirname(__file__), 'plugin-template.zip')

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    fields = {
        'name': 'Plugin',
        'description': 'A Nanome Plugin',
        'category': 'other',
        'version': '1.0.0',
        'company': 'Nanome',
        'author': 'Nanome',
        'email': 'hello@nanome.ai',
        'repo': 'https://github.com/nanome-ai/'
    }

    try:
        for key, value in fields.items():
            res = input('%s (%s): ' % (key, value))
            fields[key] = res.strip() or value
    except KeyboardInterrupt:
        sys.exit(0)

    name = ' '.join(w.title() if w.islower() else w for w in fields['name'].split())
    fields['name'] = name
    fields['class'] = name.replace(' ', '')
    fields['folder'] = 'nanome_' + name.lower().replace(' ', '_')
    fields['command'] = fields['folder'].replace('_', '-')
    fields['year'] = str(datetime.datetime.today().year)

    with zipfile.ZipFile(TEMPLATE_ZIP, 'r') as z:
        z.extractall(path)

    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                content = f.read()
            for key, value in fields.items():
                content = content.replace('{{%s}}' % key, value)
            with open(file_path, 'w') as f:
                f.write(content)

    plugin_path = os.path.join(path, 'nanome_plugin', fields['class'] + '.py')
    os.rename(os.path.join(path, 'nanome_plugin/Plugin.py'), plugin_path)
    folder_path = os.path.join(path, fields['folder'])
    os.rename(os.path.join(path, 'nanome_plugin'), folder_path)

if __name__ == '__main__':
    main()
