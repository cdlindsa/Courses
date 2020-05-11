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
   int i;
   char temp[ENTRYSIZE]="";
   temp[0] = strlen(ch_str);
   for (i=0; i<ENTRYSIZE-1; i++){
      temp[i+1] = ch_str[i];
   }
   for (i=0; i<DICTSIZE; i++){
      if (strcmp(dict[i],temp)==0){
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
   for (i=0; i<strlen(ch_str); i++){
      for (j=0; j<DICTSIZE; j++){
         if (strcmp(dict[j],temp)==0){
            index = j;
         }
      }
      temp[strlen(temp)-1] = 0;
   }
   return index;
}

// Adds str to dict (encode)
void add_dict_encode(int next, char ch_str[], char ch){
   int i;
   int k;
   if (strlen(ch_str)<ENTRYSIZE-1){
      ch_str[strlen(ch_str)]=ch;
   }
   dict[next][0] = strlen(ch_str);
   for (i=0; i<ENTRYSIZE-1; i++){
      dict[next][i+1] = ch_str[i];
   }
}

// Add str + first character of dict[k](ch) to the dict
void add_dict_decode(int next, int ch_str[], int ch, int length){
   int i;
   dict[next][0] = 1+length;
   for (i=0; i<ENTRYSIZE; i++){
      dict[next][i+1] = ch_str[i];
   }
   dict[next][1+length] = ch;
}


/*****************************************************************************/
/* encode() performs the Lempel Ziv Welch compression from the algorithm in  */
/* the assignment specification.                                             */
void encode(FILE *in, FILE *out) {
   int next = 256;
   int ch = getc(in);
   unsigned char ch_str[ENTRYSIZE] = "";
   int i;
//initialization of dictionary
   for (i=0; i<next; i++){
      dict[i][0] = 1;
      dict[i][1] = i;
   }
//reading file, output, and entries into dictionary
   while (ch != EOF){
//check if str+ch is in dict. yes = add char to str, no = output and add str to dict    
      if (strlen(ch_str)<ENTRYSIZE-1){
         ch_str[strlen(ch_str)]=ch;
      } else {
         memset(ch_str, 0, ENTRYSIZE);
         ch_str[0]=ch;
      }
      if (is_in(ch_str)!=0){
         ch_str[strlen(ch_str)-1]=0;
         write12(out, find_index(ch_str));
         if (next<DICTSIZE){
            add_dict_encode(next, ch_str, ch);
            next++;
         }
         memset(ch_str, 0, ENTRYSIZE);
         ch_str[0]=ch;
      }
      ch = getc(in); 
   }
   write12(out, find_index(ch_str));
   flush12(out);
   exit(0);
}

/*****************************************************************************/
/* decode() performs the Lempel Ziv Welch decompression from the algorithm   */
/* in the assignment specification.                                          */
void decode(FILE *in, FILE *out) {
   int next = 256;
   int ch = read12(in);
   unsigned int ch_str[ENTRYSIZE];
   int i;
   int length;
//initialization of dictionary
   for (i=0; i<next; i++){
		dict[i][0] = 1;      
      dict[i][1] = i;
   }
//reading file, output, and entries into dictionary
	for (i=0; i<dict[ch][0]; i++){   
    	fputc(dict[ch][i+1], out);
      ch_str[i] = dict[ch][i+1];
   }
   length = dict[ch][0];
   while (ch != 0x0FFF){
      ch = read12(in);
//ensure not adding padding to dict
      if (ch==0x0FFF){
         exit(0);
      }     
      if (dict[ch][0]!=0){  
	      for (i=0; i<dict[ch][0]; i++){   
    	      fputc(dict[ch][i+1], out);
         }
 // add str + first character of dict[ch] to the dict
         if (next<DICTSIZE && length<ENTRYSIZE){
         	add_dict_decode(next, ch_str, dict[ch][1], length);
         	next++;
         }
      } else {
// add str + first char of str to the dict and output it
         if (next<DICTSIZE && length<ENTRYSIZE){         
         	add_dict_decode(next, ch_str, ch_str[0], length);
	         for (i=0; i<dict[next][0]; i++){   
    	         fputc(dict[next][i+1], out);
            }      
         	next++;
         } else {  
   			for (i=0; i<length; i++){   
    				fputc(ch_str[i], out);
   			}
            fputc(ch_str[0],out);     	        
         }
      }
// sets str to dict[ch]
      memset(ch_str, 0, ENTRYSIZE);
		for (i=0; i<dict[ch][0]; i++){   
      	ch_str[i] = dict[ch][i+1];
      }
      length = dict[ch][0];
   }
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
   /*encode or decode + checks*/
   if (strcmp(argv[2], "e")== 0){
      out = fopen(strcat(argv[1], ".LZW"), "w");
      encode(in, out);
   } else if (strcmp(argv[2], "d")== 0){
      strip_lzw_ext(argv[1]);
      out = fopen(argv[1], "w");
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








