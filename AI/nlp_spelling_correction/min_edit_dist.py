

def min_edit_dist(x, y):
    dist = [[0]*(len(y)+1) for i in range(len(x)+1)]
    for i in range(1,len(x)+1):
        for j in range(1,len(y)+1):
            dist[i][0]=i
            dist[0][j] = j
            delt=0
            if x[i-1] != y[j-1]:
                delt=1

            dist[i][j] = min(dist[i-1][j-1]+delt, dist[i-1][j]+1, dist[i][j-1]+1)
       
    return dist

def backtrace(dist,x,y,two_letter):
    i = len(x)
    j = len(y)
    s = dist[i][j]
    while s != 0:
        
        delete = dist[i-1][j]
        insertion = dist[i][j-1]
        substitution = dist[i-1][j-1]
            
        
        min_value = min(delete, insertion, substitution)

        if substitution == min_value:
            i -= 1
            j -= 1
            if s != substitution:
                print(x[i]+"->"+y[j]+" subs")
        elif delete == min_value:
            i -= 1
            if s != delete:
                #print(x[i]+" del")
                asd = x[i]
                if asd not in two_letter:
                    two_letter[asd]=1
                else:
                    two_letter[asd] +=1



        elif insertion == min_value:
            if s != insertion:
                print(y[i]+" in")
            j -= 1
            
        s = dist[i][j]

        print(two_letter)

        





if __name__ == "__main__":
    x = "watch"
    y = "wakh"

    dist = min_edit_dist(x, y)

    for i in dist:
        print(i)
    
    two_letter = dict()
    backtrace(dist, x, y,two_letter)


                
