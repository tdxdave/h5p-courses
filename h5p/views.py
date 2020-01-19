import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .models import (
    H5PContent,
    H5PContentLibrary,
    H5PLibrary,
    H5PFile,
)
from .forms import (
    H5PFileForm,
    H5PUpdateForm,
)
from .content import (
    h5p_file_process,
    process_update,
)
from .dependency import (
    get_all_library_js,
    get_all_library_css,
    get_core_js,
    get_editor_js,
    get_core_css,
    get_editor_css,
    get_libraries,
    get_content_type_libraries,
    get_content_type_editor_scripts,
    get_content_type_editor_styles,
)


# todo add require admin
@staff_member_required
def h5p_content_list(request):
    # Load documents for the list page
    h5p_content = H5PContent.objects.all()

    # Render list page with the documents and the form
    return render(
        request,
        "h5p_content_list.html",
        {"h5p_content": h5p_content}
    )


# todo add require login
@login_required(login_url="/account/login/")
def h5p_view_content(request, content_id):
    # get the content_id from url
    try:
        content = H5PContent.objects.get(id=content_id)
    except:
        # todo redirect to index
        pass
    # format for H5PIntegration javascript object
    # https://h5p.org/creating-your-own-h5p-plugin
    # baseUrl,url,postUserStatistics,ajaxPath,ajax,saveFreq,user,siteUrl,l10n,
    # loadedJs,loadedCss,core,contents
    settings = {}
    # settings contents library,jsonContent,fullScreen,exportUrl,embedCode,
    # resizeCode,mainId,url,title,contentUserData,disable,styles,scripts
    # if embedType is div, we load js/css in the template
    # if its iframe, h5p javascript loads from content styles and scripts
    # according to Moodle h5p
    # https://github.com/h5p/h5p-moodle-plugin/blob/master/view.php
    # The following files are required on all pages where you wish to include
    # H5Ps:
    # jquery.js, h5p.js, h5p-event-dispatcher.js, h5p-x-api-event.js,
    # h5p-x-api.js, h5p-content-type.js and h5p.css.

    # don't generate a giant json file

    site_url = ""
    h5p_url = ""
    ajax_path = "/h5p/ajax/"
    finished_url = ""
    continue_user_data = ""
    content_url = ""
    content_title = ""
    styles = "[]"
    scripts = "[]"
    # todo log view
    return render(request, 'h5p_view_content.html', {
        'content': content,
        'ajax_path': ajax_path
    })


@staff_member_required
def h5p_editor(request, content_id):
    # TODO implement https://github.com/h5p/h5p-moodle-plugin/blob/master/editor.js
    # code to add editor to a page
    # all_libraries = get_all_editor_libraries()
    all_js = get_core_js()
    all_js.extend(get_editor_js())
    all_css = get_core_css()
    all_css.extend(get_editor_css())
    #for l in all_libraries:
    #    print(l.machine_name)
    # all_js.extend(get_all_library_js(all_libraries))
    # all_css.extend(get_all_library_css(all_libraries))
    ajax_path = "/h5p/ajax/"
    return render(request, "h5p_editor.html", {
        "all_js": all_js,
        "all_css": all_css,
        "ajax_path": ajax_path
    })


def h5p_add_content(request):
    # Handle file upload
    if request.method == "POST":
        form = H5PFileForm(request.POST, request.FILES)
        if form.is_valid():

            newfile = H5PFile(h5p_file=request.FILES["h5p_file"])
            newfile.save()

            # process library upload file
            h5p_file_process(newfile, form.cleaned_data["name"])

            messages.success(request, "Content added")
        else:
            messages.error(request, "No content added")

    return redirect("h5p_content_list")


@csrf_exempt
def h5p_ajax(request):
    print("ajax request: ", request)
    action = request.GET.get("action")

    if action == "files":
        return h5p_ajax_files(request)
    if action == "libraries":
        return h5p_ajax_libraries(request)


def h5p_ajax_libraries(request):
    """
    If machineName has been passed in, collect the
    """
    data = []
    if request.GET.get("machineName"):
        print("in h5p_ajax_libraries ({})".format(request.GET.get("machineName")))
        library = H5PLibrary.objects.get(machine_name=request.GET.get("machineName"))
        semantics = json.loads(library.semantics)
        print("in h5p_ajax_libraries, calling get_libraries")
        editor_libraries = get_libraries(library, "editor")
        editor_deps = []
        for editor_lib in editor_libraries:
            print("in h5p_ajax_libraries: one editor dependency is {}".format(editor_lib))
            lib = editor_lib.required_library
            editor_deps.append({
                "machine_name": lib.machine_name,
                "majorVersion": lib.major_version,
                "minorVersion": lib.minor_version
            })

        data = {
            "uberName": "{} {}.{}".format(
                library.machine_name, str(library.major_version), str(library.minor_version)
            ),
            "name": library.machine_name,
            "majorVersion": library.major_version,
            "minorVersion": library.minor_version,
            "title": library.title,
            "runnable": library.runnable,
            "restricted": library.restricted,
            "semantics": semantics,
            "language": None,
            "editorDependencies": editor_deps
        }
        # TODO we need to add javascript element which contains pairs of
        # js url and actual js content
        data["javascript"] = get_content_type_editor_scripts(library)
        data["css"] = get_content_type_editor_styles(library)
    else:
        if request.POST.get("libraries[]"):
            libraries = []
            requested_libraries = request.POST.getlist("libraries[]")
            for l in requested_libraries:
                libraries.append(
                    H5PLibrary.objects.get(machine_name=l.split()[0])
                )
        else:
            libraries = get_content_type_libraries()
        for library in libraries:
            library_dict = {
                "uberName": library.machine_name + " " + str(library.major_version) + "." + str(library.minor_version),
                "name": library.machine_name,
                "title": library.title,
                "majorVersion": library.major_version,
                "minorVersion": library.minor_version,
                "restricted": False,
                "tutorialUrl": library.tutorial_url
            }
            data.append(library_dict)

    return HttpResponse(json.dumps(data), content_type="application/json")


@csrf_exempt
def h5p_ajax_files(request):
    if request.method == "POST":
        h5p_file = request.FILES["file"]
        content_id = request.POST.get("contentId", None)
        data_uri = request.POST.get("dataURI")
        field_name = request.POST.get("field")
        newfile = H5PFile(h5p_file=h5p_file, mime_type=h5p_file.content_type)
        newfile.save()
        #if content_id and content_id != 0:
        #   content = H5PContent.objects.get(id=content_id)
        #else:
        #    content = H5PContent.objects.create()
        # TODO Catch error and report?
    return HttpResponse(json.dumps({"mime": newfile.mime_type, "path": newfile.h5p_file.url, "success": True, "data": {}}), "application/json")


def h5p_h5p_update(request):

    if request.method == "POST":
        form = H5PUpdateForm(request.POST, request.FILES)

        if form.is_valid():
            newfile = H5PFile(h5p_file=request.FILES["h5p_file"])
            newfile.save()

            # process library upload file
            process_update(newfile)

            messages.success(request, "Updated")

            # Redirect to the document list after POST
            return redirect("h5p_content_list")
    else:
        form = H5PUpdateForm()  # A empty, unbound form
    return render(request, "h5p_update.html", {"form": form})
