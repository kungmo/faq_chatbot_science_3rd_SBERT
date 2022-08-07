import socket

class multipleaccess:
    def __init__(self, srv_port, listen_num):
        self.port = srv_port
        self.listen = listen_num
        self.mySock = None
        # multipleaccess 객체의 생성자입니다. 인자로 사용된 생성할 소켓 서버의 포트번호(srv_port)와 동시에 연결을 수락할 클라이언트 수(listen_num)
        # 를 멤버 변수로 지정합니다. (처읍 배우는 딥러닝 챗봇 276, 조경래 지음,한빛미디어)쪽

    # sock 생성
    def create_sock(self):
        self.mySock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mySock.bind(("0.0.0.0", int(self.port)))
        self.mySock.listen(int(self.listen))
        return self.mySock
        # multipleaccess의 소켓을 생성하는 메소드입니다. 파이썬에서 지원하는 저수준 네트워킹 인터페이스 API를 사용하기 쉽도록 만든 래퍼함수입니다.
        # TCP/IP 소켓을 생성한 뒤 지정한 서버 포트(self.port)로 지정한 연결 수(self.listen)만큼 클라이언트 연결을 수락하도록 합니다.

    # client 대기
    def ready_for_client(self):
        return self.mySock.accept()
        # 챗봇 클라이언트 연결을 대기하고 있다가 연결을 수락하는 메소드입니다. 서버 소켓은 우리가 설정한 주소와 통신에 바인드되어 클라이언트 연결을
        # 주시(listening socket)하고 있어야 합니다. 클라이언트가 연결을 요청하는 즉시 accept() 함수는 클라이언트와 통신할 수 있는
        # 클라이언트용 소켓 객체를 반환합니다. 이때 반환값은 (conn, address) 튜플입니다.
        # ready_for_client 메소드의 반환값은 다음과 같습니다.
        # conn: 연결된 챗봇 클라이언트와 데이터를 송수신할 수 있는 클라이언트 소켓입니다.
        # address: 연결된 챗봇 클라이언트 소켓의 바인드된 주소입니다.

    # sock 반환
    def get_sock(self):
        return self.mySock
        # 현재 생성된 서버 소켓을 반환합니다.