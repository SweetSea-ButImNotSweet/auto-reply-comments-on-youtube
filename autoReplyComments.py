# Nhớ xem hướng dẫn tạo app để lấy OAuth2 và API key tại đây:
# https://developers.google.com/youtube/v3/getting-started?hl=vi
# Hãy đảm bảo là bạn bật đèn xanh cho quyền comment gồm "list" và "insert"

# À và lý do là phải lấy cả OAuth2 và API là vì script này dùng cả 2 cái!

# Riêng OAuth2 nhớ lấy file json và đổi tên lại thành clientid.json
# Còn với API key thì dán vào file key.txt là xong

# CHÚ Ý CÀI ĐỦ NHỮNG THƯ VIỆN SAU!
import googleapiclient.discovery, googleapiclient.errors, google_auth_oauthlib.flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


from sys import exit
from urllib.parse import urlparse   # urlparser từ thư viện urllib.parse được nạp vào để tách ID từ link
from datetime import datetime
import os

# Đoạn này kiểm tra xem có thiếu clientid.json (chứa mã OAuth2) và key.txt (chứa API key) hay không?
if not os.path.exists("clientid.json") or not os.path.exists("key.txt"):
    if not os.path.exists("clientid.json"):
        print("Thiếu file clientid.json nơi chứa mã OAuth2 để chạy! Xin vui lòng kiểm tra lại!")
    if not os.path.exists("key.txt"):
        print("Thiếu file key.txt nơi chứa mã API của app để chạy!  Xin vui lòng kiểm tra lại!")
    exit()

# Đây là thông tin cần thiết để chạy app
with open("key.txt", 'r') as tokenfile:
    DEVELOPER_KEY = tokenfile.read()

SCOPES = [
    'https://www.googleapis.com/auth/youtube',           # Quản lý tài khoản Youtube
    'https://www.googleapis.com/auth/youtube.force-ssl', # Viết, xoá bình luận
    ]

creds = ''
videoDoneAmmount=0
errorsAmount=0
commentDoneAmount = 0
expectedCommentAmount = 0

#_________________________________________________________________
# File token.json sẽ chứa dữ liệu lưu lại token của người dùng, tránh phải đăng nhập đi đăng nhập lại nhiều lần gây phiền toái
# Nếu file không tồn tại thì yêu cầu đăng nhập, còn không thì refresh lại

if os.path.exists('token.json'):
    try:
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    except:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file("clientid.json", SCOPES)
        creds = flow.run_local_server(port=0)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request()) # Lấy lại mã token mới để sử dụng
        except:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file("clientid.json", SCOPES)
            creds = flow.run_local_server(port=0)
    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file("clientid.json", SCOPES)

    try:
        creds = flow.run_local_server(port=0)
    except:
        print("Có lỗi khi đăng nhập hay sao ấy... Thử lại đi!")

with open('token.json', 'w') as token:
    token.write(creds.to_json())


# Build app youtube trong python
youtube2 = googleapiclient.discovery.build("youtube", "v3", credentials=creds)
youtube1 = googleapiclient.discovery.build("youtube", "v3", developerKey = DEVELOPER_KEY)
# youtube2 dùng OAuth2, youtube1 dùng API key đời cũ


video_id=''
maxResults = input("\nSố tin nhắn muốn gửi mỗi video (mặc định 20): ")
if maxResults == '':
    maxResults == 20

# Tách ID từ link video
def get_video_id(link):
    link = urlparse(link)
    link2 = link.netloc
    if link2 in ["www.youtube.com", "youtube.com", "m.youtube.com", "youtu.be"]:
        if link.path == '/watch':
            a = link.query
            a = a.split('v=')
            return a[1]
        else:
            a = link.path
            a = a.split("/")
            if a[1] == "embed" or a[1] == "short":
                return a[2]
            else:
                return a[1]
    else:
        return ''



def get_comment(video_id, searchTerms='', maxResults = maxResults):

    #if video_id=='':
        #return ''

    if searchTerms != '':
        request = youtube1.commentThreads().list(
            part="snippet",
            maxResults = maxResults,
            videoId = video_id,
            searchTerms = searchTerms,
#             order="orderUnspecified"
            )
    else:
        request = youtube1.commentThreads().list(
            part="snippet",
            maxResults = maxResults,
            videoId = video_id,
#             order="orderUnspecified"
            )

    response = request.execute()
    return response

# Nhập tin nhắn
def ask_input_messages():
    textmode = True
    a = ''
    c = 0
    print("\nNhập tin nhắn muốn gửi tự động, hãy nhập chúng ở dưới!\n")
    print("Nhập tin nhắn bạn muốn gửi tại đây. Nhấn Enter 3 lần liên tiếp để kết thúc\n\n")
    while textmode:
        b = input()
        if a !='':
            a = '\n'.join([a, b])
        else:
            a = b
        if b == '':
            c = c+1
            if c>0 and c<3:
                print("Nếu bấm Enter thêm {0} lần nữa thì sẽ thoát chế độ nhắn tin nhắn".format(3-c))
            if 3-c == 0:
                textmode = False
                a = a.split('\n')
                for i in range(0, 3):
                    a.pop()
                a = '\n'.join(a)
        else: c = 0
    return a


