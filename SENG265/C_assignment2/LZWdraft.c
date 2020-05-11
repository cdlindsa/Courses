#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TRUE 1
#define FALSE 0

#define DICTSIZE 4096                     /* allow 4096 entries in the dict  */
#define ENTRYSIZE 32

unsigned char dict[DICTSIZE][ENTRYSIZE];  /* of 30 chars max; the first byte */
                                          /* is string length; index 0xFFF   */
                                          /* will be reserved for padding    */
                                          /* the last byte (if necessary)    */

// These are provided below
int read12(FILE *infil);
int write12(FILE *outfil, int int12);
void strip_lzw_ext(char *fname);
void flush12(FILE *outfil);

// Determines if str is in dictionary
int is_in(char ch_str[]){
   temp[0] = strlen(ch_str);
   for (i=0; i<ENTRYSIZE-1; i++){
      temp[i+1] = ch_str[i];
   }
   for (j=0; j<DICTSIZE; j++){
         if (strcmp(dict[j],temp)==0){
            return 0;
         }
      }
   return 1;
}

// Adds char to str, compares dict input to str if not equal, removes the last char of string and returns, else returns str with add
int add_and_compare(int index, char ch_str[], char ch){
   int j; 
   if (strlen(ch_str)<ENTRYSIZE){
      ch_str[strlen(ch_str)]=ch;
   }
   for (j=0; j<strlen(ch_str); j++){
      if (dict[index][j+1] != ch_str[j]){
         ch_str[strlen(ch_str)-1] = 0;
         return 0;
      }
   }
   
   return 1;
}

// Finds the latest index in str and returns it
int find_index(char ch_str[]){
   int index = -1;
   char temp[ENTRYSIZE]="";
   int i;
   int j;
   temp[0] = strlen(ch_str);
   for (i=0; i<ENTRYSIZE-1; i++){
      temp[i+1] = ch_str[i];
   }
   // printf("find_index temp: \n");
   // for (i=0; i<ENTRYSIZE; i++){
   //    if (i==0){
   //       printf("%d ", temp[i]);   
   //    } else {
   //    printf("%c ", temp[i]);
   //    }   
   // }
   // printf("\n");
   for (i=0; i<strlen(ch_str); i++){
      for (j=0; j<DICTSIZE; j++){
         if (strcmp(dict[j],temp)==0){
            index = j;
         }
      }
      temp[strlen(temp)-1] = 0;
   }
   // printf("find_index index: %d\n", index);
   return index;
}

// Adds str to dict 
void add_dict(int next, char ch_str[], char ch){
   int i;
   int k;
   if (strlen(ch_str)<ENTRYSIZE){
      ch_str[strlen(ch_str)]=ch;
   }
   dict[next][0] = strlen(ch_str);
   for (i=0; i<ENTRYSIZE; i++){
      dict[next][i+1] = ch_str[i];
   }
}


void encode(FILE *in, FILE *out) {
   int next = 256;
   int temp;
   int boolean;
   char ch = getc(in);
   char ch_str[ENTRYSIZE] = "";
   int i;
   int k; //delete later
//initialization of dictionary
   for (i=0; i<next; i++){
      dict[i][0] = 1;
      dict[i][1] = i;
   }
//reading file, output, and entries into dictionary
   while (ch != EOF){
//check if str+ch is in dict. yes = add char to str, no = output and add str to dict
      // printf("begin while strlen = %d, ch_str: ", strlen(ch_str));
      // for(k=0;k<strlen(ch_str);k++){
      //    printf("%c ", ch_str[k]);
      // }
      // printf("\n");
      boolean = 0;
      for (i=0; i<DICTSIZE; i++){
         if (add_and_compare(i, ch_str, ch)==1){
            temp = i;
            // printf("compare loop temp: %d, strlen: %d, ch_str: \n", temp, strlen(ch_str));
            // for(k=0;k<strlen(ch_str);k++){
            //    printf("%c\n", ch_str[k]);
            // }
            boolean = 1;
         }
      }
      // printf("boolean: %d\n", boolean); 
      if (boolean != 1){ 
         // printf("index: %d\n", find_index(ch_str)); 
         // printf("write12 strlen = %d, ch_str: ", strlen(ch_str));
         // for(k=0;k<strlen(ch_str);k++){
         //    printf("%c ", ch_str[k]);
         // }
         // printf("\n");  
         // printf("\n");   
         write12(out, find_index(ch_str));     
         if (next<DICTSIZE-1){
            add_dict(next, ch_str, ch);
            next++;
         }
         memset(ch_str, 0, ENTRYSIZE);
         ch_str[0]=ch;
      }
      ch = getc(in);
   }
   flush12(out);
   //print dictionary
   // for (i=256; i<276; i++){
   //    printf("dict i: %d, ch_str length: %d, char: \n", i, dict[i][0]);
   //    for (k=0; k<strlen(dict[i]); k++){
   //       if (k==0){
   //          printf("%d", dict[i][k]);
   //       } else {
   //          printf("%c", dict[i][k]);
   //       }
   //    }
   //    printf("\n");
   // }
   exit(0);
}

