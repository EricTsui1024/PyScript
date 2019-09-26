import os
import os.path
import requests
import json
import shutil
from requests_toolbelt.multipart.encoder import MultipartEncoder


def get_access_token(server_url):
    url = '/sitdealerdesktop/api/Token'

    user_password = {
        'username': 'xxxx',
        'password': 'xx!',
        'Scope': 'xxx',
        'grant_type': 'password'
    }

    r = requests.post(server_url + url, data=user_password)
    text = json.loads(r.text)
    return text['access_token']


def create_quotation(server_url, headers, root_dir):
    url = '/sitdealerdesktop/api/dealerApplication/SaveQuotation'
    form_data = {}
    quotation_data_dir = root_dir + 'quotation'

    for parent, dirnames, filenames in os.walk(quotation_data_dir):
        for filename in filenames:
            form_data_file = os.path.join(parent, filename)
            # print(form_data_file)
            form_data.clear()

            with open(form_data_file, mode='r', encoding='UTF-8') as f:
                for line in f:
                    s = line.split(':')
                    key = s[0].strip()
                    value = s[1].strip()
                    form_data[key] = value

            r = requests.post(
                server_url + url, headers=headers, data=form_data)
            print('\n------ Create Quotation response ------\n' + r.text)


def save_application_and_genID(server_url, headers, root_dir):
    url = '/sitdealerdesktop/api/DealerApplication/GenerateApplicationNumber'
    form_data = {}
    application_data_dir = root_dir + 'application'
    tmp_data_dir = root_dir + 'tmp'

    # 每次运行前先清空 temp 目录
    if os.path.exists(tmp_data_dir):
        shutil.rmtree(tmp_data_dir, True)
    os.mkdir(tmp_data_dir)

    for parent, dirnames, filenames in os.walk(application_data_dir):
        for filename in filenames:
            form_data_file = os.path.join(parent, filename)
            tmp_data_file = tmp_data_dir + '/' + filename
            form_data.clear()
            borrower_name = ''
            fields_to_clear = 'ApplicationNumber|ApplicationID|' \
                              'Quotation[QuotationID]|CreationDate|' \
                              'LastModifiedDate|'

            with open(form_data_file, mode='r', encoding='UTF-8') as f:
                for line in f:
                    s = line.split(':')
                    key = s[0].strip()
                    value = s[1].strip()

                    if key in fields_to_clear:
                        value = ''
                    elif '[HistoryID]' in key or '[PropertyID]' in key:
                        value = '-1'
                    elif '[DealerCustomerID]' in key:
                        value = ''

                    if 'T00' in value and s[2] == '00':
                        value = value[0:10]

                    form_data[key] = value

            r = requests.post(
                server_url + url, headers=headers, data=form_data)

            if r.status_code == requests.codes.ok:
                try:
                    text = json.loads(r.text)
                    form_data['ApplicationNumber'] = text['data']['ApplicationNumber']
                    form_data['ApplicationID'] = text['data']['ApplicationID']
                    form_data['CreationDate'] = text['data']['CreationDate']
                    form_data['Quotation[QuotationID]'] = text['data']['Quotation']['QuotationID']
                    borrower_name = text['data']['Borrower']['CustomerName']

                    # 获取 DealerCustomerID
                    form_data['Borrower[DealerCustomerID]'] = text['data']['Borrower']['DealerCustomerID']
                    if text['data']['CoBorrower'] is not None:
                        form_data['CoBorrower[DealerCustomerID]'] = text['data']['CoBorrower']['DealerCustomerID']
                    if text['data']['Guarantors'] is not None:
                        for i, guarantor in enumerate(text['data']['Guarantors']):
                            form_data['Guarantors[' + str(i) + '][DealerCustomerID]'] = guarantor['DealerCustomerID']

                    # 获取 HistoryID
                    if text['data']['Borrower']['EmploymentHistories'] is not None:
                        for i, borrower in enumerate(text['data']['Borrower']['EmploymentHistories']):
                            form_data['Borrower[EmploymentHistories][' + str(i) + '][HistoryID]'] = borrower['HistoryID']

                    if text['data']['CoBorrower'] is not None and \
                       text['data']['CoBorrower']['EmploymentHistories'] is not None:
                        for i, coborrower in enumerate(text['data']['CoBorrower']['EmploymentHistories']):
                            form_data['CoBorrower[EmploymentHistories][' + str(i) + '][HistoryID]'] = coborrower['HistoryID']

                    if text['data']['Guarantors'] is not None:
                        for i, guarantor in enumerate(text['data']['Guarantors']):
                            for k, histories in enumerate(guarantor['EmploymentHistories']):
                                form_data['Guarantors[' +
                                          str(i) + '][EmploymentHistories][' +
                                          str(k) + '][HistoryID]'] = histories['HistoryID']

                    # 获取 PropertyID
                    if text['data']['Borrower']['PropertyHouses'] is not None:
                        for i, borrower in enumerate(text['data']['Borrower']['PropertyHouses']):
                            form_data['Borrower[PropertyHouses][' + str(i) + '][PropertyID]'] = borrower['PropertyID']
                    if text['data']['Borrower']['PropertyCars'] is not None:
                        for i, borrower in enumerate(text['data']['Borrower']['PropertyCars']):
                            form_data['Borrower[PropertyCars][' + str(i) + '][PropertyID]'] = borrower['PropertyID']
                    if text['data']['Borrower']['PropertyDeposits'] is not None:
                        for i, borrower in enumerate(text['data']['Borrower']['PropertyDeposits']):
                            form_data['Borrower[PropertyDeposits][' + str(i) + '][PropertyID]'] = borrower['PropertyID']
                    if text['data']['Borrower']['PropertyOthers'] is not None:
                        for i, borrower in enumerate(text['data']['Borrower']['PropertyOthers']):
                            form_data['Borrower[PropertyOthers][' + str(i) + '][PropertyID]'] = borrower['PropertyID']

                    if text['data']['CoBorrower'] is not None and \
                       text['data']['CoBorrower']['PropertyHouses'] is not None:
                        for i, coborrower in enumerate(text['data']['CoBorrower']['PropertyHouses']):
                            form_data['CoBorrower[PropertyHouses][' + str(i) + '][PropertyID]'] = coborrower['PropertyID']

                    if text['data']['CoBorrower'] is not None and \
                       text['data']['CoBorrower']['PropertyCars'] is not None:
                        for i, coborrower in enumerate(text['data']['CoBorrower']['PropertyCars']):
                            form_data['CoBorrower[PropertyCars][' + str(i) + '][PropertyID]'] = coborrower['PropertyID']

                    if text['data']['CoBorrower'] is not None and \
                       text['data']['CoBorrower']['PropertyDeposits'] is not None:
                        for i, coborrower in enumerate(text['data']['CoBorrower']['PropertyDeposits']):
                            form_data['CoBorrower[PropertyDeposits][' + str(i) + '][PropertyID]'] = coborrower['PropertyID']

                    if text['data']['CoBorrower'] is not None and \
                       text['data']['CoBorrower']['PropertyOthers'] is not None:
                        for i, coborrower in enumerate(text['data']['CoBorrower']['PropertyOthers']):
                            form_data['CoBorrower[PropertyOthers][' + str(i) + '][PropertyID]'] = coborrower['PropertyID']

                    if text['data']['Guarantors'] is not None:
                        for i, guarantor in enumerate(text['data']['Guarantors']):
                            if guarantor['PropertyHouses'] is not None:
                                for k, houses in enumerate(guarantor['PropertyHouses']):
                                    form_data['Guarantors[' + str(i) + '][PropertyHouses][' + str(k) + '][PropertyID]'] = houses['PropertyID']

                            if guarantor['PropertyCars'] is not None:
                                for k, cars in enumerate(guarantor['PropertyCars']):
                                    form_data['Guarantors[' + str(i) + '][PropertyCars][' + str(k) + '][PropertyID]'] = cars['PropertyID']

                            if guarantor['PropertyDeposits'] is not None:
                                for k, deposits in enumerate(guarantor['PropertyDeposits']):
                                    form_data['Guarantors[' + str(i) + '][PropertyDeposits][' + str(k) + '][PropertyID]'] = deposits['PropertyID']

                            if guarantor['PropertyOthers'] is not None:
                                for k, others in enumerate(guarantor['PropertyOthers']):
                                    form_data['Guarantors[' + str(i) + '][PropertyOthers][' + str(k) + '][PropertyID]'] = others['PropertyID']

                    file_object = open(tmp_data_file, mode='w', encoding='UTF-8')
                    file_object.write(str(form_data))
                except Exception as error:
                    print('borrower_name:' + borrower_name + ' Save and Generate Error:')
                    print(error)

            print('\n------ Save and Generate response ------\n' +
                  'borrower_name:' + borrower_name + '\n' + r.text)


