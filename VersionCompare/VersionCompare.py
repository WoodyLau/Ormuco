import re

#Assumes the versions are alphanumeric and periods
#Assumes any letters will be after numerals in each period subsection
def versionComparer(version1, version2):
    version1=version1.strip()
    version2=version2.strip()
    
    if version1[0]=='v':
        version1=version1[1:]
    if version2[0]=='v':
        version2=version2[1:]
        
    grouped_version1=version1.split('.')
    grouped_version2=version2.split('.')
    counter=0
    while counter<min(len(grouped_version1),len(grouped_version2)):
        comparison = compare(grouped_version1[counter],grouped_version2[counter])
        if comparison==0:
            pass
        else:
            return comparison
        counter+=1
    difference = len(grouped_version1)-len(grouped_version2)
    return min(max(difference,-1),1)

def compare(subversion1, subversion2):
    first=re.findall('\d+|\D+',subversion1)
    second=re.findall('\d+|\D+',subversion2)
    if len(first)==1:
        num1=first[0]
        alpha1=0
    elif len(first)==2:
        num1,alpha1=first
    else:
        raise ValueError("Version 1 is misconfigured at "+subversion1+". It should be a number, optionally followed by letters, or just letters.")
    if len(second)==1:
        num2=second[0]
        alpha2=0
    elif len(second)==2:
        num2,alpha2=second
    else:
        raise ValueError("Version 2 is misconfigured at "+subversion2+". It should be a number, optionally followed by letters, or just letters.")
    if int(num1)>int(num2):
        return 1
    if int(num1)<int(num2):
        return -1
    if alpha1>alpha2:
        return 1
    if alpha1<alpha2:
        return -1
    return 0
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--first', nargs='+', type=string)
    parser.add_argument('--second', nargs='+', type=string)
    args = parser.parse_args()
    if args.first is None or len(args.first)!=1:
        if args.first is not None:
            print("Too many strings in first, please retype")
        version1 = input("Please input the first version:")
    else:
        version1 = args.first[0]
    if args.second is None or len(args.second)!=1:
        if args.second is not None:
            print("Too many strings in second, please retype")
        version2 = input("Please input the second version:")
    else:
        version2 = args.second[0]
    print(versionComparer(version1,version2))
    
if __name__ == "__main__":
    main()
