import numpy as np


class Omok:
    def __init__(self):
        self.BOARD_SIZE = 19
        self.board = np.zeros((self.BOARD_SIZE,self.BOARD_SIZE),dtype=int)
        self.Player = 1
        self.Color = 'black'
        self.x = 0
        self.y = 0
    # global x
    # global y

    def Draw(self):
        for i in range(self.BOARD_SIZE): #사이즈표시 
            for j in range(self.BOARD_SIZE): #사이즈표시
                print(self.board[i][j], end=' ')
            print('\n')

    def Put_omok(self, player, x, y):
        # global x
        # global y
        # print(self.Color ," , Enter coordinate : ")
        while True:
            self.x = x
            if self.x < 0 or self.x > self.BOARD_SIZE - 1: #사이즈표시
                print("out of range! Try again")
                continue
            self.y = y
            if self.y < 0 or self.y > self.BOARD_SIZE - 1: #사이즈표시
                print("out of range! Try again")
                continue
            if self.board[self.y][self.x] != 0 :
                print("already existed. \n Enter coordinate : ")
            elif self.board[self.y][self.x] == 0:
                self.board[self.y][self.x] = player
                break 

    def Playerchange(self):
        if self.Player == 1 :
            self.Player = 2
            self.Color = 'white'
        elif self.Player == 2 :
            self.Player = 1
            self.Color = 'black'

    def Trace(self):
        # global x
        # global y
        col=[]
        row=[]
        digonal_1=[]
        digonal_2=[]
        # 가로 세로 대각선(2개) 방향에 대해 선택된 좌표를 기준으로 9가지 성분 추출하기

        for i in range(9): #y축 위에서 아래로
            if (self.y-4+i) > self.BOARD_SIZE - 1 or (self.y-4+i) < 0:
                continue
            col.append(self.board[self.y-4+i][self.x])

        
        for i in range(9): #x축 왼쪽에서 오른쪽
            if (self.x-4+i) > self.BOARD_SIZE - 1 or (self.x-4+i) < 0:
                continue
            row.append(self.board[self.y][self.x-4+i])

        
        for i in range(9): # 왼쪽위에서 오른쪽아래로
            if (self.y-4+i) > self.BOARD_SIZE - 1 or (self.y-4+i) < 0:
                continue
            if (self.x-4+i) > self.BOARD_SIZE - 1 or (self.x-4+i) < 0:
                continue
            digonal_1.append(self.board[self.y-4+i][self.x-4+i])

        for i in range(9): # 왼쪽아래에서 오른쪽위로
            if (self.y+4-i) > self.BOARD_SIZE - 1 or (self.y+4-i) < 0:
                continue
            if (self.x-4+i) > self.BOARD_SIZE - 1 or (self.x-4+i) < 0:
                continue
            digonal_2.append(self.board[self.y+4-i][self.x-4+i])
            
        return col,row,digonal_1,digonal_2

        
        #카운트 = 5 일때 오목5

        
    def Rule_Omok(self, col, row, digonal_1, digonal_2):
        #세로
        # count = 1
        checklists = [col, row, digonal_1, digonal_2]
        count_list=[]
        for checklist in checklists:
            cnt = 1
            for i in range(1,len(checklist)):
                if checklist[i] == checklist[i-1]:
                    cnt += 1
                elif checklist[i] != checklist[i-1]:
                    count_list.append(cnt)
                    cnt = 1
                if i == len(checklist)-1:
                    count_list.append(cnt)
            if max(count_list) == 5 :
                return 'exit'

        # #가로
        # cnt = 1
        # for i in range(1,len(row)):
        #     if row[i] == row[i-1]:
        #         cnt += 1
        #     elif row[i] != row[i-1]:
        #         count_list.append(cnt)
        #         cnt = 1
        #     if i == len(row)-1:
        #         count_list.append(cnt)
        # if max(count_list) == 5 :
        #     return 'exit'

        # #대각_1
        # cnt = 1
        # for i in range(1,len(digonal_1)):
        #     if digonal_1[i] == digonal_1[i-1]:
        #         cnt += 1
        #     elif digonal_1[i] != digonal_1[i-1]:
        #         count_list.append(cnt)
        #         cnt = 1
        #     if i == len(digonal_1)-1:
        #         count_list.append(cnt)
        # if max(count_list) == 5 :
        #     return 'exit'

        # #대각_2
        # cnt = 1
        # for i in range(1,len(digonal_2)):
        #     if digonal_2[i] == digonal_2[i-1]:
        #         cnt += 1
        #     elif digonal_2[i] != digonal_2[i-1]:
        #         count_list.append(cnt)
        #         cnt = 1
        #     if i == len(digonal_2)-1:
        #         count_list.append(cnt)
        # if max(count_list) == 5 :
        #     return 'exit'

    def samsam(self, sam):
        sam_count = 0
        start_point = 0
        end_point = 0
        space_count = 0
        stone_count = 0
        #변수선언
        for i in range(1,len(sam)-1):
        
            if sam[i] == self.Player : # 검은색이면 시작점
                
                for j in range(i+1,i+4): # 시작점 오른쪽으로 3칸 탐색 / start 랑 end 좌표구하기
                    start_point = i
                    if j >= len(sam) :  #사이즈표시 #세칸탐색 불가능
                        break
                    elif sam[j] == 0: # 공백일때
                        space_count +=1
                        if space_count == 2:
                            break
                    elif sam[j] == self.Player: #같은색일떄
                        end_point = j
                        stone_count += 1
                        if stone_count == 3:
                            break
                    elif sam[j] == self.Player: # 다른색일때
                        break
                    if(stone_count == 2 and space_count == 1):
                        if (start_point - 1) > -1 and (end_point + 1) < len(sam) : #사이즈표시
                            if sam[start_point -1] == 0 and sam[end_point + 1] == 0 :
                                sam_count +=1
                                return sam_count
        return sam_count

# omok = Omok()
# while True:
#     omok.Draw()
#     omok.Put_omok()
#     col,row,digonal_1,digonal_2 = omok.Trace() # 4개축의 성분을 저장
#     sam_col = omok.samsam(col)       # 삼을 판단하는 함수에 각 성분 집어넣어서 sam_XXX 라는 int 형으로 반환 1 이면 sam 0이면 nothing
#     sam_row = omok.samsam(row)
#     sam_digonal_1 = omok.samsam(digonal_1)
#     sam_digonal_2 = omok.samsam(digonal_2)
#     sum_of_sam = sam_col + sam_row + sam_digonal_1 + sam_digonal_2 # 삼의 갯수 합한다 
#     # print("col ", col , sam_col)
#     # print("row ", row), sam_row
#     # print("digonal_1 ", digonal_1, sam_digonal_1)
#     # print("digonal_2 ", digonal_2, sam_digonal_2)
#     # print("sum of sam ", sum_of_sam)
#     if omok.Rule_Omok(col,row,digonal_1,digonal_2) == 'exit':
#         print(omok.Color , " Win!")
#         break
#     elif sum_of_sam > 1:
#         print("SamSam !! Try Again ! ")
#         omok.board[omok.y][omok.x] = 0
#         continue
#     # omok.Playerchange()
        