import json
from collections import OrderedDict
from django.conf import settings
from h5p.models import H5PLibrary, H5PLibraryDependency


def get_core_js():
    return ['/site_media/static/js/jquery.js', '/site_media/static/js/djangoajax.js', '/site_media/static/js/h5p.js', '/site_media/static/js/h5p-event-dispatcher.js', '/site_media/static/js/h5p-x-api-event.js', '/site_media/static/js/h5p-x-api.js', '/site_media/static/js/h5p-content-type.js']


def get_editor_js():
    return [
        '/site_media/static/js/h5peditor.js',
        '/site_media/static/js/language/en.js',
        '/site_media/static/js/h5p-confirmation-dialog.js',
        '/site_media/static/js/h5p-action-bar.js',
        '/site_media/static/js/h5peditor-semantic-structure.js',
        '/site_media/static/js/h5peditor-library-selector.js',
        '/site_media/static/js/h5peditor-form.js',
        '/site_media/static/js/h5peditor-text.js',
        '/site_media/static/js/h5peditor-html.js',
        '/site_media/static/js/h5peditor-number.js',
        '/site_media/static/js/h5peditor-textarea.js',
        '/site_media/static/js/h5peditor-file-uploader.js',
        '/site_media/static/js/h5peditor-file.js',
        '/site_media/static/js/h5peditor-image.js',
        '/site_media/static/js/h5peditor-image-popup.js',
        '/site_media/static/js/h5peditor-av.js',
        '/site_media/static/js/h5peditor-group.js',
        '/site_media/static/js/h5peditor-boolean.js',
        '/site_media/static/js/h5peditor-list.js',
        '/site_media/static/js/h5peditor-list-editor.js',
        '/site_media/static/js/h5peditor-library.js',
        '/site_media/static/js/h5peditor-library-list-cache.js',
        '/site_media/static/js/h5peditor-select.js',
        '/site_media/static/js/h5peditor-dimensions.js',
        '/site_media/static/js/h5peditor-coordinates.js',
        '/site_media/static/js/h5peditor-none.js',
        '/site_media/static/js/ckeditor/ckeditor.js',
    ]


def get_editor_css():
    return ['/site_media/static/css/application.css']


def get_core_css():
    return ['/site_media/static/css/h5p.css']


def get_library_js(library):
    js = []
    path = '/site_media/media/h5p/libraries/' + library.machine_name + '/'
    if library.preloaded_js != "":
        preloaded_js = library.preloaded_js.replace("'", '"')
        preloaded_js_json = json.loads(preloaded_js)
        for preload in preloaded_js_json:
            js.append(path + preload['path'])
    return js


def get_library_css(library):
    css = []
    path = "/site_media/media/h5p/libraries/" + library.machine_name + "/"
    if library.preloaded_css != "":
        preloaded_css = library.preloaded_css.replace("'", '"')
        preloaded_css_json = json.loads(preloaded_css)
        for preload in preloaded_css_json:
            css.append(path + preload['path'])
    return css


def get_all_library_js(dependency_libraries):
    all_js = []
    for l in dependency_libraries:
        for js in get_library_js(l):
            if js not in all_js:
                all_js.append(js)
    return all_js


def get_all_library_css(dependency_libraries):
    all_css = []
    for l in dependency_libraries:
        for css in get_library_css(l):
            if css not in all_css:
                all_css.append(css)
    return all_css


def get_all_editor_libraries():
    all_libraries = []
    # need to calculate editor library dependency tree
    # libraries with semantics set are editor libraries

    # TODO FIXME first get all semantics libraries
    # then add their dependencies to the list and reverse it?
    all_libraries = []
    libraries = H5PLibrary.objects.exclude(semantics__isnull=True).exclude(semantics__exact='')
    dep_libraries = H5PLibrary.objects.raw("with recursive tree as (select h5p_h5plibrary.id,required_library_id, 0 as level from h5p_h5plibrary left join h5p_h5plibrarydependency on h5p_h5plibrary.id = h5p_h5plibrarydependency.library_id where coalesce(h5p_h5plibrary.semantics,'') != '' union all select h5p_h5plibrary.id,h5p_h5plibrarydependency.required_library_id, tree.level + 1 from tree, h5p_h5plibrary left join h5p_h5plibrarydependency on h5p_h5plibrary.id = h5p_h5plibrarydependency.library_id where h5p_h5plibrary.id = tree.required_library_id and h5p_h5plibrarydependency.dependency_type='editor') select h5p_h5plibrary.*, max(tree.level) as level from h5p_h5plibrary,tree where tree.required_library_id = h5p_h5plibrary.id group by h5p_h5plibrary.id order by level asc;")
    for l in dep_libraries:
        all_libraries.append(l)
    for l in libraries:
        all_libraries.append(l)
    return all_libraries


def get_library_libraries(library, dependency_type):
    libraries = []
    libraries = H5PLibraryDependency.objects.filter(library_id=library.id, dependency_type=dependency_type)
    return libraries

def get_library_dependencies(library,library_type=None,libraries=[],editor=False):
    for type in ('dynamic','preloaded','editor'):
        deps = get_library_libraries(library,type)
        if type == 'preloaded' and editor == True:
            type = 'editor'
        for d in deps:
            if d.required_library not in libraries:
                if not editor or type == 'editor':
                    libraries.append(d.required_library)
                    get_library_dependencies(d.required_library,library_type,libraries,editor)
    return libraries
                

def get_library_list():
    libraries = []


def get_content_type_libraries():
    return H5PLibrary.objects.filter(runnable=True)

def get_content_type_editor_scripts(content_type):
    libs = get_library_dependencies(content_type,'editor')
    libs.append(content_type)
    javascript = OrderedDict([])
    for l in libs:
        for j in get_library_js(l):
            if j not in javascript:
                print(j)
                js_path = settings.BASE_DIR + j
                with open(js_path,'r') as js_file:
                    javascript[j] = "\n" + js_file.read()
    return javascript

def get_content_type_editor_styles(content_type):
    libs = get_library_dependencies(content_type,'editor')
    libs.append(content_type)
    styles = {}
    for l in libs:
        for c in get_library_css(l):
            if c not in styles:
                c_path = settings.BASE_DIR + c
                with open(c_path,'r') as css_file:
                    styles[c] = css_file.read()
    return styles