/*****************************************************************************/
/* decode() performs the Lempel Ziv Welch decompression from the algorithm   */
/* in the assignment specification.                                          */
void decode(FILE *in, FILE *out) {
/*1. Start with a standard initial dictionary of 4096 entries (the first 256 are standard ASCII, the rest
are empty).
2. Read a code k from the encoded file
3. Output dict[ k ]
4. Set w to dict[ k ]
5. As long as there are more codes to read in the input file
a. read a code k
b. if k is in the dictionary
output dict[ k ]
add w + first character of dict[ k ] to the dict
else
add w + first char of w to the dict and output it
c. Set w to dict[ k ]*/
   printf("in decode");
   int next = 256;
   int temp;
   int boolean;
   char ch = getc(in);
   char ch_str[ENTRYSIZE] = "";
   int i;
   int k; //delete later
//initialization of dictionary
   for (i=0; i<next; i++){
      dict[i][0] = 1;
      dict[i][1] = i;
   }
//reading file, output, and entries into dictionary
   while (ch != EOF){
//check if str+ch is in dict. yes = add char to str, no = output and add str to dict
      printf("strlen = %d, ch_str: ", strlen(ch_str));
      for(k=0;k<strlen(ch_str);k++){
         printf("%d ", ch_str[k]);
      }
      printf("\n");
      boolean = 0;
      for (i=0; i<DICTSIZE; i++){
         if (add_and_compare(i, ch_str, ch)==1){
            temp = i;
            printf("temp: %d\n", temp);
            // printf("compare loop temp: %d, strlen: %d, ch_str: \n", temp, strlen(ch_str));
            // for(k=0;k<strlen(ch_str);k++){
            //    printf("%c\n", ch_str[k]);
            // }
            boolean = 1;
         }
      }
      printf("boolean: %d\n", boolean);
      if (boolean != 1){
         temp = next;
         if (next<DICTSIZE-1){
            add_dict(next, ch_str, ch);
            next++;
         }
         printf("before memset: \n");
         for(k=0;k<strlen(ch_str);k++){
            printf("%c ", ch_str[k]);
         }
         printf("\n");
         memset(ch_str, 0, ENTRYSIZE);
         ch_str[0]=ch;
         for(k=0;k<strlen(ch_str);k++){
            printf("after memset: %c\n", ch_str[k]);
         }
         // for(k=0;k<strlen(ch_str);k++){
         //    printf("ch_str: %c, temp: %d\n", ch_str[k], temp);
         // }
      }
      write12(out, temp);
      // printf("temp: %d, ch_str: ", temp);
      // for(k=0;k<strlen(ch_str);k++){
      //    printf("%c ", ch_str[k]);
      // }
      // printf("\n");
      ch = getc(in);
   }
   flush12(out);
   //print dictionary
   // for (i=256; i<276; i++){
   //    printf("dict i: %d, ch_str length: %d, char: \n", i, dict[i][0]);
   //    for (k=0; k<strlen(dict[i]); k++){
   //       if (k==0){
   //          printf("%d", dict[i][k]);
   //       } else {
   //          printf("%c", dict[i][k]);
   //       }
   //    }
   //    printf("\n");
   // }
   exit(0);
}


int main(int argc, char *argv[]) {
   /*checks for correct number of command line arguments*/
   if (argc== 1){
      printf("Error: No input file specified!");
      exit(1); 
   } else if (argc!= 3){
      printf("Invalid Usage, expected: LZW {input_file} [e | d]");
      exit(4);
   }
   
   /*opens input and output files + checks*/
   FILE *in;
   in = fopen(argv[1], "r");

   if (in==NULL){
      printf("Read error: file not found or cannot be read");
      exit(2);
   } 
   
   FILE *out;
   out = fopen(strcat(argv[1], ".LZW"), "wt");
   
   /*encode or decode + checks*/
   if (strcmp(argv[2], "e")== 0){
      encode(in, out);
   } else if (strcmp(argv[2], "d")== 0){
      decode(in, out);
   } else {
      printf("Invalid Usage, expected: RLE {filename} [e | d]");
      exit(4);
   }
   fclose(in);
   fclose(out);
   return 0;
}


