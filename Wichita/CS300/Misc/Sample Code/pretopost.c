#include <stdio.h>
#include <string.h>

/* return the length of the first operand in this string */
int length_of_first_operand (char *str)
{
  int len1, len2;
  if ((str[0] == '+') || (str[0] == '-') || (str[0] == '*') || (str[0] == '/'))
  {  /* General Case */

     /* return the length of operand #1 */
     len1 = length_of_first_operand(str + 1);

     /* return the length of operand #2 */
     len2 = length_of_first_operand(str + 1 + len1);
  }
  else /* Base case */
  {
      len1 = len2 = 0;
  }
  return (len1 + len2 + 1);
}

void pre_to_post (char *str, char *postfix_str)
{
  char oper;
  int len1, len2;
  char temp[100], postfix1[100], postfix2[100];

  if ((str[0] == '+') || (str[0] == '-') || (str[0] == '*') || (str[0] == '/'))
  {
    oper = str[0];
    len1 = length_of_first_operand(str+1);   /* length of operand #1 */
    strncpy (temp, str+1, len1);  
    temp[len1] = '\0';   /* operand #1 */

    pre_to_post(temp, postfix1);   /* PF1 */

      /* Length of Operand 2 */
    len2 = length_of_first_operand(str + 1 + len1);
       /* Operand #2 */
    strncpy (temp, str + 1 + len1, len2);

    pre_to_post(temp, postfix2);  /* PF2*/

    /* postfix 1 then postfix 2 then oper */
    strcpy(postfix_str, postfix1);
    strcat(postfix_str, postfix2);
    strcat(postfix_str, &oper);

    postfix_str[len1+len2+1] = '\0';
  }
  else
  /* Base Case: Only Operand */
  {
    postfix_str[0] = str[0];
    postfix_str[1] = '\0';
  }
  return;
}


int main ()
{
  char prefix_str[100] = "+-+-A*BCD/EFG";
  //char prefix_str[100] = "-+*ABC/EF";
  //char prefix_str[100] = "*AB";
  // A * B * C + D    
  // Prefix : +**ABCD

  char postfix_str[100] = "";

  printf("\n Length of %s = %d\n", prefix_str, length_of_first_operand(prefix_str));

  pre_to_post(prefix_str, postfix_str);
  printf("\n Postfix notation of %s = %s\n", prefix_str, postfix_str);
  return 0;
}