class OutOfQuota(RuntimeError):
    def __init__(self):
        print("Xin lỗi nhưng API và OAuth của bạn đã quá lượt\nXin vui lòng chờ tới 14h ngày mai để tiếp tục!")


# Nhập link Youtube
link = input("Mời bạn nhập link Youtube: ")

# Lấy ID video
video_id = get_video_id(link)

# Đoạn này nếu link hợp lệ thì tiếp, không thì dừng

if video_id:

    expectedCommentAmount = expectedCommentAmount + int(maxResults)
    videoDoneAmmount = videoDoneAmmount + 1

    # Nhập từ khoá cần tìm
    keyword = input("\n\nTừ khoá cần tìm kiếm \nBình luận nào có từ khoá sẽ tự tìm\nLưu ý: Không phân biệt chữ hoa/thường\nTừ khoá cần tìm: ").lower()

    messages = ask_input_messages()



    # Lấy comment
    try:
        allcomments = get_comment(video_id, keyword)
    except googleapiclient.errors.HttpError as e:

        # print('Error response status code : {0}, reason : {1}'.format(e.resp.status, e.error_details))

        if e.resp.status == "403" or e.resp.status == 403:
            for ee in e.error_details[0]:
                if e.error_details[0][ee] == '''commentsDisabled''':
                    print("Video đã bị tắt tính năng bình luận!")
                else:
                    print("Thiếu quyền truy cập")
        if e.resp.status == "404" or e.resp.status == 404:
            for ee in e.error_details[0]:
                if e.error_details[0][ee] == '''videoNotFound''':
                    print("Video bạn yêu cầu không tìm thấy! Đúng là link Youtube nhưng có khi bạn chép sai?")
                else:
                    print("Lỗi không xác định!")

        exit()

    # Tách lấy comment và nextPageToken
    try:
        nextpagetoken = allcomments["nextPageToken"]
    except:
        nextpagetoken = 'NotFound'

    for item in allcomments["items"]:
        item_info = item["snippet"]

        topLevelComment = item_info["topLevelComment"]
        comment_info = topLevelComment["snippet"]

        comment_text = comment_info["textOriginal"]
        author_comment = comment_info["authorDisplayName"]

        # Bắt đầu comment spam chữ nè
        try:
            request2 = youtube2.comments().insert(
                part="snippet",
                body={
                  "snippet": {
                        "parentId": item['id'],
                        "textOriginal": messages
                  }
                }
            )
            response = request2.execute()


        except googleapiclient.errors.HttpError as e:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            errorsAmount = errorsAmount + 1

            # Lỗi hết token

            with open("log.txt", 'a', encoding="utf-8") as l:
                l.write("Có lỗi xảy ra lúc {0}\n\n".format(current_time))
                for ee in e.error_details[0]:
                    l.write(e.error_details[0][ee])
                    l.write('\n')
                    if e.error_details[0][ee] == '''quotaExceeded''':
                        raise OutOfQuota
                    elif e.error_details[0][ee] =='''processingFailure''':
                        print("Lỗi từ phía máy chủ \n")
                        if errorsAmount == 3:
                            print("Chương trình sẽ thoát vì đã xảy ra quá 3 lỗi trong lúc chạy!")
                            exit()

                l.write("\n\n")
                l.write("Đã xảy ra lỗi ở bình luận {:>3}/{:>3} bình luận. . .\n".format(commentDoneAmount, expectedCommentAmount))
                l.write("Trong lúc chạy, có {:>3} lỗi khi cố trả lời\n".format(errorsAmount))
                l.write("Bình luận đã cố trả lời cuối cùng: {}\n".format(comment_text))
                l.write("Người viết bình luận             : {}\n".format(author_comment))
                l.write("\n\n\n")

        finally:
            commentDoneAmount = commentDoneAmount + 1
            print("Đã chạy tới bình luận {:>3}/{:>3} bình luận. . .".format(commentDoneAmount, expectedCommentAmount))
            print("Trong lúc chạy, có {:>3} lỗi khi cố trả lời".format(errorsAmount))
            print("Bình luận đã cố trả lời cuối cùng: {}".format(comment_text))
            print("Người viết bình luận             : {}".format(author_comment))
            print("\n")



else:
    print("\nXin lỗi, link bạn nhập không hợp lệ!\n")

print("Đã gửi {:>3}/{:>3} bình luận trong tất cả {:>3} video, có {:>3} lỗi trong lúc xử lý".format(commentDoneAmount, expectedCommentAmount, videoDoneAmmount, errorsAmount))