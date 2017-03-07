# from minio.error import ResponseError
#
# from zeus import minio_client
#
#
# def upload(files, company_id, file_name):
#     if 'file' not in files:
#         return 'No file part', 422
#
#     file = files['file']
#     if file.filename == '':
#         return 'No selected file', 422
#
#     # quick hack to get file size
#     file.seek(0, 2)
#     file_size = file.tell()
#     file.seek(0, 0)
#
#     file_path = '{0}/{1}/.{2}'.format(company_id, file_name, file.content_type)
#     try:
#         minio_client.put_object('companies', file_path, file, file_size, content_type=file.content_type)
#     except ResponseError:
#         return 'failed'
#
#     return 'companies/{0}'.format(file_path)
