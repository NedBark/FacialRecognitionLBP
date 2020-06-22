def checkUser(id, usr):
    f = open ("UserLogin.txt", "r")
    usrs = {}
    for line in f:
            line = line.strip("\n")
            split = line.split(".")
            usrs[int(split[0])]=split[1]
    if (usr in usrs.values()):
            return True
    else:
            return False
    f.close()

def main(id, usr):
    f = open ("UserLogin.txt", "r")
    usrs = {}
    for line in f:
            line = line.strip("\n")
            split = line.split(".")
            usrs[int(split[0])]=split[1]
    if (usr in usrs.values()):
            print("ASD")
    f.close()
    
    f=open("UserLogin.txt", "r")
    
    usrs = {}
    for line in f:
        line = line.strip("\n")
        split = line.split(".")
        
        
        #print(split[0])
        #print(split[1])
        
        usrs[int(split[0])]=split[1]
        
    #f.write("\n User id is " + id + " and name is " + usr +"\n")
    print (usrs)
    f.close()
    
if __name__ == "__main__":
    main()