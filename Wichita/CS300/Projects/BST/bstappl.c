
#include "bstadt.h"



void inorder_Traversal(NODE* ptr);
void menu();


int compare_appl (void *arg1, void *arg2)
{
    int *ptr1, *ptr2;
    ptr1 = (int *) arg1;
    ptr2 = (int *) arg2;
    if (*ptr1 > *ptr2)
        return 1;
    else if(*ptr1 < *ptr2)
        return-1; 

    return 0;
}

int main()
{
    int *x;
    int option = 0;
    BST_TREE* tree = BST_Create (compare_appl);
  
    while(true)
    {
        x = (int *) malloc (sizeof(int));
        printf("Enter Number to Insert into Binary Tree(-1 to exit): ");
        scanf("%d", x);
        
        if(*x == -1){
            break;
        }
        else if(*x < 0){
            printf("Cannot insert Negative numbers\n");
        }
        else{
            BST_Insert(tree, x);
        }
    }


    while(option < 5){
        menu();
        printf("\nEnter option: ");
        scanf("%d", &option);
        
        switch (option) {
            case 1:
                breadth_Traversal(tree->root);
                break;
            case 2:
                printf("Enter Number you wish to search for in Binary Tree: ");
                scanf("%d", x);
                BST_Retrieve  (tree, x);
                break;
            case 3:
                printf("Enter Number to Delete from Binary Tree: ");
                scanf("%d", x);
                BST_Delete (tree, x);
                break;
            case 4:
                x = (int *) malloc (sizeof(int));
                printf("Enter Number to Insert into Binary Tree: ");
                scanf("%d", x);
                bool success = BST_Insert(tree, x);
                // added print statement here because it would have made
                // unneccessay output while building the tree
                if(success) printf("\tInserted %d into the tree\n", *x);
                else printf("\tFailed to insert %d into the tree\n", *x);
                break;
            case 5:
                printf("Exiting program\n");
                break;
            default:
                option = 0;
                break;
        }
    }
    
    BST_Destroy(tree);
    exit(0);
}
  
void menu()
  {
      printf("\n");
      printf("Insert Corresponding Number to Option\n");
      printf("Breadth First Traversal: 1\n");
      printf("Search for Integer: 	 2\n");
      printf("Delete an Integer:       3\n");
      printf("Insert an Integer:       4\n");
      printf("Exit Program:            5\n");
  }


  
  
  
  
  