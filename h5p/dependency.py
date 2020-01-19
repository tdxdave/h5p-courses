import json
from collections import OrderedDict
from django.conf import settings
from .models import H5PLibrary, H5PLibraryDependency
from .content import get_library_path
import os


def get_core_js():
    return ["/site_media/static/js/jquery.js",
            "/site_media/static/js/djangoajax.js",
            "/site_media/static/js/h5p.js",
            "/site_media/static/js/h5p-event-dispatcher.js",
            "/site_media/static/js/h5p-x-api-event.js",
            "/site_media/static/js/h5p-x-api.js",
            "/site_media/static/js/h5p-content-type.js"]


def get_editor_js():
    return [
        "/site_media/static/js/h5peditor.js",
        "/site_media/static/js/language/en.js",
        "/site_media/static/js/h5p-confirmation-dialog.js",
        "/site_media/static/js/h5p-action-bar.js",
        "/site_media/static/js/h5peditor-semantic-structure.js",
        "/site_media/static/js/h5peditor-library-selector.js",
        "/site_media/static/js/h5peditor-form.js",
        "/site_media/static/js/h5peditor-text.js",
        "/site_media/static/js/h5peditor-html.js",
        "/site_media/static/js/h5peditor-number.js",
        "/site_media/static/js/h5peditor-textarea.js",
        "/site_media/static/js/h5peditor-file-uploader.js",
        "/site_media/static/js/h5peditor-file.js",
        "/site_media/static/js/h5peditor-image.js",
        "/site_media/static/js/h5peditor-image-popup.js",
        "/site_media/static/js/h5peditor-av.js",
        "/site_media/static/js/h5peditor-group.js",
        "/site_media/static/js/h5peditor-boolean.js",
        "/site_media/static/js/h5peditor-list.js",
        "/site_media/static/js/h5peditor-list-editor.js",
        "/site_media/static/js/h5peditor-library.js",
        "/site_media/static/js/h5peditor-library-list-cache.js",
        "/site_media/static/js/h5peditor-select.js",
        "/site_media/static/js/h5peditor-dimensions.js",
        "/site_media/static/js/h5peditor-coordinates.js",
        "/site_media/static/js/h5peditor-none.js",
        "/site_media/static/js/ckeditor/ckeditor.js",
    ]


def get_editor_css():
    return ["/site_media/static/css/fonts.css",
            "/site_media/static/css/application.css"]


def get_core_css():
    return ["/site_media/static/css/h5p.css"]


# DAVEB we will use standalone-h5p to handle library JS and CSS

def get_library_js(library):
    js = []
    path = "/site_media/media/h5p/libraries/" + library.machine_name + "/"
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
            css.append(path + preload["path"])
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
    libraries = H5PLibrary.objects.exclude(semantics__isnull=True).exclude(semantics__exact="")
    dep_libraries = H5PLibrary.objects.raw("with recursive tree as (select h5p_h5plibrary.id,required_library_id, 0 as level from h5p_h5plibrary left join h5p_h5plibrarydependency on h5p_h5plibrary.id = h5p_h5plibrarydependency.library_id where coalesce(h5p_h5plibrary.semantics,'') != '' union all select h5p_h5plibrary.id,h5p_h5plibrarydependency.required_library_id, tree.level + 1 from tree, h5p_h5plibrary left join h5p_h5plibrarydependency on h5p_h5plibrary.id = h5p_h5plibrarydependency.library_id where h5p_h5plibrary.id = tree.required_library_id and h5p_h5plibrarydependency.dependency_type='editor') select h5p_h5plibrary.*, max(tree.level) as level from h5p_h5plibrary,tree where tree.required_library_id = h5p_h5plibrary.id group by h5p_h5plibrary.id order by level asc;")
    for l in dep_libraries:
        all_libraries.append(l)
    for l in libraries:
        all_libraries.append(l)
    return all_libraries


def get_libraries(library, dependency_type):
    libraries = []
    libraries = H5PLibraryDependency.objects.filter(
        library_id=library.id,
        dependency_type=dependency_type
    )
    return libraries

def get_library_dependencies(library, level=0, libraries={}):
    for l in get_libraries(library,'preloaded'):
        if l.required_library.machine_name not in libraries:
            libraries[l.required_library.machine_name] = l.required_library
            libraries = get_library_dependencies(l.required_library, level + 1, libraries)
        libraries[l.required_library.machine_name].weight = level
    for l in get_libraries(library,'editor'):
        if l.required_library.machine_name not in libraries:
            libraries[l.required_library.machine_name] = l.required_library
            libraries = get_library_dependencies(l.required_library, level + 1, libraries)
        libraries[l.required_library.machine_name].weight = level

    return libraries

def order_library_dependencies(dependencies):
    results = []
    ordered_dependencies = {}
    for d in dependencies:
        lib = dependencies[d]
        if lib.weight not in ordered_dependencies:
            ordered_dependencies[lib.weight] = []
        ordered_dependencies[lib.weight].append(lib)
    order_keys = list(ordered_dependencies.keys())
    order_keys.sort()
    order_keys = order_keys[::-1]
    for order in order_keys:
        for lib in ordered_dependencies[order]:
            results.append(lib)
    return results

def get_library_editor_libraries(library):
    libs = get_library_dependencies(library)
    order = order_library_dependencies(libs)
    return order

def get_library_list():
    libraries = []

def get_content_type_libraries():
    return H5PLibrary.objects.filter(runnable=True)


def get_content_type_editor_scripts(content_type):
    libs = get_library_editor_libraries(content_type)
    libs.append(content_type)
    javascript = OrderedDict([])
    full_js = ''
    for l in libs:
        for j in get_library_js(l):
            if j not in javascript:
                js_path = settings.BASE_DIR + j
                with open(js_path, "r") as js_file:
                    javascript[j] = "\n"
                    js_code = "\n" + js_file.read()
                    full_js += js_code
    full_js_path = get_library_path(content_type) + "library.js"
    full_js_file = open(full_js_path, "w")
    full_js_file.write(full_js)
    full_js_file.close()
    javascript["all"] = "ns.$.ajax({url:'/site_media/media/h5p/libraries/"+l.machine_name+"/library.js', async:false});"
    return javascript

def get_content_type_editor_styles(content_type):
    libs = get_library_editor_libraries(content_type)
    libs.append(content_type)
    styles = {}
    for l in libs:
        for c in get_library_css(l):
            if c not in styles:
                c_path = settings.BASE_DIR + c
                with open(c_path, "r") as css_file:
                    styles[c] = css_file.read()
                    css_base = os.path.dirname(c)
                    styles[c] = styles[c].replace("url('","url('"+css_base+"/")
    return styles
