import argparse
import types

def isOverlap(x1,x2,x3,x4):
    #Guarantee x1 is smaller than x2 and x3 is smaller than x4
    if x1>x2:
        x1,x2=x2,x1
    if x3>x4:
        x3,x4=x4,x3
    
    #Guarantee that x1 is to the left/at the same point as x3
    if x1>x3:
        x1,x2,x3,x4=x3,x4,x1,x2
    
    if x2<=x3:
        return False
    else:
        return True
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--first', nargs='+', type=float)
    parser.add_argument('--second', nargs='+', type=float)
    args = parser.parse_args()
    if args.first is None or len(args.first)!=2:
        if args.first is not None:
            print("Not enough/too many points for first line, please retype")
        x1,x2=0,0
        while not isinstance(x1, float):
            x1 = input("Please insert the first point of the first line:")
            try:
                x1=float(x1)
            except ValueError:
                print("You did not enter a proper float")
                pass
        while not isinstance(x2, float):
            x2 = input("Please insert the second point of the first line:")
            try:
                x2=float(x2)
            except ValueError:
                print("You did not enter a proper float")
    else:
        x1,x2=args.first[0],args.first[1]
    if args.second is None or len(args.second)!=2:
        if args.second is not None:
            print("Not enough/too many points for second line, please retype")
        x3,x4=0,0
        while not isinstance(x3, float):
            x3 = input("Please insert the first point of the second line:")
            try:
                x3=float(x3)
            except ValueError:
                print("You did not enter a proper float")
        while not isinstance(x4, float):
            x4 = input("Please insert the second point of the second line:")
            try:
                x4=float(x4)
            except ValueError:
                print("You did not enter a proper float")
    else:
        x3,x4=args.second[0],args.second[1]
    print(isOverlap(x1,x2,x3,x4))
    
if __name__ == "__main__":
    main()
