def map_generate_status(list_status):
    generated_status = ['WAIT_FOR_REVIEW', 'RESUME_REVIEWED', 'REJECTED', 'ACCEPTED']
    for status in list_status:
        if status == 'PHONE':
            generated_status.append('WAIT_FOR_PHONE')
            generated_status.append('PHONE_REVIEWED')
        elif status == 'ONLINE_TEST':
            generated_status.append('WAIT_FOR_ONLINE_TEST')
            generated_status.append('ONLINE_TEST_REVIEWED')
        elif status == 'SUBMISSION':
            generated_status.append('WAIT_FOR_SUBMISSION')
            generated_status.append('SUBMISSION_REVIEWED')
        elif status == 'ONSITE':
            generated_status.append('WAIT_FOR_ONSITE_TEST')
            generated_status.append('ONSITE_TEST_REVIEWED')
    return generated_status


def map_status(status, side):
    student_side = {
        'WAIT_FOR_REVIEW': 'menunggu review',
        'RESUME_REVIEWED': 'resume direview',
        'WAIT_FOR_PHONE': 'lolos ke phone interview',
        'PHONE_REVIEWED': 'phone interview direview',
        'WAIT_FOR_ONLINE_TEST': 'lolos ke online test',
        'ONLINE_TEST_REVIEWED': 'online test direview',
        'WAIT_FOR_SUBMISSION': 'lolos ke task submission',
        'SUBMISSION_REVIEWED': 'task submission direview',
        'WAIT_FOR_ONSITE_TEST': 'lolos ke on-site interview',
        'ONSITE_TEST_REVIEWED': 'on-site interview direview',
        'REJECTED': 'ditolak',
        'ACCEPTED': 'diterima'
    }

    company_side = {
        'WAIT_FOR_REVIEW': 'pilih status',
        'RESUME_REVIEWED': 'pilih status',
        'WAIT_FOR_PHONE': 'phone interview',
        'PHONE_REVIEWED': 'review phone interview',
        'WAIT_FOR_ONLINE_TEST': 'online test',
        'ONLINE_TEST_REVIEWED': 'review online test',
        'WAIT_FOR_SUBMISSION': 'task submission',
        'SUBMISSION_REVIEWED': 'review task submission',
        'WAIT_FOR_ONSITE_TEST': 'on-site interview',
        'ONSITE_TEST_REVIEWED': 'review on-site interview',
        'REJECTED': 'tolak',
        'ACCEPTED': 'terima'
    }

    if side == 'student':
        return student_side[status]
    elif side == 'company':
        return company_side[status]
