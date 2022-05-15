from checks import ChecksAggregate
import os

integration_path = "/mnt/c/Users/micha/HOME/Studia/ASU/test/resources/unit"

checks_aggreagate = ChecksAggregate()

for root, dirs, files in os.walk(integration_path):
    # print(root, dirs, files)
    checks_aggreagate.check(root, dirs, files)
        

# print(code_file_permission_part("rw"))