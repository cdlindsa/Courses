# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# define MAX_STRING_LENGTH 41


int encode(char read[]){
    char bases[MAX_STRING_LENGTH];
    int boolean = 0;
    int count=1;
    int i;
    int j = 0;
    for (i=0; i <strlen(read)-2; i++){
        if (boolean == 1){
        printf("Error: String could not be encoded");
        exit(5);
        }
        if (read[i]!=' ' && read[i]!='A' && read[i]!='C' && read[i]!='T' && read[i]!='G'){
            boolean = 1;
        } else {
            if (count==1 || i==0){
                bases[j] = read[i];
                j++;
                count++;
            } else  if (read[i] == read[i-1]){
                count++;
            } else {
                bases[j] = '0'+ count;
                count = 1;
                j++;
            }
        }
    }
    bases[j] = '\0';
    printf("%s", bases);
    exit(0);
}



int decode(char read[]){
    char bases[MAX_STRING_LENGTH];
    int boolean = 0;
    int i;
    int j = 0;
    for (i=0; i <strlen(read); i++){
        if (boolean == 1){
        printf("Error: String could not be decoded");
        exit(5);
        }
        
        if (read[i]==' '){

        } else if (i%2==0){
            if (read[i]!='A' && read[i]!='C' && read[i]!='T' && read[i]!='G'){
            boolean = 1;
            } else {
                bases[j] = read[i];
                j++;
            }
        } else if (read[i]!='1' && read[i]!='2' && read[i]!='3' && read[i]!='4' && read[i]!='5' 
        && read[i]!='6' && read[i]!='7' && read[i]!='8' && read[i]!='9'){
            boolean = 1;
        } else {
            const int count = read[i]-'0';
            for (int k=0; k <count-1; k++){
                bases[j] = read[i-1];
                j++;
            }
        }
    }
    bases[j] = '\0';
    printf("%s", bases);
    exit(0);
}
/*NEED TO DO CHECK FOR BAD INPUT AGAIN*/

int main(int argc, char* argv[]) {
    
    if (argc== 1){
        printf("Error: No input file specified!");
        exit(1);
    } else if (argc!= 3){
        printf("Invalid Usage, expected: RLE {filename} [e | d]");
        exit(4);
    }

    FILE *infile;
    infile = fopen(argv[1], "r");
    char read[MAX_STRING_LENGTH];
    if (infile==NULL){
        printf("Read error: file not found or cannot be read");
        exit(2);
    } else {
        fgets(read, MAX_STRING_LENGTH, infile);
        int i;
        int boolean = 0;
        for (i=0; i <strlen(read)-2; i++){
            if (i!=0){
                if (read[i-1]==' ' && read[i]!=' ' ){
                    boolean = 1;
                }
            }
            if (read[i]!=' ' && read[i]!='A' && read[i]!='C' && read[i]!='T' && read[i]!='G' 
            && read[i]!='1' && read[i]!='2' && read[i]!='3' && read[i]!='4' && read[i]!='5' 
            && read[i]!='6' && read[i]!='7' && read[i]!='8' && read[i]!='9'){
                boolean = 1;
                }
        }
        if (boolean == 1){
            printf("Error: Invalid Format");
            exit(3);
        }
    }
    if (strcmp(argv[2], "e")== 0){
        encode(read);
    } else if (strcmp(argv[2], "d")== 0){
        decode(read);
    } else {
        printf("Invalid Usage, expected: RLE {filename} [e | d]");
        exit(4);
    }
    fclose(infile);
    return 0;
}