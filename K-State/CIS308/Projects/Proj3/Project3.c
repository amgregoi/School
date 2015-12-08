* Assignment: Project3: Postfix to Infix      *
***********************************************
* Takes a postfix expression, puts it into a  *
* tree and does an inorder traversal to prints*
* the expression in infix notation            *
***********************************************/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <malloc.h>
#include <ctype.h>
struct tree {
        char* root;
        struct tree* left;
        struct tree* right;
};

struct node {
        struct tree* data;
        struct node* next;
};

//your final expression tree
struct tree* expression;

//the top node on your stack
struct node* stack;


void push(struct tree* temp) {
        struct node* newnode = malloc(sizeof(struct node));
        newnode->data = temp;
        //checks if stack is null
        if(stack == NULL)
                stack = newnode;
        else{
                struct node* temp = stack;
                stack = newnode;
                stack->next = temp;
        }
}//end push

struct tree* pop(void) {
        struct node* temp = stack;//set temp = top of stack
        stack = temp->next;//set new top of stack
        return temp->data;//return poped tree
}//end pop

void inorder(struct tree* exp) {
        if(exp == NULL) return;

        //places "("
        if(!(exp->left == NULL)) printf("(");

        //traversal
        inorder(exp->left);
        printf("%s", exp->root);
        inorder(exp->right);

        //places ")"
        if(!(exp->right == NULL)) printf(")");
}//end inorder



void freeTree(struct tree* exp) {
        if(exp == NULL)
                return;
        freeTree(exp->left);
        freeTree(exp->right);
        free(exp);
}//end freeTree

int main() {
        char* expr = malloc(sizeof(char));
        int i;
        char c;
        char* tokExp=malloc(sizeof(char));
        //gets postfix expression
        printf("Enter postfix expression: ");
        for(i=0;((c=getchar())!= '\n'); i++)
                *(expr+i)=c;

        //tokenizes expressions
        tokExp=strtok(expr," ");
        while(tokExp !=NULL)
        {
                //checks if its a number
                if(isdigit(*tokExp)){
                        struct tree* newtree = malloc(sizeof(struct tree));
                        newtree->root = tokExp;//places number in root of newtree
                        newtree->left = NULL; newtree->right = NULL;//sets left/right to null
                        push(newtree);//push newtree on stack
                }
                else{//for operators
                        struct tree* newtree = malloc(sizeof(struct tree));
                        newtree->right = pop();//pops first value off stack (right tree)
                        newtree->left = pop();//pops next value off stack (left tree)
                        newtree-> root = tokExp;//places operator in root
                        push(newtree); // pushes tree  onto stack
                }

                tokExp = strtok(NULL, " "); // cycle through tokens
        }
        expression = pop();//pops entire expression tree
        printf("In infix: ");
        inorder(expression);//inorder traverse through the tree
        fflush(stdout);
        free(expression);//frees memory of tree
        printf("\n"); // new line for neatness
        exit(0); //exit
}//end main
