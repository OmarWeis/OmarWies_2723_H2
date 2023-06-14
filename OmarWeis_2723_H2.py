import socket
import threading
import csv
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reuse port number

ss.bind(('0.0.0.0', 8888))
ss.listen(5)

def ask_questions(questions, csock):
    score = 0
    for question in questions:

        csock.send(question[0].encode())  # send questions

        answer = csock.recv(1024).decode()
        if answer == question[1].strip().lower():
            score += 1
    return score


def save_result(name, score):
    with open('results{0}.csv'.format(name), 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, score])


def read_questions(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        questions = list(reader)
        return questions


def handle_client(i,csock,cadd):
    print('Accepted new client :',i,cadd)
    while True:
        try:
            csock.send("Enter the filename of the quiz questions:".encode())  # send file name

            filename = csock.recv(1024).decode()  # receive file name

            csock.send("Enter your name: ".encode())  # request the name

            name = csock.recv(1024).decode()  # receive the name
            csock.send(name.encode())  # send welcome
            questions = read_questions(filename)

            score = ask_questions(questions, csock)
            print('hh')
            csock.send("score {0}".format(score).encode())

            print("Your score is:", score)

            save_result(name, score)

        except socket.error as err_msg:
            print(err_msg)

        finally:
            print('finished serving current client')

            csock.close()


i = 0
while True:
    print('Tcp MultiThreading client server is waiting for new clients...')
    csock, cadd = ss.accept()

    client = threading.Thread(target=handle_client, args=(i, csock, cadd), daemon=True)
    client.start()
    client.join()
    i += 1

