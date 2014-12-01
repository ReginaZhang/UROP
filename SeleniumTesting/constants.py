'''p_mount_container = {'os_ep': "mspEndPoint",
                     'username': "mspUserName",
                     'password': "mspPassword",
                     'tenancy': "mspTenancyName",
                     'container': "mspContainerName",
                     'submit': "mspSwiftMountBtn",
                     'successful_popup': "Mounted  container UROP\n it should be available for use in a few seconds."}
page_constants = {'base_url': "https://genomespace.genome.edu.au/jsui",
                  'registration_link_text': "Register new GenomeSpace user",
                  'registration_username': "usernameEntry",
                  'registration_pw': "passwordEntry",
                  'registration_email': "emailEntry",
                  'registration_signup': "signupButton",
                  'login_name': "identity",
                  'login_pw': "password",
                  'login_signin': "signin_button",
                  'menu_file': "menuFile",
                  'menu_connect': "menuConnect",
                  'swift_container': "swiftMenuItem",
                  'mount_container': p_mount_container}

t_mount_container = {'os_ep': "https://keystone.rc.nectar.org.au:5000/v2.0/tokens",
                     'username': "ruijing.zhang@unimelb.edu.au",
                     'password': "NWE4Yzg4NTlkMmVlZTU4",
                     'tenancy': "pt-9344",
                     'container': "UROP"}
test_constants = {'registration_name': "",
                  'registration_pw': "",
                  'registration_email': "",
                  'login_name': "test",
                  'login_pw': "test",
                  'mount_container': t_mount_container}'''


# The constants for the page elements
p_mount_container = {'os_ep': "mspEndPoint",
                     'username': "mspUserName",
                     'password': "mspPassword",
                     'tenancy': "mspTenancyName",
                     'container': "mspContainerName",
                     'submit': "mspSwiftMountBtn",
                     'successful_popup': "Mounted  container UROP\n it should be available for use in a few seconds."}
common = {'base_url': "https://genomespace.genome.edu.au/jsui",
          'menu_file': "menuFile"}

page_register = {'registration_link_text': "Register new GenomeSpace user",
                 'registration_username': "usernameEntry",
                 'registration_pw': "passwordEntry",
                 'registration_email': "emailEntry",
                 'registration_signup': "signupButton"}

page_login = {'login_name': "identity",
              'login_pw': "password",
              'login_signin': "signin_button"}

page_container = {'menu_connect': "menuConnect",
                  'swift_container': "swiftMenuItem",
                  'mount_container': p_mount_container}

page_file = {'sort_filename': "fileNameSortFiles",
             'rename': "menuFileRename"}


# following are the keys for the tests
t_mount_container = {'os_ep': "https://keystone.rc.nectar.org.au:5000/v2.0/tokens",
                     'username': "ruijing.zhang@unimelb.edu.au",
                     'password': "NWE4Yzg4NTlkMmVlZTU4",
                     'tenancy': "pt-9344",
                     'container': "UROP"}
test_register = {'registration_name': "",
                 'registration_pw': "",
                 'registration_email': ""}

test_login = {'login_name': "test",
              'login_pw': "test"}

test_container = {'mount_container': t_mount_container}

test_folder = {'GS-Demo_xpath': "//a[@dirpath='/Home/swift:GS-Demo']",
               'test1_xpath': "//a[@dirpath='/Home/swift:GS-Demo/test1']",
               'test2_xpath': "//a[@dirpath='/Home/swift:GS-Demo/test2']"}

test_file = {'before_rename': "before_rename.txt",
             'before_rename_xpath': "//a[@filepath='/Home/swift:GS-Demo/test1/before_rename.txt']",
             'after_rename': "after_rename.txt",
             'before_rename_url': "https://genomespace.genome.edu.au/datamanager/v1.0/file//Home/swift:GS-Demo/test1/before_rename.txt",
             'after_rename_path': "/Home/swift:GS-Demo/test1/after_rename.txt"}

"""//div[contains(@class, 'ui-dialog')]/div[preceding-sibling::div/span[contains(., 'Rename display')]]/input[@value='test']"""

