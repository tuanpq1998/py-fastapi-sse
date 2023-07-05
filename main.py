import logging

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
import asyncio
import uvicorn
import time

logger = logging.getLogger()

MESSAGE_STREAM_DELAY = 0.1  # second
MESSAGE_STREAM_RETRY_TIMEOUT = 15000  # milisecond
app = FastAPI()

# add CORS so our web page can connect to our api
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

COUNTER = 0
MESSAGE= "Bộ luật Lao động hiện tại có tổng cộng 220 điều, được thông qua bởi Quốc hội nước Cộng hòa xã hội chủ nghĩa Việt Nam khóa XIV, kỳ họp thứ 8 vào ngày 20 tháng 11 năm 2019. Điều 220 của Bộ luật Lao động quy định rằng hợp đồng lao động, thỏa ước lao động tập thể, các thỏa thuận hợp pháp đã giao kết có nội dung không trái hoặc bảo đảm cho người lao động có quyền và điều kiện thuận lợi hơn so với quy định của Bộ luật này được tiếp tục thực hiện, trừ trường hợp các bên có thỏa thuận về việc sửa đổi, bổ sung để phù hợp và để áp dụng quy định của Bộ luật này. Ngoài ra, Bộ luật Lao động còn quy định về quyền và nghĩa vụ của người lao động, bao gồm việc thực hiện hợp đồng lao động, thỏa ước lao động tập thể và thỏa thuận hợp pháp khác, chấp hành kỷ luật lao động, nội quy lao động, tuân theo sự quản lý, điều hành, giám sát của người sử dụng lao động, thực hiện quy định của pháp luật về lao động, việc làm, giáo dục nghề nghiệp, bảo hiểm xã hội, bảo hiểm y tế, bảo hiểm thất nghiệp và an toàn, vệ sinh lao động [[1]](#1) [[2]](#2) [[3]](#3) [[4]](#4).\n## CITATION:\n[1] [Điều 4. Chính sách của Nhà nước về lao động Bộ luật Bộ Luật lao động 45/2019/QH14](https://vbpl.vn/TW/Pages/vbpq-toanvan.aspx?ItemID=139264)\n\n[2] [Điều 5. Quyền và nghĩa vụ của người lao động Bộ luật Bộ Luật lao động 45/2019/QH14](https://vbpl.vn/TW/Pages/vbpq-toanvan.aspx?ItemID=139264)\n\n[3] [Điều 86. Mức đóng và phương thức đóng của người sử dụng lao động Luật Bảo hiểm xã hội 58/2014/QH13](https://vbpl.vn/TW/Pages/vbpq-toanvan.aspx?ItemID=46744)\n\n[4] [Điều 220. Hiệu lực thi hành Bộ luật Bộ Luật lao động 45/2019/QH14](https://vbpl.vn/TW/Pages/vbpq-toanvan.aspx?ItemID=139264)"
#MESSAGE= "## ANSWER:giám sát của người sử dụng lao động, thực hiện quy định của pháp luật về lao động, việc làm, giáo dục nghề nghiệp, bảo hiểm xã hội, bảo hiểm y tế, bảo hiểm thất nghiệp và an toàn, vệ sinh lao động [[1]](#1) [[2]](#2) [[3]](#3) [[4]](#4).\n## CITATION:\n[1] [Điều 4. Chính sách của Nhà nước về lao động Bộ luật Bộ Luật lao động 45/2019/QH14](https://vbpl.vn/TW/Pages/vbpq-toanvan.aspx?ItemID=139264)\n\n[2] [Điều 5. Quyền và nghĩa vụ của người lao động Bộ luật Bộ Luật lao động 45/2019/QH14](https://vbpl.vn/TW/Pages/vbpq-toanvan.aspx?ItemID=139264)\n\n[3] [Điều 86. Mức đóng và phương thức đóng của người sử dụng lao động Luật Bảo hiểm xã hội 58/2014/QH13](https://vbpl.vn/TW/Pages/vbpq-toanvan.aspx?ItemID=46744)\n\n[4] [Điều 220. Hiệu lực thi hành Bộ luật Bộ Luật lao động 45/2019/QH14](https://vbpl.vn/TW/Pages/vbpq-toanvan.aspx?ItemID=139264)\n## TITLE:blablabla"

def get_message(index):
    global COUNTER
    COUNTER += 1
    return COUNTER, index<=len(MESSAGE)-1

@app.get('/healthcheck', status_code=status.HTTP_200_OK)
def perform_healthcheck():
    '''
    Simple route for the GitHub Actions to healthcheck on.
    More info is available at:
    https://github.com/akhileshns/heroku-deploy#health-check
    It basically sends a GET request to the route & hopes to get a "200"
    response code. Failing to return a 200 response code just enables
    the GitHub Actions to rollback to the last version the project was
    found in a "working condition". It acts as a last line of defense in
    case something goes south.
    Additionally, it also returns a JSON response in the form of:
    {
      'healtcheck': 'Everything OK!'
    }
    '''
    return {'healthcheck': 'Everything OK!'}
    

@app.post("/api/v1/answering_with_context")
def answer (request : Request):
    return {
        "statusCode": 200,
        "message": "",
        "timestamp":  int(round(time.time() * 1000)),
        "AI_message": MESSAGE,
    }

@app.get("/api/v1/stream_sse")
async def message_stream(request: Request):
    async def event_generator():
        index = 0
        while True:    
            if await request.is_disconnected():
                logger.debug("Request disconnected")
                break

            # Checks for new messages and return them to client if any
            counter, exists = get_message(index)
            if exists:
                yield {
                    #"event": "new_message",
                    #"id": "message_id",
                    #"retry": MESSAGE_STREAM_RETRY_TIMEOUT,
                    "data": {
                        "statusCode": 200,
                        "message": "",
                        "timestamp":  int(round(time.time() * 1000)),
                        "AI_message": MESSAGE[index]
                    },
                }
                index+=1;
            else:
                yield {
                    #"event": "end_event",
                    #"id": "message_id",
                    #"retry": MESSAGE_STREAM_RETRY_TIMEOUT,
                    "data": {
                        "statusCode": 200,
                        "message": "",
                        "timestamp":  int(round(time.time() * 1000)),
                        "AI_message": "[DONE]",
                    },
                }
                break

            await asyncio.sleep(MESSAGE_STREAM_DELAY)

    return EventSourceResponse(event_generator())


if __name__ == "__main__":
   # uvicorn.run(app, host="127.0.0.1", port=8000)
    uvicorn.run(app, host="127.0.0.1", port=8000)