def get_document_info(server_url, headers, companyId, applicationId):
    url = '/sitdealerdesktop/api/DealerApplication/GetDocumentInfo_New'

    form_data = {}
    form_data['companyId'] = companyId
    form_data['applicationId'] = applicationId
    form_data['btype'] = 1
    form_data['pagesize'] = 999
    form_data['pageindex'] = 1

    r = requests.get(server_url + url, headers=headers, params=form_data)

    return r.text


def save_letter_upload_document(server_url, headers, form_data):
    url = '/sitdealerdesktop/api/DealerApplication/SaveLetterUploadDocument'

    r = requests.post(server_url + url, headers=headers, data=form_data)

    return r.text


def upload_document(server_url, headers, root_dir):
    url = '/sitdealerdesktop/api/DealerApplication/UploadFile'
    tmp_data_dir = root_dir + 'tmp'
    upload_file_name = root_dir + 'upload_files/Global.jpg'

    form_data = {}

    for parent, dirnames, filenames in os.walk(tmp_data_dir):
        for filename in filenames:
            form_data_file = os.path.join(parent, filename)
            form_data.clear()
            companyId = 1

            with open(form_data_file, mode='r', encoding='UTF-8') as f:
                for line in f:
                    if line.strip() != '':
                        form_data = eval(line.strip())

            applicationId = form_data['ApplicationID']
            companyId = form_data['CompanyID']

            text = json.loads(
                get_document_info(server_url, headers, companyId,
                                  applicationId))
            doc_title = text['data']['TagList'][0]['name_cn']
            doc_code = text['data']['TagList'][0]['code']
            btype = text['data']['TagList'][0]['btype']

            multipart_data = MultipartEncoder(fields={
                'file': ('Global.jpg', open(upload_file_name, 'rb'),
                         'image/jpeg'),
                'companyId':
                str(companyId),
                'applicationId':
                str(applicationId),
                'docCode':
                doc_code,
                'btype':
                str(btype),
                'docTitle':
                doc_title
            })

            headers['Content-Type'] = multipart_data.content_type
            r = requests.post(
                server_url + url, data=multipart_data, headers=headers)
            print('\n------ Upload Document response ------\n' + r.text)

            if r.status_code == requests.codes.ok:
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                text = json.loads(
                    get_document_info(server_url, headers, companyId,
                                      applicationId))
                form_data.clear()
                code = ''
                key = ''
                fileID = text['data']['Page']['DocumentList'][0]['id']
                file_title = text['data']['Page']['DocumentList'][0]['title']
                tag_list = text['data']['TagList']
                for t in tag_list:
                    if t['name'] != 'Global' and t['name'] != 'Optional':
                        code = code + t['code'] + '_'
                key = str(fileID) + ',' + file_title + ',' + code[0:len(code) - 1] + '|'
                form_data['companyId'] = companyId
                form_data['key'] = key
                form_data['applicationId'] = applicationId
                form_data['comment'] = '这是自动上传的文件！'
                form_data['isConsent'] = 1

                print('\n------ Save Upload Document response ------\n')
                print(
                    save_letter_upload_document(server_url, headers,
                                                form_data))


