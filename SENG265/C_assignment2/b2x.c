#include <stdio.h>

main(int argc, char *argv[])
{
   int i = 0;  // index variable for loops

	FILE *infil;
   unsigned char bytefromfil;

   unsigned int first, last;

   unsigned char code0 = 0, code1 = 1, code2 = 2, code3 = 3, code4 = 4,
      code5 = 5, code6 = 6, code7 = 7, code8 = 8, code9 = 9, codeA = 10,
      codeB = 11, codeC = 12, codeD = 13, codeE = 14, codeF = 15;

   unsigned char message[16];

	message[code0] = 48;
   message[code1] = 49;
   message[code2] = 50;
   message[code3] = 51;
   message[code4] = 52;
	message[code5] = 53;
	message[code6] = 54;
	message[code7] = 55;
	message[code8] = 56;
	message[code9] = 57;
	message[codeA] = 65;
	message[codeB] = 66;
	message[codeC] = 67;
	message[codeD] = 68;
	message[codeE] = 69;
   message[codeF] = 70;

   if (argc == 1) {
      printf ("No file specified! \n");
      exit(1);
   }

   infil = fopen(argv[1], "rb");

   if (infil == 0) {
      printf ("Unable to open file %s \n", argv[1]);
      exit(2);
   }

   while (fread(&bytefromfil, 1, 1, infil)==1){

      if (bytefromfil < 16){
      	first = 0;
         last = bytefromfil;
      }
      else {
  	   	first = (bytefromfil / 16);
   	   last  = (bytefromfil % 16);
      }
      putchar(message[first]);
      putchar(message[last]);

      i = i+2;
      if (i>68){
      	printf ("\n");
         i = 0;
      }

   }


	printf ("\n");

   fclose(infil);

   exit(0);
}



