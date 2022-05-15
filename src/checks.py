import os
import hashlib

temporaly_name_extensions = [".tmp", "~"]
strange_chars = [":","\'","\"",";","*","?",",","$","#", "`", "|","\\"]
suggested_attributes = "rwx-rwx-rwx"

class CheckInteface:
    def __init__(self) -> None:
        pass
    
    def handle(self):
        pass

    def check(self):
        pass

class EmptyFileCheck(CheckInteface):
    def handle(self):
        pass

    def check(self, root, dirs, files):
        for file in files:
            with open(root + "/" + file) as f:
                if f.readlines() == []:
                    print("Found empty file:" + root + "/" + file)

# https://www.geeksforgeeks.org/how-to-get-the-permission-mask-of-a-file-in-python/
# kłopotliwe znaki

class TemporalyFileCheck(CheckInteface):
    def handle(self):
        pass

    def check(self, root, dirs, files):
        for file in files:
            if self.check_temporaly_name(file):
                print("Temporaly file found:" + root + "/" + file)
    
    def check_temporaly_name(self, file_name):
        for temporaly_name_extension in temporaly_name_extensions:
            if file_name[-len(temporaly_name_extension):] == temporaly_name_extension:
                return True
        return False

class UnusuallyCharsInFileNameCheck(CheckInteface):
    def check(self, root, dirs, files):
        for file in files:
            if self.check_strange_char_in_file_name(file):
                print("File with strange chars found:" + root + "/" + file)

    def check_strange_char_in_file_name(self,filename):
        for char in strange_chars:
            if char in filename:
                return True
        return False

class UnusuallyPermissionsForFileCheck(CheckInteface):
    def check(self, root, dirs, files):
        for file in files:
            if self.check_unusually_permissions_for_file_check(file, root):
                print("File with unusally permissions found:" + root + "/" + file)
    
    def check_unusually_permissions_for_file_check(self, file, root):
        status = os.stat(root + "/" + file)
        return oct(status.st_mode)[-3:] != self.code_file_permissions(suggested_attributes)

    def code_file_permissions(self, permissions):
        return ''.join([self.code_file_permission_part(permissions_part) for permissions_part in permissions.split("-")])
            
    def code_file_permission_part(self, permissions):
        code = 0
        if "r" in permissions:
            code += 4
        if "w" in permissions:
            code += 2
        if "x" in permissions:
            code += 1
        return str(code)


class SameFileNames(CheckInteface):
    def __init__(self) -> None:
        self.names = {}

    def check(self, root, dirs, files):
        for file in files:
            if file in self.names:
                self.names[file].append(root)
                print("Found file with the same name as " + file + " in " + root)
            else:
                self.names[file] = [root]

class SameFileContents(CheckInteface):
    def __init__(self) -> None:
        self.content_hashes = {}

    def check(self, root, dirs, files):
        for file in files:
            with open(root + "/" + file, "rb") as f:
                content = f.read()
            content_hash = hashlib.md5(content).hexdigest()
            if content_hash in self.content_hashes:
                self.content_hashes[content_hash].append(root + "/" + file)
                print("Found file with the same content " + file + " in " + root)
            else:
                self.content_hashes[content_hash] = [root + "/" + file]
        

class ChecksAggregate(CheckInteface):
    def __init__(self) -> None:
        self.checks = []
        self.checks.append(EmptyFileCheck())
        self.checks.append(TemporalyFileCheck())
        self.checks.append(UnusuallyCharsInFileNameCheck())
        self.checks.append(UnusuallyPermissionsForFileCheck())
        self.checks.append(SameFileNames())
        self.checks.append(SameFileContents())

    #dwa checki globalne cztery singularne

    def check(self, root, dirs, files):
        for check in self.checks:
            check.check(root, dirs, files)
        print("Checking in " + str(root))

    def check_temporaly_name(self, file_name):
        for temporaly_name_extension in temporaly_name_extensions:
            if file_name[-len(temporaly_name_extension):] == temporaly_name_extension:
                return True
        return False