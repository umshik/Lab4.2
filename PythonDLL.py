class Node:
    def __init__(self,inf,ch):
        self.inf=inf
        self.ch=ch
        self.prev=None
        self.next=None

class List:
    def __init__(self):
        self.head=None
        self.length=0

    def GetNodeByIndex(self,index):
        if self.head is None or index < 1 or index > self.length:
            return None
        current=self.head
        for _ in range(1,index):
            current=current.next
        return current

    def Insert(self,par,n,x,ch):
        if self.head is None and par!=0:
            return 1
        if self.head is None and par==0:
            newnode=Node(x,ch)
            newnode.next=newnode
            newnode.prev=newnode
            self.head=newnode
            self.length=1
            return 0
        if par!=0 and (n>self.length or n<1):
            return 1
        if par!=0:
            current=self.GetNodeByIndex(n)
        else:
            current=self.head.prev
        if par==0:
            target=self.head
            last=self.head.prev
        else:
            if par==-1:
                target=current
                last=current.prev
            else:
                target=current.next
                last=current
        newnode=Node(x,ch)
        newnode.prev=last
        newnode.next=target
        last.next=newnode
        target.prev=newnode
        if par==-1 and n==1:
            self.head=newnode
        self.length+=1
        return 0

    def Remove(self,par,n):
        if self.head is None: return 1
        if par==-1:
            if n==1: n=self.length
            else: n-=1
        elif par==1:
            if n==self.length: n=1
            else: n+=1
        if n>self.length or n<1: return 1
        if self.length==1 and n==1:
            self.head=None
            self.length=0
            return 0
        current=self.GetNodeByIndex(n)
        last=current.prev
        next=current.next
        last.next=next
        next.prev=last
        if current==self.head: self.head=next
        self.length-=1
        return 0

    def Clear(self):
        # Проходим по всем узлам и удаляем ссылки
        if self.head is None:
            self.length = 0
            return

        current = self.head.next
        while current != self.head:
            next_node = current.next
            # убиваем ссылки
            current.prev = None
            current.next = None
            current = next_node

        # убиваем голову
        self.head.prev = None
        self.head.next = None
        self.head = None
        self.length = 0

    def GetLength(self):
        return self.length

    def FindByInf(self,x):
        indices=[]
        if self.head is None: return indices
        current=self.head
        for i in range(1, self.length+1):
            if current.inf==x:
                indices.append(i)
            current=current.next
        return indices

    def FindByChar(self,ch):
        indices=[]
        if self.head is None: return indices
        current=self.head
        for i in range(1, self.length+1):
            if current.ch==ord(ch):
                indices.append(i)
            current=current.next
        return indices

    def GetInf(self,index):
        node=self.GetNodeByIndex(index+1)
        if node is None: return 0
        return node.inf

    def GetChar(self,index):
        node=self.GetNodeByIndex(index+1)
        if node is None: return 0
        return node.ch

    def GetNext(self,index):
        node=self.GetNodeByIndex(index+1)
        if node is None: return 0
        target=node.next
        node=self.head
        for i in range(1,self.length+1):
            if node==target: return i-1
            node=node.next
        return 0

    def GetPrev(self,index):
        node = self.GetNodeByIndex(index + 1)
        if node is None: return 0
        target = node.prev
        node = self.head
        for i in range(1, self.length + 1):
            if node == target: return i - 1
            node = node.next
        return 0

    def FreeArray(self, ptr):
        pass