/*****************************************************************************/
/* read12() handles the complexities of reading 12 bit numbers from a file.  */
/* It is the simple counterpart of write12(). Like write12(), read12() uses  */
/* static variables. The function reads two 12 bit numbers at a time, but    */
/* only returns one of them. It stores the second in a static variable to be */
/* returned the next time read12() is called.                                */
int read12(FILE *infil)
{
 static int number1 = -1, number2 = -1;
 unsigned char hi8, lo4hi4, lo8;
 int retval;

 if(number2 != -1)                        /* there is a stored number from   */
    {                                     /* last call to read12() so just   */
     retval = number2;                    /* return the number without doing */
     number2 = -1;                        /* any reading                     */
    }
 else                                     /* if there is no number stored    */
    {
     if(fread(&hi8, 1, 1, infil) != 1)    /* read three bytes (2 12 bit nums)*/
        return(-1);
     if(fread(&lo4hi4, 1, 1, infil) != 1)
        return(-1);
     if(fread(&lo8, 1, 1, infil) != 1)
        return(-1);

     number1 = hi8 * 0x10;                /* move hi8 4 bits left            */
     number1 = number1 + (lo4hi4 / 0x10); /* add hi 4 bits of middle byte    */

     number2 = (lo4hi4 % 0x10) * 0x0100;  /* move lo 4 bits of middle byte   */
                                          /* 8 bits to the left              */
     number2 = number2 + lo8;             /* add lo byte                     */

     retval = number1;
    }

 return(retval);
}

/*****************************************************************************/
/* write12() handles the complexities of writing 12 bit numbers to file so I */
/* don't have to mess up the LZW algorithm. It uses "static" variables. In a */
/* C function, if a variable is declared static, it remembers its value from */
/* one call to the next. You could use global variables to do the same thing */
/* but it wouldn't be quite as clean. Here's how the function works: it has  */
/* two static integers: number1 and number2 which are set to -1 if they do   */
/* not contain a number waiting to be written. When the function is called   */
/* with an integer to write, if there are no numbers already waiting to be   */
/* written, it simply stores the number in number1 and returns. If there is  */
/* a number waiting to be written, the function writes out the number that   */
/* is waiting and the new number as two 12 bit numbers (3 bytes total).      */
int write12(FILE *outfil, int int12)
{
 static int number1 = -1, number2 = -1;
 unsigned char hi8, lo4hi4, lo8;
 unsigned long bignum;

 if(number1 == -1)                         /* no numbers waiting             */
    {
     number1 = int12;                      /* save the number for next time  */
     return(0);                            /* actually wrote 0 bytes         */
    }

 if(int12 == -1)                           /* flush the last number and put  */
    number2 = 0x0FFF;                      /* padding at end                 */
 else
    number2 = int12;

 bignum = number1 * 0x1000;                /* move number1 12 bits left      */
 bignum = bignum + number2;                /* put number2 in lower 12 bits   */

 hi8 = (unsigned char) (bignum / 0x10000);                     /* bits 16-23 */
 lo4hi4 = (unsigned char) ((bignum % 0x10000) / 0x0100);       /* bits  8-15 */
 lo8 = (unsigned char) (bignum % 0x0100);                      /* bits  0-7  */

 fwrite(&hi8, 1, 1, outfil);               /* write the bytes one at a time  */
 fwrite(&lo4hi4, 1, 1, outfil);
 fwrite(&lo8, 1, 1, outfil);

 number1 = -1;                             /* no bytes waiting any more      */
 number2 = -1;

 return(3);                                /* wrote 3 bytes                  */
}

/** Write out the remaining partial codes */
void flush12(FILE *outfil)
{
 write12(outfil, -1);                      /* -1 tells write12() to write    */
}                                          /* the number in waiting          */

/** Remove the ".LZW" extension from a filename */
void strip_lzw_ext(char *fname)
{
    char *end = fname + strlen(fname);

    while (end > fname && *end != '.' && *end != '\\' && *end != '/') {
        --end;
    }
    if ((end > fname && *end == '.') &&
        (*(end - 1) != '\\' && *(end - 1) != '/')) {
        *end = '\0';
    }
}








