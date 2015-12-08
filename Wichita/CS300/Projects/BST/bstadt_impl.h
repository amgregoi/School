#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>


typedef struct NODE {
	int*            dataPtr;
	struct NODE*	left;
	struct NODE*	right;
} NODE;

typedef struct B {
	int 		count;
	NODE*		root;
	int 		(*compare) (void *arg1, void *arg2);
} BST_TREE;


BST_TREE *BST_Create (int (*compare_from_appl) (void *arg1, void *arg2))
{
    BST_TREE* tree;

    tree = (BST_TREE *) malloc (sizeof(BST_TREE));
    if (!tree) {
	printf("No memory available, Sorry !\n");
	return tree;
    }

    tree->count = 0;
    tree->root = NULL;
    tree->compare = compare_from_appl;

    return tree;
}

NODE* _insert (BST_TREE* tree, NODE* root, NODE* newPtr)
{
	if (!root)
	   return newPtr;
 
	
	if (tree->compare(newPtr->dataPtr, root->dataPtr) < 0){
	    root->left = _insert(tree, root->left, newPtr);
	}
	else{
	    root->right = _insert(tree, root->right, newPtr);
	}
	return root;
}

bool BST_Insert(BST_TREE* tree, int* dataPtr)
{
    NODE* newPtr;

    newPtr = (NODE*)malloc(sizeof(NODE));

    if(!newPtr)
        return false;
    
    newPtr->right = NULL;
    newPtr->left = NULL;
    newPtr->dataPtr = dataPtr;

    if (tree->count == 0 )
        tree->root = newPtr;
    else
        tree->root = _insert(tree, tree->root, newPtr);

    (tree->count)++;
    return true;
}


void breadth_Traversal(NODE* ptr)
{
    if(ptr!=NULL)
    {
        printf("%d ", *(int *)ptr->dataPtr);
        
        if(ptr->left!=NULL){
            breadth_Traversal(ptr->left);
        }
        
        if(ptr->right!=NULL){
            breadth_Traversal(ptr->right);
        }
    }
    return;
}

void inorder_Traversal(NODE* ptr)
{
    if(ptr!=NULL)
    {
        if(ptr->left!=NULL){
            inorder_Traversal(ptr->left);
        }
        
        printf("%d ", *(int *)ptr->dataPtr);
        
        if(ptr->right!=NULL){
            inorder_Traversal(ptr->right);
        }
    }
    return;
}



void _destroy (NODE* root)
{
	if (root)
	{
	    _destroy (root->left);
	    free (root->dataPtr);
	    _destroy (root->right);
	    free (root);
	} 
	return;
}

void BST_Destroy (BST_TREE* tree) 
{
	if(tree)
		_destroy (tree->root);
	free(tree);
	return;
}


NODE* _delete (BST_TREE* tree, NODE* root, void* dataPtr, bool* success)
{
	NODE* dltPtr;
	NODE* exchPtr;
	NODE* newRoot;
	void* holdPtr;

	if (!root)
	{
	    *success = false;
	    return NULL;
	}
	
	if (tree->compare(dataPtr, root->dataPtr) < 0)
	    root->left  = _delete (tree, root->left, dataPtr, success);
	else if (tree->compare(dataPtr, root->dataPtr) > 0)
	    root->right = _delete (tree,    root->right, dataPtr, success);
	else
	{ 
        dltPtr = root;
        if (!root->left){
            free (root->dataPtr);
            newRoot = root->right;
            free (dltPtr);            
            *success = true;
            return newRoot;        
		}
		else if (!root->right){
              free (root->dataPtr);
	          newRoot = root->left;
	          free (dltPtr);
	          *success = true;
	          return newRoot;
		}
		else{
            exchPtr = root->left;
            while (exchPtr->right)
                exchPtr = exchPtr->right;

            holdPtr= root->dataPtr;
            root->dataPtr= exchPtr->dataPtr;
            exchPtr->dataPtr= holdPtr;
            root->left= _delete (tree, root->left,exchPtr->dataPtr, success);
		}
	}
	return root; 
} 

bool BST_Delete (BST_TREE* tree, void* deleteNode)
{
	bool  success;
	NODE* newRoot;
	
	newRoot = _delete (tree, tree->root, deleteNode, &success);
	if (success){
        printf("\tSuccessfully removed node\n");
	    tree->root = newRoot;
	    (tree->count)--;
	    if (tree->count == 0)
	        tree->root = NULL;
	}
    else printf("\tNode not found\n");
	
    return success;
}

NODE* _retrieve (BST_TREE* tree, void* dataPtr, NODE* root)
{
	if (root){
        if (tree->compare(dataPtr, root->dataPtr) < 0)
	         return _retrieve(tree, dataPtr, root->left);
	     else if (tree->compare(dataPtr, root->dataPtr) > 0)
	         return _retrieve(tree, dataPtr, root->right);
         else
	         return root;
	}
	else
        return NULL;
}

void* BST_Retrieve  (BST_TREE* tree, void* dataPtr)
{
	NODE *found;
	void *dataOut = NULL;

	if (tree->root){
	    found = _retrieve (tree, dataPtr, tree->root);

        if( found ){
            printf("\tFound Node: %d\n", *found->dataPtr);
            dataOut = found->dataPtr;
        }
        else printf("\tNode not found\n");
	}
    
    return dataOut;
}