def build_request_headers(access_token):
    authorization = 'bearer ' + access_token
    headers = {}
    headers['Authorization'] = authorization
    headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
    return headers


def check_letter_document_upload(server_url, applicationId, companyId):
    url = '/sitdealerdesktop/api/DealerApplication/CheckLetterDocumentUpload'

    form_params = {
        'applicationId': applicationId,
        'companyId': companyId,
        'btype': '1'
    }

    r = requests.get(server_url + url, headers=headers, params=form_params)

    if r.status_code == requests.codes.ok:
        return True
    else:
        return False


def submit_application(server_url, headers, root_dir):
    url = '/sitdealerdesktop/api/dealerApplication/SubmitApplication'
    tmp_data_dir = root_dir + 'tmp'
    form_data = {}
    borrower_name = ''

    for parent, dirnames, filenames in os.walk(tmp_data_dir):
        for filename in filenames:
            form_data_file = os.path.join(parent, filename)
            form_data.clear()
            companyId = 1

            with open(form_data_file, mode='r', encoding='UTF-8') as f:
                for line in f:
                    if line.strip() != '':
                        form_data = eval(line.strip())

            applicationId = form_data['ApplicationID']
            application_number = form_data['ApplicationNumber']
            companyId = form_data['CompanyID']
            borrower_name = form_data['Borrower[CustomerName]']

            if check_letter_document_upload(server_url, applicationId,
                                            companyId):
                r = requests.post(
                    server_url + url, headers=headers, data=form_data)
                print('\n------ Submit Application response ------'
                      '\nborrower_name: ' + borrower_name +
                      ' ApplicationNumber = ' + application_number)
                print(r.text)
            else:
                print('\n------ Submit Application response ------\n' +
                      'Submit fail: check_letter_document_upload Fail: ' +
                      application_number + 'borrower_name:' + borrower_name)


if __name__ == "__main__":

    server_url = 'xxxxxxxxxxxxxxxxx'
    root_dir = os.getcwd() + '/test_cases/'
    root_dir = root_dir.replace('\\', '/')

    root_dir = 'D:/py/test_cases/'

    access_token = get_access_token(server_url)
    headers = build_request_headers(access_token)
    # create_quotation(server_url, headers, root_dir)
    save_application_and_genID(server_url, headers, root_dir)
    upload_document(server_url, headers, root_dir)
    submit_application(server_url, headers, root_dir)
