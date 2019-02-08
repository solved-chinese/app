from django.core.files.storage import FileSystemStorage
import os

class OverwriteFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=0):
        if os.path.exists(self.path(name)):
            os.remove(self.path(name))
        return name