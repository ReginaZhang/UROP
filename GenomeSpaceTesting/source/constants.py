'''
Module created on 26/11/2014

@author: Regina Zhang

Last Modification: 23/07/2015

@description:
    a module consisting only constants needed for the program

'''

# The constants for the page elements
common = {'base_url': "https://genomespace-dev.genome.edu.au",
          'home_suffix': '/jsui',
          'menu_file': "menuFile",}

page_register = {'link_text': "Register new GenomeSpace user",
                 'username': "usernameEntry",
                 'pw': "passwordEntry",
                 'email': "emailEntry",
                 'signup_button': "signupButton"}

page_login = {'login_name': "identity",
              'login_pw': "password",
              'login_signin': "signin_button"}


# following are the keys for the tests

default_container_one = {'Endpoint': 'https://keystone.rc.nectar.org.au:5000/v2.0/tokens'}

default_container_two = {'Endpoint': 'https://keystone.rc.nectar.org.au:5000/v2.0/tokens'}

default_user_details = {}


default_gs_folder_paths = {'dir1_path': '/Home/swift:%s/subdir1',
                        'dir2_path': '/Home/swift:%s/subdir2'}

default_gs_file_paths = {'file_to_rename_path': "/Home/swift:%s/before_rename.txt",
                 'after_rename_path': "/Home/swift:%s/after_rename.txt",
                 'file_to_copy_source_path': "/Home/swift:%s/subdir1/file_to_copy.txt",
                 'copy_to_folder_target_path': "/Home/swift:%s/subdir2/file_to_copy.txt",
                 'copy_to_container_target_path': "/Home/swift:%s/file_to_copy.txt",
                 'file_to_move_to_folder_source_path': "/Home/swift:%s/subdir1/file_to_move1.txt",
                 'file_to_move_to_container_source_path': "/Home/swift:%s/subdir1/file_to_move2.txt",
                 'move_to_folder_target_path': "/Home/swift:%s/subdir2/file_to_move1.txt",
                 'move_to_container_target_path': "/Home/swift:%s/file_to_move2.txt",
                 'file_to_delete_path': "/Home/swift:%s/file_to_delete.txt",
                 'file_to_upload_path': "/Home/swift:%s/file_to_upload.txt",
                 'file_to_publish_path': "/Home/swift:%s/file_to_publish.txt",
                 'file_to_generate_public_URL_path': "/Home/swift:%s/file_for_pURL.txt",
                 'file_to_launch_GVL_with': '/Home/swift:%s/file_to_launch_GVL_with.txt',
                 'file_to_import_with_URL_path': '/Home/swift:%s/file_for_pURL.txt',
                 'file_to_import_to_path': '/Home/swift:%s/subdir1/file_for_pURL.txt'}

default_file_name_for_renaming_test = "after_rename.txt"

default_doi_info = {"Title": "test",
            "TitleType": "AlternativeTitle",
            "Email": "test@test.com",
            "Creator": "John Dough",
            "Contributors": "John Dough",
            "Description": "test test"}

default_local_file_paths = {'file_to_rename_path': './test_files/before_rename.txt',
                            'file_to_copy_source_path': './test_files/file_to_copy.txt',
                            'file_to_move_to_folder_source_path': './test_files/file_to_move1.txt',
                            'file_to_move_to_container_source_path': './test_files/file_to_move2.txt',
                            'file_to_delete_path': './test_files/file_to_delete.txt',
                            'file_to_upload_path': './test_files/file_to_upload.txt',
                            'file_to_publish_path': './test_files/file_to_publish.txt',
                            'file_to_generate_public_URL_path': './test_files/file_for_pURL.txt',
                            'file_to_import_with_URL_path': './test_files/file_for_pURL.txt',
                            'file_to_launch_GVL_with': './test_files/file_to_launch_GVL_with.txt',
                            'file_to_import_with_URL_path': './test_files/file_for_pURL.txt'}


# js functions for http requests

