from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .models import (
    H5PContent,
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
    except H5PContent.DoesNotExist:
        # todo redirect to index
        return redirect("/")

    ajax_path = "/h5p/ajax/"

    # todo log view
    return render(request, 'h5p_view_content.html', {
        'content': content,
        'ajax_path': ajax_path
    })


@staff_member_required
def h5p_editor(request, content_id):
    # TODO
    # implement https://github.com/h5p/h5p-moodle-plugin/blob/master/editor.js
    # code to add editor to a page
    ajax_path = "/h5p/ajax/"
    return render(request, "h5p_editor.html", {
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
