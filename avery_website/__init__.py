from .app import constitution_hook
import os

constitution_contents = 'templates/constitution-contents.html'
print("working")
if not os.path.exists(constitution_contents) or \
        os.stat(constitution_contents).st_size == 0:
    print("doing hook")
    constitution_hook()
