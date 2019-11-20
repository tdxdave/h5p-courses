from django.conf import settings
from django.db import models
from django.contrib import messages


class H5PFile(models.Model):
    h5p_file = models.FileField(upload_to="uploads/")
    mime_type = models.CharField(max_length=255, default="")


class H5PLibrary(models.Model):
    tutorial_url = models.CharField(max_length=1000)
    machine_name = models.CharField(max_length=128)
    title = models.CharField(max_length=255)
    major_version = models.IntegerField()
    minor_version = models.IntegerField()
    patch_version = models.IntegerField()
    runnable = models.BooleanField(default=True)
    fullscreen = models.BooleanField(default=False)
    embed_types = models.CharField(max_length=255, default="")
    preloaded_js = models.TextField(blank=True)
    preloaded_css = models.TextField(blank=True)
    restricted = models.BooleanField(default=False)
    semantics = models.TextField(blank=True)


class H5PLibraryDependency(models.Model):
    library = models.ForeignKey(H5PLibrary, on_delete=models.CASCADE)
    required_library = models.ForeignKey(H5PLibrary, related_name="required_library", on_delete=models.CASCADE)
    dependency_type = models.CharField(max_length=128, choices=[("dynamic", "dynamic"), ("preloaded", "preloaded"), ("editor", "editor")], default="preloaded")


class H5PLibraryLanguage(models.Model):
    library = models.ForeignKey(H5PLibrary, on_delete=models.CASCADE)
    language_code = models.CharField(max_length=32)
    language_json = models.TextField()


class H5PContent(models.Model):
    name = models.CharField(max_length=255)
    intro = models.TextField()
    json_content = models.TextField()
    embed_type = models.CharField(max_length=128)
    disable = models.BooleanField(default=False)
    main_library = models.ForeignKey(H5PLibrary, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=128, blank=True)
    author = models.CharField(max_length=128, blank=True)
    license = models.CharField(max_length=7, blank=True)
    meta_keywords = models.TextField(blank=True)
    meta_description = models.TextField(blank=True)
    filtered = models.TextField(blank=True)
    slug = models.CharField(max_length=128, blank=True)
    status = models.CharField(max_length=16, default="in progress")


class H5PContentLibrary(models.Model):
    library = models.ForeignKey(H5PLibrary, on_delete=models.CASCADE)
    content = models.ForeignKey(H5PContent, on_delete=models.CASCADE)
    dependency_type = models.CharField(max_length=128, choices=[("dynamic", "dynamic"), ("preloaded", "preloaded"), ("editor", "editor")], default="preloaded")
    weight = models.IntegerField(default=999999)


class H5PPoint(models.Model):
    node = models.ForeignKey(H5PContent, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    started = models.BooleanField(default=True)
    finished = models.BooleanField(default=False)
    points = models.IntegerField()
    max_points = models.IntegerField()


class H5PContentUserData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    main_content = models.ForeignKey(H5PContent, related_name="main_content", on_delete=models.CASCADE)
    sub_content = models.ForeignKey(H5PContent, related_name="sub_content", on_delete=models.CASCADE)
    data_type = models.CharField(max_length=128)
    timestamp = models.DateTimeField()
    data = models.TextField()
    preloaded = models.BooleanField(default=False)
    delete_on_content_change = models.BooleanField(default=False)


class H5PEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    type = models.CharField(max_length=64)
    sub_type = models.CharField(max_length=64)
    content = models.ForeignKey(H5PContent, on_delete=models.CASCADE)
    content_title = models.CharField(max_length=255)
    library_name = models.CharField(max_length=128)


class H5PCounter(models.Model):
    library_name = models.CharField(max_length=128)
    library_version = models.CharField(max_length=32)
    num = models.IntegerField()
