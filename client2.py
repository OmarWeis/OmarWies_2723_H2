# TCP ECHO Client
# create a simple tcp client
# create a tcp socket object
# import socket
import sys
import socket

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # client socket
# cs.settimeout(10)
try:
    cs.connect(('127.0.0.1', 8888))  # connect to tcp server
    print('connected')
except socket.error as e:
    print(e)
    sys.exit(1)
try:

    print('now you are in the exam ')
    filename = input(cs.recv(1024).decode())   # input file name of exam
    cs.send(filename.encode())  # send file name to server

    name = input(cs.recv(1024).decode())  # input the name of client
    cs.send(name.encode())  # send the name to server
    welcome = cs.recv(1024).decode() # receive welcome

    print("welcome", welcome)  # to welcome you

    questions = "begin"
    while questions:
        questions = cs.recv(1024).decode()  # receive questions

        print(questions)

        answer = input().strip().lower()

        cs.send(answer.encode())  # send the answers
        # print('sending...')  # is an addition

    print('the exam end')
    print('your score is :', cs.recv(1024).decode())
except socket.error as e:
    print('exe2', e)


print('the exam is finish')
