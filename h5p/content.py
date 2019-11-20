from django.conf import settings
import tempfile
import shutil
import zipfile
import json
import os
import glob
from h5p.models import *

if not os.path.exists(settings.MEDIA_ROOT):
    os.makedirs(settings.MEDIA_ROOT)
H5P_DIR = settings.MEDIA_ROOT + '/h5p/'
CONTENT_DIR = H5P_DIR + 'content/'
LIBRARY_DIR = H5P_DIR + 'libraries/'
if not os.path.exists(H5P_DIR):
    os.mkdir(H5P_DIR)
if not os.path.exists(CONTENT_DIR):
    os.mkdir(CONTENT_DIR)
if not os.path.exists(LIBRARY_DIR):
    os.mkdir(LIBRARY_DIR)


def get_library_path(library):
    return LIBRARY_DIR + library.machine_name + "/"


def get_library_json(library):
    json_path = get_library_path(library) + 'library.json'
    ld_file = open(json_path)
    ld_json = json.load(ld_file)
    ld_file.close()
    return ld_json


def get_subdirectories(d):
    return filter(os.path.isdir, [os.path.join(d, f) for f in os.listdir(d)])


def process_library(ld):
    ld_file = open(ld + '/library.json', 'r')
    ld_json = json.load(ld_file)
    ld_file.close()
    # TODO inspect library json, compare to existing library objects
    # if its not in there create a new library object
    # libraries are stored in upload/h5p/libraries/name
    library, created = H5PLibrary.objects.get_or_create(machine_name=ld_json['machineName'], major_version=ld_json['majorVersion'], minor_version=ld_json['minorVersion'], patch_version=ld_json['patchVersion'], title=ld_json['title'])

    if created:
        for key in [('preloadedJs', 'preloaded_js'), ('preloadedCss', 'preloaded_css'), ('fullscreen', 'fullscreen'), ('runnable', 'runnable')]:
            json_name = key[0]
            db_name = key[1]
            if json_name in ld_json:
                setattr(library, db_name, ld_json[json_name])
        # check for semantics file
        semantics_path = ld + '/semantics.json'
        if os.path.exists(semantics_path):
            semantics_file = open(semantics_path, 'r')
            semantics_json = json.load(semantics_file)
            semantics_file.close()
            library.semantics = json.dumps(semantics_json)
        library.save()
        library.json = ld_json
        shutil.move(ld, LIBRARY_DIR + library.machine_name)
    return library


def process_library_dependencies(library):
    lib_json = get_library_json(library)
    content_libraries = [library]
    # TODO add library dependencies
    if 'preloadedDependencies' in lib_json:
        for preload in lib_json['preloadedDependencies']:
            required_library = H5PLibrary.objects.get(machine_name=preload['machineName'])
            dependency, created = H5PLibraryDependency.objects.get_or_create(library=library, required_library=required_library, dependency_type='preloaded')
            if required_library not in content_libraries:
                content_libraries.append(required_library)
    editor_libraries = []
    if 'editorDependencies' in lib_json:
        for editor_dep in lib_json['editorDependencies']:
            required_library = H5PLibrary.objects.get(machine_name=editor_dep['machineName'])
            dependency, created = H5PLibraryDependency.objects.get_or_create(library=library, required_library=required_library, dependency_type='editor')
    return {'content_libraries': content_libraries, 'editor_libraries': editor_libraries}


def h5p_file_process(h5p_file, content_name=""):

    tmpdir = tempfile.mkdtemp()
    #try:
    file_path = h5p_file.h5p_file.file.name
    if 1 == 1:
        is_zipfile = zipfile.is_zipfile(file_path)
        if is_zipfile:
            with zipfile.ZipFile(file_path) as libzip:
                libzip.extractall(tmpdir)
        #print(glob.glob(tmpdir+'/*'))
        if os.path.isfile(tmpdir + '/h5p.json'):
            h5p_file = open(tmpdir + '/h5p.json')
            h5p_json = json.load(h5p_file)
            subdirs = get_subdirectories(tmpdir)
            libdirs = []
            for sd in subdirs:
                if os.path.isfile(sd + '/library.json'):
                    libdirs.append(sd)
            libraries = []
            for ld in libdirs:
                library = process_library(ld)
                libraries.append(library)
            # loop over libraries again to create dependencies
            content_libraries = []
            for library in libraries:
                deps = process_library_dependencies(library)
                for content_lib in deps['content_libraries']:
                    if content_lib not in content_libraries:
                        content_libraries.append(content_lib)

            if os.path.exists(tmpdir + '/content'):
                content_json_path = tmpdir + '/content/content.json'
                if os.path.isfile(content_json_path):
                    content_file = open(content_json_path, 'r')
                    content_json = json.load(content_file)
                    main_library = H5PLibrary.objects.get(machine_name=h5p_json['mainLibrary'])
                    content = H5PContent.objects.create(json_content=json.dumps(content_json), main_library=main_library, name=content_name)

                    # we need to get the dependency tree level
                    # so we can load all the libraries in order
                    content_lib_ids_list = []
                    for content_lib in content_libraries:
                        content_lib_ids_list.append(content_lib.id)
                    content_lib_ids = tuple(content_lib_ids_list)
                    required_libraries = H5PLibrary.objects.raw("with recursive tree as (select h5p_h5plibrary.id,required_library_id, 0 as level from h5p_h5plibrary left join h5p_h5plibrarydependency on h5p_h5plibrary.id = h5p_h5plibrarydependency.library_id where h5p_h5plibrary.id in %s union all select h5p_h5plibrary.id,h5p_h5plibrarydependency.required_library_id, tree.level + 1 from tree, h5p_h5plibrary left join h5p_h5plibrarydependency on h5p_h5plibrary.id = h5p_h5plibrarydependency.library_id where h5p_h5plibrary.id = tree.required_library_id) select h5p_h5plibrary.*, max(tree.level) as level from h5p_h5plibrary,tree where tree.id = h5p_h5plibrary.id group by h5p_h5plibrary.id", params=[content_lib_ids])
                    for content_lib in required_libraries:
                        content_library, created = H5PContentLibrary.objects.get_or_create(content=content, library=content_lib, dependency_type='preloaded', weight=content_lib.level)
                    for key in [('embedTypes', 'embed_types'), ('contentType', 'content_type'), ('author', 'author'), ('license', 'license'), ('metaKeywords', 'meta_keywords'), ('metaDescription', 'meta_description'), ('filtered', 'filtered'), ('slug', 'slug')]:
                        json_name = key[0]
                        db_name = key[1]
                        if json_name in h5p_json:
                            setattr(content, db_name, h5p_json[json_name])
                    content.save()
                    # move content to uploads/h5p/content/id
                    shutil.move(tmpdir + '/content', CONTENT_DIR + str(content.id))

#    Except Exception as e:
#        print (e)

    shutil.rmtree(tmpdir)
    return None


def process_update(h5p_file):
    tmpdir = tempfile.mkdtemp()
    #try:
    file_path = h5p_file.h5p_file.file.name
    if 1 == 1:
        is_zipfile = zipfile.is_zipfile(file_path)
        if is_zipfile:
            with zipfile.ZipFile(file_path) as libzip:
                libzip.extractall(tmpdir)
            #print(glob.glob(tmpdir+'/*'))
            subdirs = get_subdirectories(tmpdir)
            libdirs = []
            for sd in subdirs:
                if os.path.isfile(sd + '/library.json'):
                    libdirs.append(sd)
            libraries = []
            for ld in libdirs:
                library = process_library(ld)
                libraries.append(library)
            for lib in libraries:
                process_library_dependencies(lib)

    return
