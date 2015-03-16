'''
Module created on 26/11/2014

@author: Regina Zhang

'''

# The constants for the page elements
p_mount_container = {'os_ep': "mspEndPoint",
                     'username': "mspUserName",
                     'password': "mspPassword",
                     'tenancy': "mspTenancyName",
                     'container': "mspContainerName",
                     'submit': "mspSwiftMountBtn",
                     'successful_popup': "Mounted  container %s\n it should be available for use in a few seconds." }
common = {'base_url': "https://genomespace-dev.genome.edu.au",
          'home_suffix': '/jsui',
          'menu_file': "menuFile",
          'Home_xpath': '//a[@dirpath="/Home"]'}

page_register = {'link_text': "Register new GenomeSpace user",
                 'username': "usernameEntry",
                 'pw': "passwordEntry",
                 'email': "emailEntry",
                 'signup_button': "signupButton"}

page_login = {'login_name': "identity",
              'login_pw': "password",
              'login_signin': "signin_button"}

page_container = {'menu_connect': "menuConnect",
                  'swift_container': "swiftMenuItem",
                  'mount_container': p_mount_container}

page_file = {'sort_filename': "fileNameSortFiles",
             'rename': "menuFileRename",
             'copy/move': "menuFileMove",
             'view_private_link':"menuFileLink",
             'private_url_dialog_xpath':'//span[@id="adMessage"]/input'}

page_botton = {'copy': '//div[contains(@tabindex, "-1")]//div[@class="dialogButtonDiv"]/button[contains(text(),"Copy")]'}

page_input = {'copy/move': "//div[contains(@class, 'ui-dialog')]/div[preceding-sibling::div/span[contains(., 'Copy or Move')]]/input"}


# following are the keys for the tests
container_names = {"for mounting test" : "For_Mounting_Test",
                   "for data tests" : "UROP"}

t_mount_container = {'Endpoint': 'https://keystone.rc.nectar.org.au:5000/v2.0/tokens',
                     'osUserName': 'ruijing.zhang@unimelb.edu.au',
                     'osPassword': 'NWE4Yzg4NTlkMmVlZTU4',
                     'OsTenant': 'pt-9344',
                     'container': None}
test_register = {'username': "test",
                 'pw': "test",
                 'email': "ykowsar@gmail.com"}

test_login = {'login_name': "test",
              'login_pw': "test"}

test_container = {'mount_container': t_mount_container}

test_folder = {'GS-Demo_xpath': "//a[@dirpath='/Home/swift:GS-Demo']",
               'test1_xpath': "//a[@dirpath='/Home/swift:GS-Demo/test1']",
               'test2_xpath': "//a[@dirpath='/Home/swift:GS-Demo/test2']",
               'UROP_xpath':'//tbody//div[@id="directoriesDiv"]//a[@dirpath="/Home/swift:UROP"]',
               'subdir1_xpath': '//div[@id = "filesDiv2"]//tbody//a[@dirpath = "/Home/swift:UROP/subdir1"]',
               'subdir2_xpath': '//div[@id = "filesDiv2"]//tbody//a[@dirpath = "/Home/swift:UROP/subdir2"]'}

test_file = {'before_rename_path': {"small": "/Home/swift:UROP/before_rename_s.txt"},
             'after_rename_path': {"small": "/Home/swift:UROP/after_rename_s.txt"},
             'file_to_copy': "file_to_copy.txt",
             'copy_source_path': {"folder": "/Home/swift:UROP/subdir1/file_to_copy.txt",
                                  "container": "/Home/swift:UROP/subdir1/file_to_copy.txt"},
             'copy_target_path':{"folder": "/Home/swift:UROP/subdir2/file_to_copy.txt",
                                 "container": "/Home/swift:UROP_Test/file_to_copy.txt"},
             'file_to_delete_path': "/Home/swift:UROP/subdir2/file_to_copy.txt",
             'file_to_share_xpath': '//div[@id="filesDiv2"]//a[@filepath="/Home/swift:UROP/file_to_share.txt"]',
             'file_to_upload_path': "/Home/swift:UROP/file_to_upload.txt"}