js_func = {'get_response': '''function getResponse(xmlhttp) {\
                if (xmlhttp.status >= 400 || (100 <= xmlhttp.status && xmlhttp.status < 200)) {\
                    alert("Failure: " + xmlhttp.status + "  Response: " + xmlhttp.responseText);\
                } else if (xmlhttp.status >= 300) {\
                    alert("Manual redirection needed: " + xmlhttp.status + "  Response: " + xmlhttp.responseText);\
                } else if (xmlhttp.status >= 200) {\
                    alert("Success: " + xmlhttp.status);\
                } else {\
                    alert("Http request not sent.");\
                }\
            }''',
           'check_existence':'''function check_existence(){\
                var xmlhttp=new XMLHttpRequest();\
                var urlstr = "''' + common["base_url"] + '''/datamanager/file" + escape("%s");\
                xmlhttp.open("HEAD", urlstr, false);\
                xmlhttp.send();\
                getResponse(xmlhttp);\
            }''',
           'create_subdir':'''function create_subdir() {\
                var xmlhttp=new XMLHttpRequest();\
                xmlhttp.open("PUT", "%s", false);\
                xmlhttp.send(JSON.stringify({"isDirectory":"true"}));\
                getResponse(xmlhttp);\
            }''',
           'mount':'''function mount() {\
                var xmlhttp=new XMLHttpRequest();\
                xmlhttp.open("PUT", "''' + common['base_url'] + '''/datamanager/v1.0/storage/%s/swift/%s", false);\
                xmlhttp.setRequestHeader("Content-Type", "application/json; charset=UTF-8");\
                xmlhttp.send(JSON.stringify({"storageType":"Swift","attributes":%s,"filePermissions":["R","W"]}));\
                getResponse(xmlhttp);\
            }''',
            'disconnect':'''function disconnect() {\
                var xmlhttp=new XMLHttpRequest();\
                xmlhttp.open("DELETE", "''' + common['base_url'] + '''/datamanager/v1.0/storage/%s/swift/%s", false);\
                xmlhttp.send();\
                getResponse(xmlhttp);\
            }''',
           'rename': '''function rename() {\
                var xmlhttp=new XMLHttpRequest();\
                xmlhttp.open("POST", "''' + common['base_url'] + '''/datamanager/v1.0/file/%s",false);\
                xmlhttp.setRequestHeader("Content-Type", "application/json; charset=UTF-8");\
                xmlhttp.send(JSON.stringify({"path":"%s"}));\
                getResponse(xmlhttp);\
            }''',
           'copy_file':'''function copy_file(){\
                var xmlhttp=new XMLHttpRequest();\
                xmlhttp.open("PUT", "''' + common['base_url'] + '''/datamanager/v1.0/file%s", false);\
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
            'move_file':'''function move_file() {\
                var xmlhttp=new XMLHttpRequest();\
                xmlhttp.open("POST", "''' + common['base_url'] + '''/datamanager/v1.0/file%s", false);\
                xmlhttp.setRequestHeader("Content-Type", "application/json; charset=UTF-8");\
                xmlhttp.send(JSON.stringify({"path":"%s"}));\
                getResponse(xmlhttp);\
            }''',
            'generate_public_url':'''function generate_public_url() {\
                var xmlhttp=new XMLHttpRequest();\
                xmlhttp.open("HEAD", "''' + common['base_url'] + '''/datamanager/file%s?signedURL=true",false);\
                xmlhttp.send();\
                getResponse(xmlhttp);\
                public_url = xmlhttp.getResponseHeader("external-link");\
                alert("Public URL: " + public_url);\
            }''',
            'download_file':'''function download_file() {\
                var xmlhttp=new XMLHttpRequest();\
                xmlhttp.open("GET", "%s", false);\
                xmlhttp.send();\
                getResponse(xmlhttp);\
            }''',
            'import_url':'''function import_url() {\
                var xmlhttp=new XMLHttpRequest();\
                xmlhttp.open("HEAD", "''' + common['base_url'] + '''/datamanager/file%s?signedURL=true",false);\
                xmlhttp.send();\
                getResponse(xmlhttp);\
                public_url = xmlhttp.getResponseHeader("external-link");\
                if (xmlhttp.status < 300 && xmlhttp.status > 199) {\
                    xmlhttp.open("PUT", "''' + common['base_url'] + '''/datamanager/v1.0/file%s", false);\
                    xmlhttp.setRequestHeader("x-gs-fetch-source", public_url);\
                    xmlhttp.send(JSON.stringify({"isDirectory":"true"}));\
                    getResponse(xmlhttp);\
                }\
            }''',
            'launch_with_file':'''function launch_with_file() {\
                var xmlhttp=new XMLHttpRequest();\
                xmlhttp.open("POST", "''' + common['base_url'] + '''/identityServer/usermanagement/utility/usageLog", false);\
                xmlhttp.setRequestHeader("Content-Type", "application/json");\
                var fileURL = "''' + common['base_url'] + '''/datamanager/file%s";\
                var encodedURL = encodeURIComponent(fileURL);\
                xmlhttp.send(JSON.stringify({"module":"GSUI","function":"LAUNCH","username":"%s","entity":"Galaxy : " + fileURL}));\
                getResponse(xmlhttp);\
                var xmlhttp1=new XMLHttpRequest();\
                xmlhttp1.open("GET","''' + common['base_url'] + '''/atm/v1.0/webtool/Galaxy/launchurl?URL=" + encodedURL,false);\
                xmlhttp1.setRequestHeader("Content-Type", "application/json");\
                xmlhttp1.send();\
                getResponse(xmlhttp1);\
            }''',
            'upload_file':'''function upload_file() {\
                var getrequest=new XMLHttpRequest();\
                getrequest.open("GET","''' + common['base_url'] + '''/datamanager/v1.0/uploadinfo"+escape("%s"),false);\
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
                    putrequest.send("%s");\
                    getResponse(putrequest);\
                }\
            }''',
            'get_doi':'''function get_doi() {\
                var xmlhttp=new XMLHttpRequest();\
                xmlhttp.open("POST", "''' + common['base_url'] + '''/datamanager/v1.0/tags/mintdoi/%s", false);\
                xmlhttp.setRequestHeader("Content-Type", "application/json");\
                xmlhttp.send(JSON.stringify({"Title":"%s", "TitleType":"%s", "Email":"%s", "Creator":"%s", "Contributors":"%s", "Description":"%s"}));\
                getResponse(xmlhttp);\
            }''' ,
            'get_tags':'''function get_tags() {\
                var xmlhttp=new XMLHttpRequest();\
                xmlhttp.open("Get", "''' + common["base_url"] + '''/datamanager/v1.0/tags/", false);\
                xmlhttp.send();\
                if (xmlhttp.status < 300 && xmlhttp.status > 199) {\
                    var str = xmlhttp.response;\
                    var response_obj = JSON.parse(str);\
                    var len = Object.keys(response_obj).length;\
                    alert(len);\
                }\
            }'''}