"""//div[contains(@class, 'ui-dialog')]/div[preceding-sibling::div/span[contains(., 'Rename display')]]/input[@value='test']"""

# js functions for http requests

js_func = {'get_response': '''function getResponse(xmlhttp) {\
                if (xmlhttp.status >= 400 || (100 <= xmlhttp.status && xmlhttp.status < 200)) {\
                    alert("Failure: " + xmlhttp.status + "  Response: " + xmlhttp.responseText);\
                } else if (xmlhttp.status >= 300) {\
                    alert("Manual redirection needed: " + xmlhttp.status + "&#x0A;Response: " + xmlhttp.responseText);\
                } else if (xmlhttp.status >= 200) {\
                    alert("Success: " + xmlhttp.status);\
                } else {\
                    alert("Http request not sent.");\
                }\
            }''',
           'mount':'''function mount() {\
                var xmlhttp=new XMLHttpRequest();\
                xmlhttp.open("PUT", "''' + common['base_url'] + '''/datamanager/v1.0/storage/test/swift/%s", false);\
                xmlhttp.setRequestHeader("Content-Type", "application/json; charset=UTF-8");\
                xmlhttp.send(JSON.stringify({"storageType":"Swift","attributes":%s,"filePermissions":["R","W"]}));\
                getResponse(xmlhttp);\
            }''',
            'disconnect':'''function disconnect() {\
                var xmlhttp=new XMLHttpRequest();\
                xmlhttp.open("DELETE", "''' + common['base_url'] + '''/datamanager/v1.0/storage/test/swift/%s", false);\
                xmlhttp.send();\
                getResponse(xmlhttp);\
            }''',
           'rename': '''function rename() {\
                var xmlhttp=new XMLHttpRequest();\
                xmlhttp.open("POST", "''' + common['base_url'] + '''datamanager/v1.0/file/%s",false);\
                xmlhttp.setRequestHeader("Content-Type", "application/json; charset=UTF-8");\
                xmlhttp.send(JSON.stringify({"path":"%s"}));\
                getResponse(xmlhttp);\
            }''',
           'copy_btw_folders':'''function copy_btw_folders(){\
                var xmlhttp=new XMLHttpRequest();\
                xmlhttp.open("PUT", "''' + common['base_url'] + '''/datamanager/v1.0/file%s", false);\
                xmlhttp.setRequestHeader("x-gs-copy-source", "%s");\
                xmlhttp.send();\
                getResponse(xmlhttp);\
            }''',
            'copy_btw_containers':'''function copy_btw_containers(){\
                var xmlhttp=new XMLHttpRequest();\
                xmlhttp.open("PUT", "''' + common['base_url'] + '''/datamanager/v1.0/file%s",false);\
                xmlhttp.setRequestHeader("x-gs-copy-source", "%s");\
                xmlhttp.send();\
                getResponse(xmlhttp);\
            }''',
            'delete': '''function delete_data() {\
                var xmlhttp=new XMLHttpRequest();\
                xmlhttp.open("DELETE", "''' + common['base_url'] + '''/datamanager/v1.0/file%s",false);\
                xmlhttp.send();\
                getResponse(xmlhttp);\
            }''',
            'move_btw_folders':'''function move_btw_folders() {\
                var xmlhttp=new XMLHttpRequest();\
                xmlhttp.open("POST", "''' + common['base_url'] + '''/datamanager/v1.0/file//Home/swift:UROP/subdir1/file_to_move.txt", false);\
                xmlhttp.setRequestHeader("Content-Type", "application/json; charset=UTF-8");\
                xmlhttp.send(JSON.stringify({"path":"/Home/swift:UROP/subdir2/file_to_move.txt"}));\
                getResponse(xmlhttp);\
            }''',
            'move_btw_containers':'''function move_btw_containers() {\
                var xmlhttp=new XMLHttpRequest();\
                xmlhttp.open("POST", "''' + common['base_url'] + '''/datamanager/v1.0/file//Home/swift:UROP/subdir2/file_to_move.txt",false);\
                xmlhttp.setRequestHeader("Content-Type", "application/json; charset=UTF-8");\
                xmlhttp.send(JSON.stringify({"path":"/Home/swift:UROP_Test/file_to_move.txt"}));\
                getResponse(xmlhttp);\
            }''',
            'generate_public_url':'''function generate_public_url() {\
                var xmlhttp=new XMLHttpRequest();\
                xmlhttp.open("HEAD", "''' + common['base_url'] + '''/datamanager/file/Home/swift:UROP/subdir1/file_to_copy.txt",false);\
                xmlhttp.send("signedURL=true");\
                getResponse(xmlhttp);\
                public_url = xmlhttp.getResponseHeader("external-link");\
                alert("Public URL: " + public_url);\
                alert(xmlhttp.getAllResponseHeaders());\
            }''',
            'share_data':'''function share_data() {\
                var xmlhttp=new XMLHttpRequest();\
                xmlhttp.open("GET", "%s", false);\
                xmlhttp.send();\
                getResponse(xmlhttp);\
            }''',
            'import_url':'''function import_url() {\
                var xmlhttp=new XMLHttpRequest();\
                xmlhttp.open("PUT", "''' + common['base_url'] + '''/datamanager/v1.0/file/Home/swift:UROP/subdir1", false);\
                xmlhttp.setRequestHeader("x-gs-fetch-source", "%s");\
                xmlhttp.send(JSON.stringify({"isDirectory":"true"}));\
                getResponse(xmlhttp);\
            }''',
            'launch_with_file':'''function launch_with_file() {\
                var xmlhttp=new XMLHttpRequest();\
                xmlhttp.open("POST", "''' + common['base_url'] + '''/identityServer/usermanagement/utility/usageLog", false);\
                xmlhttp.setRequestHeader("Content-Type", "application/json");\
                xmlhttp.send(JSON.stringify({"module":"GSUI","function":"LAUNCH","username":"test","entity":"Galaxy : %s"}));\
                getResponse(xmlhttp);\
                var xmlhttp1=new XMLHttpRequest();\
                xmlhttp1.open("GET","''' + common['base_url'] + '''/atm/v1.0/webtool/Galaxy/launchurl?URL=%s",false);\
                xmlhttp1.setRequestHeader("Content-Type", "application/json");\
                xmlhttp1.send(JSON.stringify({"module":"GSUI","function":"LAUNCH","username":"test","entity":"Galaxy : %s"}));\
                getResponse(xmlhttp1);\
            }''',
            'upload_file':'''function upload_file() {\
                var getrequest=new XMLHttpRequest();\
                getrequest.open("GET","''' + common['base_url'] + '''/datamanager/v1.0/uploadinfo%s",false);\
                getrequest.send();\
                getResponse(getrequest);\
                if (getrequest.status < 300 && getrequest.status > 199) {\
                    str = getrequest.response;\
                    response_obj = JSON.parse(str);\
                    path = response_obj.path;\
                    url = response_obj.swiftFileUrl;\
                    token = response_obj.token;\
                    var putrequest=new XMLHttpRequest();\
                    putrequest.open("PUT", url+"/"+path, false);\
                    putrequest.setRequestHeader("X-Auth-Token", token);\
                    putrequest.send("Testing testing");\
                    getResponse(putrequest);\
                }\
            }'''}

'''{"container":"{0}","osUserName":"ruijing.zhang@unimelb.edu.au","Endpoint":"https://keystone.rc.nectar.org.au:5000/v2.0/tokens","OsTenant":"pt-9344","osPassword":"NWE4Yzg4NTlkMmVlZTU4"}'